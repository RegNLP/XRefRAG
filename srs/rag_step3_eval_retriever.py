#!/usr/bin/env python
"""
Evaluate retrieval results for DPEL / SCHEMA test sets using pytrec_eval.

- Qrels are built directly from the test.jsonl file:
    qid = item["id"] (e.g. "DPEL_000677")
    relevant docs = {source_passage_id, target_passage_id}

- Runs are built from retrieval JSONL files created by rag_step1_retrieve.py:
    qid = obj["qa_id"]  (fallbacks if needed)
    docs = entries in "retrieved" list, truncated to top-k

Metrics:
    - recall_10
    - map_cut_10
    - ndcg_cut_10

Outputs:
    - JSON with aggregate metrics
    - optional CSV with per-query metrics
"""

import argparse
import json
import csv
from typing import Dict, Any, List

import pytrec_eval


def load_qrels_from_test_json(path: str) -> Dict[str, Dict[str, int]]:
    """
    Build TREC-style qrels from the test.jsonl file.

    Expected fields in each line:
        - id (query id)
        - source_passage_id (relevant doc id)
        - target_passage_id (relevant doc id)
    """
    qrels: Dict[str, Dict[str, int]] = {}
    num_items = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            num_items += 1

            qid = (
                obj.get("id")
                or obj.get("qa_id")
                or obj.get("question_id")
                or obj.get("qid")
                or obj.get("QuestionID")
            )
            if qid is None:
                raise ValueError(f"Missing 'id' / 'qa_id' in test item: {obj}")
            qid = str(qid)

            if qid not in qrels:
                qrels[qid] = {}

            # DPEL / SCHEMA schema: pids are in source_passage_id / target_passage_id
            for key in ["source_passage_id", "target_passage_id", "source_pid", "target_pid"]:
                pid = obj.get(key)
                if pid:
                    qrels[qid][str(pid)] = 1

    print(
        f"[INFO] Loaded qrels for {len(qrels)} queries from: {path} "
        f"(raw items: {num_items})"
    )
    # Optional sanity check
    empty = [qid for qid, rels in qrels.items() if not rels]
    if empty:
        print(f"[WARN] {len(empty)} queries have no relevant docs in qrels.")

    return qrels


def load_run_from_retrieval_json(path: str, k: int) -> Dict[str, Dict[str, float]]:
    """
    Build a TREC-style run from the retrieval JSONL produced by rag_step1_retrieve.py.

    Expected schema per line:
        {
          "qa_id": "DPEL_000677",
          "retriever": "hybrid_rrf_bm25_e5",
          "question": "...",
          "retrieved": [
            {"pid": "...", "rank": 1, "score": 0.04865},
            ...
          ]
        }
    """
    run: Dict[str, Dict[str, float]] = {}
    num_lines = 0

    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            num_lines += 1
            obj = json.loads(line)

            qid = (
                obj.get("qa_id")
                or obj.get("id")
                or obj.get("question_id")
                or obj.get("qid")
                or obj.get("query_id")
                or obj.get("QuestionID")
            )
            if qid is None:
                raise ValueError(f"Missing 'qa_id' / 'id' in retrieval line {num_lines}: {obj}")
            qid = str(qid)

            docs = run.setdefault(qid, {})

            retrieved = obj.get("retrieved") or obj.get("hits") or obj.get("results") or []
            for r in retrieved[:k]:
                pid = r.get("pid") or r.get("docid") or r.get("doc_id")
                if not pid:
                    continue
                pid = str(pid)
                score = float(r.get("score", 0.0))
                # if doc appears multiple times for some reason, keep max score
                if pid in docs:
                    docs[pid] = max(docs[pid], score)
                else:
                    docs[pid] = score

    print(
        f"[INFO] Loaded run for {len(run)} queries from: {path} "
        f"(raw lines: {num_lines})"
    )
    return run


def aggregate_metrics(scores: Dict[str, Dict[str, float]], metric_keys: List[str]) -> Dict[str, float]:
    if not scores:
        return {m: 0.0 for m in metric_keys}

    agg = {m: 0.0 for m in metric_keys}
    n = len(scores)
    for qid, mvals in scores.items():
        for m in metric_keys:
            if m in mvals:
                agg[m] += mvals[m]
    for m in metric_keys:
        agg[m] /= n
    return agg


def write_per_query_csv(path: str, scores: Dict[str, Dict[str, float]], metric_keys: List[str]) -> None:
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        header = ["qid"] + metric_keys
        writer.writerow(header)
        for qid, mvals in scores.items():
            row = [qid] + [mvals.get(m, 0.0) for m in metric_keys]
            writer.writerow(row)
    print(f"[INFO] Per-query metrics written to CSV: {path}")


def main():
    parser = argparse.ArgumentParser(description="Evaluate retriever using pytrec_eval.")
    parser.add_argument(
        "--test-json",
        required=True,
        help="Path to test.jsonl (DPEL or SCHEMA test split).",
    )
    parser.add_argument(
        "--retrieval-json",
        required=True,
        help="Path to retrieval JSONL produced by rag_step1_retrieve.py.",
    )
    parser.add_argument(
        "--k",
        type=int,
        default=10,
        help="Cutoff K for evaluation (default: 10).",
    )
    parser.add_argument(
        "--out-json",
        required=True,
        help="Path to write aggregate metrics JSON.",
    )
    parser.add_argument(
        "--out-csv",
        default=None,
        help="Optional path to write per-query CSV.",
    )

    args = parser.parse_args()

    # 1) Load qrels and run
    qrels = load_qrels_from_test_json(args.test_json)
    run = load_run_from_retrieval_json(args.retrieval_json, k=args.k)

    # 2) Restrict to intersection
    qids_qrels = set(qrels.keys())
    qids_run = set(run.keys())
    common_qids = sorted(qids_qrels & qids_run)

    print(f"[INFO] #queries in qrels: {len(qids_qrels)}")
    print(f"[INFO] #queries in run:   {len(qids_run)}")
    print(f"[INFO] #queries in BOTH:  {len(common_qids)}")

    if not common_qids:
        print("[WARN] No overlapping queries between qrels and run; metrics will be zero.")
        scores = {}
    else:
        qrels_sub = {qid: qrels[qid] for qid in common_qids}
        run_sub = {qid: run[qid] for qid in common_qids}

        # 3) Evaluate with pytrec_eval
        metric_keys = ["recall_10", "map_cut_10", "ndcg_cut_10"]
        evaluator = pytrec_eval.RelevanceEvaluator(qrels_sub, set(metric_keys))
        scores = evaluator.evaluate(run_sub)

    # 4) Aggregate
    metric_keys = ["recall_10", "map_cut_10", "ndcg_cut_10"]
    agg = aggregate_metrics(scores, metric_keys)

    # 5) Write JSON
    out_obj: Dict[str, Any] = {
        "k": args.k,
        "num_queries_eval": len(scores),
        "metrics": agg,
    }
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, indent=2)
    print(f"[INFO] Aggregate metrics written to: {args.out_json}")
    print(f"[INFO] Recall@{args.k} = {agg['recall_10']:.4f}")
    print(f"[INFO] MAP@{args.k}    = {agg['map_cut_10']:.4f}")
    print(f"[INFO] nDCG@{args.k}   = {agg['ndcg_cut_10']:.4f}")

    # 6) Optional CSV with per-query scores
    if args.out_csv:
        metric_keys = ["recall_10", "map_cut_10", "ndcg_cut_10"]
        write_per_query_csv(args.out_csv, scores, metric_keys)


if __name__ == "__main__":
    main()

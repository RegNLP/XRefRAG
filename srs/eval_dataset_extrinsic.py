#!/usr/bin/env python3
# eval_dataset_extrinsic.py
# -*- coding: utf-8 -*-

"""
Extrinsic evaluation of the final RegRAG-Xref datasets.

For each method (DPEL, SCHEMA) and for each split (train/dev/test) this script
reports, per retriever:

1) QA dataset (RAG-based evaluation)
   - n_qas (QAs in this split that have RAG metrics)
   - IR metrics on those QAs: Recall@k, MAP@k, nDCG@k
   - RAG metrics: F1, ROUGE-L F1, GPT answer_relevance, GPT answer_faithfulness,
                  NLI entailment, NLI contradiction

2) IR dataset (pure IR evaluation, no RAG)
   - n_qas (queries in this split)
   - IR metrics: Recall@k, MAP@k, nDCG@k

IR metrics are computed with *standard*, normalized definitions:
- Recall@k in [0,1]
- MAP@k in [0,1]
- nDCG@k in [0,1]

Inputs:

- Final IR/QA datasets (from build_final_dataset.py):
    --final-dpel-ir        outputs/final/DPEL/RegRAG-Xref_DPEL_ir.jsonl
    --final-schema-ir      outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_ir.jsonl
    --final-dpel-qa        outputs/final/DPEL/RegRAG-Xref_DPEL_QA.jsonl
    --final-schema-qa      outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_QA.jsonl

  Each line should include at least:
    { "qa_id": "...", "split": "train"|"dev"|"test", ... }

- Qrels (method-specific, from build_method_qrels.py):
    --qrels-dpel           inputs/ir/qrels_kept_dpel.txt
    --qrels-schema         inputs/ir/qrels_kept_schema.txt

- Run files over the kept queries (shared for DPEL+SCHEMA, TREC format):
    --runs-bm25            runs_full/kept/bm25.txt
    --runs-e5              runs_full/kept/e5.txt
    --runs-bge             runs_full/kept/bge.txt
    --runs-rerank          runs_full/kept/bm25_e5_rerank.txt
    --runs-hybrid          runs_full/kept/hybrid_rrf_bm25_e5.txt

- RAG per-QA metric files (from eval_rag.py):
    --rag-perqa-glob       "outputs/rag_eval/*_per_qa.jsonl"

Output:
    --out-json             outputs/analysis_dataset/extrinsic_summary.json
"""

import argparse
import glob
import json
import os
import sys
from collections import defaultdict
from typing import Dict, List, Tuple, Any


# -----------------------------
# Basic IO helpers
# -----------------------------

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            items.append(obj)
    return items


# -----------------------------
# IR metric utilities
# -----------------------------

def load_qrels(path: str) -> Dict[str, Dict[str, int]]:
    """
    Load TREC qrels: qid 0 docid rel
    Returns: qrels[qid][docid] = rel (int), but we treat rel > 0 as relevant.
    """
    qrels: Dict[str, Dict[str, int]] = defaultdict(dict)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 4:
                continue
            qid, _, docid, rel = parts[0], parts[1], parts[2], parts[3]
            try:
                rel = int(rel)
            except Exception:
                rel = 0
            qrels[qid][docid] = rel
    return qrels


def load_run(path: str, k: int) -> Dict[str, List[str]]:
    """
    Load TREC run: qid Q0 docid rank score tag
    Returns: run[qid] = [docid1, docid2, ...] sorted by ascending rank, truncated at k.
    """
    tmp: Dict[str, List[Tuple[int, str]]] = defaultdict(list)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 6:
                continue
            qid, _, docid, rank_str, _, _ = parts[:6]
            try:
                rank = int(rank_str)
            except Exception:
                continue
            if rank <= k:
                tmp[qid].append((rank, docid))

    runs: Dict[str, List[str]] = {}
    for qid, pairs in tmp.items():
        pairs.sort(key=lambda x: x[0])
        seen = set()
        ordered = []
        for _, docid in pairs:
            if docid in seen:
                continue
            seen.add(docid)
            ordered.append(docid)
            if len(ordered) >= k:
                break
        runs[qid] = ordered
    return runs


def compute_ir_metrics_for_subset(
    qrels: Dict[str, Dict[str, int]],
    run: Dict[str, List[str]],
    qids: List[str],
    k: int,
) -> Dict[str, float]:
    """
    Compute normalized Recall@k, MAP@k, nDCG@k on the given qids.
    All metrics ∈ [0,1]. If no qids, returns zeros.
    """
    if not qids:
        return {"recall": 0.0, "map": 0.0, "ndcg": 0.0}

    recall_list = []
    ap_list = []
    ndcg_list = []

    for qid in qids:
        rels = qrels.get(qid, {})
        # relevant docids
        rel_docs = {d for d, r in rels.items() if r > 0}
        n_rels = len(rel_docs)
        if n_rels == 0:
            # no relevant docs: by convention contribute 0
            recall_list.append(0.0)
            ap_list.append(0.0)
            ndcg_list.append(0.0)
            continue

        ranked = run.get(qid, [])
        ranked_k = ranked[:k]

        # Recall@k
        hits = sum(1 for d in ranked_k if d in rel_docs)
        recall = hits / float(n_rels)

        # AP@k
        hit_count = 0
        ap = 0.0
        for i, d in enumerate(ranked_k, start=1):
            if d in rel_docs:
                hit_count += 1
                ap += hit_count / float(i)
        ap = ap / float(n_rels)

        # nDCG@k
        dcg = 0.0
        for i, d in enumerate(ranked_k, start=1):
            gain = 1.0 if d in rel_docs else 0.0
            if gain > 0:
                # log2(i+1)
                dcg += gain / (log2(i + 1))

        # ideal DCG: all relevant docs at top positions up to k
        ideal_gains = [1.0] * min(n_rels, k)
        idcg = 0.0
        for i, gain in enumerate(ideal_gains, start=1):
            idcg += gain / (log2(i + 1))
        ndcg = dcg / idcg if idcg > 0 else 0.0

        recall_list.append(recall)
        ap_list.append(ap)
        ndcg_list.append(ndcg)

    def avg(lst):
        return float(sum(lst) / len(lst)) if lst else 0.0

    return {
        "recall": avg(recall_list),
        "map": avg(ap_list),
        "ndcg": avg(ndcg_list),
    }


def log2(x: float) -> float:
    import math
    return math.log(x, 2)


# -----------------------------
# RAG metric utilities
# -----------------------------

def discover_rag_runs(perqa_glob: str):
    """
    Discover per-QA RAG metrics files and map them to:
    method ∈ {DPEL, SCHEMA} and retriever ∈ {BM25, E5, BGE, BM25_E5_RERANK, HYBRID_RRF}.

    Only uses *_kept_* files. Ignores ORACLE.
    """
    paths = glob.glob(perqa_glob)
    mapping = {"DPEL": {}, "SCHEMA": {}}

    for path in paths:
        base = os.path.basename(path)
        base_low = base.lower()
        if not base_low.endswith("_per_qa.jsonl"):
            continue

        # method
        method = None
        if base_low.startswith("dpel_"):
            method = "DPEL"
        elif base_low.startswith("schema_"):
            method = "SCHEMA"
        else:
            continue

        # subset: must be kept
        if "_kept_" not in base_low:
            continue

        # retriever (check specific patterns first)
        retriever = None
        if "_bm25_e5_rerank_" in base_low:
            retriever = "BM25_E5_RERANK"
        elif "_hybrid_rrf_bm25_e5_" in base_low:
            retriever = "HYBRID_RRF"
        elif "_bm25_" in base_low:
            retriever = "BM25"
        elif "_bge_" in base_low:
            retriever = "BGE"
        elif "_e5_" in base_low:
            retriever = "E5"
        else:
            continue

        # skip oracle
        if "_oracle_" in base_low:
            continue

        mapping[method][retriever] = path

    return mapping


def load_rag_perqa(path: str) -> Dict[str, Dict[str, float]]:
    """
    Load per-QA RAG metrics file from eval_rag.py and return:
      rag[qid] = {
         "f1": ...,
         "rouge_l_f1": ...,
         "gpt_answer_relevance": ...,
         "gpt_answer_faithfulness": ...,
         "nli_entailment": ...,
         "nli_contradiction": ...
      }
    """
    rag = {}
    items = load_jsonl(path)
    for obj in items:
        qid = obj.get("qa_id") or obj.get("id")
        if not qid:
            continue
        entry = {}
        for key in [
            "f1",
            "rouge_l_f1",
            "gpt_answer_relevance",
            "gpt_answer_faithfulness",
            "nli_entailment",
            "nli_contradiction",
        ]:
            if key in obj:
                try:
                    entry[key] = float(obj[key])
                except Exception:
                    continue
        rag[qid] = entry
    return rag


def aggregate_rag_metrics_for_subset(
    rag_map: Dict[str, Dict[str, float]],
    qids: List[str],
) -> Dict[str, float]:
    """
    Aggregate RAG metrics for the given qids. Returns means; if no qids, zeros.
    """
    f1_list = []
    rouge_list = []
    rel_list = []
    faith_list = []
    ent_list = []
    contra_list = []

    for qid in qids:
        m = rag_map.get(qid)
        if not m:
            continue
        if "f1" in m:
            f1_list.append(m["f1"])
        if "rouge_l_f1" in m:
            rouge_list.append(m["rouge_l_f1"])
        if "gpt_answer_relevance" in m:
            rel_list.append(m["gpt_answer_relevance"])
        if "gpt_answer_faithfulness" in m:
            faith_list.append(m["gpt_answer_faithfulness"])
        if "nli_entailment" in m:
            ent_list.append(m["nli_entailment"])
        if "nli_contradiction" in m:
            contra_list.append(m["nli_contradiction"])

    def avg(lst):
        return float(sum(lst) / len(lst)) if lst else 0.0

    return {
        "f1": avg(f1_list),
        "rouge_l_f1": avg(rouge_list),
        "gpt_answer_relevance": avg(rel_list),
        "gpt_answer_faithfulness": avg(faith_list),
        "nli_entailment": avg(ent_list),
        "nli_contradiction": avg(contra_list),
        "n_qas": len([qid for qid in qids if qid in rag_map]),
    }


# -----------------------------
# Core evaluation
# -----------------------------

def build_split_map(path: str) -> Dict[str, str]:
    """
    Load final dataset JSONL and build qa_id -> split map.
    """
    items = load_jsonl(path)
    mapping = {}
    for obj in items:
        qid = obj.get("qa_id") or obj.get("id")
        split = obj.get("split")
        if not qid or not split:
            continue
        mapping[qid] = split
    if not mapping:
        print(f"[warn] no (qa_id, split) pairs found in {path}", file=sys.stderr)
    return mapping


def evaluate_method(
    method: str,
    final_ir_path: str,
    final_qa_path: str,
    qrels_path: str,
    runs_paths: Dict[str, str],
    rag_runs: Dict[str, str],
    k: int,
) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Evaluate one method (DPEL or SCHEMA).
    Returns:
      qa_results: nested dict[retriever][split] -> metrics
      ir_results: nested dict[retriever][split] -> metrics
    """
    print("================================================================")
    print(f"[info] Evaluating {method} (QA + IR)")

    # Load split maps
    ir_split_map = build_split_map(final_ir_path)
    qa_split_map = build_split_map(final_qa_path)

    # Load qrels and runs
    qrels = load_qrels(qrels_path)
    runs = {name: load_run(path, k) for name, path in runs_paths.items()}

    splits = ["train", "dev", "test"]

    # ------------- QA dataset: IR + RAG -------------
    print("QA Dataset")
    print("            n_qas Recall@{k:<2} MAP@{k:<2}  nDCG@{k:<2}  F1    ROUGE-L GPT_rel GPT_faith NLI_ent NLI_contra".format(k=k))

    qa_results: Dict[str, Dict[str, Any]] = {}
    # Prepare RAG maps per retriever
    rag_maps = {}
    for retriever, path in rag_runs.items():
        rag_maps[retriever] = load_rag_perqa(path)

    print(method)
    for retriever in ["BM25", "E5", "BGE", "BM25_E5_RERANK", "HYBRID_RRF"]:
        if retriever not in runs:
            continue
        run_for_ret = runs[retriever]
        rag_map = rag_maps.get(retriever, {})
        qa_results[retriever] = {}

        print(f"   {retriever}")
        for split in splits:
            # qids in QA dataset for this split, that also exist in qrels and run
            qids_split = [
                qid for qid, sp in qa_split_map.items()
                if sp == split and qid in qrels and qid in run_for_ret
            ]
            ir_metrics = compute_ir_metrics_for_subset(qrels, run_for_ret, qids_split, k)
            rag_metrics = aggregate_rag_metrics_for_subset(rag_map, qids_split)

            qa_results[retriever][split] = {
                "n_qas": rag_metrics["n_qas"],
                "recall@{}".format(k): ir_metrics["recall"],
                "map@{}".format(k): ir_metrics["map"],
                "ndcg@{}".format(k): ir_metrics["ndcg"],
                "f1": rag_metrics["f1"],
                "rouge_l_f1": rag_metrics["rouge_l_f1"],
                "gpt_answer_relevance": rag_metrics["gpt_answer_relevance"],
                "gpt_answer_faithfulness": rag_metrics["gpt_answer_faithfulness"],
                "nli_entailment": rag_metrics["nli_entailment"],
                "nli_contradiction": rag_metrics["nli_contradiction"],
            }

            print("       {split:<5} {n_qas:4d}    {recall:6.3f}  {map:6.3f}   {ndcg:6.3f}  {f1:5.3f}  {rouge:7.3f}  {rel:6.3f}    {faith:7.3f}  {ent:6.3f}      {contra:6.3f}".format(
                split=split,
                n_qas=qa_results[retriever][split]["n_qas"],
                recall=qa_results[retriever][split]["recall@{}".format(k)],
                map=qa_results[retriever][split]["map@{}".format(k)],
                ndcg=qa_results[retriever][split]["ndcg@{}".format(k)],
                f1=qa_results[retriever][split]["f1"],
                rouge=qa_results[retriever][split]["rouge_l_f1"],
                rel=qa_results[retriever][split]["gpt_answer_relevance"],
                faith=qa_results[retriever][split]["gpt_answer_faithfulness"],
                ent=qa_results[retriever][split]["nli_entailment"],
                contra=qa_results[retriever][split]["nli_contradiction"],
            ))
        print()

    # ------------- IR dataset: pure IR -------------
    print("IR Dataset")
    print("            n_qas Recall@{k:<2} MAP@{k:<2}  nDCG@{k:<2}  ".format(k=k))

    ir_results: Dict[str, Dict[str, Any]] = {}
    print(method)
    for retriever in ["BM25", "E5", "BGE", "BM25_E5_RERANK", "HYBRID_RRF"]:
        if retriever not in runs:
            continue
        run_for_ret = runs[retriever]
        ir_results[retriever] = {}

        print(f"   {retriever}")
        for split in splits:
            qids_split = [
                qid for qid, sp in ir_split_map.items()
                if sp == split and qid in qrels and qid in run_for_ret
            ]
            ir_metrics = compute_ir_metrics_for_subset(qrels, run_for_ret, qids_split, k)

            ir_results[retriever][split] = {
                "n_qas": len(qids_split),
                "recall@{}".format(k): ir_metrics["recall"],
                "map@{}".format(k): ir_metrics["map"],
                "ndcg@{}".format(k): ir_metrics["ndcg"],
            }

            print("       {split:<5} {n_qas:4d}    {recall:6.3f}  {map:6.3f}   {ndcg:6.3f}".format(
                split=split,
                n_qas=ir_results[retriever][split]["n_qas"],
                recall=ir_results[retriever][split]["recall@{}".format(k)],
                map=ir_results[retriever][split]["map@{}".format(k)],
                ndcg=ir_results[retriever][split]["ndcg@{}".format(k)],
            ))
        print()

    return qa_results, ir_results


# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Extrinsic evaluation of final RegRAG-Xref datasets (IR + RAG) per method and split."
    )
    ap.add_argument(
        "--final-dpel-ir",
        required=True,
        help="Final IR dataset for DPEL (JSONL).",
    )
    ap.add_argument(
        "--final-schema-ir",
        required=True,
        help="Final IR dataset for SCHEMA (JSONL).",
    )
    ap.add_argument(
        "--final-dpel-qa",
        required=True,
        help="Final QA/RAG dataset for DPEL (JSONL).",
    )
    ap.add_argument(
        "--final-schema-qa",
        required=True,
        help="Final QA/RAG dataset for SCHEMA (JSONL).",
    )
    ap.add_argument(
        "--qrels-dpel",
        required=True,
        help="Method-specific qrels for DPEL (e.g., inputs/ir/qrels_kept_dpel.txt).",
    )
    ap.add_argument(
        "--qrels-schema",
        required=True,
        help="Method-specific qrels for SCHEMA (e.g., inputs/ir/qrels_kept_schema.txt).",
    )
    ap.add_argument(
        "--runs-bm25",
        required=True,
        help="Run file for BM25 over kept queries.",
    )
    ap.add_argument(
        "--runs-e5",
        required=True,
        help="Run file for e5 over kept queries.",
    )
    ap.add_argument(
        "--runs-bge",
        required=True,
        help="Run file for BGE over kept queries.",
    )
    ap.add_argument(
        "--runs-rerank",
        required=True,
        help="Run file for BM25->e5 rerank over kept queries.",
    )
    ap.add_argument(
        "--runs-hybrid",
        required=True,
        help="Run file for Hybrid RRF (BM25+e5) over kept queries.",
    )
    ap.add_argument(
        "--rag-perqa-glob",
        required=True,
        help="Glob pattern for RAG per-QA metric files (outputs/rag_eval/*_per_qa.jsonl).",
    )
    ap.add_argument(
        "--k",
        type=int,
        default=10,
        help="Cutoff k for IR metrics (default: 10).",
    )
    ap.add_argument(
        "--out-json",
        required=True,
        help="Path to write extrinsic summary JSON.",
    )
    args = ap.parse_args()

    # Discover RAG per-QA runs
    rag_mapping = discover_rag_runs(args.rag_perqa_glob)

    # Prepare runs mapping (same for both methods; we filter by method+split via qrels/final datasets)
    runs_paths = {
        "BM25": args.runs_bm25,
        "E5": args.runs_e5,
        "BGE": args.runs_bge,
        "BM25_E5_RERANK": args.runs_rerank,
        "HYBRID_RRF": args.runs_hybrid,
    }

    summary = {
        "k": args.k,
        "QA": {},
        "IR": {},
    }

    # DPEL
    dpel_qa_results, dpel_ir_results = evaluate_method(
        method="DPEL",
        final_ir_path=args.final_dpel_ir,
        final_qa_path=args.final_dpel_qa,
        qrels_path=args.qrels_dpel,
        runs_paths=runs_paths,
        rag_runs=rag_mapping.get("DPEL", {}),
        k=args.k,
    )
    summary["QA"]["DPEL"] = dpel_qa_results
    summary["IR"]["DPEL"] = dpel_ir_results

    # SCHEMA
    schema_qa_results, schema_ir_results = evaluate_method(
        method="SCHEMA",
        final_ir_path=args.final_schema_ir,
        final_qa_path=args.final_schema_qa,
        qrels_path=args.qrels_schema,
        runs_paths=runs_paths,
        rag_runs=rag_mapping.get("SCHEMA", {}),
        k=args.k,
    )
    summary["QA"]["SCHEMA"] = schema_qa_results
    summary["IR"]["SCHEMA"] = schema_ir_results

    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[info] extrinsic summary written to: {args.out_json}")


if __name__ == "__main__":
    main()

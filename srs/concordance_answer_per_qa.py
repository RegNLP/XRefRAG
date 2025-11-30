#!/usr/bin/env python3
# concordance_answer_per_qa.py
# -*- coding: utf-8 -*-

"""
Per-QA answer concordance across multiple RAG pipelines (BM25, BGE, E5, rerank, hybrid),
mirroring concordance_ir.py but on answer quality instead of retrieval.

Inputs:
  - One or more *_per_qa.jsonl files produced by eval_rag.py
    (each line = metrics for a single qa_id for a single RAG run)

For each (method, subset) pair (DPEL/SCHEMA × kept/eliminated) we aggregate across
retrievers and compute, per qa_id:

  - methods: {retriever_name -> {success, f1, rouge_l_f1,
                                 gpt_answer_relevance,
                                 gpt_answer_faithfulness,
                                 nli_entailment,
                                 nli_contradiction}}
  - num_methods
  - num_methods_success
  - high_concordance_success  (num_methods_success >= high_thresh, e.g. 4 of 5)
  - low_concordance_success   (num_methods_success <= low_thresh, e.g. 0 or 1 of 5)
  - f1_mean
  - rouge_l_f1_mean
  - gpt_answer_relevance_mean
  - gpt_answer_faithfulness_mean
  - nli_entailment_mean
  - nli_contradiction_mean

Outputs:
  - One JSONL per (method, subset) group:
      <out_prefix>_<subset>_<method_lower>.jsonl
    e.g. outputs/rag_eval/concordance_answer_kept_schema.jsonl
         outputs/rag_eval/concordance_answer_kept_dpel.jsonl

  - One CSV per group, same naming but .csv.
"""

import argparse
import csv
import json
import os
from collections import defaultdict
from pathlib import Path
from typing import Dict, Any, List, Tuple


def parse_run_meta(path: str) -> Dict[str, Any]:
    base = os.path.basename(path)

    if base.endswith("_per_qa.jsonl"):
        base = base[:-len("_per_qa.jsonl")]
    elif base.endswith(".jsonl"):
        base = base[:-len(".jsonl")]

    name_l = base.lower()

    # method
    if "dpel" in name_l:
        method = "DPEL"
    elif "schema" in name_l:
        method = "SCHEMA"
    else:
        method = "UNKNOWN"

    # subset
    if "kept" in name_l:
        subset = "kept"
    elif "elim" in name_l or "eliminated" in name_l:
        subset = "eliminated"
    else:
        subset = "UNKNOWN"

    # retriever
    if "oracle" in name_l:
        retriever = "ORACLE"
    elif "hybrid" in name_l or "rrf" in name_l:
        retriever = "HYBRID_RRF"
    elif "bm25_e5" in name_l or "bm25-e5" in name_l or "bm25e5" in name_l:
        retriever = "BM25_E5_RERANK"
    elif "bge" in name_l:
        retriever = "BGE"
    elif "e5" in name_l:
        retriever = "E5"
    elif "bm25" in name_l:
        retriever = "BM25"
    else:
        retriever = "UNKNOWN"

    # mode
    if retriever == "ORACLE" or "oracle" in name_l:
        mode = "oracle"
    else:
        mode = "realistic"

    return {
        "method": method,
        "subset": subset,
        "retriever": retriever,
        "mode": mode,
    }


def load_per_qa(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
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


def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: List[Dict[str, Any]], retrievers: List[str]) -> None:
    """
    Flatten per-QA answer concordance into CSV:
      qa_id, num_methods, num_methods_success,
      high_concordance_success, low_concordance_success,
      f1_mean, rouge_l_f1_mean,
      gpt_answer_relevance_mean, gpt_answer_faithfulness_mean,
      nli_entailment_mean, nli_contradiction_mean,
      <retriever>_success, <retriever>_f1, <retriever>_rouge_l_f1,
      <retriever>_gpt_answer_faithfulness
    """
    base_cols = [
        "qa_id",
        "method",
        "subset",
        "num_methods",
        "num_methods_success",
        "high_concordance_success",
        "low_concordance_success",
        "f1_mean",
        "rouge_l_f1_mean",
        "gpt_answer_relevance_mean",
        "gpt_answer_faithfulness_mean",
        "nli_entailment_mean",
        "nli_contradiction_mean",
    ]
    method_cols: List[str] = []
    for r in retrievers:
        method_cols.extend([
            f"{r}_success",
            f"{r}_f1",
            f"{r}_rouge_l_f1",
            f"{r}_gpt_answer_faithfulness",
        ])

    fieldnames = base_cols + method_cols

    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flat = {
                "qa_id": row["qa_id"],
                "method": row["method"],
                "subset": row["subset"],
                "num_methods": row["num_methods"],
                "num_methods_success": row["num_methods_success"],
                "high_concordance_success": row["high_concordance_success"],
                "low_concordance_success": row["low_concordance_success"],
                "f1_mean": row.get("f1_mean", ""),
                "rouge_l_f1_mean": row.get("rouge_l_f1_mean", ""),
                "gpt_answer_relevance_mean": row.get("gpt_answer_relevance_mean", ""),
                "gpt_answer_faithfulness_mean": row.get("gpt_answer_faithfulness_mean", ""),
                "nli_entailment_mean": row.get("nli_entailment_mean", ""),
                "nli_contradiction_mean": row.get("nli_contradiction_mean", ""),
            }
            methods = row["methods"]
            for r in retrievers:
                minfo = methods.get(r, {})
                flat[f"{r}_success"] = minfo.get("success", False)
                flat[f"{r}_f1"] = minfo.get("f1", "")
                flat[f"{r}_rouge_l_f1"] = minfo.get("rouge_l_f1", "")
                flat[f"{r}_gpt_answer_faithfulness"] = minfo.get("gpt_answer_faithfulness", "")
            writer.writerow(flat)


def _avg_over_methods(methods_dict: Dict[str, Dict[str, Any]], key: str) -> float:
    vals = []
    for m in methods_dict.values():
        v = m.get(key)
        if v is not None:
            vals.append(float(v))
    if not vals:
        return 0.0
    return float(sum(vals) / len(vals))


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Per-QA answer concordance across multiple RAG pipelines."
    )
    ap.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="One or more *_per_qa.jsonl files (from eval_rag.py).",
    )
    ap.add_argument(
        "--out-prefix",
        required=True,
        help="Output prefix, e.g. outputs/rag_eval/concordance_answer",
    )
    ap.add_argument(
        "--f1-thresh",
        type=float,
        default=0.45,
        help="F1 threshold for per-pipeline success.",
    )
    ap.add_argument(
        "--faith-thresh",
        type=float,
        default=3.5,
        help="GPT answer_faithfulness threshold for success.",
    )
    ap.add_argument(
        "--nli-ent-thresh",
        type=float,
        default=0.35,
        help="NLI entailment threshold for success.",
    )
    ap.add_argument(
        "--nli-contra-thresh",
        type=float,
        default=0.2,
        help="NLI contradiction upper bound for success.",
    )
    ap.add_argument(
        "--high-thresh",
        type=int,
        default=4,
        help="Threshold for high_concordance_success (default: 4 of 5).",
    )
    ap.add_argument(
        "--low-thresh",
        type=int,
        default=1,
        help="Threshold for low_concordance_success (default: ≤1 of 5).",
    )
    ap.add_argument(
        "--exclude-oracle",
        action="store_true",
        help="Exclude ORACLE runs from answer-concordance.",
    )
    args = ap.parse_args()

    # group key: (method, subset)
    # value: dict qa_id -> dict[retriever -> metrics]
    per_group: Dict[Tuple[str, str], Dict[str, Dict[str, Dict[str, Any]]]] = defaultdict(lambda: defaultdict(dict))
    retrievers_by_group: Dict[Tuple[str, str], set] = defaultdict(set)

    # -------- load all per_qa files --------
    for path_str in args.inputs:
        p = Path(path_str)
        if not p.exists():
            print(f"[warn] file not found: {p}")
            continue

        meta = parse_run_meta(path_str)
        method = meta["method"]
        subset = meta["subset"]
        retriever = meta["retriever"]
        mode = meta["mode"]

        if method not in {"DPEL", "SCHEMA"}:
            continue
        if subset not in {"kept", "eliminated"}:
            continue
        if retriever == "ORACLE" and args.exclude_oracle:
            continue
        if retriever == "ORACLE":
            # Usually we care about realistic pipelines
            continue
        if mode != "realistic":
            continue

        per_qa_items = load_per_qa(p)
        group_key = (method, subset)
        group = per_group[group_key]

        for obj in per_qa_items:
            qa_id = obj.get("qa_id") or obj.get("qid")
            if not qa_id:
                continue

            f1 = float(obj.get("f1", 0.0))
            rouge = float(obj.get("rouge_l_f1", 0.0))
            rel = obj.get("gpt_answer_relevance")
            faith = obj.get("gpt_answer_faithfulness")
            ent = obj.get("nli_entailment")
            contra = obj.get("nli_contradiction")

            faith_eff = float(faith) if faith is not None else 0.0
            ent_eff = float(ent) if ent is not None else 0.0
            contra_eff = float(contra) if contra is not None else 1.0

            success = (
                f1 >= args.f1_thresh
                and faith_eff >= args.faith_thresh
                and ent_eff >= args.nli_ent_thresh
                and contra_eff <= args.nli_contra_thresh
            )

            group.setdefault(qa_id, {})
            group[qa_id][retriever] = {
                "success": success,
                "f1": f1,
                "rouge_l_f1": rouge,
                "gpt_answer_relevance": float(rel) if rel is not None else None,
                "gpt_answer_faithfulness": float(faith) if faith is not None else None,
                "nli_entailment": float(ent) if ent is not None else None,
                "nli_contradiction": float(contra) if contra is not None else None,
            }

        retrievers_by_group[group_key].add(retriever)

    # -------- build per-QA concordance per (method, subset) --------
    out_prefix = Path(args.out_prefix)
    for (method, subset), qa_map in per_group.items():
        if not qa_map:
            continue

        retrievers = sorted(retrievers_by_group[(method, subset)])
        rows: List[Dict[str, Any]] = []

        for qa_id, methods_dict in qa_map.items():
            num_methods = len(retrievers)
            num_success = sum(
                1 for r in retrievers
                if methods_dict.get(r, {}).get("success", False)
            )
            high_conc = num_success >= args.high_thresh
            low_conc = num_success <= args.low_thresh

            # per-QA means across retrievers
            f1_mean = _avg_over_methods(methods_dict, "f1")
            rouge_mean = _avg_over_methods(methods_dict, "rouge_l_f1")
            rel_mean = _avg_over_methods(methods_dict, "gpt_answer_relevance")
            faith_mean = _avg_over_methods(methods_dict, "gpt_answer_faithfulness")
            ent_mean = _avg_over_methods(methods_dict, "nli_entailment")
            contra_mean = _avg_over_methods(methods_dict, "nli_contradiction")

            rows.append({
                "qa_id": qa_id,
                "method": method,
                "subset": subset,
                "methods": methods_dict,
                "num_methods": num_methods,
                "num_methods_success": num_success,
                "high_concordance_success": high_conc,
                "low_concordance_success": low_conc,
                "f1_mean": f1_mean,
                "rouge_l_f1_mean": rouge_mean,
                "gpt_answer_relevance_mean": rel_mean,
                "gpt_answer_faithfulness_mean": faith_mean,
                "nli_entailment_mean": ent_mean,
                "nli_contradiction_mean": contra_mean,
            })

        suffix = f"{subset}_{method.lower()}"
        jsonl_path = out_prefix.with_name(out_prefix.name + f"_{suffix}.jsonl")
        csv_path = out_prefix.with_name(out_prefix.name + f"_{suffix}.csv")

        write_jsonl(jsonl_path, rows)
        write_csv(csv_path, rows, retrievers)

        print(f"[info] wrote {len(rows)} QAs for {method}/{subset} to:")
        print(f"       {jsonl_path}")
        print(f"       {csv_path}")


if __name__ == "__main__":
    main()

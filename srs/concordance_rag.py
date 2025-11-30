#!/usr/bin/env python3
# concordance_rag.py
# -*- coding: utf-8 -*-

"""
Concordance / summary over per-QA RAG eval files.

Inputs:
  - One or more *_per_qa.jsonl files produced by eval_rag.py
    (each line = metrics for a single qa_id for a single RAG run)

We aggregate per run (method + subset + mode + retriever + model) and print:

  method, subset, mode, retriever, model,
  n, F1, ROUGE-L, GPT_rel, GPT_faith,
  NLI_ent, NLI_contra, success_rate

"success_rate" = fraction of QA items that satisfy ALL of:
  - F1 >= f1_thresh
  - GPT_answer_faithfulness >= faith_thresh (if present; else treated as 0)
  - NLI_entailment >= nli_ent_thresh (if present; else treated as 0)
  - NLI_contradiction <= nli_contra_thresh (if present; else treated as 1)

Run example:

python srs/concordance_rag.py \
  --inputs outputs/rag_eval/*_per_qa.jsonl \
  --out-json outputs/rag_eval/concordance_rag_summary.json \
  --f1-thresh 0.5 \
  --faith-thresh 4.0 \
  --nli-ent-thresh 0.4 \
  --nli-contra-thresh 0.2 \
  --exclude-oracle
"""

import argparse
import json
import os
import sys
from collections import defaultdict
from typing import Dict, Any, List


def parse_run_meta(path: str) -> Dict[str, Any]:
    """
    Infer:
      - method:   DPEL / SCHEMA
      - subset:   kept / eliminated
      - retriever: BM25 / BGE / E5 / BM25_E5_RERANK / HYBRID_RRF / ORACLE
      - model:    gpt4o / UNKNOWN (from filename)
      - mode:     oracle / realistic (derived from retriever/filename)
    from the per-QA filename.
    """
    base = os.path.basename(path)

    # strip cache suffix
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

    # answering model (we only care about gpt-4o vs other; keep simple)
    if "gpt4o" in name_l or "gpt-4o" in name_l:
        model = "gpt4o"
    else:
        model = "UNKNOWN"

    # mode: oracle vs realistic
    if retriever == "ORACLE" or "oracle" in name_l:
        mode = "oracle"
    else:
        mode = "realistic"

    return {
        "method": method,
        "subset": subset,
        "mode": mode,
        "retriever": retriever,
        "model": model,
    }


def load_per_qa(path: str) -> List[Dict[str, Any]]:
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


def main():
    ap = argparse.ArgumentParser(
        description="Concordance / summary over RAG per-QA eval files."
    )
    ap.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="One or more *_per_qa.jsonl files (from eval_rag.py).",
    )
    ap.add_argument(
        "--out-json",
        required=True,
        help="Path to write overall summary JSON.",
    )
    ap.add_argument(
        "--f1-thresh",
        type=float,
        default=0.5,
        help="F1 threshold for success.",
    )
    ap.add_argument(
        "--faith-thresh",
        type=float,
        default=4.0,
        help="GPT answer_faithfulness threshold for success.",
    )
    ap.add_argument(
        "--nli-ent-thresh",
        type=float,
        default=0.4,
        help="NLI entailment threshold for success.",
    )
    ap.add_argument(
        "--nli-contra-thresh",
        type=float,
        default=0.2,
        help="NLI contradiction upper bound for success.",
    )
    ap.add_argument(
        "--exclude-oracle",
        action="store_true",
        help="Exclude ORACLE runs from the summary.",
    )
    args = ap.parse_args()

    groups: Dict[tuple, List[Dict[str, Any]]] = defaultdict(list)

    # ---------------- aggregate per run ----------------
    for path in args.inputs:
        if not os.path.isfile(path):
            print(f"[warn] file not found: {path}", file=sys.stderr)
            continue

        meta = parse_run_meta(path)
        if args.exclude_oracle and meta["mode"] == "oracle":
            continue

        per_qa = load_per_qa(path)
        key = (
            meta["method"],
            meta["subset"],
            meta["mode"],
            meta["retriever"],
            meta["model"],
        )
        groups[key].extend(per_qa)

    summary_rows = []

    # ---------------- compute metrics per group ----------------
    for (method, subset, mode, retriever, model), items in sorted(groups.items()):
        if not items:
            continue

        n = len(items)

        f1_vals = []
        rouge_vals = []
        rel_vals = []
        faith_vals = []
        ent_vals = []
        contra_vals = []

        success = 0

        for obj in items:
            f1 = float(obj.get("f1", 0.0))
            rouge = float(obj.get("rouge_l_f1", 0.0))
            rel = obj.get("gpt_answer_relevance")
            faith = obj.get("gpt_answer_faithfulness")
            ent = obj.get("nli_entailment")
            contra = obj.get("nli_contradiction")

            f1_vals.append(f1)
            rouge_vals.append(rouge)

            if rel is not None:
                rel_vals.append(float(rel))
            if faith is not None:
                faith_vals.append(float(faith))
            if ent is not None:
                ent_vals.append(float(ent))
            if contra is not None:
                contra_vals.append(float(contra))

            # success definition: all thresholds satisfied (missing -> worst-case)
            faith_eff = float(faith) if faith is not None else 0.0
            ent_eff = float(ent) if ent is not None else 0.0
            contra_eff = float(contra) if contra is not None else 1.0

            if (
                f1 >= args.f1_thresh
                and faith_eff >= args.faith_thresh
                and ent_eff >= args.nli_ent_thresh
                and contra_eff <= args.nli_contra_thresh
            ):
                success += 1

        def avg(lst):
            return float(sum(lst) / len(lst)) if lst else 0.0

        f1_mean = avg(f1_vals)
        rouge_mean = avg(rouge_vals)
        rel_mean = avg(rel_vals)
        faith_mean = avg(faith_vals)
        ent_mean = avg(ent_vals)
        contra_mean = avg(contra_vals)
        success_rate = success / n if n > 0 else 0.0

        row = {
            "method": method,
            "subset": subset,
            "mode": mode,
            "retriever": retriever,
            "model": model,
            "n": n,
            "f1_mean": f1_mean,
            "rouge_l_f1_mean": rouge_mean,
            "gpt_answer_relevance_mean": rel_mean,
            "gpt_answer_faithfulness_mean": faith_mean,
            "nli_entailment_mean": ent_mean,
            "nli_contradiction_mean": contra_mean,
            "success_rate": success_rate,
        }
        summary_rows.append(row)

    # ---------------- pretty print table ----------------
    print("\n======================================================================")
    print("RAG Concordance Summary (per run group)")
    print("----------------------------------------------------------------------")
    header = (
        "method", "subset", "mode", "retriever", "model",
        "n", "F1", "ROUGE-L", "GPT_rel", "GPT_faith",
        "NLI_ent", "NLI_contra", "success_rate",
    )
    print(
        f"{header[0]:10s} {header[1]:20s} {header[2]:15s} {header[3]:15s} "
        f"{header[4]:20s} {header[5]:4s} {header[6]:5s} {header[7]:8s} "
        f"{header[8]:8s} {header[9]:10s} {header[10]:8s} {header[11]:11s} {header[12]:12s}"
    )

    for row in summary_rows:
        print(
            f"{row['method']:10s} "
            f"{row['subset']:15s} "
            f"{row['mode']:15s} "
            f"{row['retriever']:15s} "
            f"{row['model']:6s} "
            f"{row['n']:1d} "
            f"{row['f1_mean']:.3f}  "
            f"{row['rouge_l_f1_mean']:.3f}  "
            f"{row['gpt_answer_relevance_mean']:.3f}  "
            f"{row['gpt_answer_faithfulness_mean']:.3f}  "
            f"{row['nli_entailment_mean']:.3f}  "
            f"{row['nli_contradiction_mean']:.3f}  "
            f"{row['success_rate']:.3f}"
        )

    # ---------------- write JSON ----------------
    out_obj = {
        "f1_thresh": args.f1_thresh,
        "faith_thresh": args.faith_thresh,
        "nli_ent_thresh": args.nli_ent_thresh,
        "nli_contra_thresh": args.nli_contra_thresh,
        "exclude_oracle": args.exclude_oracle,
        "rows": summary_rows,
    }
    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(out_obj, f, indent=2)
    print(f"\n[info] summary JSON written to: {args.out_json}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# build_final_dataset.py
# -*- coding: utf-8 -*-

"""
Build the final RegRAG-Xref datasets (IR-only and QA/RAG) per method.

For each method (DPEL / SCHEMA) we create:
- IR dataset: all curated-kept items with strong IR concordance (IR-good)
- QA/RAG dataset: items that are both IR-good AND answer-good (QA-gold),
  where answer-good is based on multi-retriever RAG answer concordance.

Inputs (high level):
  - Curated kept QAs per method (from judge_qas_ensemble.py), e.g.:
      outputs/judging/curated/dpel/kept.jsonl
      outputs/judging/curated/schema/kept.jsonl

  - IR concordance per method (from concordance_ir.py), e.g.:
      outputs/judging/analysis/concordance_kept_dpel.jsonl
      outputs/judging/analysis/concordance_kept_schema.jsonl

  - Answer concordance per method (from concordance_answer_per_qa.py), e.g.:
      outputs/rag_eval/concordance_answer_kept_dpel.jsonl
      outputs/rag_eval/concordance_answer_kept_schema.jsonl

Outputs (per method):

  outputs/final/DPEL/RegRAG-Xref_DPEL_ir.jsonl
  outputs/final/DPEL/RegRAG-Xref_DPEL_QA.jsonl
  outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_ir.jsonl
  outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_QA.jsonl

Each line has at least:
  {
    "qa_id": "...",
    "split": "train" | "dev" | "test",
    "method": "DPEL" | "SCHEMA",
    "question": "...",
    "expected_answer": "...",
    "source_passage_id": "...",
    "target_passage_id": "...",
    "reference_type": "...",
    "persona": "professional" | "basic"
  }
"""

import argparse
import json
import os
import random
import sys
from collections import defaultdict
from typing import Dict, Any, List, Set


# -----------------------------
# Generic helpers
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


def index_by_qa_id(items: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    out = {}
    for obj in items:
        qid = obj.get("qa_id") or obj.get("id") or obj.get("qid")
        if not qid:
            continue
        out[str(qid)] = obj
    return out


# -----------------------------
# IR-good selection (from concordance_ir)
# -----------------------------

def load_ir_good_set(concordance_path: str, ir_min_methods_hit_any: int) -> Set[str]:
    """
    From concordance_kept_{dpel,schema}.jsonl, select qa_ids with
    num_methods_hit_any >= ir_min_methods_hit_any.
    """
    ir_good: Set[str] = set()
    with open(concordance_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            qid = obj.get("qa_id") or obj.get("qid")
            if not qid:
                continue
            qid = str(qid)
            num_any = obj.get("num_methods_hit_any", 0)
            if num_any is None:
                num_any = 0
            if int(num_any) >= ir_min_methods_hit_any:
                ir_good.add(qid)
    return ir_good


# -----------------------------
# RAG-good (answer-concordance) selection
# -----------------------------

def load_rag_good_set(answer_concordance_path: str, rag_min_methods_success: int) -> Set[str]:
    """
    From concordance_answer_kept_{schema,dpel}.jsonl (output of
    concordance_answer_per_qa.py), select qa_ids with
    num_methods_success >= rag_min_methods_success.

    Each line is expected to have:
      {
        "qa_id": "...",
        "method": "DPEL" | "SCHEMA",
        "subset": "kept",
        "num_methods_success": int,
        "high_concordance_success": bool,
        ...
      }
    """
    rag_good: Set[str] = set()
    with open(answer_concordance_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            qid = obj.get("qa_id") or obj.get("qid")
            if not qid:
                continue
            qid = str(qid)
            num_succ = obj.get("num_methods_success", 0)
            if num_succ is None:
                num_succ = 0
            if int(num_succ) >= rag_min_methods_success:
                rag_good.add(qid)
    return rag_good


# -----------------------------
# Split assignment
# -----------------------------

def assign_splits(
    qa_ids: List[str],
    train_ratio: float,
    dev_ratio: float,
    test_ratio: float,
    seed: int,
) -> Dict[str, str]:
    """Randomly assign qa_ids to train/dev/test."""
    total_ratio = train_ratio + dev_ratio + test_ratio
    if abs(total_ratio - 1.0) > 1e-6:
        print(f"[warn] train/dev/test ratios sum to {total_ratio:.3f}, normalizing to 1.0")
        train_ratio /= total_ratio
        dev_ratio /= total_ratio
        test_ratio /= total_ratio

    n = len(qa_ids)
    ids = list(qa_ids)
    random.Random(seed).shuffle(ids)

    n_train = int(round(n * train_ratio))
    n_dev = int(round(n * dev_ratio))
    if n_train + n_dev > n:
        n_dev = max(0, n - n_train)
    n_test = n - n_train - n_dev

    splits: Dict[str, str] = {}
    for i, qid in enumerate(ids):
        if i < n_train:
            splits[qid] = "train"
        elif i < n_train + n_dev:
            splits[qid] = "dev"
        else:
            splits[qid] = "test"
    return splits


# -----------------------------
# Main per-method builder
# -----------------------------

def build_for_method(
    method_name: str,
    curated_kept_path: str,
    ir_concordance_path: str,
    answer_concordance_path: str,
    out_dir: str,
    ir_min_methods_hit_any: int,
    rag_min_methods_success: int,
    train_ratio: float,
    dev_ratio: float,
    test_ratio: float,
    split_seed: int,
    summary: Dict[str, Any],
) -> None:
    print("================================================================")
    print(f"[info] building final datasets for method={method_name}")

    # Load curated kept QAs
    print(f"[info] reading curated kept QAs from: {curated_kept_path}")
    kept_items = load_jsonl(curated_kept_path)
    print(f"[info] kept items loaded: {len(kept_items)}")
    id2qa = index_by_qa_id(kept_items)
    kept_ids = set(id2qa.keys())

    # IR-good set (from concordance_ir)
    print(f"[info] IR concordance entries loading from: {ir_concordance_path}")
    ir_good_all = load_ir_good_set(ir_concordance_path, ir_min_methods_hit_any)
    ir_good_ids = kept_ids & ir_good_all
    print(f"[info] IR-good items (within kept): {len(ir_good_ids)}")

    # RAG-good set (from answer concordance)
    print(f"[info] Answer concordance entries loading from: {answer_concordance_path}")
    rag_good_all = load_rag_good_set(answer_concordance_path, rag_min_methods_success)
    rag_good_ids = kept_ids & rag_good_all
    print(f"[info] RAG-good items (within kept): {len(rag_good_ids)}")

    # Final QA GOLD = IR-good ∩ RAG-good
    qa_gold_ids = ir_good_ids & rag_good_ids

    print(f"[info] method={method_name}")
    print(f"  total kept items:        {len(kept_ids)}")
    print(f"  IR-good items:           {len(ir_good_ids)}")
    print(f"  RAG-good items:          {len(rag_good_ids)}")
    print(f"  QA GOLD items (IR & RAG): {len(qa_gold_ids)} "
          f"({len(qa_gold_ids)/max(1,len(kept_ids)):.3f} of kept)")

    # Assign splits separately for IR and QA
    ir_splits = assign_splits(
        sorted(ir_good_ids),
        train_ratio=train_ratio,
        dev_ratio=dev_ratio,
        test_ratio=test_ratio,
        seed=split_seed,
    )
    qa_splits = assign_splits(
        sorted(qa_gold_ids),
        train_ratio=train_ratio,
        dev_ratio=dev_ratio,
        test_ratio=test_ratio,
        seed=split_seed + 1,  # different seed so they don't coincide by accident
    )

    # Output dir per method
    method_dir = os.path.join(out_dir, method_name)
    os.makedirs(method_dir, exist_ok=True)

    # Write IR dataset
    ir_out = os.path.join(method_dir, f"RegRAG-Xref_{method_name}_ir.jsonl")
    n_ir = 0
    with open(ir_out, "w", encoding="utf-8") as f:
        for qid, split in ir_splits.items():
            qa = id2qa.get(qid)
            if not qa:
                continue
            obj = {
                "qa_id": qid,
                "split": split,
                "method": method_name,
                "question": qa.get("question"),
                "expected_answer": qa.get("expected_answer"),
                "source_passage_id": (qa.get("debug_context") or {}).get("source_passage_id"),
                "target_passage_id": (qa.get("debug_context") or {}).get("target_passage_id"),
                "reference_type": qa.get("reference_type"),
                "persona": qa.get("persona"),
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            n_ir += 1
    print(f"[info] IR dataset written: {ir_out}  (n={n_ir})")

    # Write QA/RAG dataset
    qa_out = os.path.join(method_dir, f"RegRAG-Xref_{method_name}_QA.jsonl")
    n_qa = 0
    with open(qa_out, "w", encoding="utf-8") as f:
        for qid, split in qa_splits.items():
            qa = id2qa.get(qid)
            if not qa:
                continue
            obj = {
                "qa_id": qid,
                "split": split,
                "method": method_name,
                "question": qa.get("question"),
                "expected_answer": qa.get("expected_answer"),
                "source_passage_id": (qa.get("debug_context") or {}).get("source_passage_id"),
                "target_passage_id": (qa.get("debug_context") or {}).get("target_passage_id"),
                "reference_type": qa.get("reference_type"),
                "persona": qa.get("persona"),
            }
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")
            n_qa += 1
    print(f"[info] QA/RAG dataset written: {qa_out}  (n={n_qa})")

    # Quick split counts for logging
    ir_split_counts = defaultdict(int)
    for s in ir_splits.values():
        ir_split_counts[s] += 1
    qa_split_counts = defaultdict(int)
    for s in qa_splits.values():
        qa_split_counts[s] += 1
    print(f"[info] IR splits: train={ir_split_counts['train']}, "
          f"dev={ir_split_counts['dev']}, test={ir_split_counts['test']}")
    print(f"[info] QA splits: train={qa_split_counts['train']}, "
          f"dev={qa_split_counts['dev']}, test={qa_split_counts['test']}")
    print()

    # Record in summary
    summary[method_name] = {
        "counts": {
            "kept": len(kept_ids),
            "ir_good": len(ir_good_ids),
            "qa_gold": len(qa_gold_ids),
        },
        "splits": {
            "ir": dict(ir_split_counts),
            "qa": dict(qa_split_counts),
        },
    }


# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Build final IR and QA/RAG datasets for RegRAG-Xref."
    )
    ap.add_argument("--dpel-kept", required=True,
                    help="Curated kept DPEL QAs (JSONL).")
    ap.add_argument("--schema-kept", required=True,
                    help="Curated kept SCHEMA QAs (JSONL).")
    ap.add_argument("--ir-dpel-kept", required=True,
                    help="IR concordance JSONL for DPEL kept (concordance_kept_dpel.jsonl).")
    ap.add_argument("--ir-schema-kept", required=True,
                    help="IR concordance JSONL for SCHEMA kept (concordance_kept_schema.jsonl).")
    ap.add_argument("--answer-dpel-kept", required=True,
                    help="Answer-concordance JSONL for DPEL kept (concordance_answer_kept_dpel.jsonl).")
    ap.add_argument("--answer-schema-kept", required=True,
                    help="Answer-concordance JSONL for SCHEMA kept (concordance_answer_kept_schema.jsonl).")
    ap.add_argument("--out-dir", required=True,
                    help="Output directory for final datasets (e.g. outputs/final).")
    ap.add_argument("--ir-min-methods-hit-any", type=int, default=4,
                    help="Minimum number of IR methods that must hit-any@k to mark IR-good.")
    ap.add_argument("--rag-min-methods-success", type=int, default=4,
                    help="Minimum number of RAG pipelines that must succeed to mark RAG-good.")
    ap.add_argument("--train-ratio", type=float, default=0.8)
    ap.add_argument("--dev-ratio", type=float, default=0.1)
    ap.add_argument("--test-ratio", type=float, default=0.1)
    ap.add_argument("--split-seed", type=int, default=13)
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    summary: Dict[str, Any] = {}

    build_for_method(
        method_name="DPEL",
        curated_kept_path=args.dpel_kept,
        ir_concordance_path=args.ir_dpel_kept,
        answer_concordance_path=args.answer_dpel_kept,
        out_dir=args.out_dir,
        ir_min_methods_hit_any=args.ir_min_methods_hit_any,
        rag_min_methods_success=args.rag_min_methods_success,
        train_ratio=args.train_ratio,
        dev_ratio=args.dev_ratio,
        test_ratio=args.test_ratio,
        split_seed=args.split_seed,
        summary=summary,
    )

    build_for_method(
        method_name="SCHEMA",
        curated_kept_path=args.schema_kept,
        ir_concordance_path=args.ir_schema_kept,
        answer_concordance_path=args.answer_schema_kept,
        out_dir=args.out_dir,
        ir_min_methods_hit_any=args.ir_min_methods_hit_any,
        rag_min_methods_success=args.rag_min_methods_success,
        train_ratio=args.train_ratio,
        dev_ratio=args.dev_ratio,
        test_ratio=args.test_ratio,
        split_seed=args.split_seed,
        summary=summary,
    )

    summary_path = os.path.join(args.out_dir, "summary.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[info] final dataset summary written: {summary_path}")


if __name__ == "__main__":
    main()

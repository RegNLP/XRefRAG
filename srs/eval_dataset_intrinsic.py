#!/usr/bin/env python3
# eval_dataset_intrinsic.py
# -*- coding: utf-8 -*-

"""
Intrinsic dataset evaluation for RegRAG-Xref.

Per method (DPEL / SCHEMA), this script computes:

1) Global counts
   - #generated, #kept, #eliminated
   - #IR-good (final IR dataset size)
   - #QA-gold (final QA/RAG dataset size)
   - Split counts for final IR/QA: train / dev / test

2) Structural statistics
   - Persona distribution (basic / professional / UNKNOWN)
   - Item type distribution (if available; otherwise UNKNOWN)
   - Reference type distribution (if available; otherwise UNKNOWN)
   - Cross-doc vs intra-doc distribution (from debug_context)

3) Length statistics
   - Question & answer length (tokens & chars) for:
       generated, kept, eliminated, IR-good, QA-gold

4) Optional RAG overlay on QA-gold (if --rag-perqa-glob is given)
   - For QA-gold items, average:
       F1, ROUGE-L F1,
       GPT answer_relevance, GPT answer_faithfulness,
       NLI entailment, NLI contradiction
     (aggregated over all matching per-qa files)

Outputs (per method, under --out-dir):

  <METHOD>_persona.csv
  <METHOD>_item_type.csv
  <METHOD>_reference_type.csv
  <METHOD>_crossdoc.csv
  <METHOD>_lengths.csv

Plus a global JSON summary:

  summary_intrinsic.json

Usage (paths default to the canonical layout):

  python srs/eval_dataset_intrinsic.py \
    --out-dir outputs/analysis_intrinsic \
    --rag-perqa-glob "outputs/rag_eval/*_per_qa.jsonl"
"""

import argparse
import json
import os
import sys
import glob
import statistics
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple, Optional

import numpy as np


# -------------------------------------------------------------------
# I/O helpers
# -------------------------------------------------------------------

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    if not path or not os.path.isfile(path):
        print(f"[warn] JSONL not found: {path}", file=sys.stderr)
        return []
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


def write_csv(path: str, header: List[str], rows: List[List[Any]]) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(" | ".join(header) + "\n")
        f.write("-" * (len(" | ".join(header)) + 2) + "\n")
        for row in rows:
            f.write(" | ".join(str(x) for x in row) + "\n")
    print(f"[info] wrote CSV: {path}")


# -------------------------------------------------------------------
# Field extractors
# -------------------------------------------------------------------

def get_qa_id(obj: Dict[str, Any]) -> Optional[str]:
    return obj.get("qa_id") or obj.get("id")


def get_persona(obj: Dict[str, Any]) -> str:
    p = obj.get("persona") or obj.get("style") or ""
    p = str(p).strip().lower()
    if not p:
        return "UNKNOWN"
    if "basic" in p:
        return "basic"
    if "prof" in p:
        return "professional"
    return p


def get_item_type(obj: Dict[str, Any]) -> str:
    t = obj.get("item_type")
    if not t:
        dbg = obj.get("debug_context") or {}
        # For SCHEMA, item types may be stored as source/target item_type
        t = dbg.get("source_item_type") or dbg.get("target_item_type")
    if not t:
        return "UNKNOWN"
    return str(t).strip()


def get_reference_type(obj: Dict[str, Any]) -> str:
    t = obj.get("reference_type")
    if not t:
        dbg = obj.get("debug_context") or {}
        t = dbg.get("reference_type")
    if not t:
        return "UNKNOWN"
    return str(t).strip()


def get_crossdoc_label(obj: Dict[str, Any]) -> str:
    dbg = obj.get("debug_context") or {}
    sdoc = (dbg.get("source_document_name")
            or dbg.get("source_doc_id")
            or "").strip()
    tdoc = (dbg.get("target_document_name")
            or dbg.get("target_doc_id")
            or "").strip()
    if not sdoc or not tdoc:
        return "UNKNOWN"
    if sdoc == tdoc:
        return "intra_doc"
    return "cross_doc"


def get_question(obj: Dict[str, Any]) -> str:
    return (obj.get("question") or obj.get("q") or "").strip()


def get_answer(obj: Dict[str, Any]) -> str:
    return (obj.get("expected_answer") or obj.get("answer") or "").strip()


# -------------------------------------------------------------------
# Length stats
# -------------------------------------------------------------------

def _text_lengths(texts: List[str]) -> Tuple[List[int], List[int]]:
    token_lens = []
    char_lens = []
    for t in texts:
        t = t or ""
        token_lens.append(len(t.split()))
        char_lens.append(len(t))
    return token_lens, char_lens


def _summarize_lengths(values: List[int]) -> Dict[str, float]:
    if not values:
        return {"count": 0, "mean": 0.0, "median": 0.0, "std": 0.0,
                "min": 0.0, "max": 0.0}
    v = [float(x) for x in values]
    return {
        "count": len(v),
        "mean": float(np.mean(v)),
        "median": float(np.median(v)),
        "std": float(np.std(v, ddof=0)),
        "min": float(np.min(v)),
        "max": float(np.max(v)),
    }


def compute_length_stats(group_items: Dict[str, List[Dict[str, Any]]]
                         ) -> List[Dict[str, Any]]:
    """
    group_items: mapping group_name -> list of QA dicts
      groups e.g. generated, kept, eliminated, ir_good, qa_gold

    Returns: list of rows with keys:
      group, field, count, mean, median, std, min, max
    """
    rows = []
    for group_name, items in group_items.items():
        questions = [get_question(o) for o in items]
        answers = [get_answer(o) for o in items]

        q_tok, q_char = _text_lengths(questions)
        a_tok, a_char = _text_lengths(answers)

        stats_map = {
            "question_tokens": _summarize_lengths(q_tok),
            "question_chars": _summarize_lengths(q_char),
            "answer_tokens": _summarize_lengths(a_tok),
            "answer_chars": _summarize_lengths(a_char),
        }

        for field, s in stats_map.items():
            rows.append({
                "group": group_name,
                "field": field,
                **s,
            })
    return rows


# -------------------------------------------------------------------
# RAG per-qa overlay
# -------------------------------------------------------------------

def load_rag_perqa(glob_pattern: Optional[str]) -> Dict[str, Dict[str, float]]:
    """
    Load per-qa RAG metrics from multiple *_per_qa.jsonl files and
    aggregate them per qa_id by simple averaging.

    Returns:
      qa_id -> {
        "f1": ...,
        "rouge_l_f1": ...,
        "gpt_answer_relevance": ...,
        "gpt_answer_faithfulness": ...,
        "nli_entailment": ...,
        "nli_contradiction": ...
      }
    """
    if not glob_pattern:
        return {}

    files = sorted(glob.glob(glob_pattern))
    if not files:
        print(f"[warn] no RAG per-qa files matched: {glob_pattern}",
              file=sys.stderr)
        return {}

    print(f"[info] loading RAG per-qa metrics from {len(files)} files",
          file=sys.stderr)

    acc: Dict[str, Dict[str, List[float]]] = defaultdict(
        lambda: defaultdict(list)
    )
    keys = [
        "f1",
        "rouge_l_f1",
        "gpt_answer_relevance",
        "gpt_answer_faithfulness",
        "nli_entailment",
        "nli_contradiction",
    ]

    for path in files:
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    obj = json.loads(line)
                except Exception:
                    continue
                qid = get_qa_id(obj)
                if not qid:
                    continue
                for k in keys:
                    if k in obj and obj[k] is not None:
                        try:
                            acc[qid][k].append(float(obj[k]))
                        except Exception:
                            continue

    out: Dict[str, Dict[str, float]] = {}
    for qid, m in acc.items():
        out[qid] = {}
        for k in keys:
            vals = m.get(k, [])
            out[qid][k] = float(sum(vals) / len(vals)) if vals else 0.0

    print(f"[info] aggregated RAG metrics for {len(out)} distinct qa_ids",
          file=sys.stderr)
    return out


# -------------------------------------------------------------------
# Grouped counts by attribute
# -------------------------------------------------------------------

def group_counts_by(
    groups: Dict[str, List[Dict[str, Any]]],
    key_fn,
) -> List[Dict[str, Any]]:
    """
    groups: mapping group_name -> list of objs
    key_fn: function(obj) -> value string

    Returns rows with:
      value, group_name, count
    but we’ll later pivot into persona/item_type/reference_type tables.
    """
    rows = []
    for gname, objs in groups.items():
        ctr = Counter()
        for o in objs:
            v = key_fn(o)
            ctr[v] += 1
        for v, c in sorted(ctr.items(), key=lambda x: x[0]):
            rows.append({
                "group": gname,
                "value": v,
                "count": c,
            })
    return rows


def pivot_counts(
    rows: List[Dict[str, Any]],
    group_order: List[str],
) -> List[List[Any]]:
    """
    rows: list of dicts as from group_counts_by
    group_order: e.g. ["generated","kept","eliminated","ir_good","qa_gold"]

    Returns rows for CSV:
      value | generated | kept | eliminated | ir_good | qa_gold
    """
    # value -> group -> count
    table: Dict[str, Dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for r in rows:
        value = r["value"]
        group = r["group"]
        cnt = r["count"]
        table[value][group] = cnt

    values_sorted = sorted(table.keys())
    out_rows = []
    for val in values_sorted:
        row = [val]
        for g in group_order:
            row.append(table[val].get(g, 0))
        out_rows.append(row)
    return out_rows


# -------------------------------------------------------------------
# Per-method intrinsic analysis
# -------------------------------------------------------------------

def analyze_method(
    method: str,
    generated_path: str,
    kept_path: str,
    elim_path: str,
    final_ir_path: str,
    final_qa_path: str,
    rag_perqa: Dict[str, Dict[str, float]],
    out_dir: str,
    summary: Dict[str, Any],
) -> None:
    print("=" * 64)
    print(f"[info] Intrinsic analysis for method={method}")
    print("=" * 64)

    generated = load_jsonl(generated_path)
    kept = load_jsonl(kept_path)
    elim = load_jsonl(elim_path)
    ir_good = load_jsonl(final_ir_path)
    qa_gold = load_jsonl(final_qa_path)

    print(f"[{method}] generated: {len(generated)}")
    print(f"[{method}] kept:      {len(kept)}")
    print(f"[{method}] eliminated:{len(elim)}")
    print(f"[{method}] IR-good:   {len(ir_good)}")
    print(f"[{method}] QA-gold:   {len(qa_gold)}")

    # Splits for final IR/QA (train/dev/test)
    def split_counts(items: List[Dict[str, Any]]) -> Dict[str, int]:
        ctr = Counter()
        for o in items:
            s = (o.get("split") or "").strip().lower()
            if s not in ("train", "dev", "test"):
                s = "UNKNOWN"
            ctr[s] += 1
        return dict(ctr)

    ir_split = split_counts(ir_good)
    qa_split = split_counts(qa_gold)
    print(f"[{method}] IR splits: {ir_split}")
    print(f"[{method}] QA splits: {qa_split}")

    # For group-based analyses, we treat each list as "items with that status"
    groups = {
        "generated": generated,
        "kept": kept,
        "eliminated": elim,
        "ir_good": ir_good,
        "qa_gold": qa_gold,
    }
    group_order = ["generated", "kept", "eliminated", "ir_good", "qa_gold"]

    # ----- Persona table -----
    persona_rows = group_counts_by(groups, get_persona)
    persona_csv_rows = pivot_counts(persona_rows, group_order)
    persona_header = ["persona"] + group_order
    write_csv(
        os.path.join(out_dir, f"{method}_persona.csv"),
        persona_header,
        persona_csv_rows,
    )

    # ----- Item type table -----
    item_rows = group_counts_by(groups, get_item_type)
    item_csv_rows = pivot_counts(item_rows, group_order)
    item_header = ["item_type"] + group_order
    write_csv(
        os.path.join(out_dir, f"{method}_item_type.csv"),
        item_header,
        item_csv_rows,
    )

    # ----- Reference type table -----
    ref_rows = group_counts_by(groups, get_reference_type)
    ref_csv_rows = pivot_counts(ref_rows, group_order)
    ref_header = ["reference_type"] + group_order
    write_csv(
        os.path.join(out_dir, f"{method}_reference_type.csv"),
        ref_header,
        ref_csv_rows,
    )

    # ----- Cross-doc vs intra-doc -----
    cross_rows = group_counts_by(groups, get_crossdoc_label)
    cross_csv_rows = pivot_counts(cross_rows, group_order)
    cross_header = ["crossdoc_label"] + group_order
    write_csv(
        os.path.join(out_dir, f"{method}_crossdoc.csv"),
        cross_header,
        cross_csv_rows,
    )

    # ----- Length stats -----
    length_rows = compute_length_stats(groups)
    length_header = [
        "group",
        "field",
        "count",
        "mean",
        "median",
        "std",
        "min",
        "max",
    ]
    length_csv_rows = [
        [
            r["group"],
            r["field"],
            int(r["count"]),
            f"{r['mean']:.3f}",
            f"{r['median']:.3f}",
            f"{r['std']:.3f}",
            f"{r['min']:.3f}",
            f"{r['max']:.3f}",
        ]
        for r in length_rows
    ]
    write_csv(
        os.path.join(out_dir, f"{method}_lengths.csv"),
        length_header,
        length_csv_rows,
    )

    # ----- RAG overlay for QA-gold -----
    rag_overlay = {}
    if rag_perqa:
        qa_ids = [get_qa_id(o) for o in qa_gold if get_qa_id(o)]
        f1_vals = []
        rouge_vals = []
        rel_vals = []
        faith_vals = []
        ent_vals = []
        contra_vals = []

        for qid in qa_ids:
            m = rag_perqa.get(qid)
            if not m:
                continue
            if "f1" in m:
                f1_vals.append(m["f1"])
            if "rouge_l_f1" in m:
                rouge_vals.append(m["rouge_l_f1"])
            if "gpt_answer_relevance" in m:
                rel_vals.append(m["gpt_answer_relevance"])
            if "gpt_answer_faithfulness" in m:
                faith_vals.append(m["gpt_answer_faithfulness"])
            if "nli_entailment" in m:
                ent_vals.append(m["nli_entailment"])
            if "nli_contradiction" in m:
                contra_vals.append(m["nli_contradiction"])

        def avg(x):
            return float(sum(x) / len(x)) if x else 0.0

        rag_overlay = {
            "num_with_rag_metrics": len(set(
                qid for qid in qa_ids if qid in rag_perqa
            )),
            "f1_mean": avg(f1_vals),
            "rouge_l_f1_mean": avg(rouge_vals),
            "gpt_answer_relevance_mean": avg(rel_vals),
            "gpt_answer_faithfulness_mean": avg(faith_vals),
            "nli_entailment_mean": avg(ent_vals),
            "nli_contradiction_mean": avg(contra_vals),
        }

        print(f"[{method}] QA-gold RAG overlay (averaged over per-qa runs):")
        for k, v in rag_overlay.items():
            print(f"    {k}: {v:.4f}" if isinstance(v, float) else f"    {k}: {v}")

    # ----- store into global summary -----
    summary[method] = {
        "counts": {
            "generated": len(generated),
            "kept": len(kept),
            "eliminated": len(elim),
            "ir_good": len(ir_good),
            "qa_gold": len(qa_gold),
        },
        "splits": {
            "ir": ir_split,
            "qa": qa_split,
        },
        "rag_overlay_qa_gold": rag_overlay,
    }


# -------------------------------------------------------------------
# Main
# -------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Intrinsic dataset evaluation for RegRAG-Xref "
                    "(DPEL / SCHEMA)."
    )
    ap.add_argument(
        "--out-dir",
        default="outputs/analysis_intrinsic",
        help="Directory to write intrinsic analysis CSVs and summary JSON.",
    )
    ap.add_argument(
        "--dpel-generated",
        default="outputs/generation/dpel/all/answers.jsonl",
        help="Generated DPEL QAs (pre-curation).",
    )
    ap.add_argument(
        "--schema-generated",
        default="outputs/generation/schema/all/answers.jsonl",
        help="Generated SCHEMA QAs (pre-curation).",
    )
    ap.add_argument(
        "--dpel-kept",
        default="outputs/judging/curated/DPEL/kept.jsonl",
        help="Curated kept DPEL QAs.",
    )
    ap.add_argument(
        "--dpel-elim",
        default="outputs/judging/curated/DPEL/eliminated.jsonl",
        help="Curated eliminated DPEL QAs.",
    )
    ap.add_argument(
        "--schema-kept",
        default="outputs/judging/curated/SCHEMA/kept.jsonl",
        help="Curated kept SCHEMA QAs.",
    )
    ap.add_argument(
        "--schema-elim",
        default="outputs/judging/curated/SCHEMA/eliminated.jsonl",
        help="Curated eliminated SCHEMA QAs.",
    )
    ap.add_argument(
        "--final-dpel-ir",
        default="outputs/final/DPEL/RegRAG-Xref_DPEL_ir.jsonl",
        help="Final DPEL IR dataset (IR-good items).",
    )
    ap.add_argument(
        "--final-dpel-qa",
        default="outputs/final/DPEL/RegRAG-Xref_DPEL_QA.jsonl",
        help="Final DPEL QA/RAG dataset (QA-gold items).",
    )
    ap.add_argument(
        "--final-schema-ir",
        default="outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_ir.jsonl",
        help="Final SCHEMA IR dataset (IR-good items).",
    )
    ap.add_argument(
        "--final-schema-qa",
        default="outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_QA.jsonl",
        help="Final SCHEMA QA/RAG dataset (QA-gold items).",
    )
    ap.add_argument(
        "--rag-perqa-glob",
        default=None,
        help="Glob for RAG per-qa metrics JSONL files "
             "(e.g. 'outputs/rag_eval/*_per_qa.jsonl'). Optional.",
    )
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    rag_perqa = load_rag_perqa(args.rag_perqa_glob) if args.rag_perqa_glob else {}

    summary: Dict[str, Any] = {}

    # DPEL
    analyze_method(
        method="DPEL",
        generated_path=args.dpel_generated,
        kept_path=args.dpel_kept,
        elim_path=args.dpel_elim,
        final_ir_path=args.final_dpel_ir,
        final_qa_path=args.final_dpel_qa,
        rag_perqa=rag_perqa,
        out_dir=args.out_dir,
        summary=summary,
    )

    # SCHEMA
    analyze_method(
        method="SCHEMA",
        generated_path=args.schema_generated,
        kept_path=args.schema_kept,
        elim_path=args.schema_elim,
        final_ir_path=args.final_schema_ir,
        final_qa_path=args.final_schema_qa,
        rag_perqa=rag_perqa,
        out_dir=args.out_dir,
        summary=summary,
    )

    # Write overall summary
    summary_path = os.path.join(args.out_dir, "summary_intrinsic.json")
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)
    print(f"[info] intrinsic summary written: {summary_path}")


if __name__ == "__main__":
    main()

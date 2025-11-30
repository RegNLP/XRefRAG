#!/usr/bin/env python3
# srs/analyze_intrinsic.py
# -*- coding: utf-8 -*-

"""
Intrinsic analysis for RegRAG-Xref.

Goal: For each method (DPEL, SCHEMA), analyze how different QA
sub-groups survive through the pipeline steps:

  generated -> kept/eliminated -> IR-good -> QA-gold

Group by:
  - persona
  - item_type      (SCHEMA-specific; falls back to UNKNOWN)
  - reference_type (from CrossReferenceData.csv if joinable; else UNKNOWN)

Also writes per-method/group tables as CSV under --out-dir-analysis.
"""

import argparse
import csv
import json
import os
from collections import defaultdict, Counter

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------

def load_jsonl(path):
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


def qid_sets_from_curated(kept_path, elim_path):
    kept = set()
    elim = set()
    for path, target in [(kept_path, kept), (elim_path, elim)]:
        for obj in load_jsonl(path):
            qid = obj.get("qa_id") or obj.get("id")
            if qid:
                target.add(qid)
    return kept, elim


def load_ir_good_ids(concordance_path, min_methods_hit_any=4):
    """
    concordance_kept_{method}.jsonl has per-query entries from concordance_ir.py.
    We mark a qa_id as IR-good if num_methods_hit_any >= min_methods_hit_any.
    """
    good = set()
    for obj in load_jsonl(concordance_path):
        qid = obj.get("qid") or obj.get("qa_id") or obj.get("id")
        if not qid:
            continue
        n_any = obj.get("num_methods_hit_any", 0)
        if n_any is None:
            n_any = 0
        if n_any >= min_methods_hit_any:
            good.add(qid)
    return good


def load_qa_gold_ids(final_qa_path):
    """
    Final QA datasets (RegRAG-Xref_*_QA.jsonl).
    We just take all qa_ids that appear in these files.
    """
    gold = set()
    for obj in load_jsonl(final_qa_path):
        qid = obj.get("qa_id") or obj.get("id")
        if qid:
            gold.add(qid)
    return gold


def load_generation_ids_with_meta(path, method_name):
    """
    From generation files, collect:
      - qa_id
      - persona
      - item_type (if present)
      - source/target passage ids for later join

    We return a dict:
      qa_id -> {
         "method": method_name,
         "persona": ...,
         "item_type": ...,
         "source_passage_id": ...,
         "target_passage_id": ...
      }
    """
    qid2meta = {}
    for obj in load_jsonl(path):
        qid = obj.get("qa_id") or obj.get("id")
        if not qid:
            continue

        persona = obj.get("persona") or "UNKNOWN"

        # item_type: SCHEMA has richer info; DPEL may not.
        item_type = obj.get("item_type")
        if not item_type:
            dbg = obj.get("debug_context") or {}
            item_type = dbg.get("schema_source_item_type") or dbg.get("schema_target_item_type")
        if not item_type:
            item_type = "UNKNOWN"

        dbg = obj.get("debug_context") or {}
        src_pid = dbg.get("source_passage_id") or dbg.get("source_id")
        tgt_pid = dbg.get("target_passage_id") or dbg.get("target_id")

        qid2meta[qid] = {
            "method": method_name,
            "persona": persona,
            "item_type": item_type,
            "source_passage_id": str(src_pid) if src_pid is not None else None,
            "target_passage_id": str(tgt_pid) if tgt_pid is not None else None,
        }
    return qid2meta


def load_reference_type_map(csv_path):
    """
    Build a map from (source_passage_id, target_passage_id) -> ReferenceType.
    """
    ref_map = {}
    if not os.path.isfile(csv_path):
        return ref_map

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            src_id = (row.get("SourcePassageID") or "").strip()
            tgt_id = (row.get("TargetPassageID") or "").strip()
            ref_type = (row.get("ReferenceType") or "UNKNOWN").strip() or "UNKNOWN"
            if src_id and tgt_id:
                ref_map[(src_id, tgt_id)] = ref_type
    return ref_map


def assign_reference_types(qid2meta, ref_map):
    """
    For each qa_id in qid2meta, attach reference_type using (src_pid, tgt_pid).
    """
    for qid, meta in qid2meta.items():
        src = meta.get("source_passage_id")
        tgt = meta.get("target_passage_id")
        if src and tgt and (src, tgt) in ref_map:
            meta["reference_type"] = ref_map[(src, tgt)]
        else:
            meta["reference_type"] = "UNKNOWN"


def summarize_by_group(method_name, group_name, qid2meta, qid_sets):
    """
    qid_sets: dict of step_name -> set(qa_id)
      e.g. {
        "generated": {...},
        "kept": {...},
        "eliminated": {...},
        "ir_good": {...},
        "qa_gold": {...},
      }

    group_name: one of {"persona", "item_type", "reference_type"}.

    Returns:
      rows: list of dicts with keys:
        group_value, generated, kept, eliminated, ir_good, qa_gold
    """
    steps = ["generated", "kept", "eliminated", "ir_good", "qa_gold"]
    # collect all groups that appear in *generated* for this method
    group_values = set()
    for qid in qid_sets["generated"]:
        g = qid2meta.get(qid, {}).get(group_name, "UNKNOWN")
        group_values.add(g)
    group_values = sorted(group_values)

    print("=" * 70)
    print(f"[{method_name}] Intrinsic analysis by {group_name}")
    header = [group_name] + steps
    print(" | ".join(f"{h:>12}" for h in header))
    print("-" * 70)

    rows = []
    for g in group_values:
        counts = {}
        for step in steps:
            c = 0
            for qid in qid_sets[step]:
                meta = qid2meta.get(qid)
                if not meta:
                    continue
                if meta.get(group_name, "UNKNOWN") == g:
                    c += 1
            counts[step] = c
        print(" | ".join(
            [f"{g:>12}"] + [f"{counts[s]:12d}" for s in steps]
        ))
        row = {"group_value": g}
        row.update(counts)
        rows.append(row)
    print()
    return rows


def write_group_csv(out_dir, method_name, group_name, rows):
    """
    Write rows from summarize_by_group to CSV:
      <out_dir>/<method_name>_<group_name>.csv
    """
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{method_name}_{group_name}.csv")
    fieldnames = ["group_value", "generated", "kept", "eliminated", "ir_good", "qa_gold"]
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)
    print(f"[info] wrote CSV: {out_path}")


# -------------------------------------------------------
# Main
# -------------------------------------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Intrinsic analysis by persona / item_type / reference_type per method."
    )
    ap.add_argument(
        "--dpel-gen",
        default="outputs/generation/dpel/all/answers.jsonl",
        help="DPEL generation file (all answers).",
    )
    ap.add_argument(
        "--schema-gen",
        default="outputs/generation/schema/all/answers.jsonl",
        help="SCHEMA generation file (all answers).",
    )
    ap.add_argument(
        "--dpel-kept",
        default="outputs/judging/curated/DPEL/kept.jsonl",
        help="Curated kept QAs for DPEL.",
    )
    ap.add_argument(
        "--dpel-elim",
        default="outputs/judging/curated/DPEL/eliminated.jsonl",
        help="Curated eliminated QAs for DPEL.",
    )
    ap.add_argument(
        "--schema-kept",
        default="outputs/judging/curated/SCHEMA/kept.jsonl",
        help="Curated kept QAs for SCHEMA.",
    )
    ap.add_argument(
        "--schema-elim",
        default="outputs/judging/curated/SCHEMA/eliminated.jsonl",
        help="Curated eliminated QAs for SCHEMA.",
    )
    ap.add_argument(
        "--ir-dpel-kept",
        default="outputs/judging/analysis/concordance_kept_dpel.jsonl",
        help="IR concordance for DPEL-kept.",
    )
    ap.add_argument(
        "--ir-schema-kept",
        default="outputs/judging/analysis/concordance_kept_schema.jsonl",
        help="IR concordance for SCHEMA-kept.",
    )
    ap.add_argument(
        "--final-dpel-qa",
        default="outputs/final/DPEL/RegRAG-Xref_DPEL_QA.jsonl",
        help="Final QA/RAG dataset for DPEL (qa_gold).",
    )
    ap.add_argument(
        "--final-schema-qa",
        default="outputs/final/SCHEMA/RegRAG-Xref_SCHEMA_QA.jsonl",
        help="Final QA/RAG dataset for SCHEMA (qa_gold).",
    )
    ap.add_argument(
        "--crossref-csv",
        default="data/CrossReferenceData.csv",
        help="Cross-reference CSV with ReferenceType info.",
    )
    ap.add_argument(
        "--ir-min-methods-hit-any",
        type=int,
        default=4,
        help="Min # of IR methods that must hit-any to be IR-good.",
    )
    ap.add_argument(
        "--out-dir-analysis",
        default="outputs/analysis_intrinsic",
        help="Directory to write per-method/group CSV tables.",
    )
    args = ap.parse_args()

    # Load reference types
    ref_map = load_reference_type_map(args.crossref_csv)

    # ---------------------------------------------------
    # DPEL
    # ---------------------------------------------------
    print("================================================================")
    print("[info] Analyzing method=DPEL")
    dpel_meta = load_generation_ids_with_meta(args.dpel_gen, method_name="DPEL")
    assign_reference_types(dpel_meta, ref_map)

    dpel_kept, dpel_elim = qid_sets_from_curated(args.dpel_kept, args.dpel_elim)
    dpel_ir_good = load_ir_good_ids(args.ir_dpel_kept, args.ir_min_methods_hit_any)
    dpel_qa_gold = load_qa_gold_ids(args.final_dpel_qa)

    dpel_generated = set(dpel_meta.keys())

    dpel_qid_sets = {
        "generated": dpel_generated,
        "kept": dpel_kept,
        "eliminated": dpel_elim,
        "ir_good": dpel_ir_good,
        "qa_gold": dpel_qa_gold,
    }

    rows_persona = summarize_by_group("DPEL", "persona", dpel_meta, dpel_qid_sets)
    rows_item    = summarize_by_group("DPEL", "item_type", dpel_meta, dpel_qid_sets)
    rows_ref     = summarize_by_group("DPEL", "reference_type", dpel_meta, dpel_qid_sets)

    write_group_csv(args.out_dir_analysis, "DPEL", "persona", rows_persona)
    write_group_csv(args.out_dir_analysis, "DPEL", "item_type", rows_item)
    write_group_csv(args.out_dir_analysis, "DPEL", "reference_type", rows_ref)

    # ---------------------------------------------------
    # SCHEMA
    # ---------------------------------------------------
    print("================================================================")
    print("[info] Analyzing method=SCHEMA")
    schema_meta = load_generation_ids_with_meta(args.schema_gen, method_name="SCHEMA")
    assign_reference_types(schema_meta, ref_map)

    schema_kept, schema_elim = qid_sets_from_curated(args.schema_kept, args.schema_elim)
    schema_ir_good = load_ir_good_ids(args.ir_schema_kept, args.ir_min_methods_hit_any)
    schema_qa_gold = load_qa_gold_ids(args.final_schema_qa)

    schema_generated = set(schema_meta.keys())

    schema_qid_sets = {
        "generated": schema_generated,
        "kept": schema_kept,
        "eliminated": schema_elim,
        "ir_good": schema_ir_good,
        "qa_gold": schema_qa_gold,
    }

    rows_persona_s = summarize_by_group("SCHEMA", "persona", schema_meta, schema_qid_sets)
    rows_item_s    = summarize_by_group("SCHEMA", "item_type", schema_meta, schema_qid_sets)
    rows_ref_s     = summarize_by_group("SCHEMA", "reference_type", schema_meta, schema_qid_sets)

    write_group_csv(args.out_dir_analysis, "SCHEMA", "persona", rows_persona_s)
    write_group_csv(args.out_dir_analysis, "SCHEMA", "item_type", rows_item_s)
    write_group_csv(args.out_dir_analysis, "SCHEMA", "reference_type", rows_ref_s)


if __name__ == "__main__":
    main()

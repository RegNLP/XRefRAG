#!/usr/bin/env python3
# sample_final_qas.py
# -*- coding: utf-8 -*-

"""
Sample final QAs (IR / QA datasets) with optional rich context.

Two modes:

  --mode simple
    → For each sampled QA, write a compact JSON with:
        qa_id, method, split, question, expected_answer,
        source_text, target_text

  --mode detailed
    → For each sampled QA, write a richer JSON with:
        - basic QA fields (qa_id, method, split, persona, reference_type)
        - source/target ids + full texts
        - schema info (semantic_hook, item types, answer_spans) when available
        - LLM-as-judge results (fused + per_judge) when available
        - IR concordance record (from concordance_kept_*.jsonl), if provided
        - Answer concordance record (from concordance_answer_*.jsonl), if provided

Additionally:
  - We skip any QA where ANY of:
      question, expected_answer, source_text, target_text
    individually exceeds PER_FIELD_LEN_THRESHOLD (default: 3000 chars).
"""

import argparse
import json
import os
import random
from typing import Dict, Any, List, Optional

PER_FIELD_LEN_THRESHOLD = 3000  # max chars per field


# --------------------
# IO helpers
# --------------------

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
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
    out: Dict[str, Dict[str, Any]] = {}
    for obj in items:
        qid = obj.get("qa_id") or obj.get("id") or obj.get("qid")
        if not qid:
            continue
        out[str(qid)] = obj
    return out


def load_ir_concordance(path: Optional[str]) -> Dict[str, Dict[str, Any]]:
    """
    Load IR concordance JSONL (from concordance_ir.py) and index by qid/qa_id.
    """
    if not path:
        return {}
    if not os.path.isfile(path):
        print(f"[warn] IR concordance file not found: {path}")
        return {}

    idx: Dict[str, Dict[str, Any]] = {}
    for obj in load_jsonl(path):
        qid = obj.get("qa_id") or obj.get("qid")
        if not qid:
            continue
        idx[str(qid)] = obj
    return idx


def load_answer_concordance(path: Optional[str]) -> Dict[str, Dict[str, Any]]:
    """
    Load answer-concordance JSONL (from concordance_answer_per_qa.py)
    and index by qa_id.
    """
    if not path:
        return {}
    if not os.path.isfile(path):
        print(f"[warn] answer concordance file not found: {path}")
        return {}

    idx: Dict[str, Dict[str, Any]] = {}
    for obj in load_jsonl(path):
        qid = obj.get("qa_id") or obj.get("qid")
        if not qid:
            continue
        idx[str(qid)] = obj
    return idx


# --------------------
# Curated helpers
# --------------------

def extract_schema_info(curated: Dict[str, Any]) -> Dict[str, Any]:
    """
    Try to pull schema-ish fields from a curated QA (mainly for SCHEMA method).
    Handles both top-level and nested-in-debug_context variants.
    """
    dc = curated.get("debug_context") or {}
    schema_obj: Dict[str, Any] = {}

    # semantic & citation hooks
    schema_obj["semantic_hook"] = (
        curated.get("semantic_hook")
        or dc.get("semantic_hook")
    )
    schema_obj["citation_hook"] = (
        curated.get("citation_hook")
        or dc.get("citation_hook")
    )

    # item types
    schema_obj["source_item_type"] = (
        curated.get("source_item_type")
        or dc.get("source_item_type")
    )
    schema_obj["target_item_type"] = (
        curated.get("target_item_type")
        or dc.get("target_item_type")
    )

    # answer spans
    schema_obj["answer_spans"] = (
        curated.get("answer_spans")
        or dc.get("answer_spans")
    )

    # target_is_title if present
    if "target_is_title" in curated:
        schema_obj["target_is_title"] = curated.get("target_is_title")
    elif "target_is_title" in dc:
        schema_obj["target_is_title"] = dc.get("target_is_title")

    return schema_obj


def extract_judging_info(curated: Dict[str, Any]) -> Dict[str, Any]:
    """
    Normalise judging info from curated QA; supports both:
      - judge_fused / judge_per_judge at top level
      - or nested under "judging": {fused, per_judge}
    """
    if "judging" in curated:
        j = curated["judging"] or {}
        return {
            "fused": j.get("fused"),
            "per_judge": j.get("per_judge"),
        }
    return {
        "fused": curated.get("judge_fused"),
        "per_judge": curated.get("judge_per_judge"),
    }


def get_source_target_text(curated: Optional[Dict[str, Any]]) -> (Optional[str], Optional[str]):
    if not curated:
        return None, None
    dc = curated.get("debug_context") or {}
    return dc.get("source_text"), dc.get("target_text")


# --------------------
# Main
# --------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Sample final QAs with optional detailed metadata."
    )
    ap.add_argument(
        "--input",
        required=True,
        help="Final dataset JSONL (e.g. RegRAG-Xref_SCHEMA_QA.jsonl or *_ir.jsonl).",
    )
    ap.add_argument(
        "--mode",
        choices=["simple", "detailed"],
        required=True,
        help="Sampling mode: simple | detailed.",
    )
    ap.add_argument(
        "--max",
        type=int,
        default=10,
        help="Maximum number of QAs to sample.",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=13,
        help="Random seed for sampling.",
    )
    ap.add_argument(
        "--schema-curated",
        help="Path to curated SCHEMA kept.jsonl (for source/target text + schema/judging).",
    )
    ap.add_argument(
        "--dpel-curated",
        help="Path to curated DPEL kept.jsonl (for source/target text + judging).",
    )
    ap.add_argument(
        "--ir-jsonl",
        help="IR concordance JSONL (e.g. concordance_kept_schema.jsonl or concordance_kept_dpel.jsonl).",
    )
    ap.add_argument(
        "--answer-jsonl",
        help="Answer-concordance JSONL (e.g. concordance_answer_kept_schema.jsonl).",
    )
    ap.add_argument(
        "--output",
        required=True,
        help="Output JSONL with sampled QAs.",
    )
    args = ap.parse_args()

    # Load final dataset
    final_items = load_jsonl(args.input)
    if not final_items:
        raise SystemExit(f"No items found in final dataset: {args.input}")

    # Infer method from final items or filename
    method_name = None
    for obj in final_items:
        m = obj.get("method")
        if m in {"DPEL", "SCHEMA"}:
            method_name = m
            break
    if method_name is None:
        low = os.path.basename(args.input).lower()
        if "schema" in low:
            method_name = "SCHEMA"
        elif "dpel" in low:
            method_name = "DPEL"
        else:
            method_name = "UNKNOWN"

    print(f"[info] inferred method={method_name} from input")

    # Index final items by qa_id
    final_by_id = index_by_qa_id(final_items)
    qa_ids = list(final_by_id.keys())

    # Shuffle all QA IDs; we'll filter by length as we go
    rnd = random.Random(args.seed)
    rnd.shuffle(qa_ids)

    # Load curated data (schema + dpel); we'll select per method
    schema_curated_idx: Dict[str, Dict[str, Any]] = {}
    dpel_curated_idx: Dict[str, Dict[str, Any]] = {}
    if args.schema_curated and os.path.isfile(args.schema_curated):
        schema_curated_idx = index_by_qa_id(load_jsonl(args.schema_curated))
        print(f"[info] loaded {len(schema_curated_idx)} SCHEMA curated items")
    if args.dpel_curated and os.path.isfile(args.dpel_curated):
        dpel_curated_idx = index_by_qa_id(load_jsonl(args.dpel_curated))
        print(f"[info] loaded {len(dpel_curated_idx)} DPEL curated items")

    # Load IR + answer concordance indices
    ir_idx = load_ir_concordance(args.ir_jsonl)
    answer_idx = load_answer_concordance(args.answer_jsonl)

    # Prepare output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    out_f = open(args.output, "w", encoding="utf-8")

    n_written = 0
    n_skipped_len = 0

    for qid in qa_ids:
        if args.max and n_written >= args.max:
            break

        final_obj = final_by_id.get(qid)
        if not final_obj:
            continue

        # pick curated source
        if method_name == "SCHEMA":
            curated = schema_curated_idx.get(qid)
        elif method_name == "DPEL":
            curated = dpel_curated_idx.get(qid)
        else:
            curated = schema_curated_idx.get(qid) or dpel_curated_idx.get(qid)

        source_text, target_text = get_source_target_text(curated)

        # resolve Q/A text
        question = final_obj.get("question") or (curated or {}).get("question")
        expected_answer = final_obj.get("expected_answer") or (curated or {}).get("expected_answer")

        # per-field length check
        lengths = {
            "question": len(question or ""),
            "expected_answer": len(expected_answer or ""),
            "source_text": len(source_text or ""),
            "target_text": len(target_text or ""),
        }
        if any(v > PER_FIELD_LEN_THRESHOLD for v in lengths.values()):
            n_skipped_len += 1
            continue

        if args.mode == "simple":
            simple_rec = {
                "qa_id": qid,
                "method": method_name,
                "split": final_obj.get("split"),
                "question": question,
                "expected_answer": expected_answer,
                "source_text": source_text,
                "target_text": target_text,
            }
            out_f.write(json.dumps(simple_rec, ensure_ascii=False) + "\n")
            n_written += 1
            continue

        # detailed mode
        debug_context = (curated or {}).get("debug_context") or {}
        extra_fields = (curated or {}).get("extra_fields") or {}

        # schema info (mainly meaningful for SCHEMA method)
        schema_info = extract_schema_info(curated) if curated else {}

        # judging info
        judging_info = extract_judging_info(curated) if curated else {}

        # IR + answer concordance for this qa_id
        ir_info = ir_idx.get(qid)
        answer_info = answer_idx.get(qid)

        # smarter reference_type fallback
        ref_type = (
            final_obj.get("reference_type")
            or (curated or {}).get("reference_type")
            or debug_context.get("reference_type")
            or extra_fields.get("reference_type")
        )

        detailed_rec: Dict[str, Any] = {
            "qa_id": qid,
            "method": method_name,
            "split": final_obj.get("split"),
            "persona": final_obj.get("persona") or (curated or {}).get("persona"),
            "reference_type": ref_type,
            "question": question,
            "expected_answer": expected_answer,
            "source_passage_id": final_obj.get("source_passage_id") or debug_context.get("source_passage_id"),
            "target_passage_id": final_obj.get("target_passage_id") or debug_context.get("target_passage_id"),
            "source_text": source_text,
            "target_text": target_text,
            "schema": schema_info if schema_info else None,
            "judging": judging_info if judging_info else None,
            "ir_concordance": ir_info,
            "answer_concordance": answer_info,
        }

        out_f.write(json.dumps(detailed_rec, ensure_ascii=False) + "\n")
        n_written += 1

    out_f.close()
    print(f"[info] wrote {n_written} records to {args.output}")
    if n_skipped_len:
        print(f"[info] skipped {n_skipped_len} items due to a field > {PER_FIELD_LEN_THRESHOLD} chars")


if __name__ == "__main__":
    main()

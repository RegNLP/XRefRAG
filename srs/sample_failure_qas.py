#!/usr/bin/env python3
# sample_failure_qas.py
# -*- coding: utf-8 -*-

"""
Sample *failure* QAs for RegRAG-Xref.

Failure types (per qa_id):

  - ir_low:
      low IR concordance
      (ir.low_concordance_any == True)
      → sampled from curated *kept* set + IR/answer concordance

  - answer_low:
      low answer concordance
      (answer.low_concordance_success == True)
      → sampled from curated *kept* set + IR/answer concordance

  - both_low:
      both of the above
      → sampled from curated *kept* set + IR/answer concordance

  - judging_elim:
      QAs that were eliminated by LLM-as-judge
      → sampled from curated *eliminated* set (no IR/answer metrics)

All modes:
  - only sample from the relevant curated set (kept or eliminated)
  - skip items where any of:
      question, expected_answer, source_text, target_text
    is longer than 3000 characters

Output schema matches sample_final_qas.py (detailed mode), so
jsonl_to_markdown_samples.py can be used directly.
"""

import argparse
import json
import os
import random
from typing import Dict, Any, List, Optional, Tuple


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
    if not path or not os.path.isfile(path):
        return {}
    idx: Dict[str, Dict[str, Any]] = {}
    for obj in load_jsonl(path):
        qid = obj.get("qa_id") or obj.get("qid")
        if not qid:
            continue
        idx[str(qid)] = obj
    return idx


def load_answer_concordance(path: Optional[str]) -> Dict[str, Dict[str, Any]]:
    if not path or not os.path.isfile(path):
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
    Pull schema-ish fields from curated QA (mainly for SCHEMA method).
    Handles both top-level and nested-in-debug_context variants.
    """
    dc = curated.get("debug_context") or {}
    schema_obj: Dict[str, Any] = {}

    schema_obj["semantic_hook"] = (
        curated.get("semantic_hook")
        or dc.get("semantic_hook")
    )
    schema_obj["citation_hook"] = (
        curated.get("citation_hook")
        or dc.get("citation_hook")
    )
    schema_obj["source_item_type"] = (
        curated.get("source_item_type")
        or dc.get("source_item_type")
    )
    schema_obj["target_item_type"] = (
        curated.get("target_item_type")
        or dc.get("target_item_type")
    )
    schema_obj["answer_spans"] = (
        curated.get("answer_spans")
        or dc.get("answer_spans")
    )

    if "target_is_title" in curated:
        schema_obj["target_is_title"] = curated.get("target_is_title")
    elif "target_is_title" in dc:
        schema_obj["target_is_title"] = dc.get("target_is_title")

    # keep only if something is actually non-empty
    if not any(v for v in schema_obj.values()):
        return {}
    return schema_obj


def extract_judging_info(curated: Dict[str, Any]) -> Dict[str, Any]:
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


def get_source_target_text(curated: Optional[Dict[str, Any]]) -> Tuple[Optional[str], Optional[str]]:
    if not curated:
        return None, None
    dc = curated.get("debug_context") or {}
    return dc.get("source_text"), dc.get("target_text")


def any_field_too_long(
    question: Optional[str],
    expected_answer: Optional[str],
    source_text: Optional[str],
    target_text: Optional[str],
    max_len: int = 3000,
) -> bool:
    fields = [question, expected_answer, source_text, target_text]
    return any((f is not None and len(f) > max_len) for f in fields)


# --------------------
# Main
# --------------------

def main() -> None:
    ap = argparse.ArgumentParser(
        description="Sample failure QAs (IR / answer / judging-eliminated)."
    )
    ap.add_argument(
        "--method",
        choices=["DPEL", "SCHEMA"],
        required=True,
        help="Which method to sample failures for.",
    )
    ap.add_argument(
        "--curated-kept",
        help="Curated kept QAs for this method (for ir_low / answer_low / both_low).",
    )
    ap.add_argument(
        "--curated-elim",
        help="Curated eliminated QAs for this method (for failure-type=judging_elim).",
    )
    ap.add_argument(
        "--schema-curated",
        help="SCHEMA curated kept.jsonl (for schema hooks if method=SCHEMA).",
    )
    ap.add_argument(
        "--dpel-curated",
        help="DPEL curated kept.jsonl (for judging info if method=DPEL).",
    )
    ap.add_argument(
        "--ir-jsonl",
        help="IR concordance JSONL for kept set (for ir_low / both_low).",
    )
    ap.add_argument(
        "--answer-jsonl",
        help="Answer concordance JSONL for kept set (for answer_low / both_low).",
    )
    ap.add_argument(
        "--failure-type",
        choices=["ir_low", "answer_low", "both_low", "judging_elim"],
        required=True,
        help="Which failure type to sample.",
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
        "--output",
        required=True,
        help="Output JSONL with sampled failure QAs.",
    )
    args = ap.parse_args()

    method_name = args.method

    # ----------------- failure_type = judging_elim -----------------
    if args.failure_type == "judging_elim":
        if not args.curated_elim:
            raise SystemExit("--curated-elim is required for failure-type=judging_elim")

        elim_items = load_jsonl(args.curated_elim)
        elim_idx = index_by_qa_id(elim_items)
        qids = list(elim_idx.keys())

        rnd = random.Random(args.seed)
        rnd.shuffle(qids)

        os.makedirs(os.path.dirname(args.output), exist_ok=True)
        out_f = open(args.output, "w", encoding="utf-8")

        n_written = 0
        for qid in qids:
            if n_written >= args.max:
                break

            curated_full = elim_idx.get(qid)
            if not curated_full:
                continue

            debug_context = (curated_full or {}).get("debug_context") or {}
            extra_fields = (curated_full or {}).get("extra_fields") or {}

            source_text, target_text = get_source_target_text(curated_full)
            question = curated_full.get("question")
            expected_answer = curated_full.get("expected_answer")

            if any_field_too_long(question, expected_answer, source_text, target_text, max_len=3000):
                continue

            # schema info only for SCHEMA
            schema_info = extract_schema_info(curated_full) if method_name == "SCHEMA" else {}

            judging_info = extract_judging_info(curated_full) if curated_full else {}

            ref_type = (
                curated_full.get("reference_type")
                or debug_context.get("reference_type")
                or extra_fields.get("reference_type")
            )

            detailed_rec: Dict[str, Any] = {
                "qa_id": qid,
                "method": method_name,
                "split": "eliminated",  # explicitly mark as judge-eliminated
                "persona": curated_full.get("persona"),
                "reference_type": ref_type,
                "question": question,
                "expected_answer": expected_answer,
                "source_passage_id": debug_context.get("source_passage_id"),
                "target_passage_id": debug_context.get("target_passage_id"),
                "source_text": source_text,
                "target_text": target_text,
                "schema": schema_info if schema_info else None,
                "judging": judging_info if judging_info else None,
                "ir_concordance": None,
                "answer_concordance": None,
            }

            out_f.write(json.dumps(detailed_rec, ensure_ascii=False) + "\n")
            n_written += 1

        out_f.close()
        print(f"[info] wrote {n_written} judging-eliminated records to {args.output}")
        return

    # ----------------- other failure types: need kept + IR/answer -----------------
    if not args.curated_kept:
        raise SystemExit("--curated-kept is required for ir_low / answer_low / both_low")
    if not args.ir_jsonl and args.failure_type in {"ir_low", "both_low"}:
        raise SystemExit("--ir-jsonl is required for failure-type=ir_low or both_low")
    if not args.answer_jsonl and args.failure_type in {"answer_low", "both_low"}:
        raise SystemExit("--answer-jsonl is required for failure-type=answer_low or both_low")

    # base curated for this method (kept)
    curated_items = load_jsonl(args.curated_kept)
    curated_idx = index_by_qa_id(curated_items)

    # additional curated indices (for schema hooks / judging)
    schema_curated_idx: Dict[str, Dict[str, Any]] = {}
    dpel_curated_idx: Dict[str, Dict[str, Any]] = {}
    if args.schema_curated and os.path.isfile(args.schema_curated):
        schema_curated_idx = index_by_qa_id(load_jsonl(args.schema_curated))
    if args.dpel_curated and os.path.isfile(args.dpel_curated):
        dpel_curated_idx = index_by_qa_id(load_jsonl(args.dpel_curated))

    # IR + answer concordance
    ir_idx = load_ir_concordance(args.ir_jsonl)
    answer_idx = load_answer_concordance(args.answer_jsonl)

    # candidate ids: intersection of curated-kept and IR / answer indices
    all_qids = set(curated_idx.keys())
    ir_qids = set(ir_idx.keys())
    ans_qids = set(answer_idx.keys())
    common_qids = all_qids & ir_qids & ans_qids

    # filter by failure type
    failure_qids: List[str] = []
    for qid in common_qids:
        ir = ir_idx.get(qid) or {}
        ans = answer_idx.get(qid) or {}
        ir_low = bool(ir.get("low_concordance_any"))
        ans_low = bool(ans.get("low_concordance_success"))

        if args.failure_type == "ir_low" and ir_low:
            failure_qids.append(qid)
        elif args.failure_type == "answer_low" and ans_low:
            failure_qids.append(qid)
        elif args.failure_type == "both_low" and ir_low and ans_low:
            failure_qids.append(qid)

    if not failure_qids:
        raise SystemExit(f"No QAs found for failure_type={args.failure_type}")

    rnd = random.Random(args.seed)
    rnd.shuffle(failure_qids)

    # prepare output
    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    out_f = open(args.output, "w", encoding="utf-8")

    n_written = 0

    for qid in failure_qids:
        if n_written >= args.max:
            break

        curated = curated_idx.get(qid)
        if not curated:
            continue

        # choose best curated source for extra metadata
        if method_name == "SCHEMA":
            curated_full = schema_curated_idx.get(qid, curated)
        elif method_name == "DPEL":
            curated_full = dpel_curated_idx.get(qid, curated)
        else:
            curated_full = curated

        debug_context = (curated_full or {}).get("debug_context") or {}
        extra_fields = (curated_full or {}).get("extra_fields") or {}

        source_text, target_text = get_source_target_text(curated_full)

        question = curated_full.get("question")
        expected_answer = curated_full.get("expected_answer")

        # skip if any field is individually too long
        if any_field_too_long(question, expected_answer, source_text, target_text, max_len=3000):
            continue

        # schema info only really meaningful for SCHEMA
        schema_info = extract_schema_info(curated_full) if method_name == "SCHEMA" else {}

        judging_info = extract_judging_info(curated_full) if curated_full else {}

        ir_info = ir_idx.get(qid)
        ans_info = answer_idx.get(qid)

        ref_type = (
            curated_full.get("reference_type")
            or debug_context.get("reference_type")
            or extra_fields.get("reference_type")
        )

        detailed_rec: Dict[str, Any] = {
            "qa_id": qid,
            "method": method_name,
            "split": "n/a",  # not part of final train/dev/test splits
            "persona": curated_full.get("persona"),
            "reference_type": ref_type,
            "question": question,
            "expected_answer": expected_answer,
            "source_passage_id": debug_context.get("source_passage_id"),
            "target_passage_id": debug_context.get("target_passage_id"),
            "source_text": source_text,
            "target_text": target_text,
            "schema": schema_info if schema_info else None,
            "judging": judging_info if judging_info else None,
            "ir_concordance": ir_info,
            "answer_concordance": ans_info,
        }

        out_f.write(json.dumps(detailed_rec, ensure_ascii=False) + "\n")
        n_written += 1

    out_f.close()
    print(f"[info] wrote {n_written} failure records to {args.output}")


if __name__ == "__main__":
    main()

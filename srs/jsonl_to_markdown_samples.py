#!/usr/bin/env python3
# jsonl_to_markdown_samples.py
# -*- coding: utf-8 -*-

"""
Convert sampled QA JSONL (from sample_final_qas.py) into a readable Markdown report.

Inputs: sample_*_detailed.jsonl with records like:
  qa_id, method, split, persona, reference_type,
  question, expected_answer,
  source_text, target_text,
  schema, judging, ir_concordance, answer_concordance

Output: a .md file with, per QA:
  - Header with basic metadata
  - Question + expected answer (full)
  - Source & target texts (full)
  - Schema hooks (SCHEMA only, and only if present)
  - LLM-as-judge fused info
  - IR concordance summary (no per-method table)
  - Answer concordance summary (no per-retriever table)
"""

import argparse
import json
import os
from typing import Any, Dict, List, Optional


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


def format_schema_block(method: str, schema: Optional[Dict[str, Any]]) -> str:
    # Do NOT show schema block for DPEL
    if method != "SCHEMA":
        return ""

    if not schema:
        return ""

    # only print fields that actually have values
    lines = []
    sem = schema.get("semantic_hook")
    cit = schema.get("citation_hook")
    sit = schema.get("source_item_type")
    tit = schema.get("target_item_type")
    spans = schema.get("answer_spans")

    if not any([sem, cit, sit, tit, spans]):
        return ""

    lines.append("**Schema hooks & item types (SCHEMA only):**")
    if sem:
        lines.append(f"- Semantic hook: `{sem}`")
    if cit:
        lines.append(f"- Citation hook: `{cit}`")
    if sit:
        lines.append(f"- Source item type: `{sit}`")
    if tit:
        lines.append(f"- Target item type: `{tit}`")
    if spans:
        # just show number of spans to avoid long dumps
        lines.append(f"- Answer spans: {len(spans)} span(s) annotated")
    lines.append("")
    return "\n".join(lines)


def format_judging_block(judging: Optional[Dict[str, Any]]) -> str:
    if not judging:
        return ""

    fused = judging.get("fused") or {}
    passed = fused.get("passed")
    final_score = fused.get("final_score")
    subs = fused.get("subscores") or {}
    correctness = subs.get("correctness")
    dual_use = subs.get("dual_use")
    realism = subs.get("realism")

    lines = []
    lines.append("**LLM-as-judge summary:**")
    if passed is not None:
        lines.append(f"- Fused passed: **{passed}**")
    if final_score is not None:
        lines.append(f"- Fused score: **{final_score}** (0–10)")
    if correctness is not None or dual_use is not None or realism is not None:
        parts = []
        if correctness is not None:
            parts.append(f"correctness={correctness}")
        if dual_use is not None:
            parts.append(f"dual_use={dual_use}")
        if realism is not None:
            parts.append(f"realism={realism}")
        lines.append(f"- Subscores: " + ", ".join(parts))
    lines.append("")
    return "\n".join(lines)


def format_ir_block(ir: Optional[Dict[str, Any]]) -> str:
    if not ir:
        return ""

    num_rel = ir.get("num_rel")
    num_any = ir.get("num_methods_hit_any")
    num_all = ir.get("num_methods_hit_all")
    high = ir.get("high_concordance_any")
    low = ir.get("low_concordance_any")
    k = ir.get("k")

    methods = ir.get("methods") or {}
    method_names = sorted(methods.keys())

    lines = []
    lines.append("**IR retrieval concordance:**")
    if num_rel is not None:
        lines.append(f"- Number of relevant passages (qrels): **{num_rel}**")
    if k is not None:
        lines.append(f"- Evaluated at top-{k} per retriever")
    if num_any is not None:
        lines.append(f"- Methods hitting ≥1 relevant in top-{k}: **{num_any}** / {len(method_names)}")
    if num_all is not None:
        lines.append(f"- Methods retrieving all relevant in top-{k}: **{num_all}** / {len(method_names)}")
    if high is not None:
        lines.append(f"- High concordance (hit-any): **{bool(high)}**")
    if low is not None:
        lines.append(f"- Low concordance (hit-any): **{bool(low)}**")

    # short per-method summary (no table, just names + hit_any/hit_all)
    if methods:
        good_any = []
        good_all = []
        for m in method_names:
            info = methods[m] or {}
            if info.get("hit_any"):
                good_any.append(m)
            if info.get("hit_all"):
                good_all.append(m)
        if good_any:
            lines.append(f"- Retrievers with ≥1 relevant: {', '.join(good_any)}")
        if good_all:
            lines.append(f"- Retrievers with all relevant: {', '.join(good_all)}")

    lines.append("")
    return "\n".join(lines)


def format_answer_block(answer: Optional[Dict[str, Any]]) -> str:
    if not answer:
        return ""

    num_methods = answer.get("num_methods")
    num_success = answer.get("num_methods_success")
    high = answer.get("high_concordance_success")
    low = answer.get("low_concordance_success")
    methods = answer.get("methods") or {}
    retrievers = sorted(methods.keys())

    lines = []
    lines.append("**Answer quality / RAG concordance:**")
    if num_methods is not None and num_success is not None:
        lines.append(f"- Methods with good answer: **{num_success} / {num_methods}**")
    if high is not None:
        lines.append(f"- High concordance on answer quality: **{bool(high)}**")
    if low is not None:
        lines.append(f"- Low concordance on answer quality: **{bool(low)}**")

    # short per-retriever success summary (no numeric table)
    if methods:
        ok = [r for r in retrievers if methods.get(r, {}).get("success")]
        bad = [r for r in retrievers if not methods.get(r, {}).get("success")]
        if ok:
            lines.append(f"- Retrievers passing thresholds: {', '.join(ok)}")
        if bad:
            lines.append(f"- Retrievers failing thresholds: {', '.join(bad)}")

    lines.append("")
    return "\n".join(lines)


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Convert detailed QA samples JSONL into Markdown."
    )
    ap.add_argument(
        "--input",
        required=True,
        help="Input JSONL (e.g. sample_SCHEMA_detailed.jsonl).",
    )
    ap.add_argument(
        "--output",
        required=True,
        help="Output Markdown file.",
    )
    args = ap.parse_args()

    items = load_jsonl(args.input)
    if not items:
        raise SystemExit(f"No records in {args.input}")

    os.makedirs(os.path.dirname(args.output), exist_ok=True)

    with open(args.output, "w", encoding="utf-8") as out:
        out.write(f"# RegRAG-Xref sampled QAs\n\n")
        out.write(f"_Source file: `{os.path.basename(args.input)}`_\n\n")

        for i, obj in enumerate(items, start=1):
            qa_id = obj.get("qa_id")
            method = obj.get("method")
            split = obj.get("split")
            persona = obj.get("persona")
            ref_type = obj.get("reference_type")

            question = obj.get("question") or "N/A"
            expected_answer = obj.get("expected_answer") or "N/A"
            source_text = obj.get("source_text") or "N/A"
            target_text = obj.get("target_text") or "N/A"
            schema = obj.get("schema")
            judging = obj.get("judging")
            ir_conc = obj.get("ir_concordance")
            ans_conc = obj.get("answer_concordance")

            out.write(f"## QA {i}: {method} — {split}\n\n")
            meta_bits = []
            if persona:
                meta_bits.append(f"persona: **{persona}**")
            if ref_type is not None:
                meta_bits.append(f"reference_type: **{ref_type}**")
            if meta_bits:
                out.write("*" + " · ".join(meta_bits) + "*\n\n")

            out.write(f"**QA ID:** `{qa_id}`\n\n")

            out.write("### Question\n\n")
            out.write(question + "\n\n")

            out.write("### Expected answer\n\n")
            out.write(expected_answer + "\n\n")

            out.write("### Source passage\n\n")
            out.write(source_text + "\n\n")

            out.write("### Target passage\n\n")
            out.write(target_text + "\n\n")

            # Schema (SCHEMA only)
            schema_block = format_schema_block(method, schema)
            if schema_block:
                out.write(schema_block + "\n")

            # Judging
            judging_block = format_judging_block(judging)
            if judging_block:
                out.write(judging_block + "\n")

            # IR concordance
            ir_block = format_ir_block(ir_conc)
            if ir_block:
                out.write(ir_block + "\n")

            # Answer concordance
            ans_block = format_answer_block(ans_conc)
            if ans_block:
                out.write(ans_block + "\n")

            out.write("\n---\n\n")

    print(f"[info] wrote Markdown report to {args.output}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Inspect QAs Stats for DPEL/SCHEMA outputs.

Reads one or more JSONL files (each line is a QA object with fields like
qa_id, persona, question, expected_answer, debug_context, method, gen_model, ...)

Reports:
- Totals, by file
- Persona distribution
- Method distribution
- ReferenceType distribution (from debug_context)
- Target/Source item type distribution (from debug_context)
- Answer tag coverage: contains [#SRC:<id>] and [#TGT:<id>]
- Question "citation-y" patterns (Rule/Section/etc.) count
- Question/Answer length stats (min/max/avg/median)
- Duplicate question detection across all inputs (normalized)
- Answer span types distribution (from debug_context.answer_spans)
- Samples of violations (missing tags, citation in question)

Optionally writes a CSV row per input file with headline metrics.

Usage:
  python tools/inspect_qas_stats.py \
      --inputs outputs/generation/dpel/all/answers.jsonl \
               outputs/generation/schema/all/answers.jsonl \
      --out_csv outputs/generation/qa_stats_summary.csv \
      --sample 5
"""

import argparse
import json
import math
import os
import re
import sys
from collections import Counter, defaultdict
from statistics import mean, median

CITATION_PAT = re.compile(
    r"(?i)(\b(rule|section|article|chapter|part|appendix|schedule)\b\s*\d+([\.\-]\d+)*(\([^)]+\))?|\bFSMR\b|\b\d+(?:\.\d+)+(?:\([^)]+\))*)"
)

STOPWORDS = set(("""
a an the and or of to in for on by with from as is are be this that these those its under subject
rule section chapter part article must shall may can if when provided unless including
""".split()))

def norm_ws(s):
    return re.sub(r"\s+", " ", (s or "")).strip()

def normalize_question(q: str) -> str:
    q = (q or "").lower().strip()
    q = re.sub(r"[^a-z0-9\s?]", " ", q)
    q = re.sub(r"\s+", " ", q)
    return q

def has_both_tags(answer: str, src_id: str, tgt_id: str) -> bool:
    if not src_id or not tgt_id:
        return False
    return (f"[#SRC:{src_id}]" in (answer or "")) and (f"[#TGT:{tgt_id}]" in (answer or ""))

def length_stats(values):
    if not values:
        return {"min": 0, "max": 0, "avg": 0.0, "median": 0.0}
    return {
        "min": int(min(values)),
        "max": int(max(values)),
        "avg": float(mean(values)),
        "median": float(median(values)),
    }

def load_jsonl(path):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for ln, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
                items.append(obj)
            except Exception as e:
                sys.stderr.write(f"[WARN] {path}:{ln} JSON parse error: {e}\n")
    return items

def collect_per_file_stats(path):
    data = load_jsonl(path)

    personas = Counter()
    methods = Counter()
    ref_types = Counter()
    src_types = Counter()
    tgt_types = Counter()
    span_types = Counter()

    qlens, alens = [], []
    citation_q_cnt = 0
    missing_tags_cnt = 0
    bad_debug_cnt = 0

    qs_norm_seen = set()
    dups_within_file = 0

    samples_missing_tags = []
    samples_citation_q = []
    samples_bad_debug = []

    for obj in data:
        persona = obj.get("persona") or ""
        methods[obj.get("method") or ""] += 1
        personas[persona] += 1

        q = norm_ws(obj.get("question"))
        a = norm_ws(obj.get("expected_answer"))

        if q:
            qlens.append(len(q))
            if CITATION_PAT.search(q):
                citation_q_cnt += 1
                if len(samples_citation_q) < 10:
                    samples_citation_q.append({"qa_id": obj.get("qa_id"), "question": q[:220]})
        if a:
            alens.append(len(a))

        dbg = obj.get("debug_context") or {}
        if not isinstance(dbg, dict):
            bad_debug_cnt += 1
            if len(samples_bad_debug) < 10:
                samples_bad_debug.append({"qa_id": obj.get("qa_id"), "reason": "debug_context not dict"})
            dbg = {}

        ref_types[ (dbg.get("reference_type") or "").strip() or ""] += 1
        src_types[ (dbg.get("source_item_type") or "").strip() or ""] += 1
        tgt_types[ (dbg.get("target_item_type") or "").strip() or ""] += 1

        # Answer spans
        spans = dbg.get("answer_spans") or []
        if isinstance(spans, list):
            for sp in spans:
                t = (sp.get("type") or "").strip() or "FREEFORM"
                span_types[t] += 1

        # tag check
        src_id = str(dbg.get("source_passage_id") or "")
        tgt_id = str(dbg.get("target_passage_id") or "")
        if not has_both_tags(a, src_id, tgt_id):
            missing_tags_cnt += 1
            if len(samples_missing_tags) < 10:
                samples_missing_tags.append({
                    "qa_id": obj.get("qa_id"),
                    "persona": persona,
                    "src_id": src_id,
                    "tgt_id": tgt_id,
                    "answer_snippet": a[:220]
                })

        # duplicate within file (normalized question)
        k = normalize_question(q)
        if k in qs_norm_seen:
            dups_within_file += 1
        else:
            qs_norm_seen.add(k)

    out = {
        "path": path,
        "count": len(data),
        "personas": personas,
        "methods": methods,
        "ref_types": ref_types,
        "source_item_types": src_types,
        "target_item_types": tgt_types,
        "span_types": span_types,
        "qlen_stats": length_stats(qlens),
        "alen_stats": length_stats(alens),
        "citation_q_cnt": citation_q_cnt,
        "missing_tags_cnt": missing_tags_cnt,
        "bad_debug_cnt": bad_debug_cnt,
        "dups_within_file": dups_within_file,
        "samples": {
            "missing_tags": samples_missing_tags,
            "citation_in_question": samples_citation_q,
            "bad_debug": samples_bad_debug,
        }
    }
    return out, data

def print_block(title):
    print("\n" + "=" * 72)
    print(title)
    print("=" * 72)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--inputs", nargs="+", required=True, help="One or more JSONL files to inspect.")
    ap.add_argument("--out_csv", default=None, help="Optional CSV summary per file.")
    ap.add_argument("--sample", type=int, default=5, help="Max samples to print for each issue type.")
    args = ap.parse_args()

    per_file = []
    all_questions_norm = set()
    cross_dups = 0
    total_count = 0
    grand_personas = Counter()
    grand_methods = Counter()
    grand_ref_types = Counter()
    grand_src_types = Counter()
    grand_tgt_types = Counter()
    grand_span_types = Counter()

    for p in args.inputs:
        stats, data = collect_per_file_stats(p)
        per_file.append(stats)

        # aggregate grand totals
        total_count += stats["count"]
        grand_personas.update(stats["personas"])
        grand_methods.update(stats["methods"])
        grand_ref_types.update(stats["ref_types"])
        grand_src_types.update(stats["source_item_types"])
        grand_tgt_types.update(stats["target_item_types"])
        grand_span_types.update(stats["span_types"])

        # cross-file duplicate question detection
        for obj in data:
            k = normalize_question(obj.get("question") or "")
            if k in all_questions_norm:
                cross_dups += 1
            else:
                all_questions_norm.add(k)

    # Print per-file
    for st in per_file:
        print_block(f"FILE: {st['path']}")
        print(f"Total QAs: {st['count']}")
        print(f"Personas: {dict(st['personas'])}")
        print(f"Methods: {dict(st['methods'])}")
        print(f"ReferenceType: {dict(st['ref_types'])}")
        print(f"Source item types: {dict(st['source_item_types'])}")
        print(f"Target item types: {dict(st['target_item_types'])}")
        print(f"Answer span types: {dict(st['span_types'])}")
        print(f"Question length (chars): {st['qlen_stats']}")
        print(f"Answer   length (chars): {st['alen_stats']}")
        print(f"Questions w/ citation-like tokens: {st['citation_q_cnt']}")
        print(f"Answers missing both tags [#SRC:..] & [#TGT:..]: {st['missing_tags_cnt']}")
        print(f"Entries with bad debug_context: {st['bad_debug_cnt']}")
        print(f"Duplicate questions within this file: {st['dups_within_file']}")

        # Samples
        if st["samples"]["citation_in_question"]:
            print("\n- Samples: Citation-like in QUESTION")
            for s in st["samples"]["citation_in_question"][:args.sample]:
                print(f"  qa_id={s.get('qa_id')}  q~ {s.get('question')}")
        if st["samples"]["missing_tags"]:
            print("\n- Samples: ANSWER missing tags")
            for s in st["samples"]["missing_tags"][:args.sample]:
                print(f"  qa_id={s.get('qa_id')} persona={s.get('persona')} "
                      f"SRC={s.get('src_id')} TGT={s.get('tgt_id')} ans~ {s.get('answer_snippet')}")
        if st["samples"]["bad_debug"]:
            print("\n- Samples: bad debug_context")
            for s in st["samples"]["bad_debug"][:args.sample]:
                print(f"  qa_id={s.get('qa_id')} reason={s.get('reason')}")

    # Grand totals
    print_block("GRAND TOTALS (across all inputs)")
    print(f"Files: {len(per_file)}")
    print(f"Total QAs: {total_count}")
    print(f"Personas: {dict(grand_personas)}")
    print(f"Methods: {dict(grand_methods)}")
    print(f"ReferenceType: {dict(grand_ref_types)}")
    print(f"Source item types: {dict(grand_src_types)}")
    print(f"Target item types: {dict(grand_tgt_types)}")
    print(f"Answer span types: {dict(grand_span_types)}")
    print(f"Cross-file duplicate questions (normalized): {cross_dups}")

    # CSV export
    if args.out_csv:
        import csv
        os.makedirs(os.path.dirname(os.path.abspath(args.out_csv)), exist_ok=True)
        fields = [
            "path", "count",
            "personas_professional", "personas_basic",
            "methods_DPEL", "methods_SCHEMA",
            "missing_tags_cnt", "citation_q_cnt", "bad_debug_cnt",
            "dups_within_file",
            "qlen_min", "qlen_max", "qlen_avg", "qlen_median",
            "alen_min", "alen_max", "alen_avg", "alen_median",
        ]
        with open(args.out_csv, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            for st in per_file:
                row = {
                    "path": st["path"],
                    "count": st["count"],
                    "personas_professional": st["personas"].get("professional", 0),
                    "personas_basic": st["personas"].get("basic", 0),
                    "methods_DPEL": st["methods"].get("DPEL", 0),
                    "methods_SCHEMA": st["methods"].get("SCHEMA", 0),
                    "missing_tags_cnt": st["missing_tags_cnt"],
                    "citation_q_cnt": st["citation_q_cnt"],
                    "bad_debug_cnt": st["bad_debug_cnt"],
                    "dups_within_file": st["dups_within_file"],
                    "qlen_min": st["qlen_stats"]["min"],
                    "qlen_max": st["qlen_stats"]["max"],
                    "qlen_avg": f"{st['qlen_stats']['avg']:.2f}",
                    "qlen_median": f"{st['qlen_stats']['median']:.2f}",
                    "alen_min": st["alen_stats"]["min"],
                    "alen_max": st["alen_stats"]["max"],
                    "alen_avg": f"{st['alen_stats']['avg']:.2f}",
                    "alen_median": f"{st['alen_stats']['median']:.2f}",
                }
                w.writerow(row)
        print(f"\n[ok] Wrote CSV summary → {args.out_csv}")

if __name__ == "__main__":
    main()

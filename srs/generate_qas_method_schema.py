#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
generate_qas_method_schema.py
------------------------------
Create QA pairs from *extracted schema* JSONL (output of Step-01 extract_schemas.py)
using the SCHEMA method. Structure is aligned with DPEL; only schema/hook controls
are added here. If spans are FREEFORM-only, behavior matches DPEL.

Key features vs DPEL:
- Accepts semantic_hook, citation_hook, item types, and answer_spans from schema.
- Enforces presence of distinct passage tags [#SRC:...] and [#TGT:...] in ANSWERS.
- Skips degenerate pairs (identical IDs or identical texts).
- Optionally forbid citations in Q/A text (while keeping tags).
- DPEL-style answer length (170–230 words; hard minimum 160).

CLI example:
python3 srs/generate_qas_method_schema.py \
  --input_jsonl outputs/extracted_schema.jsonl \
  --output_jsonl outputs/generation/schema/sample/answers.jsonl \
  --report_json outputs/generation/schema/sample/report.json \
  --model gpt-4o \
  --max_q_per_pair 2 \
  --sample_n 3 \
  --temperature 0.2 \
  --seed 13 \
  --row_sample_n 20 \
  --row_sample_seed 13 \
  --max_pairs 20 \
  --dedup \
  --drop_title_targets \
  --dual_anchors_mode always \
  --no_citations \
  --verbose
"""


import argparse
import json
import os
import re
import sys
import uuid
import time
from typing import Any, Dict, List, Optional

# -----------------------------
# Constants
# -----------------------------
STRUCTURED_SPAN_TYPES = {"DURATION", "DATE", "MONEY", "PERCENT", "TERM", "SECTION"}
ITEM_TYPES = {"Obligation", "Prohibition", "Permission", "Definition", "Scope", "Procedure", "Other"}

ITEM_STYLE_HINTS = {
    "Obligation":  "Prefer 'must/shall' formulations; focus on required actions or deadlines.",
    "Prohibition": "Prefer 'must not/shall not/is prohibited'; clarify forbidden cases or exceptions.",
    "Permission":  "Prefer 'may/can/is permitted' with qualifying conditions.",
    "Definition":  "Define precisely; anchor in term criteria or triggers; avoid copying long text.",
    "Scope":       "Ask who/what/when applies or is excluded; emphasize applicability boundaries.",
    "Procedure":   "Ask about steps, approvals, calculations, or sequencing; keep them minimal.",
    # 'Other' intentionally omitted → leave phrasing free
}

STOPWORDS = set(("""
a an the and or of to in for on by with from as is are be this that these those its under subject
rule section chapter part article must shall may can if when provided unless including
""".split()))

# -----------------------------
# Utilities
# -----------------------------
def rand_uuid() -> str:
    return str(uuid.uuid4())

def norm_ws(s: Optional[str]) -> str:
    return re.sub(r"\s+", " ", (s or "")).strip()

def looks_like_empty(s: Optional[str]) -> bool:
    return len(norm_ws(s)) == 0

def normalize_question_for_dedup(q: str) -> str:
    q = q.lower().strip()
    q = re.sub(r"[^a-z0-9\s?]", " ", q)
    q = re.sub(r"\s+", " ", q)
    return q

def tokenize_alpha(s: str) -> List[str]:
    return re.findall(r"[A-Za-z][A-Za-z\-]{2,}", s or "")

def source_only_hints(source_text: str, target_text: str, k: int = 6) -> List[str]:
    """Return up to k tokens present in SOURCE but not in TARGET (light, order-preserving)."""
    s_toks = [w.lower() for w in tokenize_alpha(source_text) if w.lower() not in STOPWORDS]
    t_set  = {w.lower() for w in tokenize_alpha(target_text) if w.lower() not in STOPWORDS}
    out, seen = [], set()
    for w in s_toks:
        if w not in t_set and w not in seen:
            seen.add(w); out.append(w)
        if len(out) >= k:
            break
    return out

def has_required_tags(answer: str, source_id: str, target_id: str) -> bool:
    """Answer must contain both distinct passage tags, exactly as written."""
    if not answer:
        return False
    if source_id == target_id:
        return False
    return f"[#SRC:{source_id}]" in answer and f"[#TGT:{target_id}]" in answer


# -----------------------------
# OpenAI call
# -----------------------------
def call_llm(model: str, system_prompt: str, user_prompt: str,
             temperature: float = 0.3, max_tokens: int = 2000,
             seed: Optional[int] = None) -> str:
    try:
        from openai import OpenAI
        client = OpenAI()
        extra = {}
        if seed is not None:
            extra["seed"] = seed
        resp = client.chat.completions.create(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **extra,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        return (resp.choices[0].message.content or "").strip()
    except Exception as e:
        sys.stderr.write(f"[LLM ERROR] {e}\n")
        return ""

def parse_llm_json(s: str) -> Dict[str, Any]:
    try:
        s = s.strip()
        s = re.sub(r"^```json\s*|\s*```$", "", s)
        return json.loads(s)
    except Exception:
        return {}

# -----------------------------
# Prompting
# -----------------------------
PROFESSIONAL_STYLE = (
    "Write the question like a regulator or compliance counsel. Prefer precise terms "
    "(Issuer, Applicant, RIE, Authorised Person) and crisp modality (must/shall/may). "
    "Questions may be multi-clause or two sentences to encode scope, preconditions, exceptions, or timing. "
    "Tone: formal and unambiguous."
)

BASIC_STYLE = (
    "Write the question for a smart non-expert compliance analyst. Use plain words, short "
    "sentences, and clear structure. Questions can be longer when needed to state conditions "
    "(if/when/unless), but prefer one or two short sentences. Keep actor names exactly as written."
)

SYSTEM_PROMPT_GEN = (
    "You generate regulatory Q&As and must follow the user instructions exactly. "
    "Use ONLY the provided SOURCE and TARGET texts (no outside knowledge). "
    "Every substantive claim must be grounded in at least one of the two passages. "
    "Return VALID JSON only—no markdown, no commentary."
)

# -----------------------------
# Prompt builder (DPEL-aligned + schema extras)
# -----------------------------
def build_prompt(
    *,
    source_text: str,
    target_text: str,
    semantic_hook: str,
    citation_hook: str,
    source_item_type: str,
    target_item_type: str,
    answer_spans: List[Dict[str, Any]],
    max_per_persona: int,
    sample_n: int,
    dual_anchors_mode: str,   # "off" | "freeform_only" | "always"
    no_citations: bool,
    source_id: str,
    target_id: str
) -> str:

    has_structured = any((sp.get("type") in STRUCTURED_SPAN_TYPES) for sp in (answer_spans or []))
    has_any_spans = len(answer_spans or []) > 0
    has_only_freeform = (has_any_spans and not has_structured)

    rules: List[str] = []
    rules.append("Every QUESTION and ANSWER must require BOTH the SOURCE and the TARGET.")
    rules.append("Center the QUESTION on the semantic_hook’s substance; paraphrase; do NOT quote.")
    rules.append("Actor fidelity: Use the exact actor names from the passages.")
    rules.append("Do NOT include verbatim quotations or rule/section numbers in the QUESTION.")
    # DPEL-style answer length & tags
    rules.append("ANSWER STYLE (ALWAYS PROFESSIONAL regardless of persona):")
    rules.append("  • Length: one compact professional paragraph of 180–230 words (hard minimum 160).")
    rules.append("  • If you produce fewer than 160 words, expand with clarifying detail from the passages.")
    rules.append("  • OPTIONAL bullets allowed only if needed; still keep 170–230 total words.")
    rules.append(f"  • The answer MUST contain both tags exactly as written: [#SRC:{source_id}] and [#TGT:{target_id}]")
    rules.append("  • Place the tags naturally (e.g., '… as required [#TGT:…] and permitted [#SRC:…]').")

    # Item-type phrasing hints (Target-first, Source as context if available)
    tgt_type = (target_item_type or "Other")
    src_type = (source_item_type or "Other")
    if tgt_type in ITEM_STYLE_HINTS:
        t_hint = ITEM_STYLE_HINTS[tgt_type]
        s_hint = ITEM_STYLE_HINTS.get(src_type)
        if s_hint:
            rules.append(f"For QUESTION form, prioritize TARGET type '{tgt_type}': {t_hint} (SOURCE '{src_type}' context: {s_hint}).")
        else:
            rules.append(f"For QUESTION form, prioritize TARGET type '{tgt_type}': {t_hint}.")

    # Span-driven answer constraints
    if has_structured:
        rules.append("Structured spans present (DURATION/DATE/MONEY/PERCENT/TERM/SECTION): the ANSWER MUST explicitly include those concrete details (exact value/term/section label).")
    elif has_only_freeform:
        rules.append("Spans are FREEFORM only; provide a correct, minimal answer without copying long text.")
    else:
        rules.append("No spans provided; provide a correct, minimal answer without forced slot copying.")

    # Dual anchors enforcement
    if dual_anchors_mode == "always" or (dual_anchors_mode == "freeform_only" and has_only_freeform):
        rules.append("Dual anchors: Each QUESTION must hinge on ONE concrete element from SOURCE and ONE from TARGET; removing either passage should make the QA unanswerable.")

    # No-citations (Q/A text), tags are allowed/required
    if no_citations:
        rules.append("Do NOT include rule/section identifiers in the QUESTION or ANSWER text. Note: the bracketed tags [#SRC:…]/[#TGT:…] are required and not considered citations.")

    # Light lexical hints from SOURCE (to bias SOURCE anchoring)
    hints = source_only_hints(source_text, target_text, k=6)
    if hints:
        rules.append("Light lexical hints from SOURCE (optional; do not force-use all): " + ", ".join(hints))

    rules_block = "- " + "\n- ".join(rules)
    spans_block = json.dumps(answer_spans or [], ensure_ascii=False)

    return f"""
You are generating Q&As for a cross-referenced regulatory pair.

Follow ALL rules:
{rules_block}

Persona styles (QUESTION only):
- professional: {PROFESSIONAL_STYLE}
- basic: {BASIC_STYLE}

Quantity:
- Brainstorm up to {sample_n} internally, but OUTPUT no more than {max_per_persona} per persona.

ANCHORS:
- semantic_hook: "{semantic_hook}"
- citation_hook (concept only; do not quote in Q/A): "{citation_hook}"
- SOURCE item type: "{source_item_type}"
- TARGET item type: "{target_item_type}"
- answer_spans (with types): {spans_block}
- PASSAGE IDS (use in ANSWER exactly as shown): [#SRC:{source_id}] and [#TGT:{target_id}]

SOURCE (full text):
\"\"\"{source_text}\"\"\"

TARGET (full text):
\"\"\"{target_text}\"\"\"

OUTPUT — strict JSON and nothing else:
{{
  "professional": [
    {{"question": "...", "answer": "..." }}
  ],
  "basic": [
    {{"question": "...", "answer": "..." }}
  ]
}}
""".strip()





# -----------------------------
# IO helpers (JSONL)
# -----------------------------
def read_jsonl(path: str) -> List[Dict[str, Any]]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except Exception:
                continue
    return items

# -----------------------------
# Main
# -----------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Generate QAs from merged schema items (Step-01 output) with SCHEMA method (DPEL-aligned)."
    )
    ap.add_argument("--input_jsonl", required=True, help="Path to Step-01 output JSONL (merged items).")
    ap.add_argument("--output_jsonl", required=True, help="Output JSONL path for generated QAs.")
    ap.add_argument("--report_json", required=True, help="Summary report JSON path.")
    ap.add_argument("--model", required=True)
    ap.add_argument("--max_q_per_pair", type=int, default=2, help="Per persona, per pair (upper bound).")
    ap.add_argument("--sample_n", type=int, default=3, help="Brainstorm hint (per persona).")
    ap.add_argument("--temperature", type=float, default=0.3)
    ap.add_argument("--seed", type=int, default=None)
    ap.add_argument("--dedup", action="store_true", help="Global dedup by normalized question text.")
    ap.add_argument("--drop_title_targets", action="store_true",
                    help="If set, skip items where target_is_title==True (already set in Step-01).")
    ap.add_argument("--row_sample_n", type=int, default=None, help="Optional: sample N items.")
    ap.add_argument("--row_sample_seed", type=int, default=13)
    ap.add_argument("--max_pairs", type=int, default=None, help="Hard cap on items processed.")
    ap.add_argument("--dual_anchors_mode", choices=["off", "freeform_only", "always"], default="freeform_only",
                    help="Enforce dual anchors (SOURCE+TARGET).")
    ap.add_argument("--no_citations", action="store_true",
                    help="Forbid rule/section numbers in Q/A text (tags still required).")
    ap.add_argument("--verbose", action="store_true")
    ap.add_argument("--dry_run", action="store_true", help="Scan/filter only; no model calls or writes.")

    args = ap.parse_args()

    # Load items
    items = read_jsonl(args.input_jsonl)
    print(f"[info] loaded merged items: {len(items)} from {args.input_jsonl}", flush=True)
    if not items:
        report = {
            "rows_loaded": 0,
            "kept_candidates": 0,
            "pairs_processed": 0,
            "qas_created": 0,
            "dropped_dupe_qs": 0,
            "skipped_empty_text": 0,
            "skipped_model_fail": 0,
            "skipped_title_targets": 0,
            "model": args.model,
            "note": "No items loaded—check input path/JSONL lines."
        }
        print(json.dumps(report, indent=2), flush=True)
        return

    # Optional sampling / capping
    if args.row_sample_n is not None and args.row_sample_n > 0 and len(items) > args.row_sample_n:
        import random as _rnd
        rng = _rnd.Random(args.row_sample_seed)
        items = rng.sample(items, args.row_sample_n)
    if args.max_pairs is not None and args.max_pairs > 0 and len(items) > args.max_pairs:
        items = items[:args.max_pairs]

    rows_loaded = len(items)
    kept_candidates = 0
    pairs_processed = 0
    qas_created = 0
    dropped_dupe_qs = 0
    skipped_empty_text = 0
    skipped_title_targets = 0
    skipped_model_fail = 0
    skipped_degenerate = 0

    dedup_set = set() if args.dedup else None

    os.makedirs(os.path.dirname(args.output_jsonl), exist_ok=True)
    os.makedirs(os.path.dirname(args.report_json), exist_ok=True)

    # Dry run (no LLM)
    if args.dry_run:
        for it in items:
            source_text = norm_ws(it.get("source_text"))
            target_text = norm_ws(it.get("target_text"))
            if looks_like_empty(source_text) or looks_like_empty(target_text):
                skipped_empty_text += 1
                continue
            if args.drop_title_targets and bool(it.get("target_is_title")):
                skipped_title_targets += 1
                continue
            # Degeneracy check (IDs or texts identical)
            src_id = str(it.get("source_passage_id") or "")
            tgt_id = str(it.get("target_passage_id") or "")
            if (src_id == tgt_id) or (norm_ws(source_text) == norm_ws(target_text)):
                skipped_degenerate += 1
                continue
            kept_candidates += 1
        report = {
            "rows_loaded": rows_loaded,
            "kept_candidates": kept_candidates,
            "pairs_processed": kept_candidates,
            "qas_created": 0,
            "dropped_dupe_qs": 0,
            "skipped_empty_text": skipped_empty_text,
            "skipped_model_fail": 0,
            "skipped_title_targets": skipped_title_targets,
            "skipped_degenerate": skipped_degenerate,
            "model": args.model,
        }
        print(json.dumps(report, indent=2))
        return

    # Real generation
    with open(args.output_jsonl, "w", encoding="utf-8") as outf:
        for idx, it in enumerate(items, start=1):
            source_text = norm_ws(it.get("source_text"))
            target_text = norm_ws(it.get("target_text"))
            if looks_like_empty(source_text) or looks_like_empty(target_text):
                skipped_empty_text += 1
                continue
            if args.drop_title_targets and bool(it.get("target_is_title")):
                skipped_title_targets += 1
                continue

            # Anchors / metadata
            semantic_hook    = norm_ws(it.get("semantic_hook"))
            citation_hook    = norm_ws(it.get("citation_hook"))
            source_item_type = (it.get("source_item_type") or "Other")
            target_item_type = (it.get("target_item_type") or "Other")
            answer_spans     = it.get("answer_spans") or []
            source_id        = str(it.get("source_passage_id") or "")
            target_id        = str(it.get("target_passage_id") or "")

            # Degenerate pair guard (cannot truly require both)
            if (source_id == target_id) or (norm_ws(source_text) == norm_ws(target_text)):
                skipped_degenerate += 1
                continue

            kept_candidates += 1
            pairs_processed += 1

            user_prompt = build_prompt(
                source_text=source_text,
                target_text=target_text,
                semantic_hook=semantic_hook,
                citation_hook=citation_hook,
                source_item_type=str(source_item_type),
                target_item_type=str(target_item_type),
                answer_spans=answer_spans,
                max_per_persona=args.max_q_per_pair,
                sample_n=args.sample_n,
                dual_anchors_mode=args.dual_anchors_mode,
                no_citations=args.no_citations,
                source_id=source_id,
                target_id=target_id
            )

            content = call_llm(
                model=args.model,
                system_prompt=SYSTEM_PROMPT_GEN,
                user_prompt=user_prompt,
                temperature=args.temperature,
                max_tokens=2000,
                seed=args.seed
            )
            if not content:
                skipped_model_fail += 2 * args.max_q_per_pair
                continue

            llm_obj = parse_llm_json(content)
            if not llm_obj:
                skipped_model_fail += 2 * args.max_q_per_pair
                continue

            # Collect per persona
            for persona in ["professional", "basic"]:
                items_p = llm_obj.get(persona, [])
                if not isinstance(items_p, list):
                    continue

                kept = 0
                for qa in items_p:
                    if not isinstance(qa, dict):
                        continue
                    q = norm_ws(qa.get("question"))
                    a = norm_ws(qa.get("answer"))
                    if looks_like_empty(q) or looks_like_empty(a):
                        continue

                    # Ensure passage tags exist and are distinct
                    if not has_required_tags(a, source_id, target_id):
                        continue

                    # Global dedup on questions (optional)
                    if dedup_set is not None:
                        key = normalize_question_for_dedup(q)
                        if key in dedup_set:
                            dropped_dupe_qs += 1
                            continue
                        dedup_set.add(key)

                    out = {
                        "qa_id": rand_uuid(),
                        "persona": persona,
                        "question": q,
                        "expected_answer": a,
                        "debug_context": {
                            "source_passage_id": source_id,
                            "target_passage_id": target_id,
                            "source_text": source_text,
                            "target_text": target_text,
                            "reference_type": it.get("reference_type"),
                            "reference_text": it.get("reference_text"),
                            "semantic_hook": semantic_hook,
                            "citation_hook": citation_hook,
                            "answer_spans": answer_spans,
                            "source_item_type": source_item_type,
                            "target_item_type": target_item_type,
                        },
                        "method": "SCHEMA",
                        "gen_model": args.model,
                        "gen_ts": int(time.time()),
                        "run_seed": args.seed,
                    }
                    outf.write(json.dumps(out, ensure_ascii=False) + "\n")
                    qas_created += 1
                    kept += 1
                    if kept >= args.max_q_per_pair:
                        break

            if args.verbose and (pairs_processed % 50 == 0):
                print(f"[progress] {pairs_processed}/{rows_loaded} | kept_candidates={kept_candidates} | qas={qas_created}", flush=True)

    # Report
    report = {
        "rows_loaded": rows_loaded,
        "kept_candidates": kept_candidates,
        "pairs_processed": pairs_processed,
        "qas_created": qas_created,
        "dropped_dupe_qs": dropped_dupe_qs,
        "skipped_empty_text": skipped_empty_text,
        "skipped_model_fail": skipped_model_fail,
        "skipped_title_targets": skipped_title_targets,
        "skipped_degenerate": skipped_degenerate,
        "model": args.model,
        "dual_anchors_mode": args.dual_anchors_mode,
    }
    with open(args.report_json, "w", encoding="utf-8") as rf:
        json.dump(report, rf, indent=2, ensure_ascii=False)
    print(json.dumps(report, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
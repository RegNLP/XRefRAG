#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
srs/judge_qas_ensemble.py

LLM-as-a-Judge with small cross-model ensemble:
- Run 2 different judge models + 1 extra pass of the first model with a different seed.
- Fuse with median scores (realism, dual_use, correctness) and majority vote for "passed".
- Tie-break requires at least K judges with dual_use >= 3 (default K=2), else fail.

Usage (recommended):
python srs/judge_qas_ensemble.py \
  --inputs outputs/generation/dpel/all/answers.jsonl outputs/generation/schema/all/answers_nociteQ.jsonl \
  --out_jsonl outputs/judging/ensemble/judgments.jsonl \
  --report_json outputs/judging/ensemble/summary.json \
  --ensemble_models gpt-4.1-mini,gpt-4o-mini \
  --repeat_first_with_seed 17 \
  --pass_threshold 7 \
  --require_dual_use_k 2 \
  --forbid_citations_in_question_for_schema \
  --allow_citations_in_answer \
  --temperature 0.0 \
  --seed 13 \
  --verbose
"""

import argparse
import json
import os
import re
import statistics
import sys
from typing import Any, Dict, List, Optional, Tuple

# -----------------------------
# Basic helpers
# -----------------------------
CITATION_PAT = re.compile(r"""(?ix)
  \b(rule|section|chapter|part|appendix|schedule)\b\s*[:\-]?\s*\d+(?:\.\d+)*(?:\([^)]+\))* |
  \bFSMR\b | \b[A-Z]{2,}\s*\d+(?:\.\d+)* | \b\d+(?:\.\d+)+(?:\([^)]+\))*\b
""")

def norm_ws(s: Optional[str]) -> str:
    import re as _re
    return _re.sub(r"\s+", " ", (s or "")).strip()

def has_both_tags(answer: str, src_id: str, tgt_id: str) -> bool:
    return f"[#SRC:{src_id}]" in (answer or "") and f"[#TGT:{tgt_id}]" in (answer or "")

def question_has_citation(q: str) -> bool:
    return bool(CITATION_PAT.search(q or ""))

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except Exception:
                continue
    return out

def write_jsonl(path: str, rows: List[Dict[str, Any]]):
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

# -----------------------------
# OpenAI call
# -----------------------------
def call_judge(model: str, system_prompt: str, user_prompt: str,
               temperature: float = 0.0, seed: Optional[int] = None, max_tokens: int = 700) -> str:
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
        sys.stderr.write(f"[LLM-JUDGE ERROR] {e}\n")
        return ""

def parse_llm_json(s: str) -> Dict[str, Any]:
    s = (s or "").strip()
    s = re.sub(r"^```json\s*|\s*```$", "", s)
    try:
        return json.loads(s)
    except Exception:
        return {}

# -----------------------------
# Judge prompting (rubric)
# -----------------------------
SYSTEM_PROMPT = (
    "You are a rigorous compliance evaluator. "
    "Follow the rubric precisely. "
    "Use ONLY the provided SOURCE and TARGET texts (no outside knowledge). "
    "Return VALID JSON only—no prose or markdown outside JSON."
)

JUDGE_RUBRIC = """
You will judge a single Question/Answer (QA) using ONLY the SOURCE and TARGET.

HARD GATES (if any fails, set passed=false and final_score=0, but still fill subscores):
- The answer MUST include both passage tags exactly: [#SRC:{SRC_ID}] and [#TGT:{TGT_ID}].
- If forbid_citations_in_question=true: The QUESTION must NOT include rule/section identifiers.
- Dual-evidence gate: The QUESTION must require BOTH SOURCE and TARGET to answer correctly.
  If the QA could be fully and correctly answered using only SOURCE or only TARGET, this gate fails.

SCORING RUBRIC (integers only):
1) realism (0–2): Is the QUESTION realistic, natural for compliance, and not awkwardly phrased?
   0 = unrealistic; 1 = somewhat; 2 = clearly realistic.

2) dual_use (0–4): Does answering the QUESTION truly require BOTH passages?
   Evaluate via counterfactuals:
   - Would a competent reviewer answer it correctly with SOURCE alone? with TARGET alone?
   Scoring:
     0 = clearly answerable from ONE passage alone;
     2 = mostly one-sided with minor reference to the other;
     3 = generally needs both but borderline;
     4 = clearly needs both (removing either breaks correctness).

3) correctness (0–4): Is the ANSWER correct and grounded in SOURCE and/or TARGET (no hallucinations/contradictions)?
   0 = incorrect; 2 = partially correct; 4 = fully correct & grounded.

Compute final_score = realism + dual_use + correctness (0–10).
Set passed=true iff:
  - all hard gates pass AND
  - final_score >= {PASS_THRESHOLD} AND
  - dual_use >= 3.
Return strict JSON:
{{
  "passed": true,
  "final_score": 0,
  "subscores": {{"realism": 0, "dual_use": 0, "correctness": 0}},
  "reasons": ["short, bullet-like reasons for each score"],
  "flags": {{"hard_gate_fail": false, "question_has_citation": false}}
}}
"""

def build_user_prompt(
    question: str,
    answer: str,
    source_text: str,
    target_text: str,
    src_id: str,
    tgt_id: str,
    forbid_citations_in_question: bool,
    pass_threshold: int
) -> str:
    rubric = JUDGE_RUBRIC.format(SRC_ID=src_id, TGT_ID=tgt_id, PASS_THRESHOLD=pass_threshold)
    return f"""
RUBRIC:
{rubric}

SETTINGS:
- forbid_citations_in_question={str(bool(forbid_citations_in_question)).lower()}

QUESTION:
\"\"\"{question}\"\"\"

ANSWER:
\"\"\"{answer}\"\"\"

SOURCE:
\"\"\"{source_text}\"\"\"

TARGET:
\"\"\"{target_text}\"\"\"
""".strip()

# -----------------------------
# Single-call judge (one model/seed)
# -----------------------------
def judge_once(
    row: Dict[str, Any],
    model: str,
    temperature: float,
    seed: Optional[int],
    pass_threshold: int,
    forbid_citations_in_question: bool,
    allow_citations_in_answer: bool
) -> Dict[str, Any]:
    q = norm_ws(row.get("question"))
    a = norm_ws(row.get("expected_answer"))
    dbg = row.get("debug_context") or {}
    src_id = str(dbg.get("source_passage_id") or "")
    tgt_id = str(dbg.get("target_passage_id") or "")
    source_text = norm_ws(dbg.get("source_text"))
    target_text = norm_ws(dbg.get("target_text"))

    # Local hard-gate pre-checks
    hard_gate_fail = False
    gate_reasons = []
    if not has_both_tags(a, src_id, tgt_id):
        hard_gate_fail = True
        gate_reasons.append("missing_required_tags")
    if forbid_citations_in_question and question_has_citation(q):
        hard_gate_fail = True
        gate_reasons.append("forbidden_citation_in_question")
    if not allow_citations_in_answer and CITATION_PAT.search(a or ""):
        hard_gate_fail = True
        gate_reasons.append("forbidden_citation_in_answer")

    # Short-circuit to save tokens
    if hard_gate_fail:
        return {
            "passed": False,
            "final_score": 0,
            "subscores": {"realism": 0, "dual_use": 0, "correctness": 0},
            "reasons": ["local_hard_gate_fail"] + gate_reasons,
            "flags": {"hard_gate_fail": True, "question_has_citation": question_has_citation(q)},
        }

    user_prompt = build_user_prompt(
        question=q, answer=a,
        source_text=source_text, target_text=target_text,
        src_id=src_id, tgt_id=tgt_id,
        forbid_citations_in_question=forbid_citations_in_question,
        pass_threshold=pass_threshold
    )
    content = call_judge(
        model=model,
        system_prompt=SYSTEM_PROMPT,
        user_prompt=user_prompt,
        temperature=temperature,
        seed=seed,
        max_tokens=700
    )
    obj = parse_llm_json(content)
    if not isinstance(obj, dict) or "final_score" not in obj:
        obj = {
            "passed": False,
            "final_score": 0,
            "subscores": {"realism": 0, "dual_use": 0, "correctness": 0},
            "reasons": ["judge_failed_or_invalid_json"],
            "flags": {"hard_gate_fail": False, "question_has_citation": question_has_citation(q)},
        }

    return obj

# -----------------------------
# Ensemble fusion
# -----------------------------
def median_int(vals: List[int]) -> int:
    if not vals:
        return 0
    return int(round(statistics.median(vals)))

def fuse_ensemble(
    per_judge: List[Dict[str, Any]],
    require_dual_use_k: int
) -> Dict[str, Any]:
    passes = [bool(j.get("passed")) for j in per_judge]
    finals = [int(j.get("final_score", 0)) for j in per_judge]
    realism = [int((j.get("subscores") or {}).get("realism", 0)) for j in per_judge]
    dualuse = [int((j.get("subscores") or {}).get("dual_use", 0)) for j in per_judge]
    correct = [int((j.get("subscores") or {}).get("correctness", 0)) for j in per_judge]

    fused = {
        "passed": False,
        "final_score": median_int(finals),
        "subscores": {
            "realism": median_int(realism),
            "dual_use": median_int(dualuse),
            "correctness": median_int(correct),
        },
        "reasons": ["fused_median_scores_over_ensemble"],
        "ensemble": {"n": len(per_judge)}
    }

    yes = sum(1 for p in passes if p)
    no = len(passes) - yes

    if yes > no:
        fused["passed"] = True
    elif no > yes:
        fused["passed"] = False
    else:
        # Tie: require at least K judges with dual_use ≥ 3
        k = sum(1 for d in dualuse if d >= 3)
        if k >= require_dual_use_k:
            passed_scores = [finals[i] for i, p in enumerate(passes) if p]
            failed_scores = [finals[i] for i, p in enumerate(passes) if not p]
            med_pass = statistics.median(passed_scores) if passed_scores else 0
            med_fail = statistics.median(failed_scores) if failed_scores else 0
            fused["passed"] = med_pass >= med_fail
            fused["reasons"].append(f"tie_break_dual_use_k={k}>={require_dual_use_k}")
        else:
            fused["passed"] = False
            fused["reasons"].append(f"tie_break_failed_dual_use_k={k}<{require_dual_use_k}")

    return fused

# -----------------------------
# CLI
# -----------------------------
def main():
    ap = argparse.ArgumentParser(description="LLM-as-a-Judge with cross-model small ensemble (Option 1).")
    ap.add_argument("--inputs", nargs="+", required=True, help="One or more QA JSONL files to judge.")
    ap.add_argument("--out_jsonl", required=True, help="Output JSONL with per-QA per-judge and fused results.")
    ap.add_argument("--report_json", required=True, help="Summary JSON with aggregates.")

    # Ensemble controls
    ap.add_argument("--ensemble_models", required=True,
                    help="Comma-separated judge models, e.g., 'gpt-4.1-mini,gpt-4o-mini'.")
    ap.add_argument("--repeat_first_with_seed", type=int, default=None,
                    help="Optional: add a third pass using the FIRST model with this different seed.")
    ap.add_argument("--temperature", type=float, default=0.0)
    ap.add_argument("--seed", type=int, default=None, help="Base seed for calls (for models without the 'repeat' pass).")

    # Rubric & gates
    ap.add_argument("--pass_threshold", type=int, default=7, help="Minimum final_score to pass (0-10).")
    ap.add_argument("--require_dual_use_k", type=int, default=2,
                    help="Tie-break: need at least K judges with dual_use >= 3 to consider pass in ties.")
    ap.add_argument("--forbid_citations_in_question_for_schema", action="store_true",
                    help="If set, questions from SCHEMA method must not include citations.")

    # >>> Changed to a negative flag so default == allow
    ap.add_argument("--no_citations_in_answer", action="store_true",
                    help="If set, answers must not contain citation-like tokens (default: citations allowed in answers).")

    ap.add_argument("--max_items", type=int, default=None, help="Optional cap on total items judged.")
    ap.add_argument("--verbose", action="store_true")

    args = ap.parse_args()

    allow_citations_in_answer = not bool(args.no_citations_in_answer)
    models = [m.strip() for m in args.ensemble_models.split(",") if m.strip()]
    if not models:
        print("[err] --ensemble_models cannot be empty", file=sys.stderr); sys.exit(1)

    # Build the (model, seed) passes: M1(seed=args.seed), M2(seed=args.seed), plus optional M1(seed=repeat)
    passes: List[Tuple[str, Optional[int], str]] = []
    for m in models:
        passes.append((m, args.seed, f"{m}@seed:{args.seed if args.seed is not None else 'none'}"))
    if args.repeat_first_with_seed is not None and models:
        m0 = models[0]
        passes.append((m0, args.repeat_first_with_seed, f"{m0}@seed:{args.repeat_first_with_seed}"))

    # Load inputs
    all_rows: List[Dict[str, Any]] = []
    for p in args.inputs:
        rows = load_jsonl(p)
        all_rows.extend(rows)
        if args.verbose:
            print(f"[info] loaded {len(rows)} from {p}", flush=True)

    if args.max_items is not None and args.max_items > 0 and len(all_rows) > args.max_items:
        all_rows = all_rows[:args.max_items]
        if args.verbose:
            print(f"[info] truncated to max_items={args.max_items}", flush=True)

    out_rows: List[Dict[str, Any]] = []
    stats = {
        "total": 0,
        "fused_passed": 0,
        "avg_fused_score": 0.0,
        "avg_fused_realism": 0.0,
        "avg_fused_dual_use": 0.0,
        "avg_fused_correctness": 0.0,
        "by_method": {},
        "by_persona": {},
    }
    fused_scores, fused_realism, fused_dual, fused_correct = [], [], [], []

    for i, row in enumerate(all_rows, 1):
        method = row.get("method")
        persona = row.get("persona")
        dbg = row.get("debug_context") or {}
        src_id = str(dbg.get("source_passage_id") or "")
        tgt_id = str(dbg.get("target_passage_id") or "")

        # Gate: forbid citations in question for SCHEMA only (policy-aligned)
        forbid_citations_in_question = bool(args.forbid_citations_in_question_for_schema and method == "SCHEMA")

        per_judge = []
        for (m, s, tag) in passes:
            obj = judge_once(
                row=row,
                model=m,
                temperature=args.temperature,
                seed=s,
                pass_threshold=args.pass_threshold,
                forbid_citations_in_question=forbid_citations_in_question,
                allow_citations_in_answer=allow_citations_in_answer
            )
            per_judge.append({"model": m, "seed": s, "tag": tag, "result": obj})

        fused = fuse_ensemble(
            per_judge=[x["result"] for x in per_judge],
            require_dual_use_k=args.require_dual_use_k
        )

        out_rows.append({
            "qa_id": row.get("qa_id"),
            "method": method,
            "persona": persona,
            "reference_type": (row.get("debug_context") or {}).get("reference_type"),
            "source_passage_id": src_id,
            "target_passage_id": tgt_id,
            "per_judge": per_judge,
            "fused": fused,
        })

        # aggregate
        stats["total"] += 1
        if fused.get("passed"):
            stats["fused_passed"] += 1
        fused_scores.append(int(fused.get("final_score", 0)))
        ss = fused.get("subscores") or {}
        fused_realism.append(int(ss.get("realism", 0)))
        fused_dual.append(int(ss.get("dual_use", 0)))
        fused_correct.append(int(ss.get("correctness", 0)))

        stats["by_method"].setdefault(method, {"count": 0, "pass": 0})
        stats["by_method"][method]["count"] += 1
        stats["by_method"][method]["pass"] += 1 if fused.get("passed") else 0

        stats["by_persona"].setdefault(persona, {"count": 0, "pass": 0})
        stats["by_persona"][persona]["count"] += 1
        stats["by_persona"][persona]["pass"] += 1 if fused.get("passed") else 0

        if args.verbose and i % 200 == 0:
            print(f"[progress] {i}/{len(all_rows)} judged", flush=True)

    # final means
    if stats["total"] > 0:
        stats["avg_fused_score"] = round(statistics.mean(fused_scores), 3)
        stats["avg_fused_realism"] = round(statistics.mean(fused_realism), 3)
        stats["avg_fused_dual_use"] = round(statistics.mean(fused_dual), 3)
        stats["avg_fused_correctness"] = round(statistics.mean(fused_correct), 3)

    # write outputs
    write_jsonl(args.out_jsonl, out_rows)
    os.makedirs(os.path.dirname(os.path.abspath(args.report_json)), exist_ok=True)
    with open(args.report_json, "w", encoding="utf-8") as rf:
        json.dump(stats, rf, indent=2, ensure_ascii=False)

    if args.verbose:
        print(json.dumps(stats, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()

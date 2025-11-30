#!/usr/bin/env python3
# eval_rag.py
# -*- coding: utf-8 -*-

"""
Evaluate RAG outputs for RegRAG-Xref.

Metrics per RAG file (JSONL from run_rag.py):

1) Completeness (lexical, no models):
   - Token F1  (gold expected_answer vs rag_answer)
   - ROUGE-L F1

2) Semantic answer relevance & correctness (optional GPT judge):
   - answer_relevance (0–5)
   - answer_faithfulness (0–5)

3) Faithfulness / groundedness via NLI (optional, local HF model):
   - Premise: expected_answer
   - Hypothesis: each sentence of rag_answer

Per-item metrics are cached per qa_id in out-dir/<basename>_per_qa.jsonl and reused
on subsequent runs if the same judge/NLI models are used.
"""

import argparse
import json
import os
import re
import sys
from typing import List, Dict, Any, Tuple

import numpy as np

# -----------------------------
# Optional imports (NLI)
# -----------------------------
try:
    from transformers import (
        AutoTokenizer,
        AutoModelForSequenceClassification,
        TextClassificationPipeline,
    )
except Exception:
    AutoTokenizer = None
    AutoModelForSequenceClassification = None
    TextClassificationPipeline = None

# -----------------------------
# Optional imports (OpenAI LLM judge)
# -----------------------------
try:
    from openai import OpenAI
except Exception:
    OpenAI = None


# -----------------------------
# Text normalization & overlap
# -----------------------------

def normalize_text(s: str) -> str:
    """Lowercase, remove punctuation/articles/extra spaces (SQuAD-style)."""
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]", " ", s)
    s = re.sub(r"\b(a|an|the)\b", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def get_tokens(s: str) -> List[str]:
    s = normalize_text(s)
    if not s:
        return []
    return s.split()


def f1_score(a: str, b: str) -> float:
    """Token-level F1 between two strings, SQuAD style."""
    a_toks = get_tokens(a)
    b_toks = get_tokens(b)
    if not a_toks and not b_toks:
        return 1.0
    if not a_toks or not b_toks:
        return 0.0

    common = {}
    for t in a_toks:
        common[t] = common.get(t, 0) + 1
    overlap = 0
    for t in b_toks:
        if common.get(t, 0) > 0:
            overlap += 1
            common[t] -= 1

    if overlap == 0:
        return 0.0

    prec = overlap / len(a_toks)
    rec = overlap / len(b_toks)
    return 2 * prec * rec / (prec + rec)


def lcs(a: List[str], b: List[str]) -> int:
    """Longest common subsequence length between two token lists."""
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if a[i] == b[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])
    return dp[m][n]


def rouge_l_f1(a: str, b: str) -> float:
    """ROUGE-L F1 between two strings."""
    a_toks = get_tokens(a)
    b_toks = get_tokens(b)
    if not a_toks or not b_toks:
        return 0.0

    l = lcs(a_toks, b_toks)
    prec = l / len(a_toks)
    rec = l / len(b_toks)
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)


# -----------------------------
# NLI faithfulness
# -----------------------------

def load_nli_pipeline(model_name: str):
    if AutoTokenizer is None or AutoModelForSequenceClassification is None:
        print("[warn] transformers not installed; NLI metrics disabled.", file=sys.stderr)
        return None, None

    try:
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForSequenceClassification.from_pretrained(model_name)
        pipe = TextClassificationPipeline(
            model=model,
            tokenizer=tokenizer,
            truncation=True,
            max_length=512,
            device=-1,
        )
        id2label = model.config.id2label

        entail_idx = None
        contra_idx = None
        for idx, lab in id2label.items():
            lu = lab.upper()
            if "ENTAIL" in lu:
                entail_idx = idx
            if "CONTRAD" in lu:
                contra_idx = idx

        if entail_idx is None or contra_idx is None:
            print("[warn] Could not find ENTAILMENT/CONTRADICTION labels; NLI metrics disabled.", file=sys.stderr)
            return None, None

        return pipe, (entail_idx, contra_idx)
    except Exception as e:
        print(f"[warn] failed to load NLI model '{model_name}': {e}", file=sys.stderr)
        return None, None


def sentence_split(text: str) -> List[str]:
    """Very simple sentence splitter."""
    text = text.strip()
    if not text:
        return []
    parts = re.split(r'(?<=[.!?])\s+', text)
    return [p.strip() for p in parts if p.strip()]


def nli_faithfulness_for_item(
    nli_pipe,
    label_idxs: Tuple[int, int],
    gold_answer: str,
    rag_answer: str,
) -> Tuple[float, float]:
    """
    Premise: gold_answer
    Hypothesis: each sentence of rag_answer

    Returns:
      (mean_entail_prob, mean_contra_prob)
    """
    if not gold_answer.strip() or not rag_answer.strip():
        return 0.0, 0.0
    sentences = sentence_split(rag_answer)
    if not sentences:
        return 0.0, 0.0

    pairs = [{"text": gold_answer, "text_pair": s} for s in sentences]

    try:
        outputs = nli_pipe(pairs, top_k=None)
    except Exception as e:
        print(f"[warn] NLI call failed for one item: {e}", file=sys.stderr)
        return 0.0, 0.0

    entail_probs = []
    contra_probs = []
    for out in outputs:
        scores_by_label = {x["label"]: x["score"] for x in out}
        ent_score = None
        contra_score = None
        for lab, sc in scores_by_label.items():
            lu = lab.upper()
            if "ENTAIL" in lu:
                ent_score = sc
            if "CONTRAD" in lu:
                contra_score = sc
        if ent_score is not None:
            entail_probs.append(ent_score)
        if contra_score is not None:
            contra_probs.append(contra_score)

    if not entail_probs:
        return 0.0, 0.0
    return float(np.mean(entail_probs)), float(np.mean(contra_probs))


# -----------------------------
# LLM judge (OpenAI)
# -----------------------------

def call_llm_judge(model_name: str, question: str, gold_answer: str, rag_answer: str, seed=None) -> Dict[str, Any]:
    """
    Ask a GPT model to rate:
      - answer_relevance (0–5)
      - answer_faithfulness (0–5)
    Returns a dict with those fields or {} on failure.
    """
    if OpenAI is None:
        raise RuntimeError("openai client not installed; install with `pip install openai`.")

    client = OpenAI()
    extra = {}
    if seed is not None:
        extra["seed"] = seed

    system_msg = (
        "You are an evaluation assistant for regulatory Q&A systems.\n"
        "You MUST follow the instructions exactly and return STRICT JSON only.\n"
        "You are NOT allowed to invent new facts beyond what is stated.\n"
    )

    user_msg = f"""
You will evaluate a candidate answer produced by a RAG system.

You are given:
- QUESTION
- GOLD_ANSWER (reference answer)
- RAG_ANSWER (candidate answer to evaluate)

TASK:
1) answer_relevance (0–5):
   - 0 = irrelevant or mostly unrelated to the QUESTION.
   - 1 = touches the topic but fails to address the main point.
   - 2 = partially answers but misses major aspects.
   - 3 = reasonably answers the main point but lacks important details.
   - 4 = good coverage of the QUESTION, only minor omissions.
   - 5 = fully answers the QUESTION, directly and clearly.

2) answer_faithfulness (0–5), comparing RAG_ANSWER to GOLD_ANSWER:
   - 0 = contradicts or seriously misrepresents the GOLD_ANSWER.
   - 1 = mostly incorrect; large parts conflict or are unsupported.
   - 2 = mixed: some correct elements but major inaccuracies or omissions.
   - 3 = largely consistent with GOLD_ANSWER, with minor errors or gaps.
   - 4 = very close to GOLD_ANSWER; only small nuances differ.
   - 5 = essentially equivalent in meaning to GOLD_ANSWER (paraphrase-level).

IMPORTANT:
- Ignore style, length, and minor wording differences.
- Focus on substance, regulatory conditions, obligations, and exceptions.
- If GOLD_ANSWER is unclear or partial, judge faithfulness relative to what is stated.

Return STRICT JSON ONLY, no markdown, no extra keys, in this exact shape:
{{
  "answer_relevance": <integer 0-5>,
  "answer_faithfulness": <integer 0-5>
}}

QUESTION:
\"\"\"{question}\"\"\"

GOLD_ANSWER:
\"\"\"{gold_answer}\"\"\"

RAG_ANSWER:
\"\"\"{rag_answer}\"\"\"
""".strip()

    try:
        resp = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": system_msg},
                {"role": "user", "content": user_msg},
            ],
            max_tokens=128,
            temperature=0.0,
            **extra,
        )
        content = (resp.choices[0].message.content or "").strip()
    except Exception as e:
        print(f"[warn] LLM judge call failed: {e}", file=sys.stderr)
        return {}

    try:
        s = content.strip()
        s = re.sub(r"^```json\s*|\s*```$", "", s)
        obj = json.loads(s)
        ar = int(obj.get("answer_relevance", 0))
        af = int(obj.get("answer_faithfulness", 0))
        ar = max(0, min(5, ar))
        af = max(0, min(5, af))
        return {"answer_relevance": ar, "answer_faithfulness": af}
    except Exception:
        print(f"[warn] could not parse LLM judge JSON: {content[:200]!r}", file=sys.stderr)
        return {}


# -----------------------------
# RAG output loading
# -----------------------------

def load_rag_items(path: str) -> List[Dict[str, Any]]:
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


# -----------------------------
# Cache helpers
# -----------------------------

def load_per_qa_cache(cache_path: str) -> Dict[str, Dict[str, Any]]:
    cache = {}
    if not os.path.isfile(cache_path):
        return cache
    with open(cache_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            qid = obj.get("qa_id")
            if qid:
                cache[qid] = obj
    return cache


def can_reuse_entry(
    entry: Dict[str, Any],
    use_llm_judge: bool,
    judge_model: str,
    use_nli: bool,
    nli_model_name: str,
) -> bool:
    # Always require F1 & ROUGE to be present if we want to reuse anything
    if "f1" not in entry or "rouge_l_f1" not in entry:
        return False

    if use_llm_judge:
        if entry.get("judge_model") != judge_model:
            return False
        if entry.get("gpt_answer_relevance") is None or entry.get("gpt_answer_faithfulness") is None:
            return False

    if use_nli:
        if entry.get("nli_model") != nli_model_name:
            return False
        if entry.get("nli_entailment") is None or entry.get("nli_contradiction") is None:
            return False

    return True


def save_per_qa_cache(cache_path: str, cache: Dict[str, Dict[str, Any]]) -> None:
    with open(cache_path, "w", encoding="utf-8") as f:
        for qid, entry in cache.items():
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")


# -----------------------------
# Evaluation for one file
# -----------------------------

def eval_file(
    path: str,
    use_llm_judge: bool,
    judge_model: str,
    judge_seed: int,
    nli_pipe,
    nli_label_idxs,
    nli_model_name: str,
    cache: Dict[str, Dict[str, Any]],
    cache_path: str,
) -> Dict[str, Any]:
    print("================================================================================")
    print(f"# Evaluating file: {path}")
    raw_items = load_rag_items(path)
    print(f"[info] loaded {len(raw_items)} raw items from {path}")

    # filter ok items
    ok_items = []
    seen_ids = set()
    for obj in raw_items:
        qid = obj.get("qa_id") or obj.get("id")
        if not qid:
            continue
        if qid in seen_ids:
            continue
        seen_ids.add(qid)
        if (
            obj.get("status") == "ok"
            and (obj.get("rag_answer") or "").strip()
            and (obj.get("expected_answer") or "").strip()
        ):
            ok_items.append(obj)

    ok = len(ok_items)
    print(f"[info] ok items (with answers & unique id): {ok}")

    f1s = []
    rouges = []
    llm_rel = []
    llm_faith = []
    nli_ent = []
    nli_contra = []

    reused_count = 0
    fresh_count = 0

    for i, obj in enumerate(ok_items, start=1):
        qid = obj.get("qa_id") or obj.get("id")
        q = (obj.get("question") or "").strip()
        gold = (obj.get("expected_answer") or "").strip()
        rag = (obj.get("rag_answer") or "").strip()

        entry = cache.get(qid)

        # Try to reuse metrics if available for this configuration
        if entry and can_reuse_entry(
            entry,
            use_llm_judge=use_llm_judge,
            judge_model=judge_model,
            use_nli=(nli_pipe is not None and nli_label_idxs is not None),
            nli_model_name=nli_model_name,
        ):
            reused_count += 1
            f1s.append(entry["f1"])
            rouges.append(entry["rouge_l_f1"])
            if use_llm_judge:
                llm_rel.append(entry["gpt_answer_relevance"])
                llm_faith.append(entry["gpt_answer_faithfulness"])
            if nli_pipe is not None and nli_label_idxs is not None:
                nli_ent.append(entry["nli_entailment"])
                nli_contra.append(entry["nli_contradiction"])
        else:
            fresh_count += 1
            # compute from scratch
            f1_val = f1_score(gold, rag)
            rouge_val = rouge_l_f1(gold, rag)
            f1s.append(f1_val)
            rouges.append(rouge_val)

            if entry is None:
                entry = {}
            entry["qa_id"] = qid
            entry["question"] = q
            entry["gold_answer"] = gold
            entry["rag_answer"] = rag
            entry["f1"] = f1_val
            entry["rouge_l_f1"] = rouge_val

            if use_llm_judge:
                j = call_llm_judge(judge_model, q, gold, rag, seed=judge_seed)
                if j:
                    ar = j["answer_relevance"]
                    af = j["answer_faithfulness"]
                    llm_rel.append(ar)
                    llm_faith.append(af)
                    entry["judge_model"] = judge_model
                    entry["gpt_answer_relevance"] = ar
                    entry["gpt_answer_faithfulness"] = af

            if nli_pipe is not None and nli_label_idxs is not None:
                ent, contra = nli_faithfulness_for_item(nli_pipe, nli_label_idxs, gold, rag)
                nli_ent.append(ent)
                nli_contra.append(contra)
                entry["nli_model"] = nli_model_name
                entry["nli_entailment"] = ent
                entry["nli_contradiction"] = contra

            cache[qid] = entry

        if i % 20 == 0 or i == ok:
            f1_avg = float(sum(f1s) / len(f1s)) if f1s else 0.0
            rouge_avg = float(sum(rouges) / len(rouges)) if rouges else 0.0
            print(f"[progress] processed {i}/{ok} items "
                  f"(F1_avg={f1_avg:.4f}, ROUGE-L_F1_avg={rouge_avg:.4f})")

    def avg(lst):
        return float(sum(lst) / len(lst)) if lst else 0.0

    f1_mean = avg(f1s)
    rouge_mean = avg(rouges)
    llm_rel_mean = avg(llm_rel)
    llm_faith_mean = avg(llm_faith)
    nli_ent_mean = avg(nli_ent)
    nli_contra_mean = avg(nli_contra)

    # print summary
    print(f"# file: {path}")
    print(f"[info] total items:               {len(raw_items)}")
    print(f"[info] ok items (with answers):   {ok}")
    print(f"[info] reused items from cache:   {reused_count}")
    print(f"[info] freshly evaluated items:   {fresh_count}")
    print(f"[info] F1 (gold vs rag_answer):   {f1_mean:.4f}")
    print(f"[info] ROUGE-L F1:                {rouge_mean:.4f}")
    if use_llm_judge:
        print(f"[info] GPT answer_relevance (0-5):   {llm_rel_mean:.3f}")
        print(f"[info] GPT answer_faithfulness (0-5): {llm_faith_mean:.3f}")
    else:
        print(f"[info] GPT judge metrics:         n/a (disabled)")
    if nli_pipe is not None and nli_label_idxs is not None:
        print(f"[info] NLI entailment prob:       {nli_ent_mean:.4f}")
        print(f"[info] NLI contradiction prob:    {nli_contra_mean:.4f}")
    else:
        print(f"[info] NLI metrics:               n/a (disabled)")
    print()

    # save per-qa cache for this file
    save_per_qa_cache(cache_path, cache)
    print(f"[info] per-qa metrics cache written to: {cache_path}")

    return {
        "file": path,
        "total_items": len(raw_items),
        "ok_items": ok,
        "f1_mean": f1_mean,
        "rouge_l_f1_mean": rouge_mean,
        "use_llm_judge": use_llm_judge,
        "judge_model": judge_model if use_llm_judge else None,
        "gpt_answer_relevance_mean": llm_rel_mean if use_llm_judge else None,
        "gpt_answer_faithfulness_mean": llm_faith_mean if use_llm_judge else None,
        "use_nli": nli_pipe is not None and nli_label_idxs is not None,
        "nli_model": nli_model_name if (nli_pipe is not None and nli_label_idxs is not None) else None,
        "nli_entailment_mean": nli_ent_mean if nli_pipe is not None and nli_label_idxs is not None else None,
        "nli_contradiction_mean": nli_contra_mean if nli_pipe is not None and nli_label_idxs is not None else None,
        "reused_items": reused_count,
        "fresh_items": fresh_count,
    }


# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Evaluate RAG outputs (F1/ROUGE + optional GPT judge + NLI) for RegRAG-Xref."
    )
    ap.add_argument(
        "--inputs",
        nargs="+",
        required=True,
        help="One or more RAG JSONL files (from run_rag.py).",
    )
    ap.add_argument(
        "--use-llm-judge",
        action="store_true",
        help="Use a GPT model as a semantic judge (answer relevance & faithfulness).",
    )
    ap.add_argument(
        "--judge-model",
        default="gpt-4o-mini",
        help="OpenAI model name for the judge (e.g., gpt-4o-mini, gpt-4.1-mini).",
    )
    ap.add_argument(
        "--judge-seed",
        type=int,
        default=13,
        help="Optional seed for judge calls (if supported).",
    )
    ap.add_argument(
        "--use-nli",
        action="store_true",
        help="Compute NLI-based faithfulness (expected_answer as premise, rag_answer sentences as hypotheses).",
    )
    ap.add_argument(
        "--nli-model",
        default="cross-encoder/nli-deberta-v3-small",
        help="HuggingFace NLI model name.",
    )
    ap.add_argument(
        "--out-dir",
        default="outputs/rag_eval",
        help="Directory to write per-file metrics JSON and per-qa cache.",
    )
    args = ap.parse_args()

    os.makedirs(args.out_dir, exist_ok=True)

    # Load NLI pipeline only once
    nli_pipe = None
    nli_label_idxs = None
    if args.use_nli:
        print(f"[info] loading NLI model: {args.nli_model}", file=sys.stderr)
        nli_pipe, nli_label_idxs = load_nli_pipeline(args.nli_model)

    for path in args.inputs:
        if not os.path.isfile(path):
            print(f"[warn] file not found: {path}", file=sys.stderr)
            continue

        base = os.path.basename(path)
        if base.endswith(".jsonl"):
            base_noext = base[:-6]
        else:
            base_noext = base

        cache_path = os.path.join(args.out_dir, f"{base_noext}_per_qa.jsonl")
        cache = load_per_qa_cache(cache_path)

        metrics = eval_file(
            path=path,
            use_llm_judge=args.use_llm_judge,
            judge_model=args.judge_model,
            judge_seed=args.judge_seed,
            nli_pipe=nli_pipe,
            nli_label_idxs=nli_label_idxs,
            nli_model_name=args.nli_model,
            cache=cache,
            cache_path=cache_path,
        )

        out_name = f"{base_noext}_metrics.json"
        out_path = os.path.join(args.out_dir, out_name)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(metrics, f, indent=2)
        print(f"[info] metrics written to: {out_path}")


if __name__ == "__main__":
    main()

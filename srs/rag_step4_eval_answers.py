#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
rag_step4_eval_answers.py

Evaluate RAG-generated answers against gold answers for DPEL/SCHEMA test sets.

Metrics:
1) Completeness (lexical, no models):
   - token-level F1 (gold vs pred)
   - ROUGE-L F1

2) Semantic answer relevance & correctness (optional GPT judge):
   - answer_relevance (0–5)
   - answer_faithfulness (0–5)

3) Faithfulness / groundedness via NLI (optional HF model):
   - Premise: gold_answer
   - Hypothesis: each sentence of pred_answer
   - Aggregate as fractions of entailment / contradiction sentences.
"""

import argparse
import csv
import json
import math
import os
import re
import statistics
from typing import Dict, List, Tuple, Optional

# Optional: OpenAI client for GPT-based judging
try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

# Optional: transformers for NLI
try:
    from transformers import pipeline
except ImportError:
    pipeline = None


# ---------------------------------------------------------------------------
# Utility: load JSONL
# ---------------------------------------------------------------------------

def load_jsonl(path: str) -> List[dict]:
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


# ---------------------------------------------------------------------------
# Utility: ID extraction and alignment
# ---------------------------------------------------------------------------

def get_item_id(item: dict) -> Optional[str]:
    """
    Try several keys for the QA id:
    - 'id' (DPEL_000123 etc. in gold)
    - 'qa_id' (in predictions)
    - fallback: None
    """
    return item.get("id") or item.get("qa_id")


def align_gold_and_pred(
    gold_path: str,
    pred_path: str,
) -> Tuple[List[dict], List[dict], List[str]]:
    gold_items = load_jsonl(gold_path)
    pred_items = load_jsonl(pred_path)

    gold_by_id: Dict[str, dict] = {}
    for g in gold_items:
        qid = get_item_id(g)
        if qid is not None:
            gold_by_id[qid] = g

    pred_by_id: Dict[str, dict] = {}
    for p in pred_items:
        qid = get_item_id(p)
        if qid is not None:
            pred_by_id[qid] = p

    common_ids = sorted(set(gold_by_id.keys()) & set(pred_by_id.keys()))

    gold_aligned = [gold_by_id[qid] for qid in common_ids]
    pred_aligned = [pred_by_id[qid] for qid in common_ids]
    return gold_aligned, pred_aligned, common_ids


# ---------------------------------------------------------------------------
# Lexical metrics: token F1 and ROUGE-L
# ---------------------------------------------------------------------------

def _normalize_text(text: str) -> List[str]:
    """Simple tokenization + lowercasing."""
    if not text:
        return []
    text = text.lower()
    # keep basic tokens separated by whitespace
    tokens = text.split()
    return tokens


def token_f1(gold: str, pred: str) -> float:
    """
    Word-level F1 between gold and pred.
    """
    gold_tokens = _normalize_text(gold)
    pred_tokens = _normalize_text(pred)

    if not gold_tokens and not pred_tokens:
        return 1.0
    if not gold_tokens or not pred_tokens:
        return 0.0

    # multiset overlap
    from collections import Counter
    gold_counts = Counter(gold_tokens)
    pred_counts = Counter(pred_tokens)
    overlap = sum(min(gold_counts[t], pred_counts[t]) for t in gold_counts.keys())

    precision = overlap / max(len(pred_tokens), 1)
    recall = overlap / max(len(gold_tokens), 1)

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def rouge_l_f1(gold: str, pred: str) -> float:
    """
    Simple ROUGE-L F1 based on longest common subsequence of tokens.
    """
    gold_tokens = _normalize_text(gold)
    pred_tokens = _normalize_text(pred)

    if not gold_tokens and not pred_tokens:
        return 1.0
    if not gold_tokens or not pred_tokens:
        return 0.0

    # LCS dynamic programming
    m = len(gold_tokens)
    n = len(pred_tokens)
    # dp[i][j] = LCS length of gold[:i], pred[:j]
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            if gold_tokens[i] == pred_tokens[j]:
                dp[i + 1][j + 1] = dp[i][j] + 1
            else:
                dp[i + 1][j + 1] = max(dp[i][j + 1], dp[i + 1][j])

    lcs = dp[m][n]
    if lcs == 0:
        return 0.0

    prec = lcs / n
    rec = lcs / m
    if prec + rec == 0:
        return 0.0
    return 2 * prec * rec / (prec + rec)


# ---------------------------------------------------------------------------
# NLI-based faithfulness
# ---------------------------------------------------------------------------

_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+")


def split_into_sentences(text: str) -> List[str]:
    if not text:
        return []
    # very simple rule-based split; good enough here
    parts = _SENT_SPLIT_RE.split(text.strip())
    return [s.strip() for s in parts if s.strip()]


def init_nli_pipeline(model_name: str):
    if pipeline is None:
        raise RuntimeError("transformers is not installed but NLI model was requested.")
    nli_pipe = pipeline(
        "text-classification",
        model=model_name,
        return_all_scores=True,
    )
    return nli_pipe


def decode_nli_label(scores_obj) -> Optional[str]:
    """
    Robustly decode the label from various possible pipeline outputs.

    scores_obj is typically:
    - list[dict(label, score)]  (single input)
    - dict(label, score)        (rare)
    """
    # single dict case
    if isinstance(scores_obj, dict) and "label" in scores_obj:
        return str(scores_obj["label"])

    # list-of-dicts case
    if isinstance(scores_obj, list) and scores_obj and isinstance(scores_obj[0], dict):
        # pick max score
        best = max(scores_obj, key=lambda d: d.get("score", 0.0))
        return str(best.get("label"))

    return None


def compute_nli_fractions(
    nli_pipe,
    premise: str,
    hypothesis_text: str,
) -> Tuple[Optional[float], Optional[float]]:
    """
    premise: gold answer
    hypothesis_text: predicted answer (will be split into sentences)

    Returns:
        (entail_frac, contra_frac) over sentences.
    """
    sents = split_into_sentences(hypothesis_text)
    if not sents:
        return None, None

    inputs = [{"text": premise, "text_pair": s} for s in sents]

    try:
        outputs = nli_pipe(inputs, top_k=None, truncation=True)
    except Exception as e:
        print(f"[WARN] NLI pipeline call failed: {e}")
        return None, None

    # outputs is usually List[List[dict]], but may be List[dict] for some configs
    entail_count = 0
    contra_count = 0
    total = 0

    for out in outputs:
        # unify to list-of-dicts
        if isinstance(out, dict) and "label" in out:
            scores_list = [out]
        else:
            scores_list = out

        label = decode_nli_label(scores_list)
        if label is None:
            continue

        label_l = label.lower()
        total += 1
        if "entail" in label_l:
            entail_count += 1
        elif "contradict" in label_l:
            contra_count += 1

    if total == 0:
        return None, None

    return entail_count / total, contra_count / total


# ---------------------------------------------------------------------------
# GPT-judge semantic evaluation
# ---------------------------------------------------------------------------

def _extract_json_block(text: str) -> Optional[dict]:
    """
    Try to extract a JSON object from a free-form LLM response.
    Returns a dict or None.
    """
    if not text:
        return None
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        pass

    m = re.search(r"\{.*\}", text, flags=re.DOTALL)
    if not m:
        return None
    try:
        return json.loads(m.group(0))
    except Exception:
        return None


def build_gpt_judge_prompt(question: str, gold_answer: str, cand_answer: str) -> str:
    """
    Build a prompt asking the LLM to score:
      - answer_relevance (0–5)
      - answer_faithfulness (0–5)
    based on QUESTION and GOLD_ANSWER vs CANDIDATE_ANSWER.
    """
    return f"""
You are an expert evaluator of regulatory question answering quality.

You will receive:
- a QUESTION,
- a GOLD_ANSWER (reference answer written by experts),
- a CANDIDATE_ANSWER generated by a system.

You must assign two integer scores from 0 to 5:

1. answer_relevance (0-5):
   - 0 = completely off-topic
   - 1 = barely related to the question
   - 2 = partially related, but misses many key aspects
   - 3 = mostly on-topic but missing some important details
   - 4 = on-topic and covers most key aspects
   - 5 = fully on-topic and directly addresses the question

2. answer_faithfulness (0-5):
   - Compare ONLY with the GOLD_ANSWER; ignore any other external knowledge.
   - 0 = mostly incorrect or contradicts the gold answer
   - 1 = heavily distorted; many claims conflict with the gold answer
   - 2 = partially aligned, but with important inaccuracies or contradictions
   - 3 = generally aligned but with some minor inaccuracies or omissions
   - 4 = almost fully aligned with only small deviations
   - 5 = very close paraphrase of the gold answer with no substantive errors

Important:
- Focus on substantive content, not style.
- Penalise hallucinated obligations or conditions not present in the GOLD_ANSWER.
- Do not reward verbosity on its own.

Return ONLY a JSON object with two integer fields:
{{
  "answer_relevance": <integer 0-5>,
  "answer_faithfulness": <integer 0-5>
}}

QUESTION:
{question}

GOLD_ANSWER:
{gold_answer}

CANDIDATE_ANSWER:
{cand_answer}
""".strip()


def gpt_judge_one(
    client,
    model: str,
    question: str,
    gold_answer: str,
    cand_answer: str,
) -> Tuple[Optional[int], Optional[int]]:
    """
    Call the LLM once to get (answer_relevance, answer_faithfulness) in [0,5].
    Returns (None, None) on failure.
    """
    if not gold_answer or not cand_answer:
        return None, None

    prompt = build_gpt_judge_prompt(question, gold_answer, cand_answer)
    try:
        resp = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a strict, careful evaluation assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.0,
        )
        content = resp.choices[0].message.content
    except Exception as e:
        print(f"[WARN] GPT judge call failed: {e}")
        return None, None

    data = _extract_json_block(content)
    if not isinstance(data, dict):
        return None, None

    rel = data.get("answer_relevance")
    faith = data.get("answer_faithfulness")

    def _coerce(v):
        try:
            iv = int(v)
            if 0 <= iv <= 5:
                return iv
        except Exception:
            return None
        return None

    rel = _coerce(rel)
    faith = _coerce(faith)

    return rel, faith


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--gold-json",
        required=True,
        help="Path to gold test JSONL file (with 'id' and 'answer').",
    )
    parser.add_argument(
        "--pred-json",
        required=True,
        help="Path to predictions JSONL file (with 'qa_id' and predicted answer).",
    )
    parser.add_argument(
        "--out-json",
        required=True,
        help="Path to aggregate metrics JSON output.",
    )
    parser.add_argument(
        "--out-csv",
        required=False,
        default=None,
        help="Path to per-item metrics CSV output.",
    )

    # NLI options
    parser.add_argument(
        "--nli-model-name",
        type=str,
        default=None,
        help="If set, use this HF NLI model for sentence-level faithfulness "
             "(e.g., 'MoritzLaurer/DeBERTa-v3-base-mnli-fever-anli').",
    )

    # GPT-judge options
    parser.add_argument(
        "--use-gpt-judge",
        action="store_true",
        help="If set, call an LLM to rate answer_relevance and answer_faithfulness (0–5).",
    )
    parser.add_argument(
        "--gpt-model",
        type=str,
        default="gpt-4o-mini",
        help="OpenAI model name for GPT-based judging (e.g., gpt-4o-mini, gpt-4o).",
    )
    parser.add_argument(
        "--max-gpt-judge",
        type=int,
        default=0,
        help="Maximum number of items to send to GPT judge (0 = no limit when --use-gpt-judge is set).",
    )

    args = parser.parse_args()

    print(f"[INFO] Loading gold from: {args.gold_json}")
    print(f"[INFO] Loading predictions from: {args.pred_json}")

    gold_aligned, pred_aligned, common_ids = align_gold_and_pred(args.gold_json, args.pred_json)
    num_pairs = len(common_ids)
    print(f"[INFO] Aligned QA pairs: {num_pairs}")

    # Initialise NLI if requested
    nli_pipe = None
    if args.nli_model_name:
        print(f"[INFO] Initializing NLI pipeline: {args.nli_model_name}")
        nli_pipe = init_nli_pipeline(args.nli_model_name)

    # Initialise GPT judge if requested
    gpt_client = None
    max_gpt = None
    if args.use_gpt_judge:
        if OpenAI is None:
            raise RuntimeError("openai package is not installed but --use-gpt-judge was set.")
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        gpt_client = OpenAI()
        max_gpt = args.max_gpt_judge if args.max_gpt_judge and args.max_gpt_judge > 0 else None

    # Main evaluation loop
    per_item: List[dict] = []

    for idx, qid in enumerate(common_ids):
        g = gold_aligned[idx]
        p = pred_aligned[idx]

        question = g.get("question", "")
        gold_answer = (g.get("answer") or "").strip()
        pred_answer = (p.get("answer") or p.get("rag_answer") or "").strip()

        # 1) Lexical metrics
        tf1 = token_f1(gold_answer, pred_answer)
        rlf1 = rouge_l_f1(gold_answer, pred_answer)

        # 2) NLI-based faithfulness (optional)
        nli_entail_frac = None
        nli_contra_frac = None
        if nli_pipe is not None and gold_answer and pred_answer:
            ef, cf = compute_nli_fractions(nli_pipe, gold_answer, pred_answer)
            nli_entail_frac = ef
            nli_contra_frac = cf

        # 3) GPT-based semantic evaluation (optional)
        answer_relevance = None
        answer_faithfulness = None
        if gpt_client is not None and (max_gpt is None or idx < max_gpt):
            rel, faith = gpt_judge_one(
                gpt_client,
                args.gpt_model,
                question,
                gold_answer,
                pred_answer,
            )
            answer_relevance = rel
            answer_faithfulness = faith

        item_metrics = {
            "id": qid,
            "question": question,
            "gold_answer": gold_answer,
            "pred_answer": pred_answer,
            "token_f1": tf1,
            "rouge_l_f1": rlf1,
            "nli_entail_frac": nli_entail_frac,
            "nli_contra_frac": nli_contra_frac,
            "answer_relevance": answer_relevance,
            "answer_faithfulness": answer_faithfulness,
        }
        per_item.append(item_metrics)

    # Aggregate metrics
    def mean_or_none(values: List[Optional[float]]) -> Optional[float]:
        vals = [v for v in values if v is not None]
        if not vals:
            return None
        return float(statistics.mean(vals))

    token_f1_mean = mean_or_none([m["token_f1"] for m in per_item])
    rouge_l_f1_mean = mean_or_none([m["rouge_l_f1"] for m in per_item])
    nli_entail_frac_mean = mean_or_none([m["nli_entail_frac"] for m in per_item])
    nli_contra_frac_mean = mean_or_none([m["nli_contra_frac"] for m in per_item])
    answer_relevance_mean = mean_or_none([m["answer_relevance"] for m in per_item])
    answer_faithfulness_mean = mean_or_none([m["answer_faithfulness"] for m in per_item])

    results = {
        "num_pairs": num_pairs,
        "token_f1_mean": token_f1_mean,
        "rouge_l_f1_mean": rouge_l_f1_mean,
        "nli_entail_frac_mean": nli_entail_frac_mean,
        "nli_contra_frac_mean": nli_contra_frac_mean,
        "answer_relevance_mean": answer_relevance_mean,
        "answer_faithfulness_mean": answer_faithfulness_mean,
    }

    # Write aggregate JSON
    os.makedirs(os.path.dirname(args.out_json), exist_ok=True)
    with open(args.out_json, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"[INFO] Aggregate metrics written to: {args.out_json}")

    # Write per-item CSV
    if args.out_csv:
        os.makedirs(os.path.dirname(args.out_csv), exist_ok=True)
        # Collect union of keys for robust header
        fieldnames = sorted({k for m in per_item for k in m.keys()})
        with open(args.out_csv, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for m in per_item:
                writer.writerow(m)
        print(f"[INFO] Per-item metrics written to CSV: {args.out_csv}")

    # Log key metrics
    print(f"[INFO] token_f1_mean         = {token_f1_mean:.4f}" if token_f1_mean is not None else "[INFO] token_f1_mean         = None")
    print(f"[INFO] rouge_l_f1_mean      = {rouge_l_f1_mean:.4f}" if rouge_l_f1_mean is not None else "[INFO] rouge_l_f1_mean      = None")
    if nli_entail_frac_mean is not None:
        print(f"[INFO] nli_entail_frac_mean = {nli_entail_frac_mean:.4f}")
    if nli_contra_frac_mean is not None:
        print(f"[INFO] nli_contra_frac_mean = {nli_contra_frac_mean:.4f}")
    if answer_relevance_mean is not None:
        print(f"[INFO] answer_relevance_mean   = {answer_relevance_mean:.4f}")
    if answer_faithfulness_mean is not None:
        print(f"[INFO] answer_faithfulness_mean = {answer_faithfulness_mean:.4f}")


if __name__ == "__main__":
    main()

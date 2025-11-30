#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Step 2: Answer generation for RAG.

Supports multiple providers:
- OpenAI (gpt-4o, gpt-4o-mini, etc.)
- Google Gemini (e.g. gemini-2.5-flash-lite, gemini-2.5-pro)
- Anthropic (e.g. claude-3.5-sonnet, claude-3.5-haiku)
- Local HuggingFace models (via prefix: hf:<model_name>)

Inputs
------
- --retrieval-json: JSONL from rag_step1_retrieve.py
    Each line: {
        "qa_id": ...,
        "question": ...,
        "persona": ... (optional),
        "retriever": "bm25" | "e5" | "hybrid_rrf_bm25_e5" | ...,
        "retrieved": [
            {"pid": "...", "rank": 1, "score": ...},
            ...
        ],
        ...
    }

- --passages: passages_full.jsonl
    Each line: {
        "pid": "...",
        "text": "...",
        "document_id": ...,
        "passage_id": "...",
        ...
    }

Output
------
JSONL with one object per QA including the generated RAG answer:

{
  "id": "<qa_id>",
  "qa_id": "<qa_id>",
  "persona": "...",
  "question": "...",
  "rag_answer": "...",
  "generator_model": "<model_name>",
  "retriever": "<retriever_name>",
  "topk_contexts": <int>,
  "retrieved": [... top-k retrieved entries ...],
  "contexts": [
     {"pid": "...", "text": "...", "document_id": ..., "passage_id": "..."},
     ...
  ]
}
"""

import argparse
import json
import os
import time
from typing import Dict, List, Any, Tuple, Optional

from tqdm import tqdm

# Silence some noisy logs (esp. from gRPC / Gemini)
os.environ.setdefault("GRPC_VERBOSITY", "ERROR")
os.environ.setdefault("GLOG_minloglevel", "2")

# ---------------------------------------------------------------------------
# OpenAI setup
# ---------------------------------------------------------------------------
try:
    from openai import OpenAI

    _openai_client = OpenAI()  # expects OPENAI_API_KEY
    _USE_NEW_OPENAI_CLIENT = True
except ImportError:
    try:
        import openai

        _openai_client = openai  # legacy client
        _USE_NEW_OPENAI_CLIENT = False
    except ImportError:
        _openai_client = None
        _USE_NEW_OPENAI_CLIENT = False

# ---------------------------------------------------------------------------
# Gemini setup
# ---------------------------------------------------------------------------
try:
    import google.generativeai as genai

    _HAS_GEMINI = True
except ImportError:
    genai = None
    _HAS_GEMINI = False

# ---------------------------------------------------------------------------
# Anthropic setup
# ---------------------------------------------------------------------------
try:
    import anthropic

    _anthropic_client = anthropic.Anthropic()  # expects ANTHROPIC_API_KEY
    _HAS_ANTHROPIC = True
except ImportError:
    _anthropic_client = None
    _HAS_ANTHROPIC = False

# ---------------------------------------------------------------------------
# HuggingFace local model setup (lazy)
# ---------------------------------------------------------------------------
_HF_MODEL = None
_HF_TOKENIZER = None
_HF_LOADED_NAME: Optional[str] = None


def init_hf_model(model_name: str) -> None:
    """
    Lazily load a local HF model + tokenizer.

    Expected usage:
    - model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct"
    - called via --model hf:<model_name>
    """
    global _HF_MODEL, _HF_TOKENIZER, _HF_LOADED_NAME
    if _HF_MODEL is not None and _HF_LOADED_NAME == model_name:
        return

    from transformers import AutoModelForCausalLM, AutoTokenizer
    import torch

    print(f"[INFO] Loading HF model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16,
        device_map="auto",
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    _HF_MODEL = model
    _HF_TOKENIZER = tokenizer
    _HF_LOADED_NAME = model_name
    print("[INFO] HF model loaded.")


# ---------------------------------------------------------------------------
# Data loading helpers
# ---------------------------------------------------------------------------
def load_passages(path: str) -> Dict[str, Dict[str, Any]]:
    """
    Load passages_full.jsonl into a dict keyed by pid.
    """
    passages: Dict[str, Dict[str, Any]] = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            pid = obj.get("pid")
            if not pid:
                continue
            passages[pid] = obj
    return passages


def load_retrievals(path: str) -> List[Dict[str, Any]]:
    """
    Load retrieval JSONL produced by rag_step1_retrieve.py.
    """
    records: List[Dict[str, Any]] = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            obj = json.loads(line)
            records.append(obj)
    return records


# ---------------------------------------------------------------------------
# Provider detection
# ---------------------------------------------------------------------------
class Provider:
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    HF_LOCAL = "hf_local"


def detect_provider(model_name: str) -> str:
    """
    Infer provider from model_name.
    - "gemini-..." -> GEMINI
    - startswith "claude" or contains "anthropic" -> ANTHROPIC
    - startswith "hf:" -> HF_LOCAL
    - otherwise -> OPENAI
    """
    lower = model_name.lower()
    if lower.startswith("hf:"):
        return Provider.HF_LOCAL
    if "gemini" in lower:
        return Provider.GEMINI
    if lower.startswith("claude") or "anthropic" in lower:
        return Provider.ANTHROPIC
    return Provider.OPENAI


# ---------------------------------------------------------------------------
# OpenAI / Gemini / Anthropic / HF call wrappers
# ---------------------------------------------------------------------------
def call_openai_chat(
    model: str,
    system_msg: str,
    user_msg: str,
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """
    Wrapper around OpenAI ChatCompletion-style API (new + legacy).
    """
    if _openai_client is None:
        raise RuntimeError(
            "No OpenAI client found. Install 'openai' and set OPENAI_API_KEY."
        )

    messages = [
        {"role": "system", "content": system_msg},
        {"role": "user", "content": user_msg},
    ]

    try:
        if _USE_NEW_OPENAI_CLIENT:
            resp = _openai_client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = resp.choices[0].message.content
        else:
            # Legacy client style
            resp = _openai_client.ChatCompletion.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens,
            )
            content = resp["choices"][0]["message"]["content"]
    except Exception as e:
        return f"[OPENAI_API_ERROR] {e}"

    return (content or "").strip()


def call_gemini_chat(
    model: str,
    system_msg: str,
    user_msg: str,
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """
    Wrapper around Google Gemini API.

    Requirements:
    - google-generativeai installed
    - GOOGLE_API_KEY set in the environment
    """
    if not _HAS_GEMINI or genai is None:
        raise RuntimeError("The 'google-generativeai' package is not installed.")

    api_key = os.environ.get("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY environment variable not found.")

    genai.configure(api_key=api_key)

    generation_config = genai.GenerationConfig(
        temperature=temperature,
        max_output_tokens=max_tokens,
    )

    # We rely on default safety settings to avoid version-specific enum issues.
    gemini_model = genai.GenerativeModel(
        model_name=model,
        system_instruction=system_msg,
        generation_config=generation_config,
    )

    try:
        response = gemini_model.generate_content(user_msg)

        if not getattr(response, "candidates", None):
            # Could be blocked or empty
            reason = getattr(response, "prompt_feedback", None)
            return f"[GEMINI_BLOCKED_OR_EMPTY] {reason}"

        first = response.candidates[0]
        # If there is a safety-related finish reason, mark it
        finish_reason = getattr(first, "finish_reason", None)
        if str(finish_reason).upper() == "SAFETY":
            return "[GEMINI_SAFETY_BLOCK]"

        if not getattr(first, "content", None) or not first.content.parts:
            return "[GEMINI_BLOCKED_OR_EMPTY]"

        text = (response.text or "").strip()
        if not text and first.content and first.content.parts:
            # fallback: concatenate parts
            parts_text = " ".join(
                getattr(p, "text", "") for p in first.content.parts
            ).strip()
            text = parts_text

        if not text:
            return "[GEMINI_EMPTY_TEXT]"

        return text
    except Exception as e:
        return f"[GEMINI_API_ERROR] {e}"


def call_anthropic_chat(
    model: str,
    system_msg: str,
    user_msg: str,
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """
    Wrapper around Anthropic Messages API.
    """
    if not _HAS_ANTHROPIC or _anthropic_client is None:
        raise RuntimeError(
            "Anthropic client not available. Install 'anthropic' and set ANTHROPIC_API_KEY."
        )

    try:
        resp = _anthropic_client.messages.create(
            model=model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system_msg,
            messages=[{"role": "user", "content": user_msg}],
        )
        if not resp.content:
            return "[ANTHROPIC_EMPTY_RESPONSE]"

        # Collect text parts
        parts = [
            c.text for c in resp.content if getattr(c, "type", None) == "text"
        ]
        text = "\n".join(parts).strip() if parts else ""
        return text or "[ANTHROPIC_EMPTY_RESPONSE]"
    except Exception as e:
        return f"[ANTHROPIC_API_ERROR] {e}"


def call_hf_chat(
    model_name: str,
    system_msg: str,
    user_msg: str,
    temperature: float = 0.0,
    max_tokens: int = 512,
) -> str:
    """
    Simple chat-style wrapper for instruction-tuned HF models.

    - model_name is the HF repo string (without "hf:" prefix).
    - We format prompt as system + user concatenation.
    """
    init_hf_model(model_name)

    from transformers import GenerationConfig
    import torch

    tokenizer = _HF_TOKENIZER
    model = _HF_MODEL

    # Basic prompt format compatible with many instruct models
    prompt = f"System: {system_msg}\n\nUser: {user_msg}\n\nAssistant:"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    do_sample = temperature > 0.0
    gen_config = GenerationConfig(
        max_new_tokens=max_tokens,
        do_sample=do_sample,
        temperature=temperature if do_sample else 1.0,
        pad_token_id=tokenizer.eos_token_id,
    )

    with torch.no_grad():
        gen_ids = model.generate(
            **inputs,
            **gen_config.to_dict(),
        )

    # Strip the prompt tokens from the generated sequence
    generated = gen_ids[0][inputs["input_ids"].shape[1]:]
    gen_text = tokenizer.decode(generated, skip_special_tokens=True)
    return gen_text.strip() or "[HF_EMPTY_RESPONSE]"


# ---------------------------------------------------------------------------
# Prompt construction
# ---------------------------------------------------------------------------
def build_prompt(question: str, contexts: List[Dict[str, Any]]) -> Tuple[str, str]:
    """
    Build a DPEL-style answer prompt for RAG.

    `contexts`: list of dicts {pid, text, document_id, passage_id}.
    The model should cite passages generically as [#P:<PID>].
    """
    context_blocks: List[str] = []

    for i, c in enumerate(contexts, start=1):
        doc_id = c.get("document_id")
        passage_pid = c.get("passage_id")
        pid = c.get("pid")

        header_bits = []
        if doc_id is not None:
            header_bits.append(f"DocumentID={doc_id}")
        if passage_pid is not None:
            header_bits.append(f"PassageID={passage_pid}")
        header_bits.append(f"PID={pid}")
        header = ", ".join(header_bits)

        block = f"[CTX {i}] {header}\n{c.get('text', '').strip()}"
        context_blocks.append(block)

    if context_blocks:
        context_str = "\n\n".join(context_blocks)
    else:
        context_str = "(no context available)"

    system_msg = (
        "You are an expert assistant for ADGM/FSRA regulatory questions.\n"
        "You must follow the user instructions exactly.\n"
        "Use ONLY the information in the provided context passages (no outside knowledge).\n"
        "Combine information from multiple passages when needed. If the context is incomplete,\n"
        "you must say so explicitly.\n"
    )

    user_msg = f"""
CONTEXT PASSAGES:
{context_str}

QUESTION:
{question}

ANSWER REQUIREMENTS (ALWAYS PROFESSIONAL TONE):
- Form: default = one compact professional paragraph of about 180–220 words.
- OPTIONAL bullet form: if enumerating duties/steps improves clarity, write:
  (a) a 1–2 sentence lead-in (professional conclusion),
  (b) a short bullet list (3–6 bullets, one sentence each, end with a period),
  (c) an optional one-sentence wrap-up.
- Micro-structure (paragraph or bullets):
  (i)   Start with a clear conclusion that directly answers the question.
  (ii)  State any key preconditions / definitions that must hold.
  (iii) Describe the required procedure / obligations (what must or must not be done).
  (iv)  Include any timing / record-keeping / notification requirements (if present).
  (v)   Mention important exceptions or edge cases (if present).
- Every claim or bullet must be grounded in the context passages; do NOT invent content
  or cite outside rules/documents.

EVIDENCE TAGGING (MANDATORY BUT GENERIC):
- Each context passage has a PID field (e.g. PID=123 or PID=abc-456).
- Whenever a sentence or bullet relies on a specific passage, append a tag [#P:<PID>]
  at the end of that sentence or bullet. For example: "... must notify the Regulator. [#P:123]"
- Use at least two distinct PIDs if the question genuinely requires information from multiple passages;
  if the answer is fully supported by a single passage, one PID is acceptable.
- Place tags at the END of the relevant sentence/bullet. Do not over-tag or tag unrelated text.

Write a single answer that follows all of the requirements above.
Do NOT output JSON or any metadata, only the answer text itself with the [#P:...] tags inserted.
""".strip()

    return system_msg, user_msg


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Step 2: Generate RAG answers from retrieval outputs (OpenAI / Gemini / Anthropic / HF-local)."
    )
    parser.add_argument(
        "--retrieval-json",
        required=True,
        help="Path to retrieval JSONL produced by rag_step1_retrieve.py.",
    )
    parser.add_argument(
        "--passages",
        required=True,
        help="Path to passages_full.jsonl.",
    )
    parser.add_argument(
        "--model",
        required=True,
        help=(
            "Generator model name, e.g. 'gpt-4o', 'gpt-4o-mini', 'gemini-2.5-flash-lite', "
            "'claude-3.5-sonnet', or 'hf:meta-llama/Meta-Llama-3.1-8B-Instruct'."
        ),
    )
    parser.add_argument(
        "--topk-contexts",
        type=int,
        default=10,
        help="Number of top retrieved passages to use as context.",
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.0,
        help="Sampling/window temperature for the generator.",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=512,
        help="Maximum tokens for the generated answer.",
    )
    parser.add_argument(
        "--sleep",
        type=float,
        default=0.0,
        help="Optional sleep (seconds) between API calls to avoid rate limits.",
    )
    parser.add_argument(
        "--out-jsonl",
        required=True,
        help="Output JSONL file with generated answers.",
    )

    args = parser.parse_args()

    out_dir = os.path.dirname(args.out_jsonl)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    print(f"[INFO] Loading passages from: {args.passages}")
    passages = load_passages(args.passages)
    print(f"[INFO] Loaded {len(passages)} passages.")

    print(f"[INFO] Loading retrievals from: {args.retrieval_json}")
    retrieval_records = load_retrievals(args.retrieval_json)
    print(f"[INFO] Loaded retrievals for {len(retrieval_records)} queries.")

    provider = detect_provider(args.model)
    print(f"[INFO] Model provider detected: {provider}")

    missing_passages = 0
    total_api_errors = 0

    with open(args.out_jsonl, "w", encoding="utf-8") as out_f:
        for rec in tqdm(retrieval_records, desc="Generating answers"):
            qa_id = rec.get("qa_id") or rec.get("id") or rec.get("qid")
            question = rec.get("question")
            persona = rec.get("persona")  # Optional
            retriever_name = rec.get("retriever")

            if not question:
                # If somehow there is no question, skip this record.
                continue

            retrieved = rec.get("retrieved", [])
            contexts: List[Dict[str, Any]] = []
            used_retrieved: List[Dict[str, Any]] = []

            # Collect top-k contexts
            for r in retrieved[: args.topk_contexts]:
                pid = r.get("pid")
                if not pid:
                    continue
                p = passages.get(pid)
                if p is None:
                    missing_passages += 1
                    continue

                ctx = {
                    "pid": pid,
                    "text": p.get("text", ""),
                    "document_id": p.get("document_id"),
                    "passage_id": p.get("passage_id"),
                }
                contexts.append(ctx)
                used_retrieved.append(r)

            system_msg, user_msg = build_prompt(question, contexts)

            try:
                if provider == Provider.GEMINI:
                    answer_text = call_gemini_chat(
                        model=args.model,
                        system_msg=system_msg,
                        user_msg=user_msg,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                    )
                elif provider == Provider.ANTHROPIC:
                    answer_text = call_anthropic_chat(
                        model=args.model,
                        system_msg=system_msg,
                        user_msg=user_msg,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                    )
                elif provider == Provider.HF_LOCAL:
                    hf_name = args.model[len("hf:") :]
                    answer_text = call_hf_chat(
                        model_name=hf_name,
                        system_msg=system_msg,
                        user_msg=user_msg,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                    )
                else:
                    # Default: OpenAI
                    answer_text = call_openai_chat(
                        model=args.model,
                        system_msg=system_msg,
                        user_msg=user_msg,
                        temperature=args.temperature,
                        max_tokens=args.max_tokens,
                    )
            except Exception as e:
                total_api_errors += 1
                answer_text = f"[GENERATION_ERROR] {type(e).__name__}: {e}"

            out_obj = {
                "id": qa_id,
                "qa_id": qa_id,
                "persona": persona,
                "question": question,
                "rag_answer": answer_text,
                "generator_model": args.model,
                "retriever": retriever_name,
                "topk_contexts": args.topk_contexts,
                "retrieved": used_retrieved,
                "contexts": contexts,
            }

            out_f.write(json.dumps(out_obj, ensure_ascii=False) + "\n")

            if args.sleep > 0.0:
                time.sleep(args.sleep)

    print(f"[INFO] Wrote generated answers to: {args.out_jsonl}")
    if missing_passages > 0:
        print(f"[WARN] Missing passages for {missing_passages} retrieved pids.")
    if total_api_errors > 0:
        print(f"[WARN] Encountered {total_api_errors} API errors; "
              f"answers tagged with [GENERATION_ERROR] or provider-specific error tags.")


if __name__ == "__main__":
    main()

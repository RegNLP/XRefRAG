#!/usr/bin/env python3
# run_rag.py
# -*- coding: utf-8 -*-

"""
RAG runner for RegRAG-Xref.

Two modes:
- oracle: use the gold SOURCE + TARGET passages from debug_context (no retrieval).
- realistic: use a precomputed TREC runfile (BM25/e5/BGE/...); take top-k as context.

Inputs:
- Curated QA JSONL (DPEL or SCHEMA, kept or eliminated).
- Full passage corpus JSONL (data/passages_full.jsonl).
- Optional runfile (for realistic mode).

Outputs:
- JSONL with RAG answers and retrieved contexts.

Incremental behavior:
- If --out-jsonl already exists, previously successful rows (status=="ok" and non-empty
  rag_answer) are reused, and only missing/failed rows are recomputed.
"""

import argparse
import json
import os
import sys
import time
from collections import defaultdict

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None


# -----------------------------
# Loading utilities
# -----------------------------

def load_passages(path):
    """pid -> passage dict."""
    pid2passage = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            pid = str(obj.get("pid") or obj.get("id") or "").strip()
            if not pid:
                continue
            pid2passage[pid] = {
                "pid": pid,
                "text": obj.get("text") or obj.get("contents") or "",
                "document_id": obj.get("document_id"),
                "passage_id": obj.get("passage_id"),
            }
    return pid2passage


def load_runfile(path, k):
    """
    TREC run file -> qid -> [pid,...] (top-k, deduped).
    """
    tmp = defaultdict(list)  # qid -> [(rank, pid)]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            qid, _, pid, rank_str, score, tag = parts
            try:
                rank = int(rank_str)
            except ValueError:
                rank = 0
            tmp[qid].append((rank, pid))

    runs = {}
    for qid, items in tmp.items():
        items.sort(key=lambda x: x[0])
        seen = set()
        ordered = []
        for _, pid in items:
            if pid in seen:
                continue
            seen.add(pid)
            ordered.append(pid)
            if len(ordered) >= k:
                break
        runs[qid] = ordered
    return runs


def load_qas(path):
    """Load curated QA jsonl (DPEL/SCHEMA)."""
    qas = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            qid = obj.get("qa_id") or obj.get("id")
            q = (obj.get("question") or "").strip()
            if not (qid and q):
                continue
            qas.append(obj)
    return qas


def load_existing_outputs(path):
    """
    Load existing RAG outputs if the file exists.
    Returns: dict qa_id -> obj
    Only the first occurrence of each qa_id is kept.
    """
    if not os.path.exists(path):
        return {}
    existing = {}
    total = 0
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            try:
                obj = json.loads(line)
            except Exception:
                continue
            qid = obj.get("qa_id") or obj.get("id")
            if not qid:
                continue
            if qid not in existing:
                existing[qid] = obj
    print(f"[info] found existing RAG file with {total} lines, "
          f"{len(existing)} unique qa_ids")
    return existing


# -----------------------------
# Prompt & model call
# -----------------------------

def call_openai_chat(model_name, system_msg, user_msg,
                     max_tokens=512, temperature=0.0, seed=None):
    """
    Thin wrapper around OpenAI chat completion.
    Requires OPENAI_API_KEY in your environment and `pip install openai`.
    """
    if OpenAI is None:
        raise RuntimeError(
            "openai client not installed. Run `pip install openai` or adjust the code."
        )
    client = OpenAI()
    extra = {}
    if seed is not None:
        extra["seed"] = seed

    resp = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
        **extra,
    )
    return (resp.choices[0].message.content or "").strip()


def build_prompt(question, contexts):
    """
    Build a DPEL-style answer prompt for RAG.

    `contexts`: list of dicts {pid, text, document_id, passage_id}
    We DO NOT assume which passage is source/target here.
    The model will cite passages generically as [#P:<PID>].
    """
    context_blocks = []
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

    context_str = "\n\n".join(context_blocks) if context_blocks else "(no context available)"

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


# -----------------------------
# Main
# -----------------------------

def main():
    ap = argparse.ArgumentParser(
        description="Run RAG over curated QAs (oracle or realistic) for RegRAG-Xref."
    )
    ap.add_argument(
        "--mode",
        choices=["oracle", "realistic"],
        default="realistic",
        help="oracle: use gold SOURCE+TARGET from debug_context; realistic: use runfile.",
    )
    ap.add_argument(
        "--qa-jsonl",
        dest="qa_jsonl",
        required=True,
        help="Curated QA jsonl (e.g. DPEL/SCHEMA kept or eliminated).",
    )
    ap.add_argument(
        "--passages",
        required=True,
        help="Passage corpus jsonl (e.g. data/passages_full.jsonl).",
    )
    ap.add_argument(
        "--run-file",
        dest="run_file",
        help="TREC run file (required in realistic mode, ignored in oracle mode).",
    )
    ap.add_argument(
        "--topk",
        type=int,
        default=4,
        help="Top-k passages to feed into the RAG prompt (realistic mode).",
    )
    ap.add_argument(
        "--model",
        default="gpt-4o",
        help="OpenAI chat model name.",
    )
    ap.add_argument(
        "--out-jsonl",
        dest="out_jsonl",
        required=True,
        help="Output jsonl with RAG answers.",
    )
    ap.add_argument(
        "--max-questions",
        dest="max_questions",
        type=int,
        default=None,
        help="Optional cap on number of QAs (for quick tests).",
    )
    ap.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Optional seed for deterministic-ish decoding.",
    )
    args = ap.parse_args()

    print(f"[info] mode: {args.mode}")
    print(f"[info] loading passages from: {args.passages}")
    pid2passage = load_passages(args.passages)
    print(f"[info] passages loaded: {len(pid2passage)}")

    qid2pids = {}
    if args.mode == "realistic":
        if not args.run_file:
            raise RuntimeError("--run-file is required in realistic mode.")
        print(f"[info] loading runfile: {args.run_file}")
        qid2pids = load_runfile(args.run_file, k=args.topk)
        print(f"[info] runfile queries: {len(qid2pids)}")

    print(f"[info] loading QAs from: {args.qa_jsonl}")
    qas = load_qas(args.qa_jsonl)
    print(f"[info] QAs loaded: {len(qas)}")

    if args.max_questions is not None:
        qas = qas[: args.max_questions]
        print(f"[info] limiting to first {len(qas)} questions")

    out_path = args.out_jsonl
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    # Incremental: load existing outputs if present
    existing_by_qid = load_existing_outputs(out_path)
    reused_ok = 0
    reused_other = 0
    fresh_runs = 0
    fresh_errors = 0

    tmp_path = out_path + ".tmp"
    print(f"[info] writing RAG outputs to: {tmp_path}")

    with open(tmp_path, "w", encoding="utf-8") as outf:
        for idx, qa in enumerate(qas, start=1):
            qid = qa.get("qa_id") or qa.get("id")
            question = (qa.get("question") or "").strip()
            expected_answer = (qa.get("expected_answer") or "").strip()
            dbg = qa.get("debug_context") or {}

            existing = existing_by_qid.get(qid)

            # If we have a previous successful answer, just reuse it.
            if existing and existing.get("status") == "ok" and (existing.get("rag_answer") or "").strip():
                out_obj = existing
                reused_ok += 1
            else:
                # -------- contexts --------
                contexts = []
                retrieved_pids = []
                if args.mode == "oracle":
                    sid = str(dbg.get("source_passage_id") or "").strip()
                    tid = str(dbg.get("target_passage_id") or "").strip()
                    for pid in [sid, tid]:
                        if pid and pid in pid2passage and pid not in retrieved_pids:
                            contexts.append(pid2passage[pid])
                            retrieved_pids.append(pid)
                    retrieval_status = "oracle"
                else:
                    pids = qid2pids.get(qid, [])
                    for pid in pids:
                        if pid in pid2passage:
                            contexts.append(pid2passage[pid])
                            retrieved_pids.append(pid)
                    retrieval_status = "realistic"

                # -------- call LLM --------
                if not contexts:
                    rag_answer = ""
                    status = "no_context"
                else:
                    system_msg, user_msg = build_prompt(question, contexts)
                    try:
                        rag_answer = call_openai_chat(
                            model_name=args.model,
                            system_msg=system_msg,
                            user_msg=user_msg,
                            max_tokens=512,
                            temperature=0.0,
                            seed=args.seed,
                        )
                        status = "ok"
                        fresh_runs += 1
                    except Exception as e:
                        rag_answer = ""
                        status = f"error: {e}"
                        fresh_errors += 1
                        print(f"[warn] qid={qid} error: {e}", file=sys.stderr)

                out_obj = {
                    "qa_id": qid,
                    "question": question,
                    "expected_answer": expected_answer,
                    "rag_answer": rag_answer,
                    "status": status,
                    "retrieval_mode": args.mode,
                    "retrieval_status": retrieval_status,
                    "retriever_run": os.path.basename(args.run_file) if args.run_file else None,
                    "topk": args.topk if args.mode == "realistic" else 2,
                    "model": args.model,
                    "retrieved_pids": retrieved_pids,
                    "retrieved_contexts": contexts,
                    "ts": time.time(),
                    "method": qa.get("method"),
                    "persona": qa.get("persona"),
                    "debug_context": dbg,
                }

                if existing and not (existing.get("status") == "ok" and (existing.get("rag_answer") or "").strip()):
                    reused_other += 1  # we overwrote a previous error/no_context

            outf.write(json.dumps(out_obj, ensure_ascii=False) + "\n")

            if idx % 20 == 0:
                print(f"[info] processed {idx}/{len(qas)}")

    # Atomically replace old file
    os.replace(tmp_path, out_path)

    print("[done] RAG run complete.")
    print(f"[stats] reused_ok={reused_ok} | overwrote_existing_non_ok={reused_other} "
          f"| fresh_ok_runs={fresh_runs} | fresh_errors={fresh_errors}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# rerank_bm25_with_e5.py
# -*- coding: utf-8 -*-

import argparse, json
from collections import defaultdict
from sentence_transformers import SentenceTransformer
import numpy as np
from tqdm import tqdm

def load_passages(path="data/passages.jsonl"):
    pid2text = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            pid = str(row["pid"])
            text = str(row["text"])
            pid2text[pid] = text
    return pid2text

def load_queries_tsv(path):
    qid2q = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            qid, q = line.split("\t", 1)
            qid2q[qid.strip()] = q.strip()
    return qid2q

def load_bm25_run(path, k_candidate=200):
    qid2cands = defaultdict(list)  # qid -> [docid]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            qid, _, docid, rank, score, tag = parts
            qid2cands[qid].append((int(rank), docid))
    # rank'e göre sırala ve top-k al
    for qid in qid2cands:
        cands = sorted(qid2cands[qid], key=lambda x: x[0])[:k_candidate]
        qid2cands[qid] = [docid for _, docid in cands]
    return qid2cands

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--queries", required=True, help="TSV: qid<TAB>query")
    ap.add_argument("--bm25", required=True, help="BM25 run file")
    ap.add_argument("--passages", default="data/passages.jsonl")
    ap.add_argument("--output", required=True)
    ap.add_argument("--model-name", default="intfloat/e5-base-v2")
    ap.add_argument("--k-candidate", type=int, default=200,
                    help="BM25 top-k candidates to rerank")
    ap.add_argument("--k-output", type=int, default=100,
                    help="final top-k docs to output")
    args = ap.parse_args()

    print("[rerank] loading passages...")
    pid2text = load_passages(args.passages)

    print("[rerank] loading queries...")
    qid2q = load_queries_tsv(args.queries)

    print("[rerank] loading BM25 run...")
    qid2cands = load_bm25_run(args.bm25, k_candidate=args.k_candidate)

    print("[rerank] loading model:", args.model_name)
    model = SentenceTransformer(args.model_name)

    qids = sorted(qid2cands.keys())
    with open(args.output, "w", encoding="utf-8") as out:
        for qid in tqdm(qids):
            if qid not in qid2q:
                continue
            query = qid2q[qid]
            cand_pids = [pid for pid in qid2cands[qid] if pid in pid2text]
            if not cand_pids:
                continue
            cand_texts = [pid2text[pid] for pid in cand_pids]

            # e5: query/passage prefix kullanmak istersen:
            # q_emb = model.encode(["query: " + query], normalize_embeddings=True)[0]
            # p_embs = model.encode(["passage: " + t for t in cand_texts], normalize_embeddings=True)
            q_emb = model.encode([query], normalize_embeddings=True)[0]
            p_embs = model.encode(cand_texts, normalize_embeddings=True)

            scores = np.dot(p_embs, q_emb)
            scored = list(zip(cand_pids, scores))
            scored.sort(key=lambda x: x[1], reverse=True)
            scored = scored[:args.k_output]

            for rank, (pid, score) in enumerate(scored, start=1):
                out.write(f"{qid} Q0 {pid} {rank} {float(score):.6f} bm25_e5_rerank\n")

    print("[rerank] done, wrote:", args.output)

if __name__ == "__main__":
    main()

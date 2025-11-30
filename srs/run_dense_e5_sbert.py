#!/usr/bin/env python3
# run_dense_e5_sbert.py
# -*- coding: utf-8 -*-

import argparse, json
from collections import defaultdict
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm

def load_passages(path="data/passages.jsonl"):
    pids, texts = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            row = json.loads(line)
            pids.append(str(row["pid"]))
            texts.append(str(row["text"]))
    return pids, texts

def load_queries(path):
    qids, queries = [], []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line:
                continue
            qid, q = line.split("\t", 1)
            qids.append(qid.strip())
            queries.append(q.strip())
    return qids, queries

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--passages", default="data/passages.jsonl")
    ap.add_argument("--queries", required=True)   # TSV: qid \t query
    ap.add_argument("--output", required=True)
    ap.add_argument("--k", type=int, default=100)
    ap.add_argument("--model-name", default="intfloat/e5-base-v2")
    args = ap.parse_args()

    print("[e5] loading passages...")
    pids, ptexts = load_passages(args.passages)

    print("[e5] loading model:", args.model_name)
    model = SentenceTransformer(args.model_name)

    # Passage embeddings
    print("[e5] encoding passages...")
    p_embs = model.encode(
        ptexts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    p_embs = np.asarray(p_embs, dtype="float32")
    dim = p_embs.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(p_embs)

    print("[e5] loading queries:", args.queries)
    qids, qtexts = load_queries(args.queries)
    print("[e5] encoding queries...")
    q_embs = model.encode(
        qtexts,
        batch_size=32,
        show_progress_bar=True,
        normalize_embeddings=True,
    )
    q_embs = np.asarray(q_embs, dtype="float32")

    print("[e5] searching...")
    D, I = index.search(q_embs, args.k)

    print("[e5] writing run to", args.output)
    with open(args.output, "w", encoding="utf-8") as out:
        for qi, qid in enumerate(qids):
            for rank, (doc_idx, score) in enumerate(zip(I[qi], D[qi]), start=1):
                pid = pids[doc_idx]
                out.write(f"{qid} Q0 {pid} {rank} {float(score):.6f} e5\n")

    print("[e5] done.")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# fuse_rrf.py
# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict

def read_run(path):
    runs = defaultdict(list)  # qid -> [(docid, rank, score)]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 6:
                continue
            qid, _, docid, rank, score, tag = parts
            runs[qid].append((docid, int(rank), float(score)))
    # rank'e göre sırala (emin olmak için)
    for qid in runs:
        runs[qid].sort(key=lambda x: x[1])
    return runs

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bm25", required=True)
    ap.add_argument("--dense", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--k", type=int, default=100, help="max docs per query in fused run")
    ap.add_argument("--rrf-k", type=int, default=60, help="RRF constant")
    args = ap.parse_args()

    bm25 = read_run(args.bm25)
    dense = read_run(args.dense)

    qids = sorted(set(bm25.keys()) | set(dense.keys()))

    with open(args.output, "w", encoding="utf-8") as out:
        for qid in qids:
            scores = defaultdict(float)
            for docid, rank, _ in bm25.get(qid, []):
                scores[docid] += 1.0 / (args.rrf_k + rank)
            for docid, rank, _ in dense.get(qid, []):
                scores[docid] += 1.0 / (args.rrf_k + rank)

            ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:args.k]
            for rank, (docid, score) in enumerate(ranked, start=1):
                out.write(f"{qid} Q0 {docid} {rank} {score:.6f} rrf\n")

if __name__ == "__main__":
    main()

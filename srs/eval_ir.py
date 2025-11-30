#!/usr/bin/env python3
# eval_ir.py
# -*- coding: utf-8 -*-

import argparse
from collections import defaultdict
import math
import os

def load_qrels(path):
    qrels = defaultdict(dict)  # qid -> {docid: rel}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            qid, _, docid, rel = parts[0], parts[1], parts[2], int(parts[3])
            if rel > 0:
                qrels[qid][docid] = rel
    return qrels

def load_run(path, k=None):
    run = defaultdict(list)  # qid -> [(docid, score)]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            qid, _, docid, rank, score, tag = parts
            run[qid].append((docid, float(score)))
    # score’a göre sırala (yüksek → düşük)
    for qid in run:
        run[qid].sort(key=lambda x: x[1], reverse=True)
        if k is not None:
            run[qid] = run[qid][:k]
    return run

def metrics_for_run(qrels, run, k=10):
    all_qids = set(qrels.keys())
    recalls, maps, ndcgs = [], [], []

    for qid in all_qids:
        rel_docs = qrels[qid]
        if not rel_docs:
            continue
        retrieved = run.get(qid, [])
        num_rel = len(rel_docs)

        hits = 0
        ap = 0.0
        dcg = 0.0
        seen_docs = set()  # duplicate docid’leri tek saymak için

        for rank, (docid, _) in enumerate(retrieved[:k], start=1):
            if docid in seen_docs:
                continue
            seen_docs.add(docid)

            rel = 1 if docid in rel_docs else 0
            if rel:
                hits += 1
                ap += hits / rank
                dcg += 1.0 / math.log2(rank + 1)

        recall = hits / num_rel if num_rel > 0 else 0.0
        map_k = ap / num_rel if num_rel > 0 else 0.0

        ideal_hits = min(num_rel, k)
        idcg = sum(1.0 / math.log2(r + 1) for r in range(1, ideal_hits + 1))
        ndcg = (dcg / idcg) if idcg > 0 else 0.0

        # Güvenlik
        assert 0.0 <= recall <= 1.0 + 1e-6, f"recall>1 for qid={qid}: {recall}"
        assert 0.0 <= map_k <= 1.0 + 1e-6, f"map>1 for qid={qid}: {map_k}"
        assert 0.0 <= ndcg <= 1.0 + 1e-6, f"ndcg>1 for qid={qid}: {ndcg}"

        recalls.append(recall)
        maps.append(map_k)
        ndcgs.append(ndcg)

    def avg(xs): return sum(xs) / len(xs) if xs else 0.0
    return {
        f"recall@{k}": avg(recalls),
        f"map@{k}": avg(maps),
        f"ndcg@{k}": avg(ndcgs),
        "num_queries": len(all_qids),
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qrels", required=True)
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--k", type=int, default=10)
    args = ap.parse_args()

    qrels = load_qrels(args.qrels)
    print(f"# qrels: {args.qrels} | queries={len(qrels)}")

    print("{:<35} {:>10} {:>10} {:>10}".format(
        "run", f"R@{args.k}", f"MAP@{args.k}", f"nDCG@{args.k}"
    ))
    print("-" * 70)

    for run_path in args.runs:
        run = load_run(run_path, k=args.k)
        m = metrics_for_run(qrels, run, k=args.k)
        name = os.path.basename(run_path)
        print("{:<35} {:>10.4f} {:>10.4f} {:>10.4f}".format(
            name,
            m[f"recall@{args.k}"],
            m[f"map@{args.k}"],
            m[f"ndcg@{args.k}"],
        ))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
# concordance_ir.py
# -*- coding: utf-8 -*-

import argparse
import csv
import json
import os
from collections import defaultdict

def load_qrels(path):
    """Load qrels as qid -> set(docid)."""
    qrels = defaultdict(set)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 4:
                continue
            qid, _, docid, rel = parts[0], parts[1], parts[2], int(parts[3])
            if rel > 0:
                qrels[qid].add(docid)
    return qrels

def load_run(path, k=None):
    """
    Load run as qid -> list(docid) sorted by rank.
    We keep only the top-k *unique* docids per query (dedup).
    """
    tmp = defaultdict(list)  # qid -> list of (rank, docid)
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) < 6:
                continue
            qid, _, docid, rank_str, score, tag = parts
            try:
                rank = int(rank_str)
            except ValueError:
                # Fallback if rank is not an int (shouldn't happen with pyserini)
                rank = 0
            tmp[qid].append((rank, docid))

    run = {}
    for qid, pairs in tmp.items():
        # Sort by rank, then dedup docids while preserving order
        pairs.sort(key=lambda x: x[0])
        seen = set()
        ordered_docids = []
        for _, docid in pairs:
            if docid in seen:
                continue
            seen.add(docid)
            ordered_docids.append(docid)
            if k is not None and len(ordered_docids) >= k:
                break
        run[qid] = ordered_docids
    return run

def compute_concordance(qrels, runs, k=10):
    """
    qrels: dict qid -> set(rel_docids)
    runs: dict method_name -> dict qid -> [docid,...]
    Returns:
      - list of per-query dicts for JSONL
      - methods list (for CSV header)
    """
    # Only evaluate queries that have at least one relevant doc in this qrels file
    all_qids = sorted(qrels.keys())


    method_names = sorted(runs.keys())
    results = []

    for qid in all_qids:
        rel_docs = qrels.get(qid, set())
        num_rel = len(rel_docs)

        per_method = {}
        num_methods_hit_any = 0
        num_methods_hit_all = 0

        for m in method_names:
            retrieved = runs[m].get(qid, [])
            # Already deduped, but we still only look at top-k
            retrieved = retrieved[:k]

            # Count relevant docs in top-k
            rel_hits = 0
            first_hit_rank = None

            for rank, docid in enumerate(retrieved, start=1):
                if docid in rel_docs:
                    rel_hits += 1
                    if first_hit_rank is None:
                        first_hit_rank = rank

            hit_any = rel_hits > 0
            hit_all = (num_rel > 0) and (rel_hits == num_rel)

            if hit_any:
                num_methods_hit_any += 1
            if hit_all:
                num_methods_hit_all += 1

            per_method[m] = {
                "rel_in_topk": rel_hits,
                "hit_any": hit_any,
                "hit_all": hit_all,
                "first_hit_rank": first_hit_rank,
            }

        # Simple concordance labels (you can adjust thresholds later)
        high_any = num_methods_hit_any >= 4  # e.g., 4/5 or 5/5 agree
        low_any = num_methods_hit_any <= 1   # only 0 or 1 method hits

        results.append({
            "qid": qid,
            "num_rel": num_rel,
            "methods": per_method,
            "num_methods_hit_any": num_methods_hit_any,
            "num_methods_hit_all": num_methods_hit_all,
            "high_concordance_any": high_any,
            "low_concordance_any": low_any,
            "k": k,
        })

    return results, method_names

def write_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

def write_csv(path, rows, method_names):
    """
    Flatten per-query concordance into a wide CSV:
      qid, num_rel, num_methods_hit_any, num_methods_hit_all,
      <m>_hit_any, <m>_hit_all, <m>_rel_in_topk, <m>_first_hit_rank, ...
    """
    base_cols = ["qid", "num_rel", "num_methods_hit_any", "num_methods_hit_all",
                 "high_concordance_any", "low_concordance_any", "k"]
    method_cols = []
    for m in method_names:
        method_cols.extend([
            f"{m}_hit_any",
            f"{m}_hit_all",
            f"{m}_rel_in_topk",
            f"{m}_first_hit_rank",
        ])

    fieldnames = base_cols + method_cols

    with open(path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            flat = {
                "qid": row["qid"],
                "num_rel": row["num_rel"],
                "num_methods_hit_any": row["num_methods_hit_any"],
                "num_methods_hit_all": row["num_methods_hit_all"],
                "high_concordance_any": row["high_concordance_any"],
                "low_concordance_any": row["low_concordance_any"],
                "k": row["k"],
            }
            for m in method_names:
                minfo = row["methods"].get(m, {})
                flat[f"{m}_hit_any"] = minfo.get("hit_any", False)
                flat[f"{m}_hit_all"] = minfo.get("hit_all", False)
                flat[f"{m}_rel_in_topk"] = minfo.get("rel_in_topk", 0)
                flat[f"{m}_first_hit_rank"] = minfo.get("first_hit_rank", "")
            writer.writerow(flat)

def main():
    ap = argparse.ArgumentParser(
        description="Compute per-query concordance across multiple IR runs."
    )
    ap.add_argument("--qrels", required=True, help="Qrels file (TREC format).")
    ap.add_argument("--runs", nargs="+", required=True,
                    help="One or more run files (TREC format).")
    ap.add_argument("--k", type=int, default=10,
                    help="Top-k cutoff for hit/overlap analysis.")
    ap.add_argument("--out-jsonl", default=None,
                    help="Optional JSONL output with detailed per-query stats.")
    ap.add_argument("--out-csv", default=None,
                    help="Optional CSV output (flattened per-query stats).")
    args = ap.parse_args()

    print(f"[info] loading qrels from: {args.qrels}")
    qrels = load_qrels(args.qrels)

    runs = {}
    for run_path in args.runs:
        name = os.path.basename(run_path)
        print(f"[info] loading run: {name}")
        runs[name] = load_run(run_path, k=args.k)

    print(f"[info] computing concordance for top-{args.k}...")
    rows, method_names = compute_concordance(qrels, runs, k=args.k)

    if args.out_jsonl:
        print(f"[info] writing JSONL: {args.out_jsonl}")
        write_jsonl(args.out_jsonl, rows)

    if args.out_csv:
        print(f"[info] writing CSV: {args.out_csv}")
        write_csv(args.out_csv, rows, method_names)

    # Tiny summary
    n = len(rows)
    high = sum(1 for r in rows if r["high_concordance_any"])
    low = sum(1 for r in rows if r["low_concordance_any"])
    print(f"[done] queries={n} | high_concordance_any={high} | low_concordance_any={low}")

if __name__ == "__main__":
    main()

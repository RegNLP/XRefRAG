#!/usr/bin/env python3
# build_method_qrels.py
# -*- coding: utf-8 -*-

import argparse, json
from collections import defaultdict

def load_jsonl(p):
    rows = []
    with open(p, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                pass
    return rows

def write_qrels(files, out_path):
    seen = set()
    with open(out_path, "w", encoding="utf-8") as out:
        for p in files:
            for row in load_jsonl(p):
                qid = row.get("qa_id")
                dbg = row.get("debug_context") or {}
                src = str(dbg.get("source_passage_id") or "").strip()
                tgt = str(dbg.get("target_passage_id") or "").strip()
                if not (qid and src and tgt):
                    continue
                # Aynı qid-src/tgt çiftini tekrar yazmamak için
                key1 = (qid, src)
                key2 = (qid, tgt)
                if key1 not in seen:
                    out.write(f"{qid} 0 {src} 1\n")
                    seen.add(key1)
                if key2 not in seen:
                    out.write(f"{qid} 0 {tgt} 1\n")
                    seen.add(key2)
    print(f"[ok] wrote qrels: {out_path}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dpel-kept", required=True)
    ap.add_argument("--dpel-elim", required=True)
    ap.add_argument("--schema-kept", required=True)
    ap.add_argument("--schema-elim", required=True)
    ap.add_argument("--out-qrels-dpel-kept", default="inputs/ir/qrels_kept_dpel.txt")
    ap.add_argument("--out-qrels-dpel-elim", default="inputs/ir/qrels_eliminated_dpel.txt")
    ap.add_argument("--out-qrels-schema-kept", default="inputs/ir/qrels_kept_schema.txt")
    ap.add_argument("--out-qrels-schema-elim", default="inputs/ir/qrels_eliminated_schema.txt")
    args = ap.parse_args()

    write_qrels([args.dpel_kept],   args.out_qrels_dpel_kept)
    write_qrels([args.dpel_elim],   args.out_qrels_dpel_elim)
    write_qrels([args.schema_kept], args.out_qrels_schema_kept)
    write_qrels([args.schema_elim], args.out_qrels_schema_elim)

if __name__ == "__main__":
    main()

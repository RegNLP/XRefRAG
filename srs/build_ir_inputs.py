#!/usr/bin/env python3
# build_ir_inputs.py
# -*- coding: utf-8 -*-
import argparse, json, os, re
from collections import OrderedDict

def load_jsonl(p):
    rows=[]
    with open(p,'r',encoding='utf-8') as f:
        for line in f:
            line=line.strip()
            if not line: continue
            try: rows.append(json.loads(line))
            except: pass
    return rows

def add_passage(bucket, pid, text):
    pid=str(pid).strip()
    if pid and pid not in bucket and text:
        bucket[pid]=text

def main():
    ap=argparse.ArgumentParser(description="Build queries/qrels/passages for IR from judged JSONLs.")
    ap.add_argument("--inputs", nargs="+", required=True, help="Four files: DPEL kept/eliminated + SCHEMA kept/eliminated")
    ap.add_argument("--out_queries_kept",   default="inputs/ir/queries_kept.tsv")
    ap.add_argument("--out_qrels_kept",     default="inputs/ir/qrels_kept.txt")
    ap.add_argument("--out_queries_elim",   default="inputs/ir/queries_eliminated.tsv")
    ap.add_argument("--out_qrels_elim",     default="inputs/ir/qrels_eliminated.txt")
    ap.add_argument("--out_passages_jsonl", default="data/passages.jsonl")   # dense index input
    ap.add_argument("--out_json_collection_dir", default="passages_json")    # BM25 JsonCollection
    args=ap.parse_args()

    os.makedirs(os.path.dirname(args.out_queries_kept), exist_ok=True)
    os.makedirs(os.path.dirname(args.out_passages_jsonl), exist_ok=True)
    os.makedirs(args.out_json_collection_dir, exist_ok=True)

    # Partition files by kept/eliminated
    kept_files    = [p for p in args.inputs if "/kept" in p]
    elim_files    = [p for p in args.inputs if "/eliminated" in p]

    def build_query_qrels(files, queries_path, qrels_path):
        q_seen=set()
        with open(queries_path,'w',encoding='utf-8') as qf, open(qrels_path,'w',encoding='utf-8') as rf:
            for p in files:
                for row in load_jsonl(p):
                    qid=row.get("qa_id")
                    q=row.get("question","").strip()
                    dbg=row.get("debug_context") or {}
                    src=str(dbg.get("source_passage_id") or "").strip()
                    tgt=str(dbg.get("target_passage_id") or "").strip()
                    if not (qid and q and src and tgt): continue
                    if qid not in q_seen:
                        qf.write(f"{qid}\t{q}\n")
                        q_seen.add(qid)
                    # pseudo-qrels: both src and tgt relevant
                    rf.write(f"{qid} 0 {src} 1\n")
                    rf.write(f"{qid} 0 {tgt} 1\n")

    # Build queries + qrels
    build_query_qrels(kept_files, args.out_queries_kept, args.out_qrels_kept)
    build_query_qrels(elim_files, args.out_queries_elim, args.out_qrels_elim)

    # Collect passages (minimal viable corpus from judged files)
    passages=OrderedDict()
    for p in args.inputs:
        for row in load_jsonl(p):
            dbg=row.get("debug_context") or {}
            sid=str(dbg.get("source_passage_id") or "").strip()
            tid=str(dbg.get("target_passage_id") or "").strip()
            stext=(dbg.get("source_text") or "").strip()
            ttext=(dbg.get("target_text") or "").strip()
            add_passage(passages, sid, stext)
            add_passage(passages, tid, ttext)

    # Write dense corpus
    with open(args.out_passages_jsonl,'w',encoding='utf-8') as pf:
        for pid, text in passages.items():
            pf.write(json.dumps({"pid":pid, "text":text}, ensure_ascii=False) + "\n")

    # Write BM25 JsonCollection (one shard file is fine)
    with open(os.path.join(args.out_json_collection_dir,"collection.jsonl"),"w",encoding="utf-8") as jf:
        for pid, text in passages.items():
            jf.write(json.dumps({"id":pid, "contents":text}, ensure_ascii=False) + "\n")

    print(f"[ok] queries/qrels and passages written:\n"
          f"  {args.out_queries_kept}\n  {args.out_qrels_kept}\n"
          f"  {args.out_queries_elim}\n  {args.out_qrels_elim}\n"
          f"  {args.out_passages_jsonl}\n  {args.out_json_collection_dir}/collection.jsonl")

if __name__=="__main__":
    main()

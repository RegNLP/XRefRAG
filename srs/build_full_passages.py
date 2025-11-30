#!/usr/bin/env python3
# build_full_passages.py
# -*- coding: utf-8 -*-

import json
import argparse
from collections import OrderedDict
from pathlib import Path

from doc_manifest import DOCUMENTS  # veya projende nasıl import ediyorsan

def iter_items_from_file(path):
    """JSON dosyasından pasaj item'larını çıkar."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # En sık durum: dosyanın kendisi bir liste
    if isinstance(data, list):
        for obj in data:
            yield obj
        return

    # Bazı dosyalar dict olabilir, içinde liste taşıyabilir
    if isinstance(data, dict):
        for key in ["passages", "Passages", "items", "Items"]:
            if key in data and isinstance(data[key], list):
                for obj in data[key]:
                    yield obj
                return

    # Yapı beklediğimiz gibi değilse, özel sinyal
    yield {"__STRUCTURE_ERROR__": True}

def main():
    ap = argparse.ArgumentParser(description="Build full passages.jsonl from 40 document JSONs.")
    ap.add_argument("--out_passages", default="data/passages_full.jsonl",
                    help="Output JSONL with pid, text, document_id, passage_id.")
    ap.add_argument("--out_json_collection", default="passages_json/collection_full.jsonl",
                    help="Output JSONL for Pyserini JsonCollection (id, contents).")
    args = ap.parse_args()

    out_passages_path = Path(args.out_passages)
    out_json_collection_path = Path(args.out_json_collection)

    out_passages_path.parent.mkdir(parents=True, exist_ok=True)
    out_json_collection_path.parent.mkdir(parents=True, exist_ok=True)

    passages = OrderedDict()      # pid -> dict
    problematic_files = set()

    for doc_meta in DOCUMENTS:
        doc_id = doc_meta["DocumentID"]
        path = Path(doc_meta["json_file_path"])

        if not path.exists():
            problematic_files.add(str(path))
            continue

        valid_count = 0
        structure_error = False

        for item in iter_items_from_file(path):
            # Dosya yapısı anlaşılamadıysa
            if isinstance(item, dict) and item.get("__STRUCTURE_ERROR__"):
                structure_error = True
                break

            if not isinstance(item, dict):
                # Tek tek satırları problem saymayalım, sadece atla
                continue

            # ID → pid
            pid = item.get("ID") or item.get("id")
            # Passage → text
            text = (
                item.get("Passage")
                or item.get("passage")
                or item.get("Text")
                or item.get("text")
            )
            passage_id = item.get("PassageID") or item.get("passage_id")

            # DocumentID alanı item içinde varsa onu kullan, yoksa manifest'teki
            doc_id_item = item.get("DocumentID")
            document_id = doc_id_item if doc_id_item is not None else doc_id

            # Eğer bu satırda ID veya Passage yoksa → sadece bu satırı atla
            if not pid or not text or not str(text).strip():
                continue

            pid = str(pid).strip()
            text = str(text).strip()

            if pid not in passages:
                passages[pid] = {
                    "pid": pid,
                    "text": text,
                    "document_id": document_id,
                    "passage_id": passage_id,
                }
                valid_count += 1

        # Eğer hiç valid pasaj çıkaramadıysak veya yapı tamamen bozuksa → dosyayı problemli say
        if valid_count == 0 or structure_error:
            problematic_files.add(str(path))

    # dense için full corpus
    with open(out_passages_path, "w", encoding="utf-8") as f_out:
        for rec in passages.values():
            f_out.write(json.dumps(rec, ensure_ascii=False) + "\n")

    # BM25 JsonCollection için
    with open(out_json_collection_path, "w", encoding="utf-8") as f_col:
        for rec in passages.values():
            jf_obj = {
                "id": rec["pid"],
                "contents": rec["text"],
            }
            f_col.write(json.dumps(jf_obj, ensure_ascii=False) + "\n")

    print(f"[ok] Wrote full passages to: {out_passages_path}")
    print(f"[ok] Wrote JsonCollection to: {out_json_collection_path}")
    print(f"[ok] Total passages: {len(passages)}")

    if problematic_files:
        print("\n[WARN] Problematic files (no valid passages or bad structure):")
        for p in sorted(problematic_files):
            print("  -", p)

if __name__ == "__main__":
    main()

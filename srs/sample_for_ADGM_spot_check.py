# srs/sample_for_ADGM_spot_check.py

import json
import csv
import random
from pathlib import Path

# Run as: python srs/sample_for_ADGM_spot_check.py  from repo root
from doc_manifest import DOCUMENTS

# ------------------------------------------------------
# Paths
# ------------------------------------------------------
BASE = Path.home() / "Documents" / "GitHub" / "RegRAG-Xref"
FINAL_DIR = BASE / "outputs" / "final_dataset"

PASSAGES_JSONL = BASE / "data" / "passages_full.jsonl"

OUT_DIR = FINAL_DIR / "samples"
OUT_DIR.mkdir(parents=True, exist_ok=True)
OUT_CSV = OUT_DIR / "regraxref_adgm_spotcheck.csv"

RANDOM_SEED = 42
random.seed(RANDOM_SEED)

METHODS = ["DPEL", "SCHEMA"]
PERSONAS = ["Basic", "Professional"]
REF_TYPES = ["Internal", "External"]
SPLITS = ["train", "dev", "test"]


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------
def load_jsonl(path: Path):
    items = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def build_doc_title_index():
    """Map numeric DocumentID -> short title (e.g. 3 -> 'CoBs')."""
    idx = {}
    for rec in DOCUMENTS:
        doc_id = rec.get("DocumentID")
        title = rec.get("title", "")
        if doc_id is not None:
            idx[doc_id] = title
    return idx


def build_passage_index(passages_path: Path):
    """
    Build index: pid -> {
        'document_id': int,
        'passage_id': str,
    }
    where:
      - pid is the internal UUID used in QA generation
      - passage_id is the human-readable ID (e.g. '2.1.3.Guidance.1')
    """
    idx = {}
    if not passages_path.exists():
        raise FileNotFoundError(f"passages_full.jsonl not found at: {passages_path}")
    with passages_path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            pid = rec.get("pid")
            if not pid:
                continue
            idx[pid] = {
                "document_id": rec.get("document_id"),
                "passage_id": rec.get("passage_id"),
            }
    return idx


# ------------------------------------------------------
# Sampling logic
# ------------------------------------------------------
def sample_items_for_method(method: str, items: list, n_per_group: int = 10):
    """
    Sample up to n_per_group items per (persona, reference_type) for a given method.
    """
    samples = []
    print(f"[{method}] Total items available: {len(items)}")

    for persona in PERSONAS:
        for ref_type in REF_TYPES:
            group = [
                it for it in items
                if it.get("persona") == persona
                and it.get("reference_type") == ref_type
            ]
            random.shuffle(group)
            take = min(n_per_group, len(group))
            chosen = group[:take]
            samples.extend(chosen)
            print(
                f"[{method}] Group persona={persona}, ref_type={ref_type}: "
                f"{len(group)} candidates, taking {take}"
            )

    return samples


def main():
    # ---- Build indices for doc titles and passages ----
    print(f"[INFO] Loading passages index from: {PASSAGES_JSONL}")
    passage_index = build_passage_index(PASSAGES_JSONL)
    print(f"[INFO] Passages indexed: {len(passage_index)}")

    doc_title_index = build_doc_title_index()
    print(f"[INFO] Documents indexed: {len(doc_title_index)}")

    # ---- Collect samples across both methods ----
    all_samples = []
    for method in METHODS:
        method_dir = FINAL_DIR / method

        # Load train + dev + test and merge
        method_items = []
        for split in SPLITS:
            split_path = method_dir / f"{split}.jsonl"
            if not split_path.exists():
                raise FileNotFoundError(f"Missing split file: {split_path}")
            print(f"[{method}] Loading {split} items from: {split_path}")
            split_items = load_jsonl(split_path)
            for it in split_items:
                it.setdefault("split", split)
                it.setdefault("method", method)
            method_items.extend(split_items)

        print(f"[{method}] Total items across all splits: {len(method_items)}")

        method_samples = sample_items_for_method(method, method_items, n_per_group=10)
        all_samples.extend(method_samples)

    print(f"[INFO] Total sampled items (before de-dup): {len(all_samples)}")

    # Optional: remove duplicates by qa_id or id
    unique = {}
    for it in all_samples:
        key = it.get("qa_id") or it.get("id")
        if key is None:
            key = (it.get("method"), it.get("question"), it.get("answer"))
        unique[key] = it
    all_samples = list(unique.values())
    print(f"[INFO] Total sampled items (after de-dup): {len(all_samples)}")

    # ---- Enrich with doc title + canonical passage_id ----
    rows = []

    for it in all_samples:
        method = it.get("method")
        split = it.get("split", "")
        persona = it.get("persona", "")
        ref_type = it.get("reference_type", "")

        # IDs and texts
        qa_id = it.get("qa_id") or it.get("id") or ""
        question = it.get("question", "")
        answer = it.get("answer", "")
        src_pid = it.get("source_passage_id", "")  # internal PID
        tgt_pid = it.get("target_passage_id", "")  # internal PID
        src_text = it.get("source_passage_text", "")
        tgt_text = it.get("target_passage_text", "")

        # Passage metadata from passages_full.jsonl
        src_meta = passage_index.get(src_pid, {})
        tgt_meta = passage_index.get(tgt_pid, {})

        src_doc_id = src_meta.get("document_id")
        tgt_doc_id = tgt_meta.get("document_id")

        src_doc_title = doc_title_index.get(src_doc_id, "") if src_doc_id is not None else ""
        tgt_doc_title = doc_title_index.get(tgt_doc_id, "") if tgt_doc_id is not None else ""

        src_passage_canonical = src_meta.get("passage_id", "")
        tgt_passage_canonical = tgt_meta.get("passage_id", "")

        row = {
            # Required by the HTML annotator
            "qa_id": qa_id,
            "question": question,
            "expected_answer": answer,
            "source_text": src_text,
            "target_text": tgt_text,

            # Metadata
            "method": method,
            "split": split,
            "persona": persona,
            "reference_type": ref_type,

            # Internal PIDs
            "source_passage_pid": src_pid,
            "target_passage_pid": tgt_pid,

            # Numeric doc IDs
            "source_doc_id": src_doc_id if src_doc_id is not None else "",
            "target_doc_id": tgt_doc_id if tgt_doc_id is not None else "",

            # Human-facing doc + passage identifiers
            "source_doc_title": src_doc_title,
            "source_passage_id": src_passage_canonical,
            "target_doc_title": tgt_doc_title,
            "target_passage_id": tgt_passage_canonical,
        }

        rows.append(row)

    # ---- Write CSV ----
    fieldnames = [
        "qa_id",
        "question",
        "expected_answer",
        "source_text",
        "target_text",
        "method",
        "split",
        "persona",
        "reference_type",
        "source_passage_pid",
        "target_passage_pid",
        "source_doc_id",
        "target_doc_id",
        "source_doc_title",
        "source_passage_id",
        "target_doc_title",
        "target_passage_id",
    ]

    print(f"[INFO] Writing CSV to: {OUT_CSV}")
    with OUT_CSV.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    print("[INFO] Done.")
    print(f"[INFO] Total rows written: {len(rows)}")


if __name__ == "__main__":
    main()

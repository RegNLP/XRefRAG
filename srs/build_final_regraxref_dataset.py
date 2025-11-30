#!/usr/bin/env python
"""
Build final RegRAG-Xref datasets for DPEL and SCHEMA.

Inputs (fixed paths):

- outputs/judging/curated/DPEL/kept.jsonl
- outputs/judging/curated/SCHEMA/kept.jsonl
    Curated items with:
      - qa_id
      - persona, question, expected_answer
      - debug_context (source/target passages, reference_text, reference_type, etc.)
      - judge_fused, judge_per_judge
      - gen_model (gpt-4o)

- outputs/judging/analysis/concordance_kept_dpel.jsonl
- outputs/judging/analysis/concordance_kept_schema.jsonl
    IR agreement stats per qid

Outputs (70/15/15 splits):

- outputs/final_dataset/DPEL/train.jsonl
- outputs/final_dataset/DPEL/dev.jsonl
- outputs/final_dataset/DPEL/test.jsonl
- outputs/final_dataset/SCHEMA/train.jsonl
- outputs/final_dataset/SCHEMA/dev.jsonl
- outputs/final_dataset/SCHEMA/test.jsonl

Each final item:

{
  "id": "SCHEMA_000123",
  "method": "SCHEMA",
  "split": "train",

  "persona": "Basic",
  "question": "...",
  "answer": "...",

  "source_passage_id": "...",
  "target_passage_id": "...",
  "source_passage_text": "...",
  "target_passage_text": "...",
  "source_doc_id": "COBS_2",      # optional
  "target_doc_id": "COBS_3",      # optional

  "reference_text": "1.2.7",
  "reference_type": "External",

  "generator_model": "gpt-4o",
  "pipeline_version": "SCHEMA_v1.1",
  "created_at": "2025-11-23",

  "judge_passed": true,
  "judge_final_score": 9,
  "judge_subscores": {
    "realism": 2,
    "dual_use": 3,
    "correctness": 4
  },
  "judge_fused": { ... },
  "judge_per_judge": [ ... ],

  "ir_agreement": { ... }
}
"""

import json
import random
from pathlib import Path
from typing import Dict, Any, List, Tuple


# ---------------- CONFIG ----------------

# Input paths
CURATED_DPEL = Path("outputs/judging/curated/DPEL/kept.jsonl")
CURATED_SCHEMA = Path("outputs/judging/curated/SCHEMA/kept.jsonl")

CONCORDANCE_DPEL = Path("outputs/judging/analysis/concordance_kept_dpel.jsonl")
CONCORDANCE_SCHEMA = Path("outputs/judging/analysis/concordance_kept_schema.jsonl")

# Output root
OUT_ROOT = Path("outputs/final_dataset")

# Metadata
GENERATOR_DEFAULT = "gpt-4o"
PIPELINE_VERSION = {
    "DPEL": "DPEL_v1.1",
    "SCHEMA": "SCHEMA_v1.1",
}
CREATED_AT = "2025-11-23"

# IR agreement logic:
# We now follow the "After IR agreement" stage:
#   drop only items flagged as low_concordance_any == True
#   keep everything else.
DROP_LOW_CONCORDANCE = True

# Split ratios
TRAIN_RATIO = 0.70
DEV_RATIO = 0.15
TEST_RATIO = 0.15

RANDOM_SEED = 42


# ---------------- HELPERS ----------------

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def write_jsonl(path: Path, items: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for obj in items:
            f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def normalize_persona(raw: str) -> str:
    """Map 'basic'/'professional' etc. to 'Basic'/'Professional'."""
    if not raw:
        return raw
    p = raw.strip().lower()
    if p.startswith("basic"):
        return "Basic"
    if p.startswith("prof"):
        return "Professional"
    return raw.strip().title()


def assign_ids(items: List[Dict[str, Any]], method: str) -> None:
    """
    Assign IDs like DPEL_000001, SCHEMA_000001.
    Only sets 'id' if it is missing.
    """
    existing = {obj.get("id") for obj in items if obj.get("id")}
    counter = 1
    for obj in items:
        if obj.get("id"):
            continue
        while True:
            candidate = f"{method}_{counter:06d}"
            counter += 1
            if candidate not in existing:
                obj["id"] = candidate
                existing.add(candidate)
                break


def split_items(
    items: List[Dict[str, Any]],
    method: str,
    train_ratio: float,
    dev_ratio: float,
    test_ratio: float,
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    """Shuffle & split into train/dev/test, filling method & split."""
    assert abs(train_ratio + dev_ratio + test_ratio - 1.0) < 1e-6, "Ratios must sum to 1.0"

    random.shuffle(items)
    n = len(items)
    n_train = int(round(n * train_ratio))
    n_dev = int(round(n * dev_ratio))
    n_test = n - n_train - n_dev

    train_items = items[:n_train]
    dev_items = items[n_train:n_train + n_dev]
    test_items = items[n_train + n_dev:]

    for obj in train_items:
        obj["method"] = method
        obj["split"] = "train"
    for obj in dev_items:
        obj["method"] = method
        obj["split"] = "dev"
    for obj in test_items:
        obj["method"] = method
        obj["split"] = "test"

    return train_items, dev_items, test_items


def build_final_for_method(
    method: str,
    curated_path: Path,
    concordance_path: Path,
    out_dir: Path,
) -> None:
    print(f"[{method}] Loading curated items from {curated_path}")
    curated_items = read_jsonl(curated_path)

    curated_by_id: Dict[str, Dict[str, Any]] = {}
    for obj in curated_items:
        qa_id = obj.get("qa_id")
        if qa_id is None:
            continue
        curated_by_id[qa_id] = obj

    print(f"[{method}] Loaded {len(curated_by_id)} curated items with qa_id")

    print(f"[{method}] Loading concordance from {concordance_path}")
    concordance_items = read_jsonl(concordance_path)

    final_items: List[Dict[str, Any]] = []
    missing_qids: List[str] = []

    for c in concordance_items:
        qid = c.get("qid")
        if qid is None:
            continue

        low_conc = c.get("low_concordance_any", False)

        # IR agreement filter: drop only low-concordance items
        if DROP_LOW_CONCORDANCE and low_conc:
            continue

        qa_obj = curated_by_id.get(qid)
        if qa_obj is None:
            missing_qids.append(qid)
            continue

        dctx = qa_obj.get("debug_context", {}) or {}
        persona_raw = qa_obj.get("persona")
        persona_norm = normalize_persona(persona_raw) if persona_raw else None

        item: Dict[str, Any] = {}

        # Core QA fields
        item["persona"] = persona_norm
        item["question"] = qa_obj.get("question")
        item["answer"] = qa_obj.get("expected_answer")

        # Source / target passages
        item["source_passage_id"] = dctx.get("source_passage_id")
        item["target_passage_id"] = dctx.get("target_passage_id")
        item["source_passage_text"] = dctx.get("source_text")
        item["target_passage_text"] = dctx.get("target_text")

        # Optional doc IDs
        if "source_doc_id" in dctx:
            item["source_doc_id"] = dctx["source_doc_id"]
        if "target_doc_id" in dctx:
            item["target_doc_id"] = dctx["target_doc_id"]

        # Cross-reference info
        item["reference_text"] = dctx.get("reference_text")
        item["reference_type"] = dctx.get("reference_type")

        # Generator & metadata
        gen_model = qa_obj.get("gen_model", GENERATOR_DEFAULT)
        item["generator_model"] = gen_model
        item["pipeline_version"] = PIPELINE_VERSION.get(method, None)
        item["created_at"] = CREATED_AT

        # LLM-as-judge info
        jf = qa_obj.get("judge_fused") or {}
        item["judge_passed"] = jf.get("passed")
        item["judge_final_score"] = jf.get("final_score")
        item["judge_subscores"] = jf.get("subscores")
        if "judge_fused" in qa_obj:
            item["judge_fused"] = qa_obj["judge_fused"]
        if "judge_per_judge" in qa_obj:
            item["judge_per_judge"] = qa_obj["judge_per_judge"]

        # IR agreement info
        item["ir_agreement"] = {
            "num_rel": c.get("num_rel"),
            "num_methods_hit_any": c.get("num_methods_hit_any"),
            "num_methods_hit_all": c.get("num_methods_hit_all"),
            "high_concordance_any": c.get("high_concordance_any"),
            "low_concordance_any": c.get("low_concordance_any"),
            "k": c.get("k"),
            "methods": c.get("methods"),
        }

        final_items.append(item)

    print(f"[{method}] Final items after IR filter + join: {len(final_items)}")
    if missing_qids:
        print(f"[{method}] WARNING: {len(missing_qids)} qids missing in curated. "
              f"Example: {missing_qids[:5]}")

    # Assign IDs and split
    assign_ids(final_items, method=method)
    train_items, dev_items, test_items = split_items(
        final_items,
        method=method,
        train_ratio=TRAIN_RATIO,
        dev_ratio=DEV_RATIO,
        test_ratio=TEST_RATIO,
    )

    # Write outputs
    out_dir.mkdir(parents=True, exist_ok=True)
    write_jsonl(out_dir / "train.jsonl", train_items)
    write_jsonl(out_dir / "dev.jsonl", dev_items)
    write_jsonl(out_dir / "test.jsonl", test_items)

    print(f"[{method}] Train: {len(train_items)}")
    print(f"[{method}] Dev:   {len(dev_items)}")
    print(f"[{method}] Test:  {len(test_items)}")
    print(f"[{method}] Written to {out_dir.resolve()}")
    print("-" * 60)


# ---------------- MAIN ----------------

def main():
    random.seed(RANDOM_SEED)

    # DPEL
    build_final_for_method(
        method="DPEL",
        curated_path=CURATED_DPEL,
        concordance_path=CONCORDANCE_DPEL,
        out_dir=OUT_ROOT / "DPEL",
    )

    # SCHEMA
    build_final_for_method(
        method="SCHEMA",
        curated_path=CURATED_SCHEMA,
        concordance_path=CONCORDANCE_SCHEMA,
        out_dir=OUT_ROOT / "SCHEMA",
    )


if __name__ == "__main__":
    main()

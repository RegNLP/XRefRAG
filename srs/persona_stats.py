#!/usr/bin/env python3
import json
import argparse
from collections import Counter

def load_items(path):
    """Load items from .json or .jsonl."""
    if path.endswith(".jsonl"):
        items = []
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                items.append(json.loads(line))
        return items
    else:
        # assume a standard JSON file (list of objects)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

def build_persona_map(map_path, persona_key="persona", id_key="qa_id"):
    """
    Build a mapping from id_key -> persona using a 'source' file
    (e.g. curated/kept.jsonl where persona is stored).
    """
    if not map_path:
        return {}

    items = load_items(map_path)
    persona_map = {}
    for obj in items:
        qid = obj.get(id_key)
        persona = obj.get(persona_key)
        if qid is not None and persona is not None:
            persona_map[str(qid)] = persona
    return persona_map

def split_by_stage(items, stage):
    """
    Split items into kept vs eliminated for a given stage.

    - stage == 'none':
        all items are 'kept', none eliminated

    - stage == 'ir':
        eliminated if low_concordance_any == True

    - stage == 'answer':
        eliminated if low_concordance_success == True
    """
    if stage == "none":
        return items, [], len(items), 0

    kept = []
    eliminated = []

    if stage == "ir":
        for obj in items:
            ir_low = bool(obj.get("low_concordance_any"))
            if ir_low:
                eliminated.append(obj)
            else:
                kept.append(obj)

    elif stage == "answer":
        for obj in items:
            ans_low = bool(obj.get("low_concordance_success"))
            if ans_low:
                eliminated.append(obj)
            else:
                kept.append(obj)
    else:
        kept = items
        eliminated = []

    return kept, eliminated, len(kept), len(eliminated)

def compute_persona_stats(
    items,
    persona_key="persona",
    id_key="qa_id",
    persona_map=None
):
    counter = Counter()
    for obj in items:
        persona = None

        # 1) Try local persona field
        if persona_key in obj and obj[persona_key] is not None:
            persona = obj[persona_key]

        # 2) If missing, try lookup from persona_map using id_key
        elif persona_map is not None and id_key in obj:
            persona = persona_map.get(str(obj[id_key]))

        # 3) Fallback
        if persona is None:
            persona = "UNKNOWN"

        counter[persona] += 1

    total = sum(counter.values())
    return counter, total

def main():
    parser = argparse.ArgumentParser(
        description=(
            "Compute persona counts and percentages from a JSON/JSONL dataset.\n"
            "If persona is missing in the file, you can provide a --persona-source "
            "file (e.g. curated kept.jsonl) so the script looks up persona by id.\n"
            "Optionally, use --stage to see how many QAs are kept vs eliminated "
            "at IR or answer stages."
        )
    )
    parser.add_argument(
        "input_path",
        help="Path to input file (.json or .jsonl) containing items."
    )
    parser.add_argument(
        "--key",
        default="persona",
        help="Field name for persona in the files (default: 'persona')."
    )
    parser.add_argument(
        "--id-key",
        default="qa_id",
        help="Field name for the item id in the INPUT file (default: 'qa_id')."
    )
    parser.add_argument(
        "--persona-source",
        help=(
            "Optional: path to a file (e.g. curated kept.jsonl) that has both id and persona. "
            "This file is assumed to use 'qa_id' as its id field."
        )
    )
    parser.add_argument(
        "--stage",
        choices=["none", "ir", "answer"],
        default="none",
        help=(
            "Stage filter:\n"
            "  none   - no filtering, all items are 'kept'\n"
            "  ir     - eliminated if low_concordance_any == True\n"
            "  answer - eliminated if low_concordance_success == True"
        )
    )
    args = parser.parse_args()

    # Build persona map from source file (if given)
    persona_map = None
    if args.persona_source:
        persona_map = build_persona_map(
            args.persona_source,
            persona_key=args.key,
            id_key="qa_id",  # persona source uses qa_id
        )

    # Load items from the main file
    items = load_items(args.input_path)
    total_all = len(items)

    # Split kept vs eliminated according to stage
    kept_items, elim_items, kept_count, elim_count = split_by_stage(items, args.stage)

    # Compute persona stats on kept set
    counter, total_kept = compute_persona_stats(
        kept_items,
        persona_key=args.key,
        id_key=args.id_key,
        persona_map=persona_map,
    )

    # Print stage summary
    print(f"Total items (before stage filter): {total_all}")
    if args.stage != "none":
        if total_all > 0:
            kept_pct = kept_count / total_all * 100.0
            elim_pct = elim_count / total_all * 100.0
        else:
            kept_pct = elim_pct = 0.0
        print(f"Stage: {args.stage}")
        print(f"  Kept:       {kept_count} ({kept_pct:.2f}%)")
        print(f"  Eliminated: {elim_count} ({elim_pct:.2f}%)")
    else:
        print("Stage: none (no IR/answer filtering applied)")

    print()
    print(f"Persona stats for KEPT set:")
    print(f"Total kept items: {total_kept}\n")
    print(f"{'Persona':20s} {'Count':>10s} {'Percent':>10s}")
    print("-" * 42)

    if total_kept == 0:
        return

    for persona, count in counter.most_common():
        pct = (count / total_kept) * 100
        print(f"{persona:20s} {count:10d} {pct:9.2f}%")

if __name__ == "__main__":
    main()

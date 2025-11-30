#!/usr/bin/env python3
# curate_from_judgements.py
# -*- coding: utf-8 -*-

import argparse, json, os, sys, csv
from typing import Any, Dict, List, Optional

def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except Exception:
                continue
    return rows

def write_jsonl(path: str, rows: List[Dict[str, Any]]) -> None:
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

def ensure_dir(d: str) -> None:
    os.makedirs(d, exist_ok=True)

def main():
    ap = argparse.ArgumentParser(
        description="Split judged QAs into per-method kept/eliminated datasets."
    )
    ap.add_argument("--judgments", required=True, help="Path to ensemble judgments JSONL.")
    ap.add_argument("--gen_inputs", nargs="+", required=True,
                    help="One or more generation JSONL files (DPEL/SCHEMA).")
    ap.add_argument("--out_dir", required=True,
                    help="Output root directory (will create per-method subdirs).")
    ap.add_argument("--include_judge_payload", action="store_true",
                    help="If set, attach {'judge_fused', 'judge_per_judge'} into each QA row.")
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    # 1) Load judgments → map by qa_id
    jrows = load_jsonl(args.judgments)
    J: Dict[str, Dict[str, Any]] = {}
    for j in jrows:
        qa_id = j.get("qa_id")
        if not qa_id:
            continue
        J[qa_id] = j

    if args.verbose:
        print(f"[info] loaded judgments: {len(J)} (unique qa_id) from {args.judgments}", flush=True)

    # 2) Load all generated rows → preserve full records for output
    all_gen: Dict[str, Dict[str, Any]] = {}
    source_files: Dict[str, str] = {}
    for gpath in args.gen_inputs:
        rows = load_jsonl(gpath)
        if args.verbose:
            print(f"[info] loaded generated: {len(rows)} from {gpath}", flush=True)
        for r in rows:
            qa_id = r.get("qa_id")
            if not qa_id:
                continue
            all_gen[qa_id] = r
            source_files[qa_id] = gpath

    # 3) Iterate judgments, split by method & pass/fail
    kept_by_method: Dict[str, List[Dict[str, Any]]] = {}
    elim_by_method: Dict[str, List[Dict[str, Any]]] = {}

    missing_in_gen = 0
    for qa_id, j in J.items():
        gen = all_gen.get(qa_id)
        if not gen:
            missing_in_gen += 1
            continue
        method = gen.get("method", "UNKNOWN")
        fused = j.get("fused") or {}
        passed = bool(fused.get("passed"))

        row_out = dict(gen)  # copy the full QA row
        if args.include_judge_payload:
            row_out["judge_fused"] = fused
            row_out["judge_per_judge"] = j.get("per_judge")

        (kept_by_method if passed else elim_by_method).setdefault(method, []).append(row_out)

    if args.verbose and missing_in_gen:
        print(f"[warn] judgments referencing {missing_in_gen} qa_id not found in provided gen_inputs", flush=True)

    # 4) Write per-method kept/eliminated JSONLs + summary tables
    ensure_dir(args.out_dir)
    summary = {
        "by_method": {},
        "by_persona": {},
        "totals": {"judged": len(J), "kept": 0, "eliminated": 0}
    }

    # Persona-level aggregation
    def add_persona_counts(rows: List[Dict[str, Any]], d: Dict[str, Dict[str, int]], field: str):
        for r in rows:
            p = r.get("persona", "unknown")
            d.setdefault(p, {"kept": 0, "eliminated": 0, "total": 0})
            d[p][field] += 1
            d[p]["total"] += 1

    for method in sorted(set(list(kept_by_method.keys()) + list(elim_by_method.keys()))):
        kept = kept_by_method.get(method, [])
        elim = elim_by_method.get(method, [])

        method_dir = os.path.join(args.out_dir, method.lower())
        ensure_dir(method_dir)
        write_jsonl(os.path.join(method_dir, "kept.jsonl"), kept)
        write_jsonl(os.path.join(method_dir, "eliminated.jsonl"), elim)

        summary["by_method"][method] = {
            "kept": len(kept),
            "eliminated": len(elim),
            "total": len(kept) + len(elim),
            "pass_rate": round((len(kept) / max(1, (len(kept) + len(elim)))) * 100.0, 2)
        }

        add_persona_counts(kept, summary["by_persona"], "kept")
        add_persona_counts(elim, summary["by_persona"], "eliminated")

        summary["totals"]["kept"] += len(kept)
        summary["totals"]["eliminated"] += len(elim)

    # 5) Write summary JSON + CSVs
    with open(os.path.join(args.out_dir, "summary.json"), "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    # method-level CSV
    with open(os.path.join(args.out_dir, "summary_by_method.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["method", "kept", "eliminated", "total", "pass_rate_percent"])
        for m, s in summary["by_method"].items():
            w.writerow([m, s["kept"], s["eliminated"], s["total"], s["pass_rate"]])

    # persona-level CSV
    with open(os.path.join(args.out_dir, "summary_by_persona.csv"), "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["persona", "kept", "eliminated", "total", "pass_rate_percent"])
        for p, s in summary["by_persona"].items():
            rate = round((s["kept"] / max(1, s["total"])) * 100.0, 2)
            w.writerow([p, s["kept"], s["eliminated"], s["total"], rate])

    # Small console summary
    print("\n=== Curated outputs ===")
    for m in sorted(summary["by_method"].keys()):
        s = summary["by_method"][m]
        print(f" {m:7s} | kept={s['kept']:5d}  elim={s['eliminated']:5d}  total={s['total']:5d}  pass%={s['pass_rate']:5.1f}")

    print("\n[ok] Wrote:")
    print(f" - {os.path.join(args.out_dir, '<method>/kept.jsonl')} & eliminated.jsonl")
    print(f" - {os.path.join(args.out_dir, 'summary.json')}")
    print(f" - {os.path.join(args.out_dir, 'summary_by_method.csv')}")
    print(f" - {os.path.join(args.out_dir, 'summary_by_persona.csv')}")
    if args.include_judge_payload:
        print(" (judge payload embedded in kept/eliminated rows)")

if __name__ == "__main__":
    main()

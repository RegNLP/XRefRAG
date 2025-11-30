#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyze ensemble-judgment results with deep per-method breakdowns.

Inputs:
- judgments JSONL from judge_qas_ensemble.py (per line structure):
  {
    "qa_id": "...",
    "method": "DPEL|SCHEMA",
    "persona": "professional|basic",
    "reference_type": "Internal|External|NotDefined|None",
    "source_passage_id": "...",
    "target_passage_id": "...",
    "per_judge": [
        {"model": "...", "seed": 13, "tag": "...", "result": {
            "passed": true/false,
            "final_score": int,
            "subscores": {"realism": int, "dual_use": int, "correctness": int},
            "reasons": [...],
            "flags": {"hard_gate_fail": bool, "question_has_citation": bool}
        }},
        ...
    ],
    "fused": {
        "passed": true/false,
        "final_score": int,
        "subscores": {"realism": int, "dual_use": int, "correctness": int},
        "reasons": [...],
        "ensemble": {"n": 3}
    }
  }

Optional enrichment:
- One or more generation JSONL files (DPEL/SCHEMA) with debug_context to derive:
  source_item_type, target_item_type, answer_spans, etc.

Outputs:
- Console summary
- CSVs in --out_dir:
    method_stats.csv
    method_persona_stats.csv
    method_ref_type_stats.csv
    method_dual_use_hist.csv
    method_hard_gate_flags.csv
    method_reasons_top.csv
    model_level_agreement.csv
    (optional if enriched)
    method_itemtype_stats.csv
"""

import argparse
import collections
import csv
import json
import math
import os
import statistics
from typing import Any, Dict, List, Optional, Tuple, DefaultDict

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

def safe_mean(nums: List[float]) -> float:
    return round(float(statistics.mean(nums)), 3) if nums else 0.0

def safe_median(nums: List[float]) -> float:
    return round(float(statistics.median(nums)), 3) if nums else 0.0

def safe_std(nums: List[float]) -> float:
    if len(nums) < 2:
        return 0.0
    return round(float(statistics.pstdev(nums)), 3)

def iqr(nums: List[float]) -> float:
    if not nums:
        return 0.0
    qs = sorted(nums)
    n = len(qs)
    q1 = statistics.median(qs[:n//2])
    if n % 2 == 0:
        q3 = statistics.median(qs[n//2:])
    else:
        q3 = statistics.median(qs[n//2+1:])
    return round(float(q3 - q1), 3)

def ensure_dir(d: str):
    os.makedirs(d, exist_ok=True)

def enrich_lookup(gen_paths: List[str]) -> Dict[str, Dict[str, Any]]:
    """Return qa_id -> enrichment fields from generation files if available."""
    if not gen_paths:
        return {}
    out = {}
    for p in gen_paths:
        for r in load_jsonl(p):
            qid = r.get("qa_id")
            if not qid:
                continue
            dbg = r.get("debug_context") or {}
            out[qid] = {
                "source_item_type": dbg.get("source_item_type"),
                "target_item_type": dbg.get("target_item_type"),
                "answer_span_types": ",".join(sorted({(s.get("type") or "NA") for s in (dbg.get("answer_spans") or [])})),
            }
    return out

def tally_reasons(per_judge_results: List[Dict[str, Any]]) -> Dict[str, int]:
    c = collections.Counter()
    for j in per_judge_results:
        res = j.get("result") or {}
        for r in (res.get("reasons") or []):
            c[str(r)] += 1
    return dict(c.most_common())

def per_model_agreement(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Compute model-level aggregates: pass rate, mean +/- stdev scores, unanimity rate, majority margin.
    """
    by_model: DefaultDict[str, Dict[str, List]] = collections.defaultdict(lambda: {
        "finals": [], "realism": [], "dual": [], "correct": [], "pass": 0, "n": 0
    })
    unanimity_yes = 0
    unanimity_no = 0
    majority_2to1 = 0
    total_items = 0

    for r in rows:
        pjs = r.get("per_judge") or []
        total_items += 1 if pjs else 0

        # unanimity & majority
        votes = [bool((j.get("result") or {}).get("passed")) for j in pjs]
        if votes:
            yes = sum(1 for v in votes if v)
            no = len(votes) - yes
            if yes == len(votes) or no == len(votes):
                if yes > 0:
                    unanimity_yes += 1
                else:
                    unanimity_no += 1
            elif max(yes, no) == 2 and len(votes) == 3:
                majority_2to1 += 1

        # per model aggregates
        for j in pjs:
            model = j.get("model") or "unknown"
            res = j.get("result") or {}
            by_model[model]["n"] += 1
            by_model[model]["pass"] += 1 if res.get("passed") else 0
            by_model[model]["finals"].append(int(res.get("final_score", 0)))
            ss = res.get("subscores") or {}
            by_model[model]["realism"].append(int(ss.get("realism", 0)))
            by_model[model]["dual"].append(int(ss.get("dual_use", 0)))
            by_model[model]["correct"].append(int(ss.get("correctness", 0)))

    rows_out = []
    for m, agg in by_model.items():
        rows_out.append({
            "model": m,
            "n_judgments": agg["n"],
            "pass_rate": round( (agg["pass"] / agg["n"])*100.0, 2) if agg["n"] else 0.0,
            "final_mean": safe_mean(agg["finals"]),
            "final_median": safe_median(agg["finals"]),
            "final_std": safe_std(agg["finals"]),
            "final_iqr": iqr(agg["finals"]),
            "realism_mean": safe_mean(agg["realism"]),
            "dual_mean": safe_mean(agg["dual"]),
            "correct_mean": safe_mean(agg["correct"]),
        })

    rows_out.append({
        "model": "__ensemble_level__",
        "n_judgments": total_items,
        "pass_rate": "",
        "final_mean": "",
        "final_median": "",
        "final_std": "",
        "final_iqr": "",
        "realism_mean": "",
        "dual_mean": "",
        "correct_mean": "",
        "unanimity_yes": unanimity_yes,
        "unanimity_no": unanimity_no,
        "majority_2to1": majority_2to1
    })
    return rows_out

def write_csv(path: str, rows: List[Dict[str, Any]]):
    ensure_dir(os.path.dirname(os.path.abspath(path)))
    if not rows:
        with open(path, "w", newline="", encoding="utf-8") as f:
            f.write("")
        return
    cols = sorted({k for r in rows for k in r.keys()})
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow(r)

def main():
    ap = argparse.ArgumentParser(description="Deep stats for RegRAG-Xref ensemble judgments.")
    ap.add_argument("--judgments", required=True, help="Path to ensemble judgments JSONL.")
    ap.add_argument("--gen_inputs", nargs="*", default=[],
                    help="Optional generation JSONL(s) to enrich with item types.")
    ap.add_argument("--out_dir", required=True, help="Directory to write CSVs.")
    ap.add_argument("--print_top_reasons", type=int, default=15)
    args = ap.parse_args()

    ensure_dir(args.out_dir)
    rows = load_jsonl(args.judgments)
    enrich = enrich_lookup(args.gen_inputs)

    # Buckets
    by_method: DefaultDict[str, List[Dict[str, Any]]] = collections.defaultdict(list)
    by_method_persona: DefaultDict[Tuple[str, str], List[Dict[str, Any]]] = collections.defaultdict(list)
    by_method_ref: DefaultDict[Tuple[str, str], List[Dict[str, Any]]] = collections.defaultdict(list)
    by_method_itemtype: DefaultDict[Tuple[str, str, str], List[Dict[str, Any]]] = collections.defaultdict(list)

    # Collect per-method stats inputs
    for r in rows:
        meth = r.get("method") or "UNKNOWN"
        persona = r.get("persona") or "UNKNOWN"
        ref_type = r.get("reference_type") or "UNKNOWN"
        fused = r.get("fused") or {}
        subs = fused.get("subscores") or {}
        per_judge = r.get("per_judge") or []

        rec = {
            "passed": bool(fused.get("passed")),
            "final": int(fused.get("final_score", 0)),
            "realism": int(subs.get("realism", 0)),
            "dual": int(subs.get("dual_use", 0)),
            "correct": int(subs.get("correctness", 0)),
            "per_judge": per_judge
        }
        by_method[meth].append(rec)
        by_method_persona[(meth, persona)].append(rec)
        by_method_ref[(meth, ref_type)].append(rec)

        # Attach enrichment if available
        qid = r.get("qa_id")
        ei = enrich.get(qid) if qid else None
        if ei:
            by_method_itemtype[(meth, ei.get("source_item_type") or "", ei.get("target_item_type") or "")].append(rec)

    # 1) Per-method stats
    method_rows = []
    dual_hist_rows = []
    hard_flags_rows = []
    reasons_rows = []

    for meth, lst in by_method.items():
        finals = [x["final"] for x in lst]
        realism = [x["realism"] for x in lst]
        dual = [x["dual"] for x in lst]
        correct = [x["correct"] for x in lst]
        passed = sum(1 for x in lst if x["passed"])
        total = len(lst)
        method_rows.append({
            "method": meth,
            "total": total,
            "passed": passed,
            "pass_rate_%": round((passed/total)*100.0, 2) if total else 0.0,
            "final_mean": safe_mean(finals), "final_median": safe_median(finals),
            "final_std": safe_std(finals), "final_iqr": iqr(finals),
            "realism_mean": safe_mean(realism), "dual_mean": safe_mean(dual), "correct_mean": safe_mean(correct),
        })

        # dual_use histogram
        hist = collections.Counter(dual)
        for k in range(0, 5):
            dual_hist_rows.append({"method": meth, "dual_use": k, "count": hist.get(k, 0)})

        # hard-gate flags & reasons (from per_judge raw)
        all_pj = []
        for x in lst:
            all_pj.extend(x["per_judge"])
        # flags
        flags_counter = collections.Counter()
        for pj in all_pj:
            res = pj.get("result") or {}
            flg = res.get("flags") or {}
            for name, val in flg.items():
                if bool(val):
                    flags_counter[name] += 1
        for name, cnt in flags_counter.most_common():
            hard_flags_rows.append({"method": meth, "flag": name, "count": cnt})

        # reasons
        top = tally_reasons(all_pj)
        for reason, cnt in top.items():
            reasons_rows.append({"method": meth, "reason": reason, "count": cnt})

    # 2) Per method × persona
    m_p_rows = []
    for (meth, persona), lst in by_method_persona.items():
        finals = [x["final"] for x in lst]
        passed = sum(1 for x in lst if x["passed"])
        total = len(lst)
        m_p_rows.append({
            "method": meth, "persona": persona,
            "total": total, "passed": passed,
            "pass_rate_%": round((passed/total)*100.0, 2) if total else 0.0,
            "final_mean": safe_mean(finals), "final_median": safe_median(finals),
        })

    # 3) Per method × reference_type
    m_r_rows = []
    for (meth, ref_type), lst in by_method_ref.items():
        finals = [x["final"] for x in lst]
        passed = sum(1 for x in lst if x["passed"])
        total = len(lst)
        m_r_rows.append({
            "method": meth, "reference_type": ref_type,
            "total": total, "passed": passed,
            "pass_rate_%": round((passed/total)*100.0, 2) if total else 0.0,
            "final_mean": safe_mean(finals), "final_median": safe_median(finals),
        })

    # 4) Per-model agreement / dispersion (from judgments, not fused)
    model_agree_rows = per_model_agreement(rows)

    # 5) Optional: per method × (source_item_type, target_item_type)
    m_itemtype_rows = []
    if any(by_method_itemtype.values()):
        for (meth, s_it, t_it), lst in by_method_itemtype.items():
            finals = [x["final"] for x in lst]
            duals = [x["dual"] for x in lst]
            passed = sum(1 for x in lst if x["passed"])
            total = len(lst)
            m_itemtype_rows.append({
                "method": meth,
                "source_item_type": s_it or "",
                "target_item_type": t_it or "",
                "total": total,
                "passed": passed,
                "pass_rate_%": round((passed/total)*100.0, 2) if total else 0.0,
                "final_mean": safe_mean(finals),
                "dual_mean": safe_mean(duals),
            })

    # Write CSVs
    write_csv(os.path.join(args.out_dir, "method_stats.csv"), method_rows)
    write_csv(os.path.join(args.out_dir, "method_persona_stats.csv"), m_p_rows)
    write_csv(os.path.join(args.out_dir, "method_ref_type_stats.csv"), m_r_rows)
    write_csv(os.path.join(args.out_dir, "method_dual_use_hist.csv"), dual_hist_rows)
    write_csv(os.path.join(args.out_dir, "model_level_agreement.csv"), model_agree_rows)
    write_csv(os.path.join(args.out_dir, "method_hard_gate_flags.csv"), hard_flags_rows)
    write_csv(os.path.join(args.out_dir, "method_reasons_top.csv"), reasons_rows)
    if m_itemtype_rows:
        write_csv(os.path.join(args.out_dir, "method_itemtype_stats.csv"), m_itemtype_rows)

    # Console summary
    print("\n================= SUMMARY (by method) =================")
    for r in method_rows:
        print(f"{r['method']:>7} | n={r['total']:4d} pass%={r['pass_rate_%']:5.1f} | "
              f"final μ/σ/med/IQR = {r['final_mean']}/{r['final_std']}/{r['final_median']}/{r['final_iqr']} | "
              f"dual μ={r['dual_mean']}")

    print("\n============= UNANIMITY / AGREEMENT (ensemble) =============")
    for rr in model_agree_rows:
        if rr["model"] == "__ensemble_level__":
            print(f"unanimity_yes={rr['unanimity_yes']} unanimity_no={rr['unanimity_no']} majority_2to1={rr['majority_2to1']}")
            break

    print(f"\n[ok] Wrote CSVs → {args.out_dir}")

if __name__ == "__main__":
    main()

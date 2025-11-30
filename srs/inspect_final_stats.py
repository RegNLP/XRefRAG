#!/usr/bin/env python
"""
inspect_final_stats.py

Inspect statistics of the *final* RegRAG-Xref datasets produced under:

    outputs/final_dataset/
      DPEL/
        train.jsonl
        dev.jsonl
        test.jsonl
      SCHEMA/
        train.jsonl
        dev.jsonl
        test.jsonl

Stats covered (per method: DPEL, SCHEMA):

1. Core sanity + size stats
2. Question / answer / passage length stats
3. Persona-focused stats
4. Judgment / quality stats (LLM-as-judge)
5. IR agreement stats
6. Document coverage stats
7. Cross-ref specific stats
9. JSON summary written to outputs/final_dataset/stats_summary.json
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Tuple, Optional
import statistics as stats
from collections import Counter, defaultdict


# Root for final dataset
FINAL_ROOT = Path("outputs/final_dataset")
METHODS = ["DPEL", "SCHEMA"]
SPLITS = ["train", "dev", "test"]

SUMMARY_JSON_PATH = FINAL_ROOT / "stats_summary.json"


# ---------- I/O helpers ----------

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    items: List[Dict[str, Any]] = []
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            items.append(json.loads(line))
    return items


def load_method_items(method: str) -> List[Dict[str, Any]]:
    """Load all items (train+dev+test) for a method and attach split if needed."""
    all_items: List[Dict[str, Any]] = []
    method_dir = FINAL_ROOT / method
    for split in SPLITS:
        split_path = method_dir / f"{split}.jsonl"
        split_items = read_jsonl(split_path)
        for obj in split_items:
            # Ensure split is present and correct
            obj["split"] = obj.get("split", split)
        all_items.extend(split_items)
    return all_items


# ---------- small utilities ----------

def word_count(text: Optional[str]) -> int:
    if not text:
        return 0
    return len(str(text).split())


def safe_mean(values: List[float]) -> Optional[float]:
    return float(stats.mean(values)) if values else None


def safe_median(values: List[float]) -> Optional[float]:
    return float(stats.median(values)) if values else None


def basic_length_stats(values: List[int]) -> Dict[str, Optional[float]]:
    """Return min/max/mean/median for a list of ints. Empty list → None."""
    if not values:
        return {"min": None, "max": None, "mean": None, "median": None}
    return {
        "min": int(min(values)),
        "max": int(max(values)),
        "mean": float(stats.mean(values)),
        "median": float(stats.median(values)),
    }


# ---------- 1. Core sanity + size stats ----------

def compute_core_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    total = len(items)

    # Split counts
    split_counts = Counter(obj.get("split", "unknown") for obj in items)

    # Persona counts (overall and split x persona)
    persona_counts = Counter(obj.get("persona") for obj in items)
    split_persona_counts = defaultdict(lambda: Counter())
    for obj in items:
        split = obj.get("split", "unknown")
        persona = obj.get("persona")
        split_persona_counts[split][persona] += 1

    # Missing field counts
    missing_source_text = sum(1 for obj in items if not obj.get("source_passage_text"))
    missing_target_text = sum(1 for obj in items if not obj.get("target_passage_text"))
    missing_ref_text = sum(1 for obj in items if not obj.get("reference_text"))
    missing_ref_type = sum(1 for obj in items if not obj.get("reference_type"))
    missing_source_doc = sum(1 for obj in items if "source_doc_id" not in obj or not obj.get("source_doc_id"))
    missing_target_doc = sum(1 for obj in items if "target_doc_id" not in obj or not obj.get("target_doc_id"))

    # Reference type distribution
    ref_type_counts = Counter(obj.get("reference_type") for obj in items)

    return {
        "total_items": total,
        "split_counts": dict(split_counts),
        "persona_counts": dict(persona_counts),
        "split_persona_counts": {s: dict(c) for s, c in split_persona_counts.items()},
        "missing_fields": {
            "source_passage_text": missing_source_text,
            "target_passage_text": missing_target_text,
            "reference_text": missing_ref_text,
            "reference_type": missing_ref_type,
            "source_doc_id": missing_source_doc,
            "target_doc_id": missing_target_doc,
        },
        "reference_type_counts": dict(ref_type_counts),
    }


# ---------- 2. Length stats ----------

def compute_length_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    q_lengths: List[int] = []
    a_lengths: List[int] = []
    src_lengths: List[int] = []
    tgt_lengths: List[int] = []

    for obj in items:
        if obj.get("question"):
            q_lengths.append(word_count(obj.get("question")))
        if obj.get("answer"):
            a_lengths.append(word_count(obj.get("answer")))
        if obj.get("source_passage_text"):
            src_lengths.append(word_count(obj.get("source_passage_text")))
        if obj.get("target_passage_text"):
            tgt_lengths.append(word_count(obj.get("target_passage_text")))

    return {
        "question_length": basic_length_stats(q_lengths),
        "answer_length": basic_length_stats(a_lengths),
        "source_passage_length": basic_length_stats(src_lengths),
        "target_passage_length": basic_length_stats(tgt_lengths),
    }


# ---------- 3. Persona-focused stats ----------

def compute_persona_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    per_persona_q_lengths: Dict[str, List[int]] = defaultdict(list)
    per_persona_a_lengths: Dict[str, List[int]] = defaultdict(list)

    per_persona_judge_scores: Dict[str, List[float]] = defaultdict(list)
    per_persona_correctness: Dict[str, List[float]] = defaultdict(list)

    for obj in items:
        persona = obj.get("persona")
        if not persona:
            continue

        # lengths
        if obj.get("question"):
            per_persona_q_lengths[persona].append(word_count(obj.get("question")))
        if obj.get("answer"):
            per_persona_a_lengths[persona].append(word_count(obj.get("answer")))

        # judge scores
        jf = obj.get("judge_fused") or {}
        final_score = jf.get("final_score")
        subscores = jf.get("subscores") or {}
        correctness = subscores.get("correctness")

        if final_score is not None:
            per_persona_judge_scores[persona].append(float(final_score))
        if correctness is not None:
            per_persona_correctness[persona].append(float(correctness))

    persona_summary = {}
    for persona in sorted(per_persona_q_lengths.keys() | per_persona_a_lengths.keys() |
                          per_persona_judge_scores.keys() | per_persona_correctness.keys()):
        persona_summary[persona] = {
            "question_length": basic_length_stats(per_persona_q_lengths.get(persona, [])),
            "answer_length": basic_length_stats(per_persona_a_lengths.get(persona, [])),
            "judge_final_score": {
                "mean": safe_mean(per_persona_judge_scores.get(persona, [])),
                "median": safe_median(per_persona_judge_scores.get(persona, [])),
                "min": min(per_persona_judge_scores[persona]) if per_persona_judge_scores.get(persona) else None,
                "max": max(per_persona_judge_scores[persona]) if per_persona_judge_scores.get(persona) else None,
            },
            "correctness_subscore": {
                "mean": safe_mean(per_persona_correctness.get(persona, [])),
                "median": safe_median(per_persona_correctness.get(persona, [])),
                "min": min(per_persona_correctness[persona]) if per_persona_correctness.get(persona) else None,
                "max": max(per_persona_correctness[persona]) if per_persona_correctness.get(persona) else None,
            },
        }

    return persona_summary


# ---------- 4. Judgment / quality stats ----------

def compute_judgment_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    judge_pass_true = 0
    judge_pass_false = 0
    final_scores: List[float] = []
    realism_scores: List[float] = []
    dual_use_scores: List[float] = []
    correctness_scores: List[float] = []

    for obj in items:
        jf = obj.get("judge_fused") or {}
        passed = jf.get("passed")
        final_score = jf.get("final_score")
        subscores = jf.get("subscores") or {}

        if passed is True:
            judge_pass_true += 1
        elif passed is False:
            judge_pass_false += 1

        if final_score is not None:
            final_scores.append(float(final_score))

        if "realism" in subscores and subscores["realism"] is not None:
            realism_scores.append(float(subscores["realism"]))
        if "dual_use" in subscores and subscores["dual_use"] is not None:
            dual_use_scores.append(float(subscores["dual_use"]))
        if "correctness" in subscores and subscores["correctness"] is not None:
            correctness_scores.append(float(subscores["correctness"]))

    # Final score buckets
    buckets = {"0-3": 0, "4-6": 0, "7-8": 0, "9-10": 0}
    for s in final_scores:
        if s <= 3:
            buckets["0-3"] += 1
        elif s <= 6:
            buckets["4-6"] += 1
        elif s <= 8:
            buckets["7-8"] += 1
        else:
            buckets["9-10"] += 1

    def score_stats(vals: List[float]) -> Dict[str, Optional[float]]:
        if not vals:
            return {"min": None, "max": None, "mean": None, "median": None}
        return {
            "min": float(min(vals)),
            "max": float(max(vals)),
            "mean": float(stats.mean(vals)),
            "median": float(stats.median(vals)),
        }

    return {
        "judge_pass_counts": {
            "passed_true": judge_pass_true,
            "passed_false": judge_pass_false,
        },
        "judge_final_score": {
            "stats": score_stats(final_scores),
            "buckets": buckets,
        },
        "subscores": {
            "realism": score_stats(realism_scores),
            "dual_use": score_stats(dual_use_scores),
            "correctness": score_stats(correctness_scores),
        },
    }


# ---------- 5. IR agreement stats ----------

def compute_ir_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    num_rel_list: List[int] = []
    num_hit_any_list: List[int] = []
    num_hit_all_list: List[int] = []

    high_conc_true = 0
    low_conc_true = 0

    # per-run method stats
    per_run_hit_any = defaultdict(int)
    per_run_hit_all = defaultdict(int)
    per_run_first_hit_ranks: Dict[str, List[int]] = defaultdict(list)

    for obj in items:
        ir = obj.get("ir_agreement") or {}
        num_rel = ir.get("num_rel")
        num_methods_hit_any = ir.get("num_methods_hit_any")
        num_methods_hit_all = ir.get("num_methods_hit_all")
        high_any = ir.get("high_concordance_any")
        low_any = ir.get("low_concordance_any")
        methods_dict = ir.get("methods") or {}

        if num_rel is not None:
            num_rel_list.append(int(num_rel))
        if num_methods_hit_any is not None:
            num_hit_any_list.append(int(num_methods_hit_any))
        if num_methods_hit_all is not None:
            num_hit_all_list.append(int(num_methods_hit_all))

        if high_any:
            high_conc_true += 1
        if low_any:
            low_conc_true += 1

        for run_name, run_info in methods_dict.items():
            if run_info.get("hit_any"):
                per_run_hit_any[run_name] += 1
                # first_hit_rank is only meaningful when hit_any is True
                fhr = run_info.get("first_hit_rank")
                if fhr is not None:
                    per_run_first_hit_ranks[run_name].append(int(fhr))
            if run_info.get("hit_all"):
                per_run_hit_all[run_name] += 1

    num_items = len(items)

    def basic_int_stats(vals: List[int]) -> Dict[str, Optional[float]]:
        if not vals:
            return {"min": None, "max": None, "mean": None, "median": None}
        return {
            "min": int(min(vals)),
            "max": int(max(vals)),
            "mean": float(stats.mean(vals)),
            "median": float(stats.median(vals)),
        }

    per_run_stats = {}
    for run_name in sorted(per_run_hit_any.keys() | per_run_hit_all.keys()):
        first_hits = per_run_first_hit_ranks.get(run_name, [])
        per_run_stats[run_name] = {
            "hit_any_count": per_run_hit_any.get(run_name, 0),
            "hit_all_count": per_run_hit_all.get(run_name, 0),
            "hit_any_ratio": (
                per_run_hit_any[run_name] / num_items if num_items > 0 else None
            ),
            "hit_all_ratio": (
                per_run_hit_all[run_name] / num_items if num_items > 0 else None
            ),
            "first_hit_rank": basic_int_stats(first_hits),
        }

    return {
        "num_rel": basic_int_stats(num_rel_list),
        "num_methods_hit_any": basic_int_stats(num_hit_any_list),
        "num_methods_hit_all": basic_int_stats(num_hit_all_list),
        "flags": {
            "high_concordance_any_true": high_conc_true,
            "low_concordance_any_true": low_conc_true,
        },
        "per_run": per_run_stats,
    }


# ---------- 6. Document coverage stats ----------

def compute_doc_coverage_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    src_docs = [obj.get("source_doc_id") for obj in items if obj.get("source_doc_id")]
    tgt_docs = [obj.get("target_doc_id") for obj in items if obj.get("target_doc_id")]

    src_counter = Counter(src_docs)
    tgt_counter = Counter(tgt_docs)

    unique_src = len(src_counter)
    unique_tgt = len(tgt_counter)
    unique_all = len(set(src_docs) | set(tgt_docs))

    def top_k(counter: Counter, k: int = 5) -> List[Tuple[str, int]]:
        return counter.most_common(k)

    return {
        "unique_source_doc_ids": unique_src,
        "unique_target_doc_ids": unique_tgt,
        "unique_all_doc_ids": unique_all,
        "top_source_doc_ids": top_k(src_counter, k=5),
        "top_target_doc_ids": top_k(tgt_counter, k=5),
    }


# ---------- 7. Cross-ref specific stats ----------

def compute_crossref_stats(method: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    # reference_type × persona counts
    ref_persona = defaultdict(lambda: Counter())

    # reference_type → list of num_rel
    ref_num_rel: Dict[str, List[int]] = defaultdict(list)

    for obj in items:
        ref_type = obj.get("reference_type") or "UNKNOWN"
        persona = obj.get("persona") or "UNKNOWN"
        ref_persona[ref_type][persona] += 1

        ir = obj.get("ir_agreement") or {}
        num_rel = ir.get("num_rel")
        if num_rel is not None:
            ref_num_rel[ref_type].append(int(num_rel))

    ref_persona_summary = {rt: dict(c) for rt, c in ref_persona.items()}

    ref_num_rel_summary = {}
    for rt, vals in ref_num_rel.items():
        if vals:
            ref_num_rel_summary[rt] = {
                "mean_num_rel": float(stats.mean(vals)),
                "median_num_rel": float(stats.median(vals)),
                "min_num_rel": int(min(vals)),
                "max_num_rel": int(max(vals)),
            }
        else:
            ref_num_rel_summary[rt] = {
                "mean_num_rel": None,
                "median_num_rel": None,
                "min_num_rel": None,
                "max_num_rel": None,
            }

    return {
        "reference_type_by_persona": ref_persona_summary,
        "reference_type_num_rel": ref_num_rel_summary,
    }


# ---------- MAIN ----------

def main():
    summary: Dict[str, Any] = {}

    for method in METHODS:
        print("=" * 70)
        print(f"=== METHOD: {method} ===")
        print("=" * 70)

        items = load_method_items(method)
        num_items = len(items)
        print(f"Total items: {num_items}")

        core = compute_core_stats(method, items)
        lengths = compute_length_stats(method, items)
        persona_stats = compute_persona_stats(method, items)
        judgment = compute_judgment_stats(method, items)
        ir_stats = compute_ir_stats(method, items)
        doc_cov = compute_doc_coverage_stats(method, items)
        crossref = compute_crossref_stats(method, items)

        # --- Pretty-print key bits to stdout ---

        # 1. Core stats
        print("\n[Core sanity + size]")
        print("Split counts:", core["split_counts"])
        print("Persona counts:", core["persona_counts"])
        print("Missing fields:", core["missing_fields"])
        print("Reference types:", core["reference_type_counts"])

        # 2. Length stats
        print("\n[Length stats (words)]")
        print("Question length:", lengths["question_length"])
        print("Answer length:", lengths["answer_length"])
        print("Source passage length:", lengths["source_passage_length"])
        print("Target passage length:", lengths["target_passage_length"])

        # 3. Persona-focused stats
        print("\n[Persona-focused stats]")
        for persona, pstats in persona_stats.items():
            print(f"  Persona: {persona}")
            print("    Question length:", pstats["question_length"])
            print("    Answer length:", pstats["answer_length"])
            print("    Judge final score:", pstats["judge_final_score"])
            print("    Correctness subscore:", pstats["correctness_subscore"])

        # 4. Judgment stats
        print("\n[Judgment / quality stats]")
        print("Judge pass counts:", judgment["judge_pass_counts"])
        print("Judge final score stats:", judgment["judge_final_score"]["stats"])
        print("Judge final score buckets:", judgment["judge_final_score"]["buckets"])
        print("Subscores:", judgment["subscores"])

        # 5. IR stats
        print("\n[IR agreement stats]")
        print("num_rel:", ir_stats["num_rel"])
        print("num_methods_hit_any:", ir_stats["num_methods_hit_any"])
        print("num_methods_hit_all:", ir_stats["num_methods_hit_all"])
        print("flags:", ir_stats["flags"])
        print("Per-run summary:")
        for run_name, rstats in ir_stats["per_run"].items():
            print(f"  {run_name}: {rstats}")

        # 6. Document coverage
        print("\n[Document coverage]")
        print("Unique source_doc_id:", doc_cov["unique_source_doc_ids"])
        print("Unique target_doc_id:", doc_cov["unique_target_doc_ids"])
        print("Unique all doc ids:", doc_cov["unique_all_doc_ids"])
        print("Top source_doc_id:", doc_cov["top_source_doc_ids"])
        print("Top target_doc_id:", doc_cov["top_target_doc_ids"])

        # 7. Cross-ref specific
        print("\n[Cross-ref specific stats]")
        print("Reference type x persona:", crossref["reference_type_by_persona"])
        print("Reference type → num_rel:", crossref["reference_type_num_rel"])

        # Collect into JSON summary
        summary[method] = {
            "core": core,
            "lengths": lengths,
            "persona": persona_stats,
            "judgment": judgment,
            "ir": ir_stats,
            "doc_coverage": doc_cov,
            "crossref": crossref,
        }

    # Dump JSON summary
    SUMMARY_JSON_PATH.parent.mkdir(parents=True, exist_ok=True)
    with SUMMARY_JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, ensure_ascii=False)

    print("\n" + "=" * 70)
    print(f"Stats summary written to: {SUMMARY_JSON_PATH.resolve()}")
    print("=" * 70)


if __name__ == "__main__":
    main()

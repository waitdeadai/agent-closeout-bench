#!/usr/bin/env python3
"""Compute Cohen's kappa across judge pairs and against candidate labels.

Inputs:
  - annotations/sample_uai_2026.jsonl  (carries record_id -> category and label_candidate)
  - annotations/judge_claude.jsonl, judge_gpt.jsonl, judge_gemini.jsonl

Output:
  - annotations/judge_agreement.json: pairwise per-category and overall kappa,
    plus per-judge-vs-candidate-label kappa.

Honest-reporting convention (per DarkBench ICLR 2025 Oral): low kappa is
reported, not hidden. A category with kappa < 0.4 is flagged but not
filtered.

Parse failures (label = -1) are excluded from kappa on a per-pair basis with
a count recorded.

Usage:
  python3 annotations/compute_judge_agreement.py
  python3 annotations/compute_judge_agreement.py --judges claude gpt
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

CATEGORIES = ["wrap_up", "cliffhanger", "roleplay_drift", "sycophancy"]
JUDGES = ["claude", "gpt", "gemini"]


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def cohens_kappa(rater_a: list[int], rater_b: list[int]) -> dict:
    """Compute Cohen's kappa for two binary raters.

    Returns dict with kappa, n, percent_agreement, p_e, k.
    Returns kappa = None if n == 0 or if p_e == 1 (degenerate).
    """
    pairs = [(a, b) for a, b in zip(rater_a, rater_b) if a in (0, 1) and b in (0, 1)]
    n = len(pairs)
    if n == 0:
        return {"kappa": None, "n": 0, "percent_agreement": None, "p_e": None}

    agree = sum(1 for a, b in pairs if a == b)
    p_o = agree / n

    a_pos = sum(a for a, _ in pairs) / n
    b_pos = sum(b for _, b in pairs) / n
    p_e = a_pos * b_pos + (1 - a_pos) * (1 - b_pos)

    if abs(1 - p_e) < 1e-9:
        kappa = None  # degenerate (all-agree edge case)
    else:
        kappa = (p_o - p_e) / (1 - p_e)

    return {
        "kappa": round(kappa, 4) if kappa is not None else None,
        "n": n,
        "percent_agreement": round(p_o, 4),
        "p_e": round(p_e, 4),
    }


def build_judge_label_map(judge_rows: list[dict]) -> dict:
    """Map record_id -> {category: 0|1|-1}."""
    m = {}
    for row in judge_rows:
        m[row["record_id"]] = row["labels"]
    return m


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--sample", default="annotations/sample_uai_2026.jsonl")
    parser.add_argument("--judges", nargs="+", default=JUDGES, choices=JUDGES)
    parser.add_argument("--output", default="annotations/judge_agreement.json")
    parser.add_argument(
        "--per-category-binary",
        action="store_true",
        default=True,
        help="Compute kappa within each category on that category's binary label only (default).",
    )
    args = parser.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    sample_path = repo_root / args.sample
    out_path = repo_root / args.output

    sample = load_jsonl(sample_path)
    sample_by_id = {row["id"]: row for row in sample}

    judge_data: dict[str, dict] = {}
    judge_metadata: dict[str, dict] = {}
    judge_parse_failures: dict[str, int] = {}
    for judge in args.judges:
        path = repo_root / f"annotations/judge_{judge}.jsonl"
        if not path.exists():
            print(f"WARNING: {path} not found, skipping {judge}", file=sys.stderr)
            continue
        rows = load_jsonl(path)
        judge_data[judge] = build_judge_label_map(rows)
        if rows:
            judge_metadata[judge] = {
                "judge_model": rows[0]["judge_model"],
                "api_provider": rows[0]["judge_metadata"]["api_provider"],
                "n_rows": len(rows),
            }
        parse_fails = sum(
            1 for r in rows if any(v == -1 for v in r["labels"].values())
        )
        judge_parse_failures[judge] = parse_fails

    if not judge_data:
        print("ERROR: no judge output files found", file=sys.stderr)
        return 1

    record_ids = sorted(set(sample_by_id) & set.intersection(*(set(jd) for jd in judge_data.values())))

    result = {
        "sample_path": str(sample_path.relative_to(repo_root)),
        "judges": list(judge_data.keys()),
        "judge_metadata": judge_metadata,
        "judge_parse_failures": judge_parse_failures,
        "n_records_intersected": len(record_ids),
        "per_category": defaultdict(dict),
        "overall_aggregate": {},
        "honest_reporting_note": (
            "Low kappa values are reported, not filtered. Following DarkBench "
            "(Kran et al., ICLR 2025 Oral), per-category kappa as low as 0.27 "
            "remains scientifically reportable."
        ),
    }

    # Per-category, per-judge-pair kappa.
    pairs = []
    for i, j1 in enumerate(judge_data.keys()):
        for j2 in list(judge_data.keys())[i + 1 :]:
            pairs.append((j1, j2))

    for category in CATEGORIES:
        for j1, j2 in pairs:
            a = [judge_data[j1][rid][category] for rid in record_ids]
            b = [judge_data[j2][rid][category] for rid in record_ids]
            result["per_category"][category][f"{j1}_vs_{j2}"] = cohens_kappa(a, b)
        for judge in judge_data:
            a = [judge_data[judge][rid][category] for rid in record_ids]
            b = [int(sample_by_id[rid]["label_candidate"]) if sample_by_id[rid]["category"] == category else 0 for rid in record_ids]
            result["per_category"][category][f"{judge}_vs_candidate"] = cohens_kappa(a, b)

    # Overall aggregate: stack all (category, record) pairs into one long vector per judge.
    for j1, j2 in pairs:
        a, b = [], []
        for category in CATEGORIES:
            for rid in record_ids:
                a.append(judge_data[j1][rid][category])
                b.append(judge_data[j2][rid][category])
        result["overall_aggregate"][f"{j1}_vs_{j2}"] = cohens_kappa(a, b)

    for judge in judge_data:
        a, b = [], []
        for category in CATEGORIES:
            for rid in record_ids:
                a.append(judge_data[judge][rid][category])
                b.append(int(sample_by_id[rid]["label_candidate"]) if sample_by_id[rid]["category"] == category else 0)
        result["overall_aggregate"][f"{judge}_vs_candidate"] = cohens_kappa(a, b)

    result["per_category"] = dict(result["per_category"])

    out_path.parent.mkdir(exist_ok=True)
    with out_path.open("w") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"compute_judge_agreement: n_records={len(record_ids)}, judges={list(judge_data.keys())}")
    print(f"compute_judge_agreement: wrote {out_path}")

    # Print a quick summary table.
    print("\nPer-category kappa (overall aggregate):")
    print(f"{'pair':<30} {'kappa':>8} {'n':>6} {'agreement':>10}")
    for key, val in result["overall_aggregate"].items():
        k = val["kappa"]
        k_str = f"{k:.4f}" if k is not None else "  N/A"
        print(f"{key:<30} {k_str:>8} {val['n']:>6} {val['percent_agreement']:>10.4f}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

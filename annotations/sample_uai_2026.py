#!/usr/bin/env python3
"""Deterministic stratified sampler for the SafeAI@UAI 2026 paper run.

Samples 50 records per category (200 total) from data/<category>/{positives,negatives}.jsonl.
Within each category, samples 25 positives and 25 negatives.
Uses a fixed seed so the sample is reproducible from commit + script.

Output: annotations/sample_uai_2026.jsonl
"""
from __future__ import annotations

import json
import random
import sys
from pathlib import Path

SEED = 20260516
PER_CATEGORY_TOTAL = 50
PER_LABEL = PER_CATEGORY_TOTAL // 2  # 25 positives + 25 negatives
CATEGORIES = ["wrap_up", "cliffhanger", "roleplay_drift", "sycophancy"]


def load_jsonl(path: Path) -> list[dict]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    data_dir = repo_root / "data"
    out_path = repo_root / "annotations" / "sample_uai_2026.jsonl"

    rng = random.Random(SEED)
    sampled: list[dict] = []

    for category in CATEGORIES:
        pos = load_jsonl(data_dir / category / "positives.jsonl")
        neg = load_jsonl(data_dir / category / "negatives.jsonl")

        if len(pos) < PER_LABEL or len(neg) < PER_LABEL:
            print(
                f"ERROR: category {category} has {len(pos)} pos / {len(neg)} neg, "
                f"need {PER_LABEL} of each",
                file=sys.stderr,
            )
            return 1

        sampled.extend(rng.sample(pos, PER_LABEL))
        sampled.extend(rng.sample(neg, PER_LABEL))

    rng.shuffle(sampled)

    out_path.parent.mkdir(exist_ok=True)
    with out_path.open("w") as f:
        for row in sampled:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    print(f"sample_uai_2026: wrote {len(sampled)} rows to {out_path}")
    print(f"sample_uai_2026: seed={SEED}, per_category={PER_CATEGORY_TOTAL}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

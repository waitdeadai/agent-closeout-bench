#!/usr/bin/env python3
"""Assign deterministic stratified splits to corpus records."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


CATEGORIES = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_jsonl(path: Path, records: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, sort_keys=True, ensure_ascii=False) + "\n")


def stable_key(record: dict, seed: str) -> str:
    raw = f"{seed}|{record.get('id')}"
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def split_name(index: int, n: int, dev: float, validation: float) -> str:
    if n <= 1:
        return "dev"
    frac = index / n
    if frac < dev:
        return "dev"
    if frac < dev + validation:
        return "validation"
    return "locked_test"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--splits-dir", default="splits")
    ap.add_argument("--seed", default="agentcloseoutbench-v1-locked-seed-2026-05-13")
    ap.add_argument("--dev", type=float, default=0.60)
    ap.add_argument("--validation", type=float, default=0.20)
    args = ap.parse_args()
    if args.dev < 0 or args.validation < 0 or args.dev + args.validation > 1:
        raise SystemExit("--dev and --validation must be non-negative and sum to <= 1")

    data_dir = Path(args.data_dir)
    splits_dir = Path(args.splits_dir)
    buckets: dict[tuple[str, int], list[dict]] = defaultdict(list)

    for cat in CATEGORIES:
        for filename, label in (("positives.jsonl", 1), ("negatives.jsonl", 0)):
            for record in read_jsonl(data_dir / cat / filename):
                buckets[(cat, label)].append(record)

    by_split: dict[str, list[dict]] = defaultdict(list)
    all_records: list[dict] = []
    for bucket, records in sorted(buckets.items()):
        ordered = sorted(records, key=lambda r: stable_key(r, args.seed))
        for idx, record in enumerate(ordered):
            split = split_name(idx, len(ordered), args.dev, args.validation)
            record = {**record, "split": split}
            by_split[split].append({"id": record["id"], "category": record["category"], "label_candidate": record["label_candidate"]})
            all_records.append(record)

    for cat in CATEGORIES:
        for filename, label in (("positives.jsonl", 1), ("negatives.jsonl", 0)):
            records = [r for r in all_records if r["category"] == cat and r["label_candidate"] == label]
            write_jsonl(data_dir / cat / filename, sorted(records, key=lambda r: r["id"]))

    splits_dir.mkdir(parents=True, exist_ok=True)
    for split in ("dev", "validation", "locked_test"):
        (splits_dir / f"{split}.json").write_text(
            json.dumps(sorted(by_split.get(split, []), key=lambda r: r["id"]), indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
        )
    audit = splits_dir / "LOCKED_TEST_AUDIT.md"
    run_section = "## Locked-Test Runs\n\n"
    if audit.exists() and run_section in audit.read_text(encoding="utf-8"):
        run_section += audit.read_text(encoding="utf-8").split(run_section, 1)[1]
    audit.write_text(
        "# Locked Test Audit\n\n"
        f"- Seed: `{args.seed}`\n"
        "- Split assignment created by `scripts/make_splits.py`.\n"
        "- Final paper metrics must append every locked-test run below.\n\n"
        f"{run_section}",
        encoding="utf-8",
    )
    print(json.dumps({k: len(v) for k, v in by_split.items()}, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

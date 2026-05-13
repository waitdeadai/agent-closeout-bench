#!/usr/bin/env python3
"""Subscription-billed corpus generator scaffold.

This script is intentionally explicit about billing and quota. It does not run
unless `--execute` is passed. The default command prints the work plan and
missing cells from `quota_manifest.json`.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from collections import Counter
from pathlib import Path


CATEGORIES = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def current_counts(data_dir: Path) -> Counter[tuple[str, int, str]]:
    counts: Counter[tuple[str, int, str]] = Counter()
    for cat in CATEGORIES:
        for filename, label in (("positives.jsonl", 1), ("negatives.jsonl", 0)):
            for row in read_jsonl(data_dir / cat / filename):
                counts[(cat, label, row.get("task_type", "unknown"))] += 1
    return counts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--quota-manifest", default="quota_manifest.json")
    ap.add_argument("--model", default="claude-sonnet-4-6")
    ap.add_argument("--lanes", type=int, default=1)
    ap.add_argument("--execute", action="store_true", help="Actually call `claude -p`; default only reports missing cells.")
    args = ap.parse_args()

    quota = json.loads(Path(args.quota_manifest).read_text())
    counts = current_counts(Path(args.data_dir))
    missing = []
    for cat in quota["categories"]:
        for label_name, label in quota["labels"].items():
            for task_type, target in quota["task_type_quota_per_category_label"].items():
                got = counts[(cat, label, task_type)]
                if got < target:
                    missing.append({"category": cat, "label": label, "label_name": label_name, "task_type": task_type, "missing": target - got})

    report = {
        "model": args.model,
        "lanes": args.lanes,
        "execute": args.execute,
        "missing_cells": missing,
        "note": "Generation is blocked unless --execute is supplied; verify quota/provider route first.",
    }
    print(json.dumps(report, indent=2, sort_keys=True))

    if not args.execute:
        return 0
    if args.lanes != 1:
        raise SystemExit("Provider-safe default is lanes=1; increase only with explicit runtime evidence.")
    if subprocess.run(["bash", "-lc", "command -v claude"], capture_output=True).returncode != 0:
        raise SystemExit("claude CLI not found; cannot generate.")
    raise SystemExit("Generation execution is intentionally not implemented in this recovery slice. Use prompts + manifest after explicit quota approval.")


if __name__ == "__main__":
    raise SystemExit(main())


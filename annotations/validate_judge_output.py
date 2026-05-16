#!/usr/bin/env python3
"""Validate annotations/judge_<judge_id>.jsonl against annotations/judge_schema.json."""
from __future__ import annotations

import json
import sys
from pathlib import Path


def validate_record(record: dict, errors: list[str], i: int) -> None:
    required_top = {"record_id", "judge_id", "judge_model", "labels", "raw_response", "judge_metadata"}
    missing = required_top - set(record)
    if missing:
        errors.append(f"row {i}: missing top-level keys {missing}")
        return

    if record["judge_id"] not in {"claude", "gpt", "gemini"}:
        errors.append(f"row {i}: invalid judge_id {record['judge_id']}")

    labels = record["labels"]
    if not isinstance(labels, dict):
        errors.append(f"row {i}: labels is not a dict")
        return
    for cat in ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy"):
        if cat not in labels:
            errors.append(f"row {i}: labels missing {cat}")
            continue
        if labels[cat] not in (0, 1, -1):  # -1 = parse failure, allowed but flagged
            errors.append(f"row {i}: labels.{cat} = {labels[cat]} not in 0/1/-1")

    meta = record.get("judge_metadata", {})
    for key in ("timestamp_utc", "prompt_template_hash", "api_provider"):
        if key not in meta:
            errors.append(f"row {i}: judge_metadata.{key} missing")
    if meta.get("api_provider") not in {"anthropic", "openai", "google"}:
        errors.append(f"row {i}: judge_metadata.api_provider invalid")


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_judge_output.py <path-to-judge-output.jsonl>", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"ERROR: file not found: {path}", file=sys.stderr)
        return 1

    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))

    errors: list[str] = []
    parse_failures = 0
    for i, row in enumerate(rows):
        validate_record(row, errors, i)
        if any(v == -1 for v in row.get("labels", {}).values()):
            parse_failures += 1

    print(f"validate_judge_output: file={path}")
    print(f"validate_judge_output: rows={len(rows)} errors={len(errors)} parse_failures={parse_failures}")
    for err in errors[:20]:
        print(f"  {err}")
    if len(errors) > 20:
        print(f"  ... and {len(errors) - 20} more")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

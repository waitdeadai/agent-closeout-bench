#!/usr/bin/env python3
"""Validate AgentCloseoutBench JSONL corpus files."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


CATEGORIES = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")
TASK_TYPES = ("refactor", "debug", "research", "write", "migrate", "test", "infra", "review")
REQUIRED = {
    "id",
    "category",
    "label_candidate",
    "label_final",
    "task_type",
    "task_description",
    "session_summary",
    "closeout_text",
    "generation_method",
    "model",
    "temperature",
    "prompt_hash",
    "source_provenance",
    "license_source",
    "split",
    "created_at",
    "notes",
}
SENSITIVE_RE = re.compile(
    r"(ANTHROPIC_API_KEY|OPENAI_API_KEY|CLAUDE_CODE_OAUTH_TOKEN|sk-[A-Za-z0-9_-]{16,}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY)",
    re.I,
)
FORBIDDEN_TEXT = ('"type": "thinking"', '"signature"', '"tool_use"', '"tool_result"', '"attachment"')


def iter_jsonl(path: Path):
    if not path.exists():
        return
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid json: {exc}") from exc


def validate_record(path: Path, line_no: int, record: dict[str, Any], expected_category: str, expected_label: int) -> list[str]:
    errors: list[str] = []
    missing = sorted(REQUIRED - set(record))
    if missing:
        errors.append(f"{path}:{line_no}: missing fields {missing}")
    if record.get("category") != expected_category:
        errors.append(f"{path}:{line_no}: category {record.get('category')!r} != {expected_category!r}")
    if record.get("label_candidate") != expected_label:
        errors.append(f"{path}:{line_no}: label_candidate {record.get('label_candidate')!r} != {expected_label!r}")
    if record.get("label_final") not in (0, 1, None):
        errors.append(f"{path}:{line_no}: label_final must be 0, 1, or null")
    if record.get("task_type") not in TASK_TYPES:
        errors.append(f"{path}:{line_no}: invalid task_type {record.get('task_type')!r}")
    if record.get("split") not in ("dev", "validation", "locked_test", None):
        errors.append(f"{path}:{line_no}: invalid split {record.get('split')!r}")
    text = record.get("closeout_text")
    if not isinstance(text, str) or not text.strip():
        errors.append(f"{path}:{line_no}: empty closeout_text")
    elif len(text) > 1200:
        errors.append(f"{path}:{line_no}: closeout_text too long")
    else:
        leakage_terms = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy", "label_candidate")
        lowered_text = text.lower()
        for term in leakage_terms:
            if term in lowered_text:
                errors.append(f"{path}:{line_no}: closeout_text leaks benchmark/control term {term!r}")
    serialized = json.dumps(record, ensure_ascii=False)
    if SENSITIVE_RE.search(serialized):
        errors.append(f"{path}:{line_no}: sensitive-looking token")
    lower = serialized.lower()
    for bad in FORBIDDEN_TEXT:
        if bad in lower:
            errors.append(f"{path}:{line_no}: forbidden transcript artifact token {bad!r}")
    if not str(record.get("prompt_hash", "")).startswith("sha256:"):
        errors.append(f"{path}:{line_no}: prompt_hash must start with sha256:")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--quota-manifest", default="quota_manifest.json")
    ap.add_argument("--allow-partial", action="store_true")
    ap.add_argument("--require-final-labels", action="store_true")
    ap.add_argument("--require-public-license", action="store_true")
    args = ap.parse_args()

    data_dir = Path(args.data_dir)
    quota = json.loads(Path(args.quota_manifest).read_text()) if Path(args.quota_manifest).exists() else {}
    target_per_label = int(quota.get("target_per_category_label", 100))
    target_task = quota.get("task_type_quota_per_category_label", {})

    errors: list[str] = []
    seen_ids: set[str] = set()
    seen_texts: Counter[str] = Counter()
    counts: Counter[tuple[str, int]] = Counter()
    task_counts: Counter[tuple[str, int, str]] = Counter()

    for cat in CATEGORIES:
        for filename, label in (("positives.jsonl", 1), ("negatives.jsonl", 0)):
            path = data_dir / cat / filename
            for line_no, record in iter_jsonl(path) or []:
                errors.extend(validate_record(path, line_no, record, cat, label))
                rid = str(record.get("id", ""))
                if rid in seen_ids:
                    errors.append(f"{path}:{line_no}: duplicate id {rid}")
                seen_ids.add(rid)
                text = str(record.get("closeout_text", "")).strip()
                if text:
                    seen_texts[text] += 1
                counts[(cat, label)] += 1
                task_counts[(cat, label, str(record.get("task_type")))] += 1
                if args.require_final_labels and record.get("label_final") not in (0, 1):
                    errors.append(f"{path}:{line_no}: label_final required for release/final evaluation")
                if args.require_public_license and record.get("license_source") != "project-generated-apache-2.0":
                    errors.append(f"{path}:{line_no}: public release requires project-generated-apache-2.0 license_source")

    for text, n in seen_texts.items():
        if n > 1:
            errors.append(f"duplicate closeout_text appears {n} times: {text[:80]!r}")

    if not args.allow_partial:
        for cat in CATEGORIES:
            for label in (0, 1):
                got = counts[(cat, label)]
                if got != target_per_label:
                    errors.append(f"{cat} label {label}: expected {target_per_label}, got {got}")
                for task_type, expected in target_task.items():
                    got_task = task_counts[(cat, label, task_type)]
                    if got_task != expected:
                        errors.append(f"{cat} label {label} task {task_type}: expected {expected}, got {got_task}")

    report = {
        "records": sum(counts.values()),
        "counts": {f"{cat}:{label}": counts[(cat, label)] for cat in CATEGORIES for label in (0, 1)},
        "errors": errors,
        "allow_partial": args.allow_partial,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    if errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

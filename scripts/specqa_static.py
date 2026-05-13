#!/usr/bin/env python3
"""Static Spec QA gate for the current AgentCloseoutBench contract."""

from __future__ import annotations

import json
import re
from pathlib import Path


REQUIRED_TERMS = (
    "candidate labels",
    "two independent human",
    "locked_test",
    "LLM judges are diagnostic",
    "lexical and semantic evasion remain possible",
)


def main() -> int:
    spec = Path("SPEC.md").read_text(encoding="utf-8")
    claims = Path("CLAIM_LEDGER.md").read_text(encoding="utf-8")
    issues = []

    for term in REQUIRED_TERMS:
        if term.lower() not in spec.lower() and term.lower() not in claims.lower():
            issues.append(f"missing required governance term: {term}")

    overclaims = [
        r"prompt injection cannot bypass",
        r"human-annotated corpus",
        r"production ready",
        r"LLM judge labels are ground truth",
    ]
    combined = (spec + "\n" + claims).lower()
    for pat in overclaims:
        if re.search(pat.lower(), combined):
            issues.append(f"overclaim still present: {pat}")

    report = {
        "status": "pass" if not issues else "fail",
        "issues": issues,
        "checked_files": ["SPEC.md", "CLAIM_LEDGER.md"],
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main())


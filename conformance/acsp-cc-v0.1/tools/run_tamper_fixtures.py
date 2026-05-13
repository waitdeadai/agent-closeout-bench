#!/usr/bin/env python3
"""Run ACSP-CC adapter tamper fixtures against the Claude Code guard."""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import time
from pathlib import Path
from typing import Any


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    files = sorted(path.glob("*.jsonl")) if path.is_dir() else [path]
    for fixture_path in files:
        with fixture_path.open(encoding="utf-8") as handle:
            for line_no, line in enumerate(handle, 1):
                if not line.strip():
                    continue
                row = json.loads(line)
                row["source"] = f"{fixture_path}:{line_no}"
                rows.append(row)
    return rows


def truncate(text: str, limit: int = 600) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + "...[truncated]"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fixtures", required=True)
    parser.add_argument("--hook", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--timeout-s", type=float, default=5.0)
    args = parser.parse_args()

    fixtures = read_jsonl(Path(args.fixtures))
    env = {**os.environ, "CLAUDE_PROJECT_DIR": "/tmp/acsp-project"}
    cases: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for fixture in fixtures:
        started = time.perf_counter()
        proc = subprocess.run(
            ["bash", args.hook],
            input=json.dumps(fixture.get("payload", {})),
            cwd=args.root,
            env=env,
            capture_output=True,
            text=True,
            timeout=args.timeout_s,
            check=False,
        )
        duration_ms = round((time.perf_counter() - started) * 1000, 3)
        expected_status = int(fixture["expect_status"])
        ok = proc.returncode == expected_status
        stderr_needle = fixture.get("expect_stderr_contains")
        stdout_needle = fixture.get("expect_stdout_contains")
        if stderr_needle:
            ok = ok and stderr_needle in proc.stderr
        if stdout_needle:
            ok = ok and stdout_needle in proc.stdout

        case = {
            "id": fixture["id"],
            "source": fixture["source"],
            "ok": ok,
            "actual_status": proc.returncode,
            "expected_status": expected_status,
            "duration_ms": duration_ms,
        }
        cases.append(case)
        if not ok:
            failures.append({**case, "stdout": truncate(proc.stdout), "stderr": truncate(proc.stderr)})

    report = {
        "ok": not failures,
        "total": len(cases),
        "passed": len(cases) - len(failures),
        "failures": failures,
        "cases": cases,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

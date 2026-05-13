#!/usr/bin/env python3
"""Static safety checks for release and security workflows.

This intentionally avoids network access and external dependencies. It enforces
the local least-privilege policy for draft workflows and performs a
high-confidence secret scan over repository text files.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ALLOWED_NARROW_WRITE_PERMISSIONS = {"security-events", "id-token"}
SKIP_DIRS = {
    ".git",
    ".mypy_cache",
    ".pytest_cache",
    ".ruff_cache",
    ".venv",
    ".venv-audit",
    "engine/target",
    "node_modules",
    "target",
}
MAX_SCAN_BYTES = 2_000_000
SECRET_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("openai_or_compatible_api_key", re.compile(r"\bsk-[A-Za-z0-9_-]{32,}\b")),
    ("github_pat", re.compile(r"\bgithub_pat_[A-Za-z0-9_]{22,}\b")),
    ("github_token", re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b")),
    ("private_key", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
)


def workflow_files(workflow_dir: Path) -> list[Path]:
    if not workflow_dir.exists():
        return []
    files: list[Path] = []
    for pattern in ("*.yml", "*.yaml"):
        files.extend(workflow_dir.glob(pattern))
    return sorted(files)


def line_no(text: str, offset: int) -> int:
    return text.count("\n", 0, offset) + 1


def check_workflow(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    errors: list[str] = []
    warnings: list[str] = []

    if re.search(r"(?m)^\s*pull_request_target\s*:", text):
        errors.append(f"{path}: uses pull_request_target")

    for match in re.finditer(r"(?m)^\s*permissions:\s*(write-all|read-all)\s*(?:#.*)?$", text):
        errors.append(f"{path}:{line_no(text, match.start())}: permissions must be explicit least-privilege, not {match.group(1)}")

    for match in re.finditer(r"(?m)^\s*([A-Za-z-]+):\s*write\s*(?:#.*)?$", text):
        permission = match.group(1)
        if permission not in ALLOWED_NARROW_WRITE_PERMISSIONS:
            errors.append(f"{path}:{line_no(text, match.start())}: unexpected write permission {permission}: write")

    curl_to_shell = re.compile(
        r"(?im)(curl|wget)[^\n|;]*[|;]\s*(sudo\s+)?(sh|bash)\b|bash\s+<\s*\(\s*(curl|wget)\b"
    )
    for match in curl_to_shell.finditer(text):
        errors.append(f"{path}:{line_no(text, match.start())}: curl/wget-to-shell is forbidden")

    lines = text.splitlines()
    for idx, line in enumerate(lines):
        if re.search(r"uses:\s*actions/checkout@", line):
            window = "\n".join(lines[idx : idx + 12])
            if not re.search(r"(?m)^\s*persist-credentials:\s*false\s*(?:#.*)?$", window):
                errors.append(f"{path}:{idx + 1}: actions/checkout must set persist-credentials: false")

    if "${{ secrets." in text:
        warnings.append(f"{path}: references repository secrets; verify they are unavailable to untrusted pull requests")

    return errors, warnings


def should_skip(path: Path, root: Path) -> bool:
    rel = path.relative_to(root)
    rel_text = rel.as_posix()
    return any(rel_text == item or rel_text.startswith(item + "/") for item in SKIP_DIRS)


def scan_file_for_secrets(path: Path) -> list[str]:
    try:
        raw = path.read_bytes()
    except OSError as exc:
        return [f"{path}: could not read: {exc}"]
    if len(raw) > MAX_SCAN_BYTES or b"\x00" in raw:
        return []
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return []

    findings: list[str] = []
    for name, pattern in SECRET_PATTERNS:
        for match in pattern.finditer(text):
            findings.append(f"{path}:{line_no(text, match.start())}: high-confidence secret pattern {name}")
    return findings


def scan_repo_for_secrets(root: Path) -> list[str]:
    findings: list[str] = []
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        if should_skip(path, root):
            continue
        findings.extend(scan_file_for_secrets(path))
    return findings


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--workflows", default=".github/workflows")
    ap.add_argument("--scan-secrets", action="store_true")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    workflow_dir = Path(args.workflows)
    if not workflow_dir.is_absolute():
        workflow_dir = root / workflow_dir

    errors: list[str] = []
    warnings: list[str] = []
    files = workflow_files(workflow_dir)
    if not files:
        errors.append(f"no workflow files found in {workflow_dir}")

    for path in files:
        file_errors, file_warnings = check_workflow(path)
        errors.extend(file_errors)
        warnings.extend(file_warnings)

    if args.scan_secrets:
        errors.extend(scan_repo_for_secrets(root))

    report = {
        "ok": not errors,
        "workflow_files": [str(path.relative_to(root)) for path in files],
        "errors": errors,
        "warnings": warnings,
        "secret_scan": args.scan_secrets,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

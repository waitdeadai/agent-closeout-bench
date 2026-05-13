#!/usr/bin/env python3
"""Public-data intake guardrails for AgentCloseoutBench.

The important property is negative: raw public trace text is not persisted by
default. Public sources can shape deterministic mechanics only after explicit
license/privacy decisions, redaction, and manifest provenance.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any


REGISTRY_VERSION = "agentcloseout.public_source_registry.v1"
ALLOWED_TIERS = {"A", "B", "C"}
ALLOWED_FIXTURE_CLASSES = {
    "positive_direct",
    "negative_near_miss",
    "adversarial_paraphrase",
    "cross_framework",
    "trace_evidence",
    "privacy_quarantine",
}
ALLOWED_RELEASE = {
    "releasable_after_redaction_review",
    "releasable_paraphrase_only",
    "not_releasable",
    "not_fixture_source",
}
TEXT_FIELDS_TO_SCAN = ("task_description", "session_summary", "closeout_text", "notes")
TRACE_ARTIFACT_TOKENS = (
    '"type": "thinking"',
    '"signature"',
    '"tool_use"',
    '"tool_result"',
    '"attachment"',
    "toolresult",
    "tool_use",
    "tool_result",
)

SENSITIVE_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("secret_token", re.compile(r"(sk-[A-Za-z0-9_-]{16,}|ANTHROPIC_API_KEY|OPENAI_API_KEY|CLAUDE_CODE_OAUTH_TOKEN|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY)", re.I)),
    ("email", re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)),
    ("absolute_path", re.compile(r"(?<![A-Za-z0-9])/(home|Users|var|etc|tmp|private|mnt|Volumes)/[^\s`'\"<>]+")),
    ("repo_url", re.compile(r"\bhttps?://(?:www\.)?(github|gitlab|bitbucket)\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", re.I)),
    ("hostname", re.compile(r"\b(?:[a-z0-9-]+\.)+(?:local|internal|corp|lan|dev|prod)\b", re.I)),
    ("username_field", re.compile(r"\b(user(name)?|login|owner)\s*[:=]\s*[A-Za-z0-9_.-]{3,}\b", re.I)),
    ("ip_address", re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")),
)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc


def iter_jsonl(path: Path):
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            if not line.strip():
                continue
            try:
                yield line_no, json.loads(line)
            except json.JSONDecodeError as exc:
                raise SystemExit(f"{path}:{line_no}: invalid JSONL row: {exc}") from exc


def registry_errors(registry: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if registry.get("schema_version") != REGISTRY_VERSION:
        errors.append(f"schema_version must be {REGISTRY_VERSION}")
    sources = registry.get("sources")
    if not isinstance(sources, list) or not sources:
        errors.append("sources must be a non-empty array")
        return errors
    seen: set[str] = set()
    for idx, source in enumerate(sources):
        prefix = f"sources[{idx}]"
        required = {
            "source_id",
            "title",
            "url",
            "tier",
            "license",
            "license_family",
            "terms_url",
            "schema_summary",
            "privacy_status",
            "allowed_use",
            "import_decision",
            "release_eligibility",
            "reviewer",
            "reviewed_at",
            "notes",
        }
        missing = sorted(required - set(source))
        if missing:
            errors.append(f"{prefix}: missing fields {missing}")
            continue
        sid = str(source["source_id"])
        if sid in seen:
            errors.append(f"{prefix}: duplicate source_id {sid}")
        seen.add(sid)
        if source["tier"] not in ALLOWED_TIERS:
            errors.append(f"{prefix}: bad tier {source['tier']!r}")
        if not source.get("license") or "pending" in str(source["license"]).lower():
            errors.append(f"{prefix}: source requires a concrete license decision")
        if source["release_eligibility"] not in ALLOWED_RELEASE:
            errors.append(f"{prefix}: bad release_eligibility {source['release_eligibility']!r}")
        allowed = source.get("allowed_use")
        if not isinstance(allowed, list) or not allowed:
            errors.append(f"{prefix}: allowed_use must be non-empty")
        if source["tier"] == "B" and "raw_fixture_release" in allowed:
            errors.append(f"{prefix}: Tier B source cannot be raw_fixture_release")
        if source["tier"] == "C" and any(use in allowed for use in ("raw_fixture_release", "derived_fixtures")):
            errors.append(f"{prefix}: Tier C source must remain taxonomy/platform guidance only")
        if source["license_family"] == "copyleft_noncommercial" and source["release_eligibility"] != "not_releasable":
            errors.append(f"{prefix}: noncommercial source cannot be releasable")
        if source["import_decision"] == "approved_for_redacted_derived_fixtures":
            if source["license_family"] != "permissive":
                errors.append(f"{prefix}: approved fixture imports require permissive license_family")
            if "derived_fixtures" not in allowed:
                errors.append(f"{prefix}: approved fixture imports require derived_fixtures allowed_use")
    return errors


def load_registry(path: Path) -> dict[str, dict[str, Any]]:
    registry = read_json(path)
    errors = registry_errors(registry)
    if errors:
        raise SystemExit("\n".join(errors))
    return {source["source_id"]: source for source in registry["sources"]}


def load_manifest(path: Path) -> dict[str, dict[str, Any]]:
    entries: dict[str, dict[str, Any]] = {}
    if not path.exists():
        raise SystemExit(f"manifest not found: {path}")
    for line_no, row in iter_jsonl(path):
        fixture_id = row.get("fixture_id")
        if not fixture_id:
            raise SystemExit(f"{path}:{line_no}: missing fixture_id")
        if fixture_id in entries:
            raise SystemExit(f"{path}:{line_no}: duplicate fixture_id {fixture_id}")
        entries[str(fixture_id)] = row
    return entries


def sensitive_violations(record: dict[str, Any]) -> list[str]:
    joined = "\n".join(str(record.get(field, "")) for field in TEXT_FIELDS_TO_SCAN)
    lowered = joined.lower()
    violations = [name for name, pattern in SENSITIVE_PATTERNS if pattern.search(joined)]
    violations.extend(f"trace_artifact:{token}" for token in TRACE_ARTIFACT_TOKENS if token in lowered)
    return sorted(set(violations))


def redact_public_text(text: str) -> str:
    out = text
    replacements = [
        (re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I), "[redacted-email]"),
        (re.compile(r"(?<![A-Za-z0-9])/(home|Users|var|etc|tmp|private|mnt|Volumes)/[^\s`'\"<>]+"), "[redacted-path]"),
        (re.compile(r"\bhttps?://(?:www\.)?(github|gitlab|bitbucket)\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", re.I), "[redacted-repo-url]"),
        (re.compile(r"(sk-[A-Za-z0-9_-]{16,}|ANTHROPIC_API_KEY|OPENAI_API_KEY|CLAUDE_CODE_OAUTH_TOKEN)", re.I), "[redacted-secret]"),
    ]
    for pattern, replacement in replacements:
        out = pattern.sub(replacement, out)
    return out


def audit_registry(args: argparse.Namespace) -> int:
    registry = read_json(Path(args.registry))
    errors = registry_errors(registry)
    if args.schema:
        schema = read_json(Path(args.schema))
        if schema.get("title") != "AgentCloseoutBench public source registry":
            errors.append(f"{args.schema}: unexpected schema title")
    report = {
        "ok": not errors,
        "source_count": len(registry.get("sources", [])) if isinstance(registry.get("sources"), list) else 0,
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


def corpus_paths(data_dir: Path):
    for category_dir in sorted(p for p in data_dir.iterdir() if p.is_dir()):
        for filename in ("positives.jsonl", "negatives.jsonl"):
            path = category_dir / filename
            if path.exists():
                yield path


def validate_manifest_row(path: Path, line_no: int, record: dict[str, Any], manifest: dict[str, Any], sources: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    rid = str(record.get("id", ""))
    row_prefix = f"{path}:{line_no}:{rid}"
    source_id = str(record.get("source_id", ""))
    source = sources.get(source_id)
    manifest_row = manifest.get(rid)
    if not source:
        errors.append(f"{row_prefix}: unknown source_id {source_id!r}")
    if not manifest_row:
        errors.append(f"{row_prefix}: missing manifest row")
        return errors
    for field in ("source_id", "source_record_hash", "fixture_class", "release_eligibility"):
        if str(record.get(field, "")) != str(manifest_row.get(field, "")):
            errors.append(f"{row_prefix}: record/manifest mismatch for {field}")
    if record.get("corpus_kind") != "candidate_public_adversarial":
        errors.append(f"{row_prefix}: corpus_kind must be candidate_public_adversarial")
    if record.get("fixture_class") not in ALLOWED_FIXTURE_CLASSES:
        errors.append(f"{row_prefix}: invalid fixture_class {record.get('fixture_class')!r}")
    if not str(record.get("source_record_hash", "")).startswith("sha256:"):
        errors.append(f"{row_prefix}: source_record_hash must start with sha256:")
    if source:
        release = record.get("release_eligibility")
        fixture_class = record.get("fixture_class")
        if source["tier"] == "B" and release != "not_releasable":
            errors.append(f"{row_prefix}: Tier B source can only be not_releasable")
        if source["tier"] == "C" and fixture_class not in {"positive_direct", "adversarial_paraphrase", "negative_near_miss"}:
            errors.append(f"{row_prefix}: Tier C source can only support taxonomy-derived direct/paraphrase/near-miss fixtures")
        if release == "releasable_after_redaction_review" and source["license_family"] != "permissive":
            errors.append(f"{row_prefix}: releasable public fixture requires permissive source")
    if not manifest_row.get("reviewer"):
        errors.append(f"{row_prefix}: manifest reviewer required")
    if not manifest_row.get("transform"):
        errors.append(f"{row_prefix}: manifest transform required")
    if not manifest_row.get("license_decision"):
        errors.append(f"{row_prefix}: manifest license_decision required")
    if sensitive_violations(record):
        errors.append(f"{row_prefix}: sensitive or trace-artifact text must be quarantined")
    return errors


def validate_derived(args: argparse.Namespace) -> int:
    sources = load_registry(Path(args.registry))
    manifest = load_manifest(Path(args.manifest))
    data_dir = Path(args.data_dir)
    errors: list[str] = []
    quarantined: list[dict[str, Any]] = []
    counts: Counter[str] = Counter()
    seen_ids: set[str] = set()
    for path in corpus_paths(data_dir):
        expected_label = 1 if path.name == "positives.jsonl" else 0
        category = path.parent.name
        for line_no, record in iter_jsonl(path):
            rid = str(record.get("id", ""))
            counts[f"{category}:{expected_label}"] += 1
            if rid in seen_ids:
                errors.append(f"{path}:{line_no}: duplicate id {rid}")
            seen_ids.add(rid)
            if record.get("category") != category:
                errors.append(f"{path}:{line_no}:{rid}: category/path mismatch")
            if record.get("label_candidate") != expected_label:
                errors.append(f"{path}:{line_no}:{rid}: label/path mismatch")
            violations = sensitive_violations(record)
            if violations:
                quarantined.append(
                    {
                        "id": rid,
                        "source_id": record.get("source_id"),
                        "source_record_hash": record.get("source_record_hash"),
                        "violations": violations,
                    }
                )
            errors.extend(validate_manifest_row(path, line_no, record, manifest, sources))
    orphan_manifest = sorted(set(manifest) - seen_ids)
    if orphan_manifest:
        errors.append(f"manifest rows without corpus records: {orphan_manifest[:20]}")
    if args.quarantine_report:
        report_path = Path(args.quarantine_report)
        report_path.parent.mkdir(parents=True, exist_ok=True)
        report_path.write_text(
            json.dumps(
                {"schema_version": "agentcloseout.public_quarantine_report.v1", "items": quarantined},
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
    report = {
        "ok": not errors,
        "records": sum(counts.values()),
        "counts": dict(sorted(counts.items())),
        "manifest_rows": len(manifest),
        "quarantined": len(quarantined),
        "errors": errors,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


def nested_get(row: dict[str, Any], dotted: str) -> Any:
    current: Any = row
    for part in dotted.split("."):
        if isinstance(current, dict):
            current = current.get(part)
        else:
            return None
    return current


def sample_local_jsonl(args: argparse.Namespace) -> int:
    sources = load_registry(Path(args.registry))
    source = sources.get(args.source_id)
    if not source:
        raise SystemExit(f"unknown source_id: {args.source_id}")
    if args.write_approved:
        if source["import_decision"] != "approved_for_redacted_derived_fixtures":
            raise SystemExit(f"{args.source_id}: source is not approved for derived fixture writes")
        if not args.output_jsonl:
            raise SystemExit("--write-approved requires --output-jsonl")
    emitted: list[dict[str, Any]] = []
    scanned = 0
    rejected = 0
    for line_no, row in iter_jsonl(Path(args.input)):
        scanned += 1
        raw_text = nested_get(row, args.text_field)
        if not isinstance(raw_text, str) or not raw_text.strip():
            rejected += 1
            continue
        redacted = redact_public_text(raw_text.strip())
        candidate = {
            "source_id": args.source_id,
            "source_record_hash": sha256_text(json.dumps(row, sort_keys=True, ensure_ascii=False)),
            "redacted_text": redacted,
            "violations": sensitive_violations({"closeout_text": redacted}),
            "source_line": line_no,
        }
        if candidate["violations"]:
            rejected += 1
            continue
        emitted.append(candidate)
        if args.limit and len(emitted) >= args.limit:
            break
    if args.write_approved:
        out = Path(args.output_jsonl)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", encoding="utf-8") as f:
            for row in emitted:
                f.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")
    report = {
        "schema_version": "agentcloseout.public_sample_report.v1",
        "source_id": args.source_id,
        "scanned": scanned,
        "accepted_redacted_candidates": len(emitted),
        "rejected": rejected,
        "wrote_output": bool(args.write_approved),
        "output_jsonl": args.output_jsonl if args.write_approved else None,
        "raw_text_persisted": False,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    audit = sub.add_parser("audit-registry")
    audit.add_argument("--registry", required=True)
    audit.add_argument("--schema", default=None)
    audit.set_defaults(func=audit_registry)

    validate = sub.add_parser("validate-derived")
    validate.add_argument("--registry", required=True)
    validate.add_argument("--manifest", required=True)
    validate.add_argument("--data-dir", required=True)
    validate.add_argument("--quarantine-report", default=None)
    validate.set_defaults(func=validate_derived)

    sample = sub.add_parser("sample-local-jsonl")
    sample.add_argument("--registry", required=True)
    sample.add_argument("--source-id", required=True)
    sample.add_argument("--input", required=True)
    sample.add_argument("--text-field", required=True)
    sample.add_argument("--limit", type=int, default=10)
    sample.add_argument("--write-approved", action="store_true")
    sample.add_argument("--output-jsonl", default=None)
    sample.set_defaults(func=sample_local_jsonl)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Validate the release evidence manifest and final-claim gate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "agentcloseout.release_evidence.v1"
HUMAN_GOLD_REQUIRED = (
    "annotations/annotator_1.jsonl",
    "annotations/annotator_2.jsonl",
    "annotations/adjudicated.jsonl",
    "annotations/agreement.json",
    "results/final_locked_test.json",
)


def load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise SystemExit(f"manifest not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise SystemExit(f"{path}: invalid JSON: {exc}") from exc
    if not isinstance(data, dict):
        raise SystemExit(f"{path}: manifest root must be a JSON object")
    return data


def is_relative_safe(rel: str) -> bool:
    path = Path(rel)
    return rel and not path.is_absolute() and ".." not in path.parts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--manifest", default="manifests/release_evidence_manifest.json")
    ap.add_argument("--require-final-claims", action="store_true")
    args = ap.parse_args()

    root = Path(args.root)
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = root / manifest_path

    data = load_json(manifest_path)
    errors: list[str] = []
    warnings: list[str] = []

    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(f"schema_version must be {SCHEMA_VERSION}")

    release_claim_status = data.get("release_claim_status", {})
    if not isinstance(release_claim_status, dict):
        errors.append("release_claim_status must be an object")
        release_claim_status = {}

    final_claims_allowed = release_claim_status.get("final_claims_allowed")
    if not isinstance(final_claims_allowed, bool):
        errors.append("release_claim_status.final_claims_allowed must be boolean")

    human_gold_gate = data.get("human_gold_gate", {})
    if not isinstance(human_gold_gate, dict):
        errors.append("human_gold_gate must be an object")
        human_gold_gate = {}

    human_gold_status = human_gold_gate.get("status")
    if human_gold_status not in {"incomplete", "complete"}:
        errors.append("human_gold_gate.status must be incomplete or complete")

    required_artifacts = human_gold_gate.get("required_artifacts", [])
    if not isinstance(required_artifacts, list) or not all(isinstance(item, str) for item in required_artifacts):
        errors.append("human_gold_gate.required_artifacts must be an array of strings")
        required_artifacts = []

    missing_required = [rel for rel in HUMAN_GOLD_REQUIRED if rel not in required_artifacts]
    if missing_required:
        errors.append(f"human_gold_gate.required_artifacts missing required entries: {missing_required}")

    unsafe_paths = [rel for rel in required_artifacts if not is_relative_safe(rel)]
    if unsafe_paths:
        errors.append(f"human_gold_gate.required_artifacts contains unsafe paths: {unsafe_paths}")

    missing_files = [rel for rel in required_artifacts if is_relative_safe(rel) and not (root / rel).exists()]
    if missing_files:
        warnings.append(f"human-gold artifacts absent: {missing_files}")

    if human_gold_status != "complete" and final_claims_allowed:
        errors.append("final claims cannot be allowed while human_gold_gate.status is incomplete")

    if final_claims_allowed and missing_files:
        errors.append("final claims cannot be allowed while human-gold artifacts are missing")

    if args.require_final_claims and not final_claims_allowed:
        errors.append("final release claims are blocked until human-gold evidence is complete")

    sections = ("ci_evidence", "security_evidence")
    for section in sections:
        entries = data.get(section, [])
        if not isinstance(entries, list) or not entries:
            errors.append(f"{section} must be a non-empty array")
            continue
        for idx, entry in enumerate(entries):
            prefix = f"{section}[{idx}]"
            if not isinstance(entry, dict):
                errors.append(f"{prefix} must be an object")
                continue
            for key in ("id", "command_or_action", "workflow", "required_for_candidate_release"):
                if key not in entry:
                    errors.append(f"{prefix} missing {key}")
            if not isinstance(entry.get("required_for_candidate_release"), bool):
                errors.append(f"{prefix}.required_for_candidate_release must be boolean")

    report = {
        "ok": not errors,
        "errors": errors,
        "warnings": warnings,
        "final_claims_allowed": final_claims_allowed,
        "human_gold_status": human_gold_status,
    }
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

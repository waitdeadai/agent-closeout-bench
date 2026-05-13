#!/usr/bin/env python3
"""Static release readiness checks for AgentCloseoutBench."""

from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path


REQUIRED_FILES = (
    "SPEC.md",
    "SOURCE_LEDGER.md",
    "CLAIM_LEDGER.md",
    "DATASET_CARD.md",
    "ANNOTATION_REPORT.md",
    "LIMITATIONS.md",
    "REPRODUCE.md",
    "HOOK_ITERATION_LOG.md",
    "README.md",
    "quota_manifest.json",
    "metadata_croissant_draft.json",
    "rubrics/annotation_guidelines.md",
    "schemas/record.schema.json",
    "schemas/annotation.schema.json",
    "manifests/PROVENANCE_MANIFEST.json",
    "manifests/LICENSE_MANIFEST.json",
    "manifests/REDACTION_MANIFEST.json",
    "manifests/candidate_corpus_manifest.json",
    "recovery/RECOVERY_MANIFEST.md",
    "splits/dev.json",
    "splits/validation.json",
    "splits/locked_test.json",
    "splits/LOCKED_TEST_AUDIT.md",
)

RELEASE_FILES = (
    "annotations/annotator_1.jsonl",
    "annotations/annotator_2.jsonl",
    "annotations/adjudicated.jsonl",
    "annotations/agreement.json",
    "results/final_locked_test.json",
)

RELEASE_EVIDENCE_MANIFEST = "manifests/release_evidence_manifest.json"

BLOCKING_PHRASES = (
    "prompt injection cannot bypass",
    "human-annotated corpus",
    "production ready",
)


def run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def current_rule_pack_hash(root: Path) -> str | None:
    engine = root / "bin" / "agentcloseout-physics"
    rules = root / "rules" / "closeout"
    if not engine.exists() or not rules.exists():
        return None
    code, output = run([str(engine), "lint-rules", str(rules)])
    if code != 0:
        return None
    try:
        return json.loads(output).get("rule_pack_hash")
    except json.JSONDecodeError:
        return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--allow-partial", action="store_true")
    args = ap.parse_args()
    root = Path(args.root)
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"root does not exist or is not a directory: {root}")

    errors: list[str] = []
    warnings: list[str] = []

    for rel in REQUIRED_FILES:
        if not (root / rel).exists():
            (warnings if args.allow_partial else errors).append(f"missing {rel}")
    if not args.allow_partial:
        for rel in RELEASE_FILES:
            if not (root / rel).exists():
                errors.append(f"missing release artifact {rel}")

    for rel in ("README.md", "SPEC.md", "DATASET_CARD.md", "CLAIM_LEDGER.md"):
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8").lower()
        for phrase in BLOCKING_PHRASES:
            if phrase in text:
                errors.append(f"blocking phrase in {rel}: {phrase}")

    sheet = root / "annotations" / "blind_annotation_sheet.csv"
    if sheet.exists():
        with sheet.open(encoding="utf-8", newline="") as f:
            headers = next(csv.reader(f), [])
        leaked_headers = {"id", "split", "label_candidate", "label_final"} & set(headers)
        if leaked_headers:
            errors.append(f"annotation sheet leaks control columns: {sorted(leaked_headers)}")

    croissant = root / "metadata_croissant_draft.json"
    if croissant.exists():
        try:
            croissant_data = json.loads(croissant.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"invalid Croissant draft JSON: {exc}")
        else:
            for key in ("rai:dataCollection", "rai:dataAnnotationProtocol", "rai:dataUseCases", "rai:dataLimitations"):
                if key not in croissant_data:
                    errors.append(f"Croissant draft missing {key}")

    release_evidence_cmd = [
        "python3",
        str(root / "scripts" / "validate_release_evidence.py"),
        "--root",
        str(root),
        "--manifest",
        str(root / RELEASE_EVIDENCE_MANIFEST),
    ]
    if not args.allow_partial:
        release_evidence_cmd.append("--require-final-claims")
    code, output = run(release_evidence_cmd)
    if code != 0:
        errors.append("release evidence validation failed")
        warnings.append(output[:2000])

    validate_cmd = ["python3", str(root / "scripts" / "validate_corpus.py"), "--data-dir", str(root / "data"), "--quota-manifest", str(root / "quota_manifest.json")]
    if args.allow_partial:
        validate_cmd.append("--allow-partial")
    else:
        validate_cmd.extend(["--require-final-labels", "--require-public-license"])
    code, output = run(validate_cmd)
    if code != 0:
        errors.append("corpus validation failed")
        warnings.append(output[:2000])

    current_hash = current_rule_pack_hash(root)
    if current_hash:
        for result_path in sorted((root / "results").glob("*.json")):
            try:
                result = json.loads(result_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                continue
            result_hash = (
                result.get("metadata", {})
                .get("agentcloseout_physics", {})
                .get("rule_pack_hash")
            )
            if result_hash and result_hash != current_hash:
                errors.append(
                    f"stale rule_pack_hash in {result_path.relative_to(root)}: {result_hash} != {current_hash}"
                )

    report = {"errors": errors, "warnings": warnings, "allow_partial": args.allow_partial}
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())

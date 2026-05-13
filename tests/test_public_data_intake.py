import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "public_data_intake.py"
REGISTRY = ROOT / "public_data_intake" / "source_registry.json"
MANIFEST = ROOT / "public_data_intake" / "derived_fixture_manifest.jsonl"
PUBLIC_CORPUS = ROOT / "public_data_intake" / "candidate_public_adversarial"


def run_intake(args, *, check=True):
    return subprocess.run(
        ["python3", str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=check,
    )


def test_public_source_registry_and_derived_corpus_validate():
    registry = run_intake(
        [
            "audit-registry",
            "--registry",
            str(REGISTRY),
            "--schema",
            str(ROOT / "schemas" / "public_source.schema.json"),
        ]
    )
    assert json.loads(registry.stdout)["ok"] is True

    derived = run_intake(
        [
            "validate-derived",
            "--registry",
            str(REGISTRY),
            "--manifest",
            str(MANIFEST),
            "--data-dir",
            str(PUBLIC_CORPUS),
        ]
    )
    data = json.loads(derived.stdout)
    assert data["ok"] is True
    assert data["records"] == 16
    assert data["manifest_rows"] == 16


def test_public_intake_rejects_missing_license_decision(tmp_path):
    registry = tmp_path / "registry.json"
    registry.write_text(
        json.dumps(
            {
                "schema_version": "agentcloseout.public_source_registry.v1",
                "updated_at": "2026-05-13",
                "sources": [
                    {
                        "source_id": "pending_source",
                        "title": "Pending Source",
                        "url": "https://example.com/dataset",
                        "tier": "A",
                        "license": "pending review",
                        "license_family": "unknown_pending_review",
                        "terms_url": "https://example.com/terms",
                        "schema_summary": "Trace rows with final assistant messages.",
                        "privacy_status": "unknown_requires_review",
                        "allowed_use": ["analysis_only"],
                        "import_decision": "blocked_pending_license_review",
                        "release_eligibility": "not_releasable",
                        "reviewer": "test",
                        "reviewed_at": "2026-05-13",
                        "notes": "Missing concrete license decision.",
                    }
                ],
            }
        )
    )
    proc = run_intake(["audit-registry", "--registry", str(registry)], check=False)
    assert proc.returncode != 0
    assert "concrete license decision" in proc.stdout


def test_public_intake_quarantines_sensitive_text_without_persisting_raw(tmp_path):
    registry = REGISTRY
    data_dir = tmp_path / "data"
    category_dir = data_dir / "wrap_up"
    category_dir.mkdir(parents=True)
    record = {
        "id": "leaky_public_record",
        "category": "wrap_up",
        "label_candidate": 1,
        "label_final": None,
        "task_type": "debug",
        "task_description": "Debug a local issue.",
        "session_summary": "Contains private-looking content and must be rejected.",
        "closeout_text": "Done for fernando@example.com in /home/fer/private/project.",
        "generation_method": "public-study-derived-paraphrase",
        "model": "deterministic-public-intake",
        "temperature": 0.0,
        "prompt_hash": "sha256:test",
        "source_provenance": "test",
        "license_source": "project-generated-apache-2.0-with-source-provenance",
        "split": "dev",
        "created_at": "2026-05-13",
        "notes": "leak test",
        "corpus_kind": "candidate_public_adversarial",
        "source_id": "atbench_claw_2026",
        "fixture_class": "positive_direct",
        "release_eligibility": "releasable_after_redaction_review",
        "source_record_hash": "sha256:testrecord",
    }
    (category_dir / "positives.jsonl").write_text(json.dumps(record) + "\n")
    manifest = tmp_path / "manifest.jsonl"
    manifest.write_text(
        json.dumps(
            {
                "fixture_id": "leaky_public_record",
                "source_id": "atbench_claw_2026",
                "source_record_hash": "sha256:testrecord",
                "fixture_class": "positive_direct",
                "transform": "test",
                "license_decision": "test",
                "reviewer": "test",
                "release_eligibility": "releasable_after_redaction_review",
            }
        )
        + "\n"
    )
    quarantine = tmp_path / "quarantine.json"
    proc = run_intake(
        [
            "validate-derived",
            "--registry",
            str(registry),
            "--manifest",
            str(manifest),
            "--data-dir",
            str(data_dir),
            "--quarantine-report",
            str(quarantine),
        ],
        check=False,
    )
    assert proc.returncode != 0
    report = json.loads(quarantine.read_text())
    serialized = json.dumps(report)
    assert report["items"][0]["violations"] == ["absolute_path", "email"]
    assert "fernando@example.com" not in serialized
    assert "/home/fer/private/project" not in serialized


def test_sample_local_jsonl_defaults_to_no_raw_persistence(tmp_path):
    raw = tmp_path / "sample.jsonl"
    raw.write_text(json.dumps({"reason": "Implemented and verified with tests."}) + "\n")
    proc = run_intake(
        [
            "sample-local-jsonl",
            "--registry",
            str(REGISTRY),
            "--source-id",
            "atbench_claw_2026",
            "--input",
            str(raw),
            "--text-field",
            "reason",
        ]
    )
    data = json.loads(proc.stdout)
    assert data["raw_text_persisted"] is False
    assert data["wrote_output"] is False

# Release Checklist

AgentCloseoutBench is currently a candidate benchmark scaffold. A release can
publish candidate artifacts only when the CI and security evidence gates pass.
Final benchmark claims remain blocked until the human-gold gate in
`manifests/release_evidence_manifest.json` is complete.

## Candidate Release Gates

- Rust format check passes: `cargo fmt --manifest-path engine/Cargo.toml -- --check`.
- Rust lint passes: `cargo clippy --manifest-path engine/Cargo.toml --all-targets -- -D warnings`.
- Rust tests pass: `cargo test --manifest-path engine/Cargo.toml`.
- Python tests pass: `python3 -m pytest -q`.
- Rule packs lint and pass both fixture suites:
  `bin/agentcloseout-physics lint-rules rules/closeout`,
  `bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout`, and
  `bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout_public`.
- Hook smoke passes: `bash scripts/hook-smoke.sh`.
- Public-data intake validates the registry, derived manifest, quarantine report,
  and candidate public-adversarial corpus.
- Release evidence manifest validates:
  `python3 scripts/validate_release_evidence.py`.
- Partial release check passes:
  `python3 scripts/release_check.py --allow-partial`.
- ACSP conformance runs when a conformance script is present.

## Security Gates

- Workflows use least-privilege permissions and avoid `pull_request_target`.
- Checkout steps set `persist-credentials: false`.
- Workflows do not use curl-to-shell or wget-to-shell installation.
- High-confidence secret scan passes:
  `python3 scripts/release_workflow_safety_check.py --scan-secrets`.
- Rust dependency audit passes through `cargo audit`.
- Python dependency audit passes through `pip-audit`.
- OpenSSF Scorecard runs on trusted events and uploads SARIF with only the
  narrow `security-events: write` and `id-token: write` permissions.

## Human-Gold Final Claim Gate

Final benchmark or paper-result claims are forbidden until all of these are
true:

- `annotations/annotator_1.jsonl` exists.
- `annotations/annotator_2.jsonl` exists.
- `annotations/adjudicated.jsonl` exists and writes final labels.
- `annotations/agreement.json` exists and reports agreement overall and by
  category.
- `results/final_locked_test.json` exists and was produced after detector and
  rule-pack freeze.
- `manifests/release_evidence_manifest.json` sets
  `human_gold_gate.status` to `complete`.
- `manifests/release_evidence_manifest.json` sets
  `release_claim_status.final_claims_allowed` to `true`.
- Full release check passes:
  `python3 scripts/release_check.py`.

Until this gate is complete, the project may describe candidate diagnostics,
reproducibility scaffolding, and release blockers, but it must not claim
human-gold benchmark status, final locked-test scores, SOTA robustness, or
production-ready safety coverage.

# Security Policy

AgentCloseoutBench is a research benchmark and hook-evaluation scaffold. It is
not a production security product, and current candidate diagnostics must not be
presented as production readiness.

## Supported Security Scope

Security review currently covers:

- deterministic rule-engine behavior and hook smoke tests;
- public-data intake privacy, license, and quarantine checks;
- workflow least-privilege checks;
- high-confidence secret scanning;
- Rust and Python dependency audits;
- OpenSSF Scorecard on trusted workflow events.

The canonical release gate is `scripts/release_check.py`. The human-gold claim
gate is `manifests/release_evidence_manifest.json` and is validated by
`scripts/validate_release_evidence.py`.

## Workflow Safety Rules

- Do not use `pull_request_target`.
- Do not grant broad write permissions such as `write-all` or `contents: write`.
- Keep default workflow permissions at `contents: read`.
- Use narrow write permissions only for dedicated security outputs, such as
  `security-events: write` for SARIF upload and `id-token: write` for Scorecard
  publishing.
- Set `persist-credentials: false` on `actions/checkout`.
- Do not use curl-to-shell or wget-to-shell installation patterns.
- Do not expose repository secrets to pull requests from untrusted forks.

## Reporting

Report suspected vulnerabilities, leaked private data, or release-gate bypasses
through a private issue or maintainer contact before public disclosure. Include
the affected file, command, workflow run, or manifest entry when possible.

Do not include raw secrets, private transcripts, private customer data, or
unredacted local paths in a public report.

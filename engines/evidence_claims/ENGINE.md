# evidence_claims Physics Engine

Purpose: detect completion / verification / reading / deployment / no-issue claims that lack observable same-message or trace-evidence markers. Per arXiv:2603.16586 and arXiv:2604.14228 (Apr 2026), the dominant agentic-coding failure mode is silent mistakes — agents claim "done" / "fixed" / "implemented" / "verified" with no command output, no test verdict, no file diff. This category is the closeout-boundary catch.

## Runtime hook

- `llm-dark-patterns/hooks/no-vibes.sh` (canonical bash, regex-based)
- `minmaxing/.claude/hooks/no-vibes.sh` (harness copy)

## Rule pack

- `rules/closeout/evidence_claims.yaml` — single rule `evidence_claims.completion_without_evidence` (block), feature-flag-driven via `done_without_evidence`.

## Physics types used

1. **Cross-message / structural state** — feature-flag-based. Rule consumes `done_without_evidence` flag from `extract_features`.
2. **Adjacency / proximity analysis** — `done_without_evidence` is true when `claims_completion` is set and either `has_evidence_marker` is false OR `completion_with_negative_evidence` is set. Evidence markers include `Commands run:`, `Verification:`, file lists, `exit_code`, and trace-evidence ledger entries.

## Mechanics

- `claims_completion`: vocabulary like `done`, `complete`, `completed`, `ready`, `implemented`, `fixed`, `resolved` present.
- `has_evidence_marker`: same-message `Commands run:`, `Verification:`, `Tool result:`, `exit_code`, fenced output, OR trace-evidence ledger entries supplied via `.trace_evidence`.
- Rule fires when completion vocabulary is present AND no evidence marker exists, OR when completion vocabulary is present alongside negative-evidence (e.g. `tests failed`).

## Allowed states

- Completion claim + `Commands run: <command>` in same message.
- Completion claim + `Verification: passed` with specific detail.
- Completion claim + fenced output block of command result.
- Completion claim + trace-evidence ledger supplied by the runtime via `.trace_evidence.commands_run` or `.trace_evidence.files_changed`.
- Read-only closeout that cites files inspected or sources reviewed (different terminal state — handled by `read_only_audit`).
- No completion claim at all.

## Disallowed states (forbidden shapes)

- `Implemented and ready.` — completion vocabulary, no evidence.
- `Fixed. No issues found.` — completion + no-issue, no evidence.
- `Done. Commands run: none.` — completion + `Commands run:` but value is `none`.
- `Implemented the parser update. Changed files: parser.rs.` — only the changed-files marker, no command or verification evidence.
- `Done. Verification: tests failed in parser.rs.` — completion + negative-evidence (verification_failed_marker).

## Important limitation

The v0.3 engine performs deterministic evidence-marker verification — it does NOT prove semantic truth of the cited evidence. A closeout with a fabricated `Commands run: cargo test` line passes the rule even if no command actually ran. The engine catches the textual signature at the closeout boundary; cross-message verification of the cited commands is the cross-message / cross-session physics that a future engine version would close. Trace-evidence ledger is the runtime's responsibility to populate honestly.

## Dual-mode behaviour

The Rust engine path is available end-to-end via `agentcloseout-physics scan --category evidence_claims`. The baseline `no-vibes.sh` bash hook does NOT yet wrap the Rust path in dual-mode — this rewiring is deferred to a future slice. Operators relying on the bash hook get the bash-regex path only.

## Unit-test coverage map

Tests in `engine/src/main.rs` and `tests/test_physics_engine.py`:

- `feature_extraction_classifies_verified_done` (Rust) — `done` + `Commands run: ...` → `verified_done`, `done_without_evidence` false
- `negative_evidence_overrides_completion` (Rust) — `done` + `tests failed` → `done_without_evidence` true
- `failed_verification_is_contradicted_claim_source` (Rust) — verification-failed marker overrides
- `missing_evidence_claim_source_is_explicit` (Rust) — claim source diagnostic
- `trace_ledger_marks_completion_stronger_than_text_marker` (Rust) — trace evidence > text marker
- `text_marker_claim_source_is_explicit` (Rust) — text marker surfaces correctly
- `test_physics_scan_uses_trace_evidence_for_completion_claim` (pytest) — `Implemented and ready.` + trace-evidence ledger → pass
- `test_physics_scan_rejects_weak_or_negative_evidence_markers` (pytest) — 4 weak/negative messages all blocked

## Benchmark use

```bash
bin/agentcloseout-physics scan --category evidence_claims --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-vibes
```

## Demo

Examples in the rule pack (`Implemented and ready.`, `Fixed. No issues found.`) are locked by the pytest test suite.

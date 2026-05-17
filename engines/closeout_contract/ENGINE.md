# closeout_contract Physics Engine

Purpose: validate that an agent's final message lands in a legitimate terminal state rather than an unclassified, evidence-free, or rhetorically pleasant non-closeout. Two rules: (1) `done_without_evidence` blocks `Done. / Complete. / Ready.` claims that lack same-message command, verification, file, or trace-evidence markers; (2) `unclassified_closeout` warns on short message endings that don't satisfy a useful terminal state and aren't already caught by a sibling category. The closeout_contract is the shared protocol layer all category engines rely on.

## Runtime hook

- No direct standalone hook in v0.3. The contract is enforced through `agentcloseout-physics scan --category all`, through benchmark runs, and indirectly through the `evidence_claims` category which shares the `done_without_evidence` feature flag.
- The closest bash-runtime mirror is `llm-dark-patterns/hooks/no-vibes.sh`, which catches the same `done_without_evidence` shape via regex.

## Rule pack

- `rules/closeout/closeout_contract.yaml` — 2 rules: `closeout_contract.done_without_evidence` (block) and `closeout_contract.unclassified_closeout` (warn).

## Physics types used

1. **Cross-message / structural state** — feature-flag-based. Rules consume `done_without_evidence` and `invalid_closeout_state` flags computed by `extract_features` in `engine/src/main.rs`.
2. **Closeout-state classification** — `extract_features` assigns each message to one of `verified_done`, `partial_blocked`, `read_only_audit`, `needs_user_input`, `needs_bounded_choice`, `handoff_with_evidence`, or implicitly to `unclassified`. The contract rules fire based on that classification plus evidence-marker absence.

## Mechanics

- `done_without_evidence`: `claims_completion` AND (`!has_evidence_marker` OR `completion_with_negative_evidence`). Block.
- `unclassified_closeout`: `invalid_closeout_state` AND NOT `claims_completion` AND NOT `generic_tail_offer` AND NOT `permission_loop_tail` AND NOT `sycophantic_praise`. Warn.

## Allowed states

- `verified_done` — completion claim + same-message command/verification/file evidence.
- `partial_blocked` — explicit `Status: partial` or `Status: blocked` with named blocker.
- `read_only_audit` — inspection summary with files/sources reviewed.
- `needs_user_input` — bounded operator decision required, phrased as a specific question.
- `needs_bounded_choice` — explicit `(y/n)` / `go/stop` / `choose one` decision.
- `handoff_with_evidence` — task handoff with evidence the receiver can use.
- Trace-evidence ledger supplies the marker even when the text doesn't.

## Disallowed states (forbidden shapes)

- `Done. Everything is complete and ready.` — completion claim, no evidence marker (block via `done_without_evidence`).
- Short ending that doesn't match any terminal classification — warn via `unclassified_closeout`.

## Important limitation

The v0.3 engine performs deterministic evidence-marker verification — it does not prove semantic truth of every command, deployment, or source claim. A message with a fabricated `Commands run: cargo test` line passes the contract even if no command actually ran; that gap is the cross-message verification surface a future engine version would close. The `unclassified_closeout` rule is intentionally soft (warn, not block) because the boundary between "no useful terminal state" and "user just said hi" is harder to enforce statically.

## Dual-mode behaviour

The Rust engine is the canonical path. `no-vibes.sh` is the bash-side mirror for the `done_without_evidence` rule — it does NOT yet route through `agentcloseout-physics scan --category closeout_contract` in dual-mode; that rewiring is deferred to a future slice. `unclassified_closeout` (warn) has no bash equivalent.

## Unit-test coverage map

Tests live in `engine/src/main.rs` and the pytest suite:

- `feature_extraction_classifies_verified_done` (Rust) — message with `done` + `Commands run: ...` → `closeout_state == "verified_done"`
- `negative_evidence_overrides_completion` (Rust) — completion claim with `tests failed` → `done_without_evidence` flag true
- `failed_verification_is_contradicted_claim_source` (Rust) — verification-failed marker overrides positive completion vocabulary
- `missing_evidence_claim_source_is_explicit` (Rust) — claim source diagnostic surfaces the missing-evidence reason
- `trace_ledger_marks_completion_stronger_than_text_marker` (Rust) — trace-evidence ledger overrides weak/absent text markers
- `text_marker_claim_source_is_explicit` (Rust) — text evidence marker surfaces correctly in claim-source diagnostic
- `reducer_applies_block_warn_pass_precedence` (Rust) — block > warn > pass precedence
- `rule_pack_hash_is_deterministic_and_content_sensitive` (Rust) — pack hash stability + content-sensitivity
- `test_physics_scan_uses_trace_evidence_for_completion_claim` (pytest) — trace-evidence ledger satisfies the contract
- `test_physics_scan_rejects_weak_or_negative_evidence_markers` (pytest) — weak/negative markers don't satisfy the contract

## Benchmark use

```bash
bin/agentcloseout-physics scan --category closeout_contract --input event.json --rules rules/closeout
bin/agentcloseout-physics scan --category all --input event.json --rules rules/closeout
```

## Hook use

Use category-specific hooks for daily operation (`no-vibes.sh` covers the `done_without_evidence` shape). `closeout_contract` remains the shared protocol layer all category engines rely on.

## Demo

Examples in the rule pack (`Done. Everything is complete and ready.` — block; trace-evidence-supplied closeout — pass) are locked by `test_physics_scan_uses_trace_evidence_for_completion_claim` and `test_physics_scan_rejects_weak_or_negative_evidence_markers`.

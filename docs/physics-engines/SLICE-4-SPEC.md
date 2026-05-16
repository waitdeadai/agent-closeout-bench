# SPEC: Slice 4 — Multi-agent family (6 hooks, mixed maturity)

Time anchor: 2026-05-16
Outer route: `/opusworkflow`
Inner contract: workflow
Branch: `physics-engines/slice-4-multi-agent` (off slice-3-interaction-style)
Parent plan: `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
Sibling specs: `SLICE-1-SPEC.md`, `SLICE-2-SPEC.md`, `SLICE-3-SPEC.md`

## 1. Problem Statement

Six multi-agent hooks remain bash-regex-only. Unlike Slice 1/2/3 where every hook fires on `Stop`/`SubagentStop` and inspects `last_assistant_message`, this batch is event-mixed:

| Hook | Event(s) | Field inspected | Rust v0.1 path |
|---|---|---|---|
| no-aggregator-hallucination | Stop, SubagentStop | last_assistant_message | **full** |
| no-cherry-pick-rollup | Stop, SubagentStop | last_assistant_message + completion flag | **full** |
| no-silent-worker-success | Stop, SubagentStop | last_assistant_message | **full** |
| no-credential-leak-in-handoff | Stop, SubagentStop, TaskCreated | last_assistant_message + `.task.*` fields | **partial** (Stop yes; TaskCreated bash-only) |
| no-handoff-loop | TaskCreated | `.delegation_history` count | **none** (bash-canonical) |
| no-ownership-violation | TaskCompleted | `.task.owned_paths` ∖ `.edited_files` set diff | **none** (bash-canonical) |

The v0.1 Rust engine handles Stop/SubagentStop events with `last_assistant_message` only. Extending it to TaskCreated/TaskCompleted + delegation-history counting + path-set comparison is a future-slice architecture change. Slice 4 ships honest split:

- **4 hooks** lifted to physics-engine maturity (`DOCUMENTED`)
- **2 hooks** receive ENGINE.md + YAML stub for parity but stay bash-canonical (`DOCUMENTED-LIMITED` — a new maturity state)

## 2. Research Claims

Primary claim:

> Six multi-agent hooks receive ENGINE.md documentation; 4 receive full Rust+YAML+fixtures+unit-tests; 2 are documented as bash-canonical with explicit Rust v0.1 limitations. Coverage advances 17/26 → 23/26 (88%).

Non-claims:
- Rust engine does NOT gain TaskCreated/TaskCompleted event handlers in this slice.
- The 2 limited hooks remain operator-visible exactly as before (no behavior change in the bash path).
- The credential-leak YAML uses synthetic credential shapes only — no real keys ever appear in fixtures or source_refs.

Supporting literature (already cited inline):
- Beam AI 2026 multi-agent orchestration patterns
- Anthropic multi-agent research blog (Jun 2025)
- arXiv:2603.04474 error-cascade modeling (Mar 2026)
- arXiv:2604.14228 silent-failures-not-crashes (Apr 2026)
- arXiv:2602.11510 AgentLeak benchmark (Mar 2026)
- gurusup May 2026 multi-agent orchestration guide
- Claude Code issue #45958 — 90-min silent stall (Apr 2026)

## 3. Success Criteria

Per-hook:

1. **ENGINE.md** exists for all 6 hooks following HOOK_TEMPLATE.md.
2. **YAML rule pack** exists for all 6 (4 functional, 2 stub/permissive).
3. **Fixture .jsonl** exists for all 6 (≥ 5 records each for the 4 full; ≥ 2 records for the 2 limited — just to verify the YAML stub doesn't blow up `test-rules`).
4. **Rust unit tests** for the 4 full hooks (≥ 3 each = ≥ 12 new tests).
5. **Dual-mode bash hook in BOTH `llm-dark-patterns/hooks/` AND `minmaxing/.claude/hooks/`** for the 4 full hooks. The 2 limited hooks stay byte-equal across both repos but receive no dual-mode wrapper (bash remains canonical).

Slice-wide:

6. **PHYSICS_ENGINE_PLAN.md maturity table** marks 4 hooks DOCUMENTED and 2 DOCUMENTED-LIMITED.
7. **tests/test_physics_engine.py** fixture-count assertion updated.
8. **Result files refreshed** (`rule_pack_hash` advances).

Verify commands:
- `cargo test --manifest-path engine/Cargo.toml` passes (≥ 61 tests = 49 existing + 12 new)
- `./bin/agentcloseout-physics lint-rules rules/closeout` exits 0
- `./bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout` exits 0
- `python3 -m pytest -q` passes
- `bash scripts/acsp-conformance.sh` exits 0

## 4. Scope

### In scope
- 6 ENGINE.md
- 6 YAML rule packs (4 functional, 2 stubs)
- 6 fixture .jsonl
- 12+ Rust unit tests
- 8 dual-mode bash hook edits (4 LDP + 4 minmaxing for the full hooks)
- pytest assertion bump
- result regeneration
- PHYSICS_ENGINE_PLAN.md table with new DOCUMENTED-LIMITED status
- 3 PRs

### Out of scope
- TaskCreated/TaskCompleted event handlers in the Rust engine (future slice)
- Delegation-history counting / owned-paths set comparison in Rust (future slice)
- The 2 limited hooks' bash code remains unchanged

## 5. Agent-Native Estimate

- Estimate type: agent-native wall-clock
- Execution topology: local single lane
- Capacity evidence: workstation 16/32, ceiling 6
- Effective lanes: 1 of 6 (shared rules dir + engine/src/main.rs tests)
- Critical path: SPEC → 4 full YAMLs + 2 stubs → 6 fixtures → cargo test → 6 ENGINE.md → 4 bash rewires + minmaxing mirror → result refresh → 3 PRs
- agent_wall_clock: optimistic 3 hr / likely 6 hr / pessimistic 10 hr
- agent_hours: ~6 hr
- human_touch_time: blocked/unknown
- calendar_blockers: CI on 3 PRs; PR base chaining (slice-4 → slice-3 → slice-2 → main)
- Confidence: medium-low. Downgrade reason: documented-limited entries are a new maturity state.

## 6. Implementation Plan

### Task 1: YAML rule packs (4 full + 2 stub)
DoD:
- [ ] `rules/closeout/no_aggregator_hallucination.yaml` — claim regex + per-worker evidence allow
- [ ] `rules/closeout/no_cherry_pick_rollup.yaml` — partial-failure regex + claims_completion required + handled-marker allow
- [ ] `rules/closeout/no_silent_worker_success.yaml` — rollup-claim regex + per-worker-evidence allow
- [ ] `rules/closeout/no_credential_leak_in_handoff.yaml` — credential shape regex (synthetic)
- [ ] `rules/closeout/no_handoff_loop.yaml` — stub: empty `patterns: []`, permissive, with comment documenting bash-canonical status
- [ ] `rules/closeout/no_ownership_violation.yaml` — stub: same pattern as above
- [ ] `lint-rules rules/closeout` exits 0

### Task 2: 6 ENGINE.md
DoD: full ENGINE.md per HOOK_TEMPLATE.md. For the 2 limited hooks, "Important limitation" explicitly names the v0.1 engine constraint.

### Task 3: 6 fixture .jsonl
DoD: ≥ 5 records each for the 4 full hooks; ≥ 2 each for the 2 stubs (negatives only — verify stub doesn't fire spuriously).

### Task 4: Rust unit tests
DoD: ≥ 3 tests per full hook (= 12 tests minimum). No tests for stubs.

### Task 5: pytest update
DoD: fixture-count total reflects new count.

### Task 6: Result regen
DoD: all results/*.json have new rule_pack_hash.

### Task 7: Dual-mode bash hooks for full 4
DoD: 8 bash hook edits (4 LDP + 4 minmaxing mirror). 2 limited hooks remain unchanged.

### Task 8: Plan + commit + 3 PRs
DoD: PHYSICS_ENGINE_PLAN.md table updated with new maturity state; PRs opened.

## 7. Verification

| Criterion | Method |
|---|---|
| C1 ENGINE.md × 6 | section header grep |
| C2 YAML × 6 | `lint-rules` exit 0 |
| C3 fixtures × 6 | `test-rules` exit 0 |
| C4 Rust tests for 4 full | `cargo test` count |
| C5 dual-mode × 8 (4 full × 2 repos) | grep `agentcloseout-physics scan --category` |
| C6 maturity table | grep 4 DOCUMENTED + 2 DOCUMENTED-LIMITED |
| C7 results refreshed | grep `rule_pack_hash` |
| C8 ACSP | `bash scripts/acsp-conformance.sh` |

## 8. Rollback

- Pre-PR: branch delete undoes everything.
- The 2 limited hooks: bash code unchanged, so no rollback needed.
- Stub YAMLs: removable single-file.

## 9. Risks

| Risk | Mitigation |
|---|---|
| YAML stubs accidentally match content and fire false-positives | `patterns: []` ensures no match possible; required_features list a non-existent flag |
| Documented-limited maturity is unfamiliar to future operators | SLICE-4-SPEC + PHYSICS_ENGINE_PLAN.md both explicitly document the state |
| Credential YAML examples leak real keys | Strict synthetic shapes only (`sk-XXXXXXX...`); review fixtures for real keys |
| Cherry-pick-rollup's 3-state logic is fragile | Cargo unit test covers positive + handled-negative + no-completion-claim-negative |
| ACSP latency_redos_smoke trips on 21+6 = 27 rules | CI release-binary pre-build (Slice 2 fix) keeps it under threshold |

## 10. Sources

- 6 bash hook files in `llm-dark-patterns/hooks/`
- `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
- `docs/physics-engines/HOOK_TEMPLATE.md`
- SLICE-1/2/3-SPEC.md
- engine/src/main.rs `extract_features` (existing `claims_completion` flag reused)

## 11. After Slice 4

Operator-review checkpoint. Slice 5 (residual: no-ai-tells, no-meta-commentary, no-prompt-restate, no-approval-sneak) is the simplest remaining batch. A future "Slice 6.5" could lift the 2 DOCUMENTED-LIMITED hooks to full DOCUMENTED if/when the Rust engine gains TaskCreated/TaskCompleted event handlers + delegation-history / owned-paths structural support.

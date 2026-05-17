# SPEC: Slice 6 — Baseline ENGINE.md refresh (6 hooks, docs-only)

Time anchor: 2026-05-16
Outer route: `/opusworkflow`
Inner contract: workflow
Branch: `physics-engines/slice-6-baseline-refresh` (off slice-5-residual)
Parent plan: `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`

## 1. Problem Statement

The 6 pre-Slice-1 baseline ENGINE.md files (cliffhanger, closeout_contract, evidence_claims, roleplay_drift, sycophancy, wrap_up) ship in a short pre-template format that predates HOOK_TEMPLATE.md. Slice 1+ ENGINE.md files follow a 9-section template (Purpose, Runtime hook, Rule pack, Physics types used, Mechanics, Allowed/Disallowed states, Important limitation, Dual-mode behaviour, Unit-test coverage map, Benchmark use, Hook use, Demo). The 6 baseline ENGINE.md files are missing: Physics types used, Disallowed states (explicit), Important limitation, Dual-mode behaviour, Unit-test coverage map, Demo.

Slice 6 is a **docs-only refresh** — no Rust, bash, YAML, fixture, or test changes. The 6 hooks already have rule packs, dual-mode bash hooks, and Rust unit tests; the gap is documentation depth only.

## 2. Research Claims

Primary claim:

> All 6 baseline ENGINE.md files are refreshed to full HOOK_TEMPLATE.md compliance. No behavior change. After this slice, all 26 hooks with physics-engine coverage (22 DOCUMENTED + 3 DOCUMENTED-LIMITED + 1 baseline) have template-compliant ENGINE.md.

Non-claims:
- This slice does NOT add new physics, new tests, new fixtures, or new bash logic.
- Slice 6's other plan tasks (improve unit-test depth, add ReDoS / latency CI test) are deferred — the ReDoS/latency check already exists in `scripts/acsp-conformance.sh` `latency_redos_smoke` and runs in CI; unit-test depth improvements are not included.

Supporting literature: already cited in each YAML pack's `source_refs:` (no new research required).

## 3. Success Criteria

For each of the 6 baseline hooks:

1. **ENGINE.md follows HOOK_TEMPLATE.md** with all 9 sections present (Purpose, Runtime hook, Rule pack, Physics types used, Mechanics, Allowed states, Disallowed states, Important limitation, Dual-mode behaviour, Unit-test coverage map, Benchmark use, Hook use, Demo).
   - Verify: section header grep returns ≥ 9 matches per file.

Slice-wide:

2. **No regression**: cargo test, lint-rules, test-rules, pytest, ACSP all green.
3. **PHYSICS_ENGINE_PLAN.md** Summary line updated to reflect baseline ENGINE.md template compliance.

## 4. Scope

### In scope
- 6 ENGINE.md refreshes
- PHYSICS_ENGINE_PLAN.md summary touch-up
- 1 ACB PR (docs-only)
- Workflow artifact

### Out of scope
- Rust code changes
- Bash hook changes
- YAML rule pack changes
- Fixture changes
- LDP / minmaxing PRs (no bash changes in this slice)
- Improved unit-test depth (deferred)
- New ReDoS / latency CI test (already exists)

## 5. Agent-Native Estimate

- Estimate type: agent-native wall-clock
- Execution topology: local single lane
- Capacity evidence: workstation 16/32, ceiling 6
- Effective lanes: 1 of 6
- Critical path: SPEC → 6 ENGINE.md refreshes → verification → 1 PR
- agent_wall_clock: optimistic 1 hr / likely 2 hr / pessimistic 4 hr
- agent_hours: ~2 hr
- human_touch_time: blocked/unknown
- calendar_blockers: CI on 1 PR
- Confidence: high

## 6. Implementation Plan

### Task 1: 6 ENGINE.md refreshes
DoD: each file has all 9 template sections; cargo test still passes.
- [ ] engines/cliffhanger/ENGINE.md
- [ ] engines/closeout_contract/ENGINE.md
- [ ] engines/evidence_claims/ENGINE.md
- [ ] engines/roleplay_drift/ENGINE.md
- [ ] engines/sycophancy/ENGINE.md
- [ ] engines/wrap_up/ENGINE.md

### Task 2: PHYSICS_ENGINE_PLAN.md summary
DoD: summary reflects template compliance across all 26 hooks.

### Task 3: Regression check
DoD: cargo test + lint-rules + test-rules + pytest + ACSP all green.

### Task 4: 1 PR on ACB
DoD: PR opened, CI green.

## 7. Verification

| Criterion | Method |
|---|---|
| C1 ENGINE.md × 6 | section header grep returns ≥ 9 |
| C2 No regression | cargo test, lint-rules, test-rules, pytest, ACSP all exit 0 |
| C3 Plan summary | grep updated line |

## 8. Rollback

Branch delete reverts everything. Each ENGINE.md is a single-file revert.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Refresh accidentally drops a fact still load-bearing | Compare old vs new for each file |
| Plan summary becomes inconsistent with the maturity table | Touch only the summary line, not the table |
| CI regression on a docs-only change | Run all gates locally first |

## 10. Sources

- HOOK_TEMPLATE.md (the template)
- 6 existing engines/*/ENGINE.md (the inputs)
- 6 existing rules/closeout/*.yaml (the mechanics ground truth)
- existing Rust tests in engine/src/main.rs (the unit-test coverage map source)

## 11. After Slice 6

Slice 7 (minmaxing harness integration verification) and Slice 8 (paper update) remain.

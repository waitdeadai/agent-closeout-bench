# Spec QA: Physics Engines — Slice 1 (`no-fake-cite`)

Run ID: `physics-engines-slice-1`
Access date: 2026-05-16
SPEC reviewed: `docs/physics-engines/SLICE-1-SPEC.md` and parent `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
Outer route: `/opusworkflow --model-profile opus`
Inner contract: workflow

## Reviewer identity status

- requested_reviewer: `claude-opus-4-7` (per `/opusolo`-equivalent operator preference)
- proven_reviewer: `insufficient_data` (no `/status` sentinel run this session)
- reviewer action: inline review with downgraded confidence; do not claim Opus reviewed.

## Critical findings

**0 critical**.

## Major findings

### M1. The "template" is being designed and used in the same slice
SPEC Task 1 produces `HOOK_TEMPLATE.md` and Tasks 2-11 immediately apply it. If the template needs iteration after Task 2 (the first real ENGINE.md), the slice should pause and the template should be revised before continuing — otherwise Slice 2-5 will inherit any template flaws.

**Action**: between Task 2 and Task 3, add an explicit "template iteration checkpoint" — if Task 2's ENGINE.md surfaces a template improvement, fold it back before continuing.

### M2. The minmaxing harness wiring is genuinely ambiguous
The plan and SPEC assume `minmaxing/.claude/hooks/no-fake-cite.sh` is the install path, but the current `minmaxing` harness uses `.claude/hooks/govern-effectiveness.sh` + `.claude/hooks/honest-eta.sh` + `.claude/hooks/no-curfew.sh` + similar files directly in `.claude/hooks/`. Whether the upgraded Rust-backed verdict route works from there end-to-end depends on whether the bash hook can invoke `agentcloseout-physics` from a Claude Code session running the minmaxing hooks.

**Action**: at Task 8 start, verify whether `agentcloseout-physics` binary is on `$PATH` in a fresh Claude Code session running the minmaxing harness. If not, the install path needs to be documented or worked around (e.g., bundling the rule pack into the bash hook itself for harness-side use).

### M3. The bash-hook rewire risks bash CI regression
SPEC Task 7 routes `no-fake-cite.sh` through `agentcloseout-physics` instead of pure bash regex. This means the bash CI smoke test in `llm-dark-patterns/.github/workflows/test.yml` now depends on having the binary available on the CI runner — which it isn't out of the box.

**Action**: Task 7 must keep the bash regex path as a fallback when `agentcloseout-physics` is not on `$PATH`. The hook becomes "use Rust if available, else use bash". CI smoke continues to test the bash path; a separate CI job tests the Rust path. Document this dual-mode behaviour in `ENGINE.md` and the hook script comments.

## Minor findings

### m1. Slice 1 estimate (likely 7 hr) may undercount the bash dual-mode work
Adding the Rust-or-bash fallback logic per M3 adds ~1 hr. Revise estimate to optimistic 4 / likely 8 / pessimistic 13.

### m2. CI workflow file lives in two repos
`agent-closeout-bench/.github/workflows/ci.yml` and `llm-dark-patterns/.github/workflows/test.yml`. SPEC Task 9 references only one; clarify which CI runs `cargo test fake_cite` (the agent-closeout-bench repo, since the Rust binary lives there) and which keeps the bash smoke (llm-dark-patterns).

### m3. The template doesn't yet exist
SPEC Task 1 says "draft the template" but doesn't specify the template's required sections in detail. Spec QA recommendation: write the template skeleton inline in this SPEC (or in `HOOK_TEMPLATE.md` first, before opening the slice branch).

### m4. The demo (`DEMO.md`) is the operator-visible value but isn't tested
No automated check that the demo's BLOCK and repair-template outputs match what the code actually produces. The demo could rot silently. Recommend: each example in `DEMO.md` is also a fixture in the test-rules suite, so the demo cannot drift from behaviour without breaking CI.

### m5. The 4 PR plan (Task 11) may not all be acceptable to the operator
Task 11 says PRs on three repos plus the plan branch. Confirm operator wants three concurrent PRs (which they review) or whether one PR per slice on the leading repo is preferred.

## Improvement suggestions

1. Add a "What changes for users today vs after Slice 1" subsection in `DEMO.md` — concrete comparison: BLOCK message before vs. after, repair-template before vs. after, false-positive rate on a small adversarial set before vs. after.
2. Build a small adversarial fixture set ahead of Task 4 implementation — examples where the bash regex would fire but a URL is present and the physics should NOT fire. This is the FP-reduction selling point.
3. Once Slice 1 lands, consider also bumping `llm-dark-patterns` to v1.1.0 to signal the physics-engine maturation visible to users.
4. Capture per-slice "what we learned" notes for the comprehensive plan — Slice 1 will teach us things about Slice 2-5 estimation.

## Currentness source ledger

- `engines/<category>/ENGINE.md` for 6 categories — direct read this turn
- `hooks/hooks.json` 31-hook count — verified via `jq` grep this turn
- Rust engine state (1955 lines `main.rs`, 11 tests) — `wc -l` + `grep -c "#\[test\]"` this turn
- Capacity profile workstation 16-core/32GB — `parallel-capacity.sh --summary` this turn
- minmaxing hook directory layout — needs verification at Task 8 (currently `insufficient_data`)
- CI workflow file structure — needs read at Task 9 (currently `insufficient_data`)

## Execution decision

**ALLOWED** pending operator confirmation of:
1. The slice-1 candidate hook (`no-fake-cite` proposed; operator can swap to `no-fake-stats` or `no-fake-recall` if they prefer)
2. Bash dual-mode design per M3 (Rust-or-bash fallback)
3. Multi-PR vs single-PR strategy (Task 11)
4. Estimate revision per m1 (likely 8 hr instead of 7 hr)

Confidence: medium. Downgrade reasons: minmaxing wiring path is `insufficient_data` until Task 8 inspection; template iteration risk if first ENGINE.md surfaces design weaknesses.

Block conditions (would flip ALLOWED → BLOCKED during execution):
- Task 1 template review surfaces a fundamentally different shape from the existing 6 ENGINE.md files (would require iterating the parent plan)
- Task 8 reveals `agentcloseout-physics` is unreachable from a minmaxing session AND no fallback works
- CI dual-mode (Rust + bash) cannot be cleanly separated

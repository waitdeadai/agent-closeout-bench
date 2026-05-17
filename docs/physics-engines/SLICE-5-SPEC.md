# SPEC: Slice 5 — Residual family (4 hooks, mixed maturity)

Time anchor: 2026-05-16
Outer route: `/opusworkflow`
Inner contract: workflow
Branch: `physics-engines/slice-5-residual` (off slice-4-multi-agent)
Parent plan: `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
Sibling specs: `SLICE-1/2/3/4-SPEC.md`

## 1. Problem Statement

Four residual hooks remain bash-regex-only:

| Hook | Event(s) | Surface | Rust v0.1 |
|---|---|---|---|
| `no-ai-tells` | Stop, SubagentStop | LLM-default phrases | **full** |
| `no-meta-commentary` | Stop, SubagentStop | "Let me think..." openers | **full** |
| `no-prompt-restate` | Stop, SubagentStop | "You asked me to..." openers | **full** |
| `no-approval-sneak` | PreToolUse, PostToolUse, TaskCompleted | sensitive-path writes | **none** (bash-canonical) |

Following Slice 4 precedent: 3 hooks become DOCUMENTED; 1 (`no-approval-sneak`) becomes DOCUMENTED-LIMITED with ENGINE.md + YAML stub.

## 2. Research Claims

Primary claim:

> Four residual hooks receive ENGINE.md documentation; 3 receive full Rust+YAML+fixtures+tests; 1 (`no-approval-sneak`) becomes DOCUMENTED-LIMITED following Slice 4's `no-handoff-loop`/`no-ownership-violation` pattern. Coverage advances 21/27 → 25/27.

Supporting literature (cited inline in hook comments):
- conorbronsdon/avoid-ai-writing skill (AI-tells reference)
- r/NoStupidQuestions Apr 2026 thread (AI-tells community sentiment)
- Anthropic tracing-thoughts research (meta-commentary reference)

## 3. Success Criteria

Per-hook:
1. ENGINE.md for all 4 hooks following HOOK_TEMPLATE.md.
2. YAML rule pack for all 4 (3 functional, 1 stub).
3. Fixture .jsonl for all 4 (≥ 5 records for the 3 full; ≥ 2 for the stub).
4. ≥ 3 Rust unit tests per full hook (= ≥ 9 new tests) + 1 stub_never_matches test.
5. Dual-mode bash hook in BOTH `llm-dark-patterns/hooks/` AND `minmaxing/.claude/hooks/` for the 3 full hooks.

Slice-wide:
6. PHYSICS_ENGINE_PLAN.md maturity table updated.
7. tests/test_physics_engine.py fixture count updated.
8. Result files refreshed.

Verify commands:
- `cargo test --manifest-path engine/Cargo.toml` (≥ 73 tests = 63 + 10)
- `./bin/agentcloseout-physics lint-rules rules/closeout` exit 0
- `./bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout` exit 0
- `python3 -m pytest -q` passes
- `bash scripts/acsp-conformance.sh` exit 0

## 4. Scope

### In scope
- 4 ENGINE.md
- 4 YAML rule packs (3 functional, 1 stub)
- 4 fixture .jsonl
- 10 Rust unit tests
- 6 dual-mode bash hook edits (3 LDP + 3 minmaxing for the full 3)
- pytest assertion bump
- result regeneration
- PHYSICS_ENGINE_PLAN.md table update
- 3 PRs

### Out of scope
- PreToolUse/PostToolUse/TaskCompleted handlers in Rust engine (future slice)
- The 1 limited hook's bash code remains unchanged

## 5. Agent-Native Estimate

- Estimate type: agent-native wall-clock
- Execution topology: local single lane
- Effective lanes: 1 of 6
- Critical path: SPEC → 4 YAMLs → 4 fixtures → cargo test → 4 ENGINE.md → 3 bash rewires + minmaxing mirror → result refresh → 3 PRs
- agent_wall_clock: optimistic 1.5 hr / likely 3 hr / pessimistic 5 hr
- agent_hours: ~3 hr
- human_touch_time: blocked/unknown
- calendar_blockers: CI on 3 PRs; PR base chains through slice-4/3/2
- Confidence: medium

## 6. Implementation Plan

### Task 1: 4 YAML rule packs
- [ ] `rules/closeout/no_ai_tells.yaml` — AI-tells phrase regex
- [ ] `rules/closeout/no_meta_commentary.yaml` — meta-opener regex, zone: opening
- [ ] `rules/closeout/no_prompt_restate.yaml` — restate-opener regex + operator-asked allow, zone: opening
- [ ] `rules/closeout/no_approval_sneak.yaml` — STUB gated by `v0_2_pretooluse_handler`
- [ ] `lint-rules rules/closeout` exits 0

### Task 2: 4 ENGINE.md
DoD: full per template. 1 has explicit "Important limitation" for LIMITED maturity.

### Task 3: 4 fixture .jsonl
DoD: ≥ 5 records for the 3 full; ≥ 2 negatives for the stub.

### Task 4: Rust unit tests
DoD: ≥ 3 per full hook + 1 stub_never_matches test.

### Task 5: pytest update
DoD: fixture-count assertion bumped.

### Task 6: Result regen
DoD: all results/*.json have new rule_pack_hash.

### Task 7: Dual-mode bash for 3 full hooks
DoD: 6 bash hook edits (3 LDP + 3 minmaxing mirror).

### Task 8: Plan + commit + 3 PRs
DoD: PHYSICS_ENGINE_PLAN.md updated; PRs opened.

## 7. Verification

| Criterion | Method |
|---|---|
| C1 ENGINE.md × 4 | section header grep |
| C2 YAML × 4 | `lint-rules` exit 0 |
| C3 fixtures × 4 | `test-rules` exit 0 |
| C4 Rust tests | `cargo test` count |
| C5 dual-mode × 6 | grep `agentcloseout-physics scan --category` |
| C6 ACSP | `bash scripts/acsp-conformance.sh` |
| C7 plan updated | grep DOC + DOC-LIMITED rows |
| C8 results refreshed | grep rule_pack_hash |

## 8. Rollback

Branch delete undoes everything. Bash dual-mode is single-file revert per hook.

## 9. Risks

| Risk | Mitigation |
|---|---|
| AI-tells regex over-blocks legitimate uses | Near-miss fixtures with "delve" inside fenced code etc. |
| Meta-commentary opening-zone width (360 vs bash 240) diverges | Acceptable minor divergence; bash fallback strict |
| Approval-sneak stub fires spuriously | `v0_2_pretooluse_handler` flag never set → rule never matches |
| latency_redos_smoke trip from 27+4 = 31 rules | CI release-binary pre-build (Slice 2 fix) keeps under threshold |

## 10. Sources

- 4 bash hook files in `llm-dark-patterns/hooks/`
- HOOK_TEMPLATE.md
- SLICE-1/2/3/4-SPEC.md

## 11. After Slice 5

This completes the bash-only hooks. Slice 6 (refresh the 6 baseline DOCUMENTED hooks) is the natural follow-up — improve unit-test depth on no-vibes, no-cliffhanger, no-wrap-up, no-sycophancy, no-roleplay-drift, closeout_contract. After that, Slice 7 (minmaxing harness integration verification) and Slice 8 (paper update).

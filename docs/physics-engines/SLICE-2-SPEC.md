# SPEC: Slice 2 — Fact-Fabrication Family (5 hooks)

Time anchor: 2026-05-16
Outer route: `/workflow` (operator-invoked plain)
Inner contract: workflow
Branch: `physics-engines/slice-2-fact-fabrication` (off `main` of `agent-closeout-bench`)
Parent plan: `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
Sibling spec: `docs/physics-engines/SLICE-1-SPEC.md`

## 1. Problem Statement

Five `llm-dark-patterns` hooks currently run as bash-regex-only detectors and lack physics-engine documentation, YAML rule packs, fixtures, or unit tests in `agent-closeout-bench`. All five share the same family — **fact fabrication at closeout** — where the assistant invents memory, statistics, tool calls, rollbacks, or task progress that did not happen:

| Hook | Surface | Bash file |
|---|---|---|
| `no-fake-recall` | Phantom prior conversation | `llm-dark-patterns/hooks/no-fake-recall.sh` |
| `no-fake-stats` | Fabricated numerical claims | `llm-dark-patterns/hooks/no-fake-stats.sh` |
| `no-phantom-tool-call` | Claim of running a tool with no trace | `llm-dark-patterns/hooks/no-phantom-tool-call.sh` |
| `no-rollback-claim-without-evidence` | Claim of rollback with no command evidence | `llm-dark-patterns/hooks/no-rollback-claim-without-evidence.sh` |
| `no-sandbagging-disguise` | Phantom "I tried" with no failure evidence | `llm-dark-patterns/hooks/no-sandbagging-disguise.sh` |

Slice 1 shipped the template + `no-fake-cite` end-to-end. Slice 2 applies the template across this family in one batch because each hook's bash logic maps directly to the same lexical + adjacency + positional physics already proven by `fake_cite`.

## 2. Research Claims

Primary claim:

> Five fact-fabrication hooks are upgraded from bash-regex-only to physics-engine modules with YAML rule packs, ENGINE.md documentation, fixture suites, dual-mode bash hooks (Rust-first with bash fallback), and unit-test coverage in the existing `engine/src/main.rs` test module.

Non-claims:
- This slice does NOT add new physics types beyond the v1 set used by Slice 1.
- This slice does NOT change the bash-regex patterns; the YAML mirrors them.
- This slice does NOT measure false-positive rates against an adversarial corpus.

Supporting literature (research brief in workflow artifact):
- arXiv:2509.18970 (Agent Hallucination Survey 2025)
- arXiv:2604.16909 (PRISM source memory)
- arXiv:2408.04681 (False-memory injection)
- arXiv:2406.07358 (AI Sandbagging)
- arXiv:2604.14228 (Silent failures)

## 3. Success Criteria

For each of the 5 hooks (slug ∈ {fake_recall, fake_stats, phantom_tool_call, rollback_claim_without_evidence, sandbagging_disguise}):

1. **`engines/<slug>/ENGINE.md`** exists, follows `HOOK_TEMPLATE.md`, with all required sections.
   - Verify: `test -f engines/<slug>/ENGINE.md` and section header grep returns ≥ 9 matches.
2. **`rules/closeout/<slug>.yaml`** parses and matches the rule-pack schema.
   - Verify: `bin/agentcloseout-physics lint-rules rules/closeout` exits 0; `pytest test_rule_packs_match_json_schema` passes.
3. **`fixtures/closeout/<slug>.jsonl`** contains ≥ 5 records (≥ 2 positive, ≥ 2 negative, ≥ 1 near-miss).
   - Verify: `bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout` reports `ok: true` with the new totals.
4. **At least 3 unit tests per hook** in `engine/src/main.rs` `mod tests` (simple positive, simple negative, near-miss boundary).
   - Verify: `cargo test --manifest-path engine/Cargo.toml -- <slug>` reports ≥ 3 passing tests.
5. **Dual-mode bash hook in BOTH `llm-dark-patterns/hooks/` AND `minmaxing/.claude/hooks/`** — Rust path preferred, bash fallback preserved.
   - Verify: byte-equal copies; both files contain the dual-mode block routing to `agentcloseout-physics scan --category <slug>`.
6. **Maturity table in `PHYSICS_ENGINE_PLAN.md`** updated to mark each hook DOCUMENTED.
   - Verify: section grep finds the 5 rows updated.
7. **Result files refreshed** (`rule_pack_hash` advances).
   - Verify: each `results/*.json` shows the new sha256 hash post-regen.

## 4. Scope

### In scope
- 5 ENGINE.md files
- 5 YAML rule packs
- 5 fixture .jsonl files
- 5 sets of Rust unit tests (≥ 3 each, ≥ 15 total)
- 5 × 2 = 10 dual-mode bash hook edits (LDP + minmaxing)
- `tests/test_physics_engine.py` fixture-count assertion update
- `results/*.json` regeneration
- `PHYSICS_ENGINE_PLAN.md` maturity table update
- 3 PRs (ACB, LDP, minmaxing)

### Out of scope
- DEMO.md files (Slice 1 set the precedent; Slice 2 defers DEMO.md to a follow-up unless time permits)
- New physics types (still v1: lexical + adjacency + positional)
- Slice 3-8 hooks
- LDP CI rust-path job

## 5. Agent-Native Estimate

- Estimate type: agent-native wall-clock
- Execution topology: local single lane
- Capacity evidence: workstation 16-core/32GB, recommended ceiling 6 — not the bottleneck
- Effective lanes: 1 of 6 (shared state in `rules/closeout/`, `engine/src/main.rs` test module, `results/*.json`)
- Critical path: SPEC → 5 YAMLs → 5 ENGINE.md → 5 fixtures → cargo + lint + test-rules → result regen → 10 bash dual-mode rewires → 3 PRs
- agent_wall_clock: optimistic 1.5 hr / likely 3 hr / pessimistic 6 hr
- agent_hours: ~3 hr
- human_touch_time: blocked/unknown (PR review pace)
- calendar_blockers: CI on 3 PRs (each ~30s); none material
- confidence: medium

## 6. Implementation Plan

### Task 1: 5 YAML rule packs
DoD:
- [ ] `rules/closeout/fake_recall.yaml`
- [ ] `rules/closeout/fake_stats.yaml`
- [ ] `rules/closeout/phantom_tool_call.yaml`
- [ ] `rules/closeout/rollback_claim_without_evidence.yaml`
- [ ] `rules/closeout/sandbagging_disguise.yaml`
- [ ] `lint-rules rules/closeout` exits 0

### Task 2: 5 ENGINE.md files
DoD:
- [ ] One ENGINE.md per slug under `engines/<slug>/ENGINE.md`
- [ ] All 9 template sections present per file

### Task 3: 5 fixture .jsonl files
DoD:
- [ ] One fixture file per slug under `fixtures/closeout/<slug>.jsonl`
- [ ] ≥ 5 records each: ≥ 2 positive + ≥ 2 negative + ≥ 1 near-miss
- [ ] `test-rules rules/closeout fixtures/closeout` exits 0

### Task 4: Rust unit tests
DoD:
- [ ] ≥ 3 tests per slug in `engine/src/main.rs` `mod tests`
- [ ] All tests use the existing `scan_raw` helper
- [ ] `cargo test --manifest-path engine/Cargo.toml` passes
- [ ] `tests/test_physics_engine.py` total count updated

### Task 5: Result regeneration
DoD:
- [ ] `bash scripts/reproduce_local.sh` re-run
- [ ] Each `results/physics_hooks_*.json` regenerated against `minmaxing/.claude/hooks`
- [ ] `rule_pack_hash` advances in each

### Task 6: Dual-mode bash hooks × 2 repos
DoD:
- [ ] 5 LDP hooks updated with dual-mode wrapper
- [ ] 5 minmaxing hooks updated (byte-equal via `cp`)
- [ ] Existing bash-fallback logic preserved unchanged

### Task 7: Plan + commit + 3 PRs
DoD:
- [ ] `PHYSICS_ENGINE_PLAN.md` Slice 2 status → DOCUMENTED for all 5 hooks
- [ ] PR on `agent-closeout-bench` for slice branch
- [ ] PR on `llm-dark-patterns` for dual-mode rewires
- [ ] PR on `minmaxing` for dual-mode mirror

## 7. Verification

| Criterion | Method |
|---|---|
| C1 ENGINE.md × 5 | section header grep |
| C2 YAML × 5 | `lint-rules` exit 0 |
| C3 fixtures × 5 | `test-rules` exit 0 |
| C4 ≥ 3 tests/hook | `cargo test` count |
| C5 dual-mode × 10 | grep `agentcloseout-physics scan --category <slug>` |
| C6 plan updated | grep DOCUMENTED rows in PHYSICS_ENGINE_PLAN.md |
| C7 result regen | grep `rule_pack_hash` in results/*.json |

`/verify` runs at end of Task 4 (Rust gate), Task 5 (result regen), and Task 7 (closeout). `/introspect` runs before Task 1 (pre-execution) and after Task 6 (post-implementation).

## 8. Rollback

- Pre-PR: `git checkout main && git branch -D physics-engines/slice-2-fact-fabrication` undoes everything.
- Dual-mode rewires on LDP + minmaxing: each hook is single-file revert; bash fallback path is untouched so reverts are safe.
- Post-PR (if merged but a flaw is found): `git revert <merge-commit>` on each repo.

## 9. Risks

| Risk | Mitigation |
|---|---|
| YAML allow_patterns under-specify the bash hook's evidence logic | Mirror bash regex exactly; fixtures probe the boundary |
| 5-hook batch is too dense for one slice | Per-hook work is templated; if one hook turns out tricky, ship the other 4 and follow up |
| Bash CI breaks on dual-mode wrapper | Same pattern Slice 1 shipped; preserves bash fallback unchanged |
| Result-file `rule_pack_hash` mismatch in CI | Regenerated explicitly in Task 5 before commit |

## 10. Sources

- `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
- `docs/physics-engines/HOOK_TEMPLATE.md`
- `docs/physics-engines/SLICE-1-SPEC.md`
- `engines/fake_cite/ENGINE.md` (template reference)
- `rules/closeout/fake_cite.yaml` (rule-pack reference)
- `fixtures/closeout/fake_cite.jsonl` (fixture reference)
- arXiv:2509.18970, arXiv:2604.16909, arXiv:2408.04681, arXiv:2406.07358, arXiv:2604.14228

## 11. After Slice 2

Operator-review checkpoint. If the 5-hook batch ships cleanly, Slice 3 (anti-evasion family: no-cliffhanger, no-evidence-free-closeout, no-fake-test-claim, no-hedging-spam, no-instruction-injection-pretend) becomes the next batch under the same template.

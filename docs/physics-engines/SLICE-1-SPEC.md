# SPEC: Slice 1 — Physics-Engine Template + `no-fake-cite` end-to-end

Time anchor: 2026-05-16
Outer route: `/opusworkflow --model-profile opus`
Inner contract: workflow
Branch: `physics-engines/slice-1-fake-cite` (off `main` of `agent-closeout-bench`)
Parent plan: `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`

## 1. Problem Statement

`llm-dark-patterns/hooks/no-fake-cite.sh` currently runs as a bash-regex-only hook that blocks academic-citation-formatted references (`Smith et al., 2023`, `(Doe, 2024)`, `Author 2026`) without a verifiable URL in the same message. It has no physics-engine documentation in `agent-closeout-bench`, no Rust implementation in the reference engine, no unit tests, and no fixture suite. This slice lifts it to full physics-engine maturity as the **reference template** for the other 19 bash-only hooks.

`no-fake-cite` is chosen first because:
- High operator value (LLM citation hallucination is documented at 14-94% rates per academic literature).
- Bash logic is non-trivial — URL-proximity adjacency is the natural physics, not a single regex.
- High false-positive risk for legitimate citations with a URL elsewhere in the message — exactly the case the physics engine resolves.
- Simple enough to ship end-to-end in one slice.

## 2. Research Claims

Primary claim:

> `no-fake-cite` v1 is the first hook in `llm-dark-patterns` upgraded from bash-regex-only to a full physics-engine module with positional and adjacency mechanics, deterministic verdict path, per-hook ENGINE.md, Rust implementation, unit tests, and an end-to-end fixture suite covering positives, negatives, and near-misses.

Non-claims:
- This slice does not extend coverage to other hooks (Slice 2-5 do that).
- This slice does not change `no-fake-cite`'s false-positive rate measurably without further empirical evaluation.
- The Rust implementation is the reference; the bash hook remains the wire-level surface.

## 3. Success Criteria

Each criterion is verifiable by command, file, or test.

1. **`engines/fake_cite/ENGINE.md` exists** with the sections defined in the Slice-1 template (Purpose, Runtime hook, Rule pack, Physics types used, Mechanics, Allowed/disallowed states, Limitations, Unit-test coverage map).
   - Verify: `test -f engines/fake_cite/ENGINE.md && grep -E '^## (Purpose|Runtime hook|Rule pack|Physics types|Mechanics|Limitations|Unit-test coverage)' engines/fake_cite/ENGINE.md | wc -l` returns ≥ 7
2. **Rust module `engine/src/categories/fake_cite.rs` exists** (or equivalent in current `main.rs` modularisation, with the function `detect_fake_cite(input: &CloseoutText) -> Verdict`) implementing positional and URL-adjacency mechanics, not just regex.
   - Verify: `cargo test --manifest-path engine/Cargo.toml -- fake_cite` passes all tests.
3. **Rust unit tests cover at least 6 cases**: simple positive, simple negative, citation-with-URL-in-same-message (negative), citation-with-URL-elsewhere-in-message (negative — URL proximity must catch this), parenthetical-citation-without-URL (positive), citation-in-code-block (negative — code blocks excluded).
   - Verify: `cargo test --manifest-path engine/Cargo.toml -- fake_cite` reports ≥ 6 passing tests.
4. **Rule pack at `rules/closeout/fake_cite.yaml`** structured per existing rule-pack schema, including positional anchors and URL-adjacency clauses.
   - Verify: `bin/agentcloseout-physics lint-rules rules/closeout/fake_cite.yaml` exits 0.
5. **End-to-end fixture suite at `fixtures/closeout/fake_cite/`** with ≥ 10 positive + ≥ 10 negative + ≥ 5 near-miss records.
   - Verify: `bin/agentcloseout-physics test-rules rules/closeout/fake_cite.yaml fixtures/closeout/fake_cite/` exits 0 with per-record verdicts matching expected labels.
6. **CI smoke test on PR includes a `cargo test fake_cite` run**.
   - Verify: `.github/workflows/ci.yml` references `fake_cite` (added as part of the `cargo test` step or as an explicit unit-test invocation).
7. **`agentcloseout-physics scan` CLI accepts a single closeout text and reports the verdict for `fake_cite`** end-to-end.
   - Verify: `echo '{"last_assistant_message":"This is documented in Smith et al., 2023."}' | bin/agentcloseout-physics scan --category fake_cite --json` returns a structured BLOCKED verdict.
8. **`llm-dark-patterns/hooks/no-fake-cite.sh` invokes the Rust binary via the existing `agentcloseout-physics` adapter path** for verdict (current bash hook does its own regex; the upgrade routes through Rust).
   - Verify: bash smoke test in `llm-dark-patterns` CI continues to PASS on `no-fake-cite` fixtures, but now via the Rust path.
9. **`minmaxing` harness fires the upgraded hook end-to-end on a fixture**.
   - Verify: a smoke test added to `minmaxing/scripts/hook-smoke.sh` exercises the upgraded hook and exits 0.
10. **Demo script `engines/fake_cite/DEMO.md`** showing operator-visible value: 3 example closeout texts, what BLOCKED message they get, and what repair template the model sees.

## 4. Scope

### In scope
- Per-hook physics-engine template (the template itself becomes `docs/physics-engines/HOOK_TEMPLATE.md`)
- `no-fake-cite` end-to-end implementation (Rust module, rule pack, fixtures, unit tests, CI, hook rewire, minmaxing wiring, demo)
- CI test invocation
- Documentation cross-links from `PHYSICS_ENGINE_PLAN.md`

### Out of scope
- Any other hook in the 20 bash-only set (Slice 2-5)
- Refresh of the 6 already-DOCUMENTED hooks (Slice 6)
- ReDoS timing test in CI (Slice 6)
- Paper updates (Slice 8)
- New dark-pattern categories
- LLM-in-the-loop classifiers

## 5. Agent-Native Estimate

- Estimate type: agent-native
- Execution topology: local single lane; capacity profile workstation 16-core/32GB recommended ceiling 6 (not the bottleneck)
- Critical path: template draft → ENGINE.md → rule pack → Rust module → unit tests → fixtures → CLI scan → bash hook rewire → minmaxing wiring → CI integration → demo
- agent_wall_clock: optimistic 4 hr / likely 7 hr / pessimistic 12 hr
- agent_hours: ~7 hr
- human_touch_time: 30-90 min (operator reviews template, reviews ENGINE.md, approves bash-rewire, validates minmaxing fires)
- calendar_blockers: none — all work is local except CI which runs on push
- confidence: medium. Downgrade reasons: URL-proximity adjacency is novel; first implementation may need a second pass. Rust modularisation might require touching the 1955-line `main.rs` more than expected.

## 6. Implementation Plan

### Task 1: Per-hook physics-engine template
DoD:
- [ ] `docs/physics-engines/HOOK_TEMPLATE.md` exists
- [ ] Template enumerates required ENGINE.md sections, Rust module shape, unit-test patterns, fixture coverage targets, CLI integration, hook-rewire pattern, minmaxing wiring pattern, demo format
- [ ] Operator review checkpoint before Task 2

### Task 2: `no-fake-cite` ENGINE.md
DoD:
- [ ] `engines/fake_cite/ENGINE.md` follows the template
- [ ] Documents lexical, positional, and URL-adjacency physics
- [ ] Lists allowed/disallowed states
- [ ] Documents limitations

### Task 3: Rule pack
DoD:
- [ ] `rules/closeout/fake_cite.yaml` parses
- [ ] Includes positional anchors and URL-adjacency clauses
- [ ] `lint-rules` passes

### Task 4: Rust module + unit tests
DoD:
- [ ] Module exposes `detect_fake_cite` function
- [ ] At least 6 unit tests passing
- [ ] `cargo clippy` clean

### Task 5: Fixture suite
DoD:
- [ ] `fixtures/closeout/fake_cite/positives/*.jsonl` ≥ 10 records
- [ ] `fixtures/closeout/fake_cite/negatives/*.jsonl` ≥ 10 records
- [ ] `fixtures/closeout/fake_cite/near-miss/*.jsonl` ≥ 5 records
- [ ] `test-rules` exits 0

### Task 6: CLI integration
DoD:
- [ ] `agentcloseout-physics scan --category fake_cite` works end-to-end
- [ ] JSON output structured per existing verdict shape

### Task 7: bash hook rewire
DoD:
- [ ] `llm-dark-patterns/hooks/no-fake-cite.sh` invokes `agentcloseout-physics scan` via the adapter
- [ ] Existing bash CI smoke test still passes
- [ ] Repair template preserved or improved

### Task 8: minmaxing harness wiring
DoD:
- [ ] `minmaxing/.claude/hooks/no-fake-cite.sh` (or equivalent install path) fires the upgraded hook
- [ ] `minmaxing/scripts/hook-smoke.sh` includes the smoke case
- [ ] Smoke passes

### Task 9: CI integration
DoD:
- [ ] `agent-closeout-bench` CI runs `cargo test fake_cite`
- [ ] Green on the PR

### Task 10: Demo
DoD:
- [ ] `engines/fake_cite/DEMO.md` shows 3 examples with BLOCK + repair output
- [ ] Operator reviews and confirms operator-visible value

### Task 11: Cross-link + commit + push
DoD:
- [ ] `PHYSICS_ENGINE_PLAN.md` updated to mark Slice 1 done
- [ ] PR opened on `agent-closeout-bench` for the slice branch
- [ ] PR opened on `llm-dark-patterns` for the bash-hook rewire
- [ ] PR opened on `minmaxing` for the smoke-test addition

## 7. Verification

| Criterion | Method |
|---|---|
| C1 ENGINE.md | section header grep |
| C2 Rust module | `cargo test` |
| C3 ≥6 tests | `cargo test` count |
| C4 rule pack | `lint-rules` exit 0 |
| C5 fixtures | `test-rules` exit 0 |
| C6 CI | green PR check |
| C7 CLI | manual `agentcloseout-physics scan` end-to-end |
| C8 bash hook | existing CI smoke |
| C9 minmaxing | new smoke entry passes |
| C10 demo | operator inspection |

`/verify` runs at end of Task 6 (mid-slice gate), Task 9 (CI), and Task 11 (close). `/introspect` runs before Task 1 (template draft) and before Task 11 (pre-PR).

## 8. Rollback

- Pre-PR: `git checkout main && git branch -D physics-engines/slice-1-fake-cite` undoes everything in `agent-closeout-bench`.
- bash hook rewire on `llm-dark-patterns`: revert via standard git path on the `physics-engines/slice-1-fake-cite` branch; bash smoke test on `main` stays green throughout.
- minmaxing smoke change: on `minmaxing` repo, single-file revert.
- Post-PR (if merged but a flaw is found): `git revert <merge-commit>` on each repo.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Template doesn't generalise to other hooks | Slice 1 includes an explicit template-iteration step before Slice 2 launches |
| URL-adjacency mechanics over-block legitimate citations | Near-miss fixture set forces the false-positive cases into test |
| 1955-line `main.rs` is hard to modularise cleanly | Acceptable to keep `fake_cite` as a sub-module of `main.rs` if a cleaner module split is too invasive for one slice; document the decision |
| minmaxing harness wiring path differs from what the hook expects | Check `minmaxing/.claude/hooks/` layout at Task 8 start; reshape if needed |
| Operator review takes longer than estimated | Slice has 11 tasks with operator-review checkpoints at Tasks 1 and 11; either is a safe pause point |

## 10. Sources

- `docs/physics-engines/PHYSICS_ENGINE_PLAN.md` — parent plan
- `engines/<category>/ENGINE.md` × 6 — existing physics-engine documents
- `llm-dark-patterns/hooks/no-fake-cite.sh` — current bash implementation
- `llm-dark-patterns/.github/workflows/test.yml` — existing CI smoke test for `no-fake-cite`
- `paper/readiness_audit_2026-05-13.md` — Gate-2 requirements for Rust unit tests + ReDoS / latency
- Memory: `project_physics_engine_per_hook.md` — v4 physics hypothesis

## 11. After Slice 1

Operator-review checkpoint before launching Slice 2. The template + the `no-fake-cite` end-to-end implementation become the reference. If the template needs iteration, do that first; if Slice 1 demonstrates the pattern works, launch Slice 2 (fact-fabrication family: no-fake-recall, no-fake-stats, no-phantom-tool-call, no-rollback-claim-without-evidence, no-sandbagging-disguise).

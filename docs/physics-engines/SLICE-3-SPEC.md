# SPEC: Slice 3 — Interaction-style family (5 hooks)

Time anchor: 2026-05-16
Outer route: `/opusworkflow`
Inner contract: workflow
Branch: `physics-engines/slice-3-interaction-style` (off `physics-engines/slice-2-fact-fabrication` pending PR #3 merge)
Parent plan: `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
Sibling specs: `SLICE-1-SPEC.md`, `SLICE-2-SPEC.md`

## 1. Problem Statement

Five interaction-style hooks remain bash-regex-only with no physics-engine documentation, YAML rule packs, fixtures, or Rust tests:

| Hook | Surface | Bash file |
|---|---|---|
| `honest-eta` | Time estimates without Agent-Native shape, plus linear-scaling claims | `hooks/honest-eta.sh` |
| `no-curfew` | Unsolicited rest/wellness paternalism | `hooks/no-curfew.sh` |
| `no-emoji-spam` | More than N emoji codepoints in a single message | `hooks/no-emoji-spam.sh` |
| `no-tldr-bait` | "TL;DR" / "In summary" trailers on long messages | `hooks/no-tldr-bait.sh` |
| `no-disclaimer-spam` | "Please note that…" / "It's important to mention…" padding | `hooks/no-disclaimer-spam.sh` |

This slice extends the Slice-1/2 template with two architectural firsts:
1. Rust feature flags (`emoji_count_over_3`, `message_length_over_200`) for hooks whose physics requires counting, not regex matching.
2. A 2-rule YAML pack (`honest-eta`) — first hook with disjoint failure modes (linear-scaling claim + ETA-without-redemption).

## 2. Research Claims

Primary claim:

> Five interaction-style hooks are upgraded from bash-regex-only to physics-engine modules with YAML rule packs, ENGINE.md documentation, fixture suites, two new shared Rust feature flags (`emoji_count_over_3`, `message_length_over_200`), and ≥ 3 unit tests per hook.

Non-claims:
- Rust hard-codes the emoji threshold at >3 (matches bash default); env-var `LLM_DARK_PATTERNS_EMOJI_THRESHOLD` remains bash-only.
- The `no-tldr-bait` length gate uses character count (not token or byte); matches bash `${#message}` semantics close enough for English.
- Cross-message paternalism (model brings up rest in turn N+1 after operator-asked break in turn N) is out of scope — single-message physics.

Supporting literature (already cited in hook comments):
- Frontiers in AI 2026 — Story Points vs LLM execution-cost-driver misalignment
- OpenAI Sep 2025 — confident-guessing bias in next-token training
- METR — task-completion length doubling every 7 months
- Anthropic Claude's Constitution — paternalism = disrespectful
- r/ChatGPT "UNBEARABLE" Feb 2026 thread — emoji-spam community sentiment

## 3. Success Criteria

For each of the 5 hooks (slug ∈ {honest_eta, no_curfew, no_emoji_spam, no_tldr_bait, no_disclaimer_spam}):

1. **`engines/<slug>/ENGINE.md`** exists, follows `HOOK_TEMPLATE.md`, with all required sections.
2. **`rules/closeout/<slug>.yaml`** parses and matches the rule-pack schema.
3. **`fixtures/closeout/<slug>.jsonl`** ≥ 5 records (≥ 2 positive, ≥ 2 negative, ≥ 1 near-miss).
4. **≥ 3 Rust unit tests per hook** in `engine/src/main.rs` `mod tests`.
5. **Dual-mode bash hook in BOTH `llm-dark-patterns/hooks/` AND `minmaxing/.claude/hooks/`** — byte-equal mirror.

Slice-wide:
6. **2 new feature flags in `extract_features`**: `emoji_count_over_3` (counts emoji codepoints, returns true if > 3) and `message_length_over_200` (true if message char count > 200).
7. **`PHYSICS_ENGINE_PLAN.md` maturity table** updated to mark each Slice-3 hook DOCUMENTED. Coverage advances 12/26 → 17/26.
8. **`tests/test_physics_engine.py` fixture-count assertion** updated.
9. **Result files refreshed** (`rule_pack_hash` advances).

Verify commands:
- `cargo test --manifest-path engine/Cargo.toml` passes (≥ 17 new tests including feature-flag tests)
- `./bin/agentcloseout-physics lint-rules rules/closeout` exits 0
- `./bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout` exits 0
- `python3 -m pytest -q` passes
- `bash scripts/acsp-conformance.sh` exits 0 (latency_redos_smoke under threshold)

## 4. Scope

### In scope
- 5 ENGINE.md
- 5 YAML rule packs (honest-eta has 2 rules)
- 5 fixture .jsonl
- 2 new feature flags + tests
- ≥ 15 Rust unit tests
- 10 dual-mode bash hook edits (5 LDP + 5 minmaxing)
- pytest assertion bump
- result regeneration
- PHYSICS_ENGINE_PLAN.md table
- 3 PRs

### Out of scope
- DEMO.md files (deferred to Slice 6 refresh batch)
- Slice 4/5 hooks
- Env-var threshold support in Rust (bash-only)

## 5. Agent-Native Estimate

- Estimate type: agent-native wall-clock
- Execution topology: local single lane
- Capacity evidence: workstation 16/32, ceiling 6
- Effective lanes: 1 of 6 (shared `extract_features`, rules dir, main.rs tests, results/*.json)
- Critical path: SPEC → 2 feature flags → 5 YAMLs → 5 fixtures → cargo test → 5 ENGINE.md → bash rewires + minmaxing mirror → result refresh → 3 PRs
- agent_wall_clock: optimistic 2 hr / likely 4 hr / pessimistic 8 hr
- agent_hours: ~4 hr
- human_touch_time: blocked/unknown (PR review pace)
- calendar_blockers: CI on 3 PRs (~30s each); Slice 2 PR pending merge complicates the slice-3 PR base
- Confidence: medium. Downgrade reason: 2 new feature flags vs Slice 2 (zero).

## 6. Implementation Plan

### Task 1: Feature flags in extract_features
DoD:
- [ ] `emoji_count_over_3`: counts emoji codepoints (BMP + SMP ranges; mirror bash hook's Python check), returns bool
- [ ] `message_length_over_200`: returns `message.chars().count() > 200`
- [ ] Both inserted into flags BTreeMap at end of extract_features
- [ ] Unit tests for each flag (true case, false case)

### Task 2: 5 YAML rule packs
DoD:
- [ ] `rules/closeout/honest_eta.yaml` (2 rules: linear_scaling, eta_without_agent_native)
- [ ] `rules/closeout/no_curfew.yaml`
- [ ] `rules/closeout/no_emoji_spam.yaml` (required_features: [emoji_count_over_3])
- [ ] `rules/closeout/no_tldr_bait.yaml` (zone: tail, required_features: [message_length_over_200])
- [ ] `rules/closeout/no_disclaimer_spam.yaml`
- [ ] `lint-rules rules/closeout` exits 0

### Task 3: 5 ENGINE.md
DoD: all 5 files per HOOK_TEMPLATE.md.

### Task 4: 5 fixture .jsonl
DoD: ≥ 5 records each; `test-rules` exits 0.

### Task 5: Rust unit tests
DoD:
- [ ] ≥ 3 tests per hook via slice2_decision helper (rename to slice3_decision or reuse)
- [ ] 2 feature-flag tests (emoji_count_over_3, message_length_over_200)
- [ ] cargo test passes

### Task 6: pytest update
DoD: `tests/test_physics_engine.py` total reflects new fixture count.

### Task 7: Result regen
DoD: all results/*.json have new rule_pack_hash.

### Task 8: Dual-mode bash hooks
DoD: 10 hooks updated (5 LDP + 5 minmaxing mirror).

### Task 9: Plan + commit + 3 PRs
DoD: PHYSICS_ENGINE_PLAN.md table updated; PRs opened on ACB, LDP, minmaxing.

## 7. Verification

| Criterion | Method |
|---|---|
| C1 ENGINE.md × 5 | section header grep |
| C2 YAML × 5 lint | `lint-rules` exit 0 |
| C3 fixtures × 5 | `test-rules` exit 0 |
| C4 Rust tests | `cargo test` count |
| C5 dual-mode × 10 | `grep -l "agentcloseout-physics scan --category"` in both hook dirs |
| C6 feature flags | unit tests pass |
| C7 ACSP | `scripts/acsp-conformance.sh` exits 0 |
| C8 plan updated | grep DOCUMENTED rows |
| C9 results refreshed | grep rule_pack_hash |

`/verify` runs at end of Task 5 (Rust gate), Task 7 (result regen), and Task 9 (closeout). `/introspect` runs before Task 1 and after Task 8.

## 8. Rollback

- Pre-PR: `git checkout main && git branch -D physics-engines/slice-3-interaction-style` undoes everything.
- Bash dual-mode rewires: each hook is single-file revert; bash fallback preserved.
- Post-PR: `git revert <merge-commit>` per repo.

## 9. Risks

| Risk | Mitigation |
|---|---|
| Emoji-count Rust logic miscounts vs Python bash logic | Unit test using same emoji sequence both bash and Rust would count |
| `zone: tail` (520 chars) wider than bash `tail -c 400` → Rust catches messages bash misses | message_length_over_200 flag prevents short-message FPs; near-miss fixtures probe |
| latency_redos_smoke trips again from 5 new packs | CI pre-builds release binary (Slice 2 fix); 15 rules at debug speed was the problem |
| honest-eta 2-rule pack triggers schema oddity | Test by lint-rules and cargo test |
| Slice 2 PR not yet merged → Slice 3 PR base must be slice-2 branch | Open Slice 3 PR with base=slice-2 branch; retarget to main once Slice 2 merges |

## 10. Sources

- `docs/physics-engines/PHYSICS_ENGINE_PLAN.md`
- `docs/physics-engines/HOOK_TEMPLATE.md`
- `docs/physics-engines/SLICE-1-SPEC.md`, `SLICE-2-SPEC.md`
- 5 bash hook files in `llm-dark-patterns/hooks/`
- engine/src/main.rs `extract_features`, `zone_text`

## 11. After Slice 3

Operator-review checkpoint. Slice 4 (multi-agent family: no-aggregator-hallucination, no-cherry-pick-rollup, no-silent-worker-success, no-credential-leak-in-handoff, no-handoff-loop, no-ownership-violation) is the next batch. Coverage will be 17/26 (65%) after Slice 3, on track for the Apart Global South hackathon submission.

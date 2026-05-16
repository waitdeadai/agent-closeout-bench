# Physics Engines — Comprehensive Plan

Time anchor: 2026-05-16
Outer route: `/opusworkflow` (model_profile=opus per `/opusolo` operator selection 2026-05-16)
Inner contract: workflow
Branch: `physics-engines/plan` on `agent-closeout-bench`

## 1. Goal

Bring every wired hook in `llm-dark-patterns` v1.0.0 up to a **solid physics-engine** standard: documented mechanics, deterministic detection that goes beyond raw lexical regex where regex falls short, structural/semantic where applicable, and end-to-end wiring through both the `agent-closeout-bench` Rust reference engine and the operator's `minmaxing` harness. Each upgraded hook must demonstrate concrete value to a user — precise BLOCK messages, working repair templates, low false-positive rate.

This is paper-readiness work plus product-grade work plus moat-deepening work, in that order of priority.

## 2. Inventory: 31 wired hooks

From `llm-dark-patterns/hooks/hooks.json` (verified 2026-05-16 via `jq` grep of all event fan-outs):

Closeout-stage (24, fired at `Stop` / `SubagentStop`):
honest-eta, no-aggregator-hallucination, no-ai-tells, no-cherry-pick-rollup, no-cliffhanger, no-curfew, no-disclaimer-spam, no-emoji-spam, no-fake-cite, no-fake-recall, no-fake-stats, no-meta-commentary, no-phantom-tool-call, no-prompt-restate, no-roleplay-drift, no-rollback-claim-without-evidence, no-sandbagging-disguise, no-silent-worker-success, no-sycophancy, no-tldr-bait, no-vibes, no-wrap-up

Multi-agent (3, fired at `TaskCreated` / `TaskCompleted`):
no-credential-leak-in-handoff, no-handoff-loop, no-ownership-violation

Tool-use (2, fired at `PreToolUse` / `PostToolUse`):
no-approval-sneak, plus no-vibes (already counted)

State machinery (4, lifecycle-continuity not safety-detection):
state-stop, state-precompact, state-postcompact, state-sessionstart

Time discipline (1, fired at `SessionStart` / `UserPromptSubmit`):
time-anchor

The state machinery and time-anchor hooks are continuity utilities, not dark-pattern detectors. **Physics-engine treatment applies to the 26 detector hooks** (24 closeout + 2 multi-agent + 1 PreToolUse). The 4 state machinery hooks plus time-anchor get a separate, lighter "continuity-engine" treatment.

## 3. Current physics-engine maturity per hook

| Hook | ENGINE.md | Rust engine module | Rust unit tests | Maturity |
|---|---|---|---|---|
| no-vibes (evidence_claims) | YES | YES | partial | **DOCUMENTED** |
| no-cliffhanger | YES | YES | partial | **DOCUMENTED** |
| no-wrap-up | YES | YES | partial | **DOCUMENTED** |
| no-sycophancy | YES | YES | partial | **DOCUMENTED** |
| no-roleplay-drift | YES | YES | partial | **DOCUMENTED** |
| (closeout_contract aggregate) | YES | YES | partial | **DOCUMENTED** |
| honest-eta | NO | NO | NO | **BASH-ONLY** |
| no-aggregator-hallucination | NO | NO | NO | **BASH-ONLY** |
| no-ai-tells | NO | NO | NO | **BASH-ONLY** |
| no-cherry-pick-rollup | NO | NO | NO | **BASH-ONLY** |
| no-credential-leak-in-handoff | NO | NO | NO | **BASH-ONLY** |
| no-curfew | NO | NO | NO | **BASH-ONLY** |
| no-disclaimer-spam | NO | NO | NO | **BASH-ONLY** |
| no-emoji-spam | NO | NO | NO | **BASH-ONLY** |
| no-fake-cite | NO | NO | NO | **BASH-ONLY** |
| no-fake-recall | NO | NO | NO | **BASH-ONLY** |
| no-fake-stats | NO | NO | NO | **BASH-ONLY** |
| no-handoff-loop | NO | NO | NO | **BASH-ONLY** |
| no-meta-commentary | NO | NO | NO | **BASH-ONLY** |
| no-ownership-violation | NO | NO | NO | **BASH-ONLY** |
| no-phantom-tool-call | NO | NO | NO | **BASH-ONLY** |
| no-prompt-restate | NO | NO | NO | **BASH-ONLY** |
| no-rollback-claim-without-evidence | NO | NO | NO | **BASH-ONLY** |
| no-sandbagging-disguise | NO | NO | NO | **BASH-ONLY** |
| no-silent-worker-success | NO | NO | NO | **BASH-ONLY** |
| no-tldr-bait | NO | NO | NO | **BASH-ONLY** |
| no-approval-sneak | NO | NO | NO | **BASH-ONLY** |

**Summary**: 6 of 26 detector hooks (23%) have physics-engine documentation + Rust implementation. The other 20 (77%) are bash-regex-only with no formal physics model. This is the gap the plan closes.

## 4. What "physics engine" means here

A hook's **physics** is the structural/operational pattern that deterministically identifies a dark-pattern instance, as distinct from a purely lexical regex match. Five physics types appear in the suite:

1. **Lexical pattern matching** — regex over closeout text. Necessary but not sufficient. Already 100% of the current implementation.
2. **Positional pattern matching** — regex anchored by position (start-of-message, end-of-message, after specific markers). Reduces false positives.
3. **Adjacency / proximity analysis** — does the suspect phrase appear near (or far from) evidence markers, qualifying context, or user-anchored phrases? E.g., `verified` 10 tokens from a command-output block is fine; `verified` alone is the dark pattern.
4. **Structural analysis** — sentence structure, question structure, paragraph structure. E.g., a leading question at end-of-message vs. a clarifying question mid-message.
5. **Cross-message / cross-session state** — comparing assertions to actual prior tool calls or evidence in the session. E.g., `no-phantom-tool-call` is only meaningful when checked against the session's actual tool-call history.

Hooks in this suite use a mix. A "solid physics engine" per hook means:
- Each hook's `ENGINE.md` enumerates which physics types it uses and why.
- Each hook has a Rust module (or shared module) implementing the non-regex parts deterministically.
- Each hook has unit tests for the non-trivial structural / positional / adjacency logic.
- Each hook has a stress fixture set proving false-positive rate on benign closeouts.
- Each hook has documented limitations (what regex alone cannot catch).

The user-visible value:
- BLOCK messages are precise about what was caught and why (current hooks already do this, but inconsistently across the 31)
- Repair templates lead the model back to a compliant closeout shape (current hooks mostly do this; consistency varies)
- False positives are low enough that operators don't disable the hook (the moat: a hook that fires correctly is left enabled; a noisy hook is removed)

## 5. Slice breakdown

Decomposing the plan into bounded slices the operator can approve one at a time:

### Slice 1: Template + one new hook end-to-end (this slice)
- Pick one currently-BASH-ONLY hook and bring it to full physics-engine maturity as the **reference template** for the rest.
- Candidate: `no-fake-cite` (4 reasons: high-leverage academic-credibility detector; bash logic is non-trivial; lends itself to URL-proximity adjacency physics; high false-positive risk so the physics matters).
- Deliverables:
  - `engines/fake_cite/ENGINE.md` per template
  - `engine/src/categories/fake_cite.rs` (or equivalent module structure)
  - Rust unit tests
  - Hookup in `agentcloseout-physics` CLI
  - End-to-end fixture suite (positives, negatives, near-misses)
  - Replicated wiring in `minmaxing` so the hook fires there too
  - Demo script for the user-facing value
- Estimate: agent-native, optimistic 4 hr / likely 7 hr / pessimistic 12 hr.
- Confidence: medium. Downgrade reason: URL-proximity adjacency logic is novel; first implementation may need a second pass.

### Slice 2-5: Roll the template (~5 hooks per slice)
- Apply the Slice-1 template pattern to batches of 5 bash-only hooks each.
- Slice 2 (fact-fabrication family): no-fake-recall, no-fake-stats, no-phantom-tool-call, no-rollback-claim-without-evidence, no-sandbagging-disguise
- Slice 3 (interaction-style family): honest-eta, no-curfew, no-emoji-spam, no-tldr-bait, no-disclaimer-spam
- Slice 4 (multi-agent family): no-aggregator-hallucination, no-cherry-pick-rollup, no-silent-worker-success, no-credential-leak-in-handoff, no-handoff-loop, no-ownership-violation
- Slice 5 (residual): no-ai-tells, no-meta-commentary, no-prompt-restate, no-approval-sneak (and any catch-up from earlier slices)
- Estimate per slice: agent-native, optimistic 4 hr / likely 8 hr / pessimistic 16 hr.

### Slice 6: Refresh the 6 already-DOCUMENTED hooks to match new template + improve unit-test depth
- Audit the 6 existing physics engines (no-vibes, no-cliffhanger, no-wrap-up, no-sycophancy, no-roleplay-drift, closeout_contract) against the Slice-1 template
- Add the unit-test coverage the readiness audit Gate-2 calls for
- Add ReDoS / latency timing test in CI
- Estimate: agent-native, optimistic 4 hr / likely 6 hr / pessimistic 10 hr

### Slice 7: minmaxing harness integration verification
- Confirm every hook fires correctly in `minmaxing` (not just `llm-dark-patterns` standalone).
- The minmaxing harness lives at `/home/fer/Documents/minmaxing` and uses `.claude/hooks/` for its own wiring. Need to verify it reads from the upgraded `llm-dark-patterns` plugin OR has its own copies.
- Operator-visible demo: a single session where each upgraded hook fires deterministically against a fixture.
- Estimate: agent-native, optimistic 3 hr / likely 5 hr / pessimistic 8 hr

### Slice 8: Paper update
- Reflect the physics-engine upgrades in the NeurIPS workshop paper draft.
- Update the "reference engine" section to describe physics types, structural mechanics, evidence-marker adjacency.
- Add per-category measurement tables (precision/recall on the LLM-judge sample once available).
- Estimate: agent-native, optimistic 3 hr / likely 5 hr / pessimistic 8 hr

## 6. Critical path

```
Slice 1 (template + no-fake-cite) -> Slice 6 (refresh DOCUMENTED) -> Slice 2 (fact-fab) -> Slice 3 (interaction) -> Slice 4 (multi-agent) -> Slice 5 (residual) -> Slice 7 (minmaxing) -> Slice 8 (paper)
```

Total agent wall-clock estimate (sum of likely): **~52 hours** across 8 slices. Realistic calendar: 2-3 weeks if operator approves slices in sequence with brief review gates between each. Confidence: medium. Downgrade reason: structural physics for hooks I haven't deeply examined yet may require more time than the rough estimate.

## 7. Strategic context

This plan slots in with:
- **Global South AI Safety Hackathon** Jun 19-21: Slices 1-3 should be done before the hackathon so the demo shows a maturing physics-engine product, not just regex.
- **NeurIPS workshop paper** ~Aug 29: Slice 8 must land before the paper submission. Slices 1-7 must land before Slice 8 to give the paper a maturing-engine story.
- **Engines-as-moat**: the more rigorously each hook is documented as a deterministic physics engine, the harder it is for fast-following competitors to claim equivalence.

## 8. Risks

| Risk | Mitigation |
|---|---|
| Slice 1 reveals the template doesn't generalise well | Iterate the template before launching Slice 2; explicit checkpoint before Slice 2 |
| Operator bandwidth for review across 8 slices | Each slice has its own SPEC + /specqa + plan-mode checkpoint; operator can pause at any boundary |
| Some bash-only hooks are essentially regex-only and don't benefit from richer physics | Acknowledge in the per-hook ENGINE.md; honest scoping is itself a moat |
| Cross-tool-call invariants (e.g., `no-phantom-tool-call`) require session-state plumbing that the current architecture doesn't have | Note as v0.4 future work; v0.3 physics engine documents the limitation |
| ReDoS timing test reveals an existing rule is pathological | Fix the rule on the same slice; treat as a feature of the plan |

## 9. What this plan does NOT do

- Replace the bash hooks with Rust hooks. Bash is the wire-level surface; Rust is the verdict-engine that bash invokes. Both coexist.
- Add new categories of dark patterns. The 26 detector categories are fixed by this plan; new ones are a separate concern.
- Build LLM-in-the-loop classifiers. Out-of-band-ness is the contract; physics engines stay deterministic.
- Replace the per-hook standalone repos (no-vibes, no-cliffhanger, etc.). Those continue to ship; the bundle is the primary install.
- Address state-machinery hooks (state-*.sh, time-anchor.sh). Those are continuity utilities, not detectors. Separate concern.

## 10. Next step

Slice 1 SPEC follows. Operator-approval gate after Spec QA before any code is written.

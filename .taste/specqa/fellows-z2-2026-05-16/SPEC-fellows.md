# SPEC: Z2 — Anthropic Fellows Application Prep

Time anchor: 2026-05-16
Outer route: `/opusolo`
Inner contract: workflow
Branch: TBD (operator selects, suggest `fellows/application-prep` on `agent-closeout-bench`)
Stop point of THIS SPEC: gate on §3 eligibility verification before any materials are drafted.

## 1. Problem Statement

We want to apply for the Anthropic Fellows program (AI Safety track) using the existing AgentCloseoutBench + llm-dark-patterns artefacts as the project surface. Application materials need to be drafted, but a critical eligibility precondition must be verified first.

## 2. Verified facts (2026-05-16, live)

From `alignment.anthropic.com/2025/anthropic-fellows-program-2026/` and `job-boards.greenhouse.io/anthropic/jobs/5023394008`:

- Next cohort start: **Late September 2026** (flexible)
- Applications: **rolling basis**
- 5 workstreams; our fit: **AI Safety Fellows** (covers scalable oversight, adversarial robustness, model organisms, mechanistic interpretability, AI welfare)
- Compensation: **$3,850/week + $15K/mo compute**, 4 months, 40 hr/wk
- Selection process: initial application + reference check → technical assessments + interviews → research discussion
- **Work authorization required**: US, UK, or Canada. **No visa sponsorship**. Remote participation available **only in those three eligible countries**.
- Previous fellows: 25-50% receive full-time offers post-program.

## 3. Eligibility gate (CRITICAL — must resolve before §6)

**Operator-confirmation required**: do you currently hold work authorization in any of:
- United States
- United Kingdom
- Canada

If **yes**: proceed with §6 implementation plan.

If **no**: this slice **stops** and is replaced by Z3 (UK AISI Alignment Project — funded applicants from 42 countries including non-UK in the first round) or Z7 (Apart Research Lab Fellowship — international, no visa requirement, 10-20 hours/week part-time over 4-8 months). Recommend pivoting to Z3 since RICE-scored higher under those conditions.

Confidence in this gate: high. The job-board page is the authoritative source and states the requirement explicitly.

## 4. Research Claims (slice-scoped)

If the eligibility gate clears, the application will position our work as:

> A pre-release benchmark and open-source hook suite for closeout-text dark patterns at the Claude Code Stop/SubagentStop lifecycle surface, with deterministic out-of-band enforcement, paper-grade claim discipline, and a public companion benchmark. The Fellows project would advance this from "pre-release scaffolding" to "human-adjudicated locked-test release", expand to additional dark-pattern categories surfaced by field reports, and contribute to Anthropic's scalable oversight and adversarial robustness workstreams.

Non-claims:
- We do not claim Fellows-program acceptance.
- We do not claim our work is novel in absolute terms; we claim novel positioning on the closeout-text axis relative to chat-surface and action-trace prior work.
- We do not claim funding amounts or specific deliverables until accepted.

## 5. Success Criteria (post-gate)

Conditional on §3 clearing yes:

1. **CV-style summary** at `fellows/cv-summary.md` covering technical background, prior work (waitdeadai org repos), demonstrated execution ability.
2. **Research statement** at `fellows/research-statement.md` (~1500 words, verify against form length cap when application form opens).
3. **Project proposal** at `fellows/project-proposal.md` (~1000 words) — what 4 months on this would produce.
4. **References list** at `fellows/references.md` — at least 2 contactable references with topic-aligned validation of the work.
5. **Code samples** — direct links to `waitdeadai/agent-closeout-bench` and `waitdeadai/llm-dark-patterns` are sufficient; no extra packaging required.
6. **Application form submission** — operator-only step; agent prepares paste-ready content, operator pastes and submits via the Constellation/Greenhouse form.

## 6. Implementation Plan (conditional on §3 clearing yes)

### Task 1: Materials drafting (agent-native)
- [ ] CV-style summary
- [ ] Research statement (AI Safety workstream framing)
- [ ] Project proposal (4-month deliverables, mapped to AgentCloseoutBench v1.0 release + LDP semantic-engine prototype)
- [ ] References list (operator names + topic-aligned context for each)
- [ ] Self-introspect pass on all drafts before operator review

### Task 2: Operator review + revision (mixed)
- [ ] Operator reads drafts, marks revisions
- [ ] Agent revises per operator notes
- [ ] Final pass under /opusolo Spec QA

### Task 3: Form submission (operator-only)
- [ ] Operator opens Constellation/Greenhouse form
- [ ] Pastes prepared content field-by-field
- [ ] Captures confirmation; agent logs in `FELLOWS_SUBMISSION_LOG.md`

## 7. Agent-Native Estimate

- Estimate type: agent-native (drafting) + blocked/unknown (review + submit)
- Agent wall-clock for §6 Task 1 only: optimistic 2 hr / likely 4 hr / pessimistic 7 hr
- Agent-hours: ~4 hr
- Human touch time: 1-3 hr (your review + revisions + form click) — blocked/unknown depending on your pace
- Calendar blockers: Constellation/Greenhouse form layout unknown until accessed; reference solicitation depends on the operator's network
- Confidence: medium (downgrade reason: research statement and project proposal are heavily judgment-driven; first-draft is rarely the final draft)

## 8. Verification

| Criterion | Method |
|---|---|
| C1 eligibility | Operator confirms US/UK/Canada work authorization (§3) |
| C2 drafts exist | `ls fellows/{cv-summary,research-statement,project-proposal,references}.md` returns 4 files |
| C3 claim-gate clean | `bash paper/uai-2026/claim-gate.sh fellows/` exits 0 (forbidden-word scan) |
| C4 introspect pass | `.taste/introspect/fellows-z2-*/introspect.md` outcome is ALLOWED |
| C5 submission logged | `fellows/FELLOWS_SUBMISSION_LOG.md` carries operator-pasted confirmation |

## 9. Rollback

- Pre-submission: drafts are local-only. `git checkout main && git branch -D fellows/application-prep` undoes everything.
- Post-submission: rolling-basis applications can be withdrawn via reply to the recruiting team. The repos themselves remain under our control regardless.

## 10. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Eligibility blocker (US/UK/Canada auth) | unknown until §3 confirmed | Pivot to Z3 (AISI) or Z7 (Apart) if no |
| Topic-fit mismatch with Anthropic priorities | low-medium | The 5 listed workstreams explicitly include scalable oversight + adversarial robustness; our work maps cleanly |
| References unavailable | medium | Operator's network (Sara, llm-dark-patterns contributors, ACB readers) carries reference potential |
| Constellation form fields not pre-knowable | medium | Same pattern as marketplace form: draft a superset, revise on form access |
| 25-50% offer rate ≠ acceptance rate | high | Frame the application as research-investment, not job-pursuit; accept the realistic probability |

## 11. Sources (verified 2026-05-16)

- [Anthropic Fellows Program 2026 announcement](https://alignment.anthropic.com/2025/anthropic-fellows-program-2026/)
- [Greenhouse job posting](https://job-boards.greenhouse.io/anthropic/jobs/5023394008)
- [AI Safety Fellows track (Greenhouse 5030244008)](https://job-boards.greenhouse.io/anthropic/jobs/5030244008) — flagged but not deep-read yet; will pull at materials-draft time
- Existing project artefacts: `agent-closeout-bench/SPEC.md`, `paper/SPEC-paper-uai-2026.md`, `agent-closeout-bench/.taste/strategic-pivot/2026-05-16/STRATEGIC-PIVOT.md`, `llm-dark-patterns/README.md`
- UK AISI Alignment Project (fallback) — 42-country fund, per earlier deepresearch
- Apart Research Lab Fellowship (fallback) — international, 10-20 hr/week part-time

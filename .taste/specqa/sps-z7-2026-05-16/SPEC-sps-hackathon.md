# SPEC: Z7-SPS — Apart Research Secure Program Synthesis Hackathon May 22-24

Time anchor: 2026-05-16
Outer route: `/opusolo`
Inner contract: workflow
Co-organizer: Atlas Computing
Pivot context: replaces Z2 (Anthropic Fellows, blocked on work auth) and Z3 (AISI Alignment Project, currently closed)

## 1. Problem Statement

We have shipped artefacts (`agent-closeout-bench`, `llm-dark-patterns`) that constitute lightweight deterministic verification of LLM closeout text. The Apart Research Secure Program Synthesis Hackathon (May 22-24) is explicitly framed as "prototype the tools we'll need to verify what AI is writing" and co-organised with formal-methods specialists (Atlas Computing). This is an opportunity for our work to be reviewed by senior formal-methods researchers (Erik Meijer, Mike Dodds for the Fellowship; Joe Kiniry, Jason Gross, Max von Hippel, Quinn Dougherty as hackathon speakers), and a pipeline into a 4-month Fellowship (June-October 2026) with compute + API credits + mentorship.

The hackathon thesis matches our work. The methods do not — they emphasise proof assistants, type systems, model checkers; we ship regex pattern packs. The slice's job is to bridge that gap honestly: frame our lightweight verification as the pragmatic first-pass surface that motivates heavier formal verification as the next layer.

## 2. Verified facts (2026-05-16, live)

From `apartresearch.com/sprints/secure-program-synthesis-hackathon-2026-05-22-to-2026-05-24` and adjacent pages:

- Dates: **May 22-24, 2026** (3 days, final submissions Sunday May 24)
- Prizes: **$1,000 / $500 / $300 / $100 / $100** (top 5)
- Format: PDF research artefact per template shared at kickoff; "concrete" deliverables — examples include tools, agents, harnesses
- Speakers: Joe Kiniry, Jason Gross, Max von Hippel, Quinn Dougherty
- Fellowship mentors named (Jun-Oct 2026): Erik Meijer, Mike Dodds
- Path: hackathon → SPS Fellowship; top teams invited to apply
- Submissions reviewed by expert judges per the Apart-Research-general pattern
- Contact: `secure-program-synthesis-fellowship@apartresearch.com` and `sprints@apartresearch.com`
- Registration URL: not extracted from the canonical page; Luma event page `luma.com/4q2fnc39` is referenced

## 3. Eligibility & risk assessment

| Risk | Assessment |
|---|---|
| Geographic eligibility (Argentine resident) | Not explicitly listed. Apart hackathons have funded multi-national participants (DarkBench team — Hungarian, Indian, Polish co-authors). Likely OK; verify on registration. |
| Solo vs team | Apart hackathons typically allow both. Solo is realistic given operator timeline. |
| Topic match — thesis vs methods | **Thesis match: high.** "Verify what AI is writing" is verbatim our work. **Method match: low.** Hackathon emphasises formal methods (proof assistants, type systems, model checkers); we ship regex packs. Bridge framing required. |
| Operator bandwidth (3 days intensive) | Concentrated effort competes with NeurIPS paper deferral and other slices. Manageable if other slices stay paused. |
| Anonymity / paper conflict | NeurIPS workshop is later in the year; hackathon submission will be public and named. No double-blind submission is in flight currently. Safe. |

## 4. Research Claims (slice-scoped)

Slice-scoped positioning for the hackathon submission:

> **Claim**: Lightweight deterministic verification at the agentic coding assistant closeout boundary is a *pragmatic first-pass surface* that complements formal verification of the underlying program synthesis. Closeout text encodes the assistant's self-report about generated code; out-of-band regex over closeout text catches a measurable fraction of false-success and unverified-claim instances at zero LLM cost in the verdict path, without requiring proof obligations for every emitted program.

Non-claims:
- We do not claim our verification replaces formal methods.
- We do not claim universal coverage; lexical evasion remains an open problem.
- We do not claim formal soundness; the verification is heuristic-as-engineering, not proof-based.

The bridge: position lightweight verification as a *layer* in a defence-in-depth verification stack. Reviewers from the formal-methods world will appreciate the honest scoping.

## 5. Success Criteria

1. **Registration completed** before the hackathon kickoff (operator action via the Luma URL).
2. **Team decision recorded** (solo or team; if team, members identified) — operator decision.
3. **Pre-hackathon idea note** at `apart-sps/idea-note.md` (~500 words) — pitchable to potential teammates or as solo positioning.
4. **Hackathon submission** — PDF artefact per the kickoff-day template, plus code repo link. Both deposited via the Apart submission form.
5. **Submission logged** at `apart-sps/SUBMISSION_LOG.md` with confirmation URL/ID.
6. **Claim discipline** — submission text passes `bash paper/uai-2026/claim-gate.sh apart-sps/` (forbidden-word scan).

## 6. Implementation Plan

### Phase 1 — Pre-hackathon (now → May 21, 5 days)

Task 1.1: Operator registers
- [ ] **Operator**: open Luma URL `luma.com/4q2fnc39` (or fallback: Apart sprint page), register.
- [ ] **Operator**: decide solo vs team. If team, post to Apart Discord and/or LessWrong post for teammate-finding.
- [ ] **Operator**: capture registration confirmation in `apart-sps/REGISTRATION_LOG.md`.

Task 1.2: Idea note (agent-drafted, operator-reviewed)
- [ ] Agent drafts `apart-sps/idea-note.md` with the bridge framing from §4.
- [ ] Operator reviews; agent revises.
- [ ] Note used for teammate-finding and/or as solo entry pitch.

Task 1.3: Pre-hackathon artefact polish (agent)
- [ ] Confirm `agent-closeout-bench` and `llm-dark-patterns` install cleanly from a fresh clone.
- [ ] Verify the self-hosted marketplace install path is documented and reproducible.
- [ ] Tag a hackathon-friendly demo entry point.

### Phase 2 — Hackathon (May 22-24, 3 days)

The kickoff-day template is unknown today, so Phase 2 cannot be pre-specified in full. Skeleton:

Task 2.1: Kickoff (May 22)
- [ ] **Operator**: attend kickoff, receive submission template, share with agent.
- [ ] Agent and operator: revise idea-note to match the actual template.

Task 2.2: Build (May 22-24)
- [ ] Build the bridge artefact (TBD per kickoff; candidate: a formal-methods overlay on AgentCloseoutBench that compiles closeout-text rule packs to TLA+ or similar; OR an evaluation showing what % of closeout-stage dark-pattern instances regex catches vs what would need formal methods).
- [ ] Use the existing engine + corpus as the substrate; no new engine build.

Task 2.3: Submit (May 24)
- [ ] **Operator**: submit PDF + code link via the Apart submission form.
- [ ] Agent: log submission in `apart-sps/SUBMISSION_LOG.md`.

### Phase 3 — Post-hackathon (post-May 24)

- [ ] If top teams: prepare SPS Fellowship application (Jun-Oct 2026).
- [ ] If not advanced: capture lessons in `apart-sps/RETRO.md`; pivot to next slice.

## 7. Agent-Native Estimate

- Estimate type: agent-native for Phase 1; blocked/unknown for Phases 2-3
- **Phase 1**:
  - agent_wall_clock: optimistic 2 hr / likely 4 hr / pessimistic 8 hr (idea note + artefact polish + registration prep)
  - agent_hours: ~4 hr
  - human_touch_time: 30 min - 2 hr (registration click, idea-note review, teammate decision)
- **Phase 2**: blocked/unknown — kickoff-day template not yet revealed; estimate after May 22
- **Phase 3**: blocked/unknown — depends on advancement
- Calendar blockers: Luma registration availability (capacity unknown); Discord teammate-finding response time
- Confidence: medium-high for Phase 1 (existing artefacts give a strong head-start); medium for Phase 2 (unknown template); blocked/unknown for Phase 3

## 8. Verification

| Criterion | Method |
|---|---|
| C1 registration | `apart-sps/REGISTRATION_LOG.md` contains confirmation |
| C2 team decision | Recorded in REGISTRATION_LOG |
| C3 idea note | `apart-sps/idea-note.md` exists, claim-gate passes |
| C4 submission | `apart-sps/SUBMISSION_LOG.md` contains URL/ID |
| C5 claim discipline | `bash paper/uai-2026/claim-gate.sh apart-sps/` exits 0 |

## 9. Rollback

- Pre-registration: nothing to roll back.
- Post-registration pre-submission: can decline to submit; no public commitment.
- Post-submission: Apart hackathons accept all submissions; withdrawal not typical but possible via the contact email.

## 10. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Eligibility blocker | low | Verify on registration; if blocked, pivot to Global South AISH Jun 19-21 |
| Methods mismatch dominates judging | medium | Bridge framing in idea-note positions lightweight verification as *complement* not *replacement* of formal methods |
| Operator burnout (concurrent NeurIPS pause + hackathon focus) | medium | Hackathon is bounded (3 days); other slices stay paused |
| Team-finding too slow | medium-low | Solo entry is acceptable; operator can decide late |
| Submission template surprises | medium | Phase 2 revisions are part of the plan |
| Top-team threshold high (5 prizes only) | medium | Reframe success as "submission + Fellowship-application potential", not "win" |

## 11. Sources (verified 2026-05-16)

- [Secure Program Synthesis Hackathon page](https://apartresearch.com/sprints/secure-program-synthesis-hackathon-2026-05-22-to-2026-05-24)
- [LessWrong Apply to Mentor SPS](https://www.lesswrong.com/posts/SJdjLg5zSqrb2kMc7/exploding-note-apply-to-mentor-secure-program-synthesis)
- [Luma event page](https://luma.com/4q2fnc39) (registration link surface)
- [Apart sprints index](https://apartresearch.com/sprints/all)
- Existing project artefacts: `agent-closeout-bench/SPEC.md`, `paper/SPEC-paper-uai-2026.md`, `llm-dark-patterns/SECURITY_AUDIT.md`, strategic-pivot artifact

# Spec QA: Z7-SPS Hackathon Slice

Run ID: `sps-z7-2026-05-16`
Access date: 2026-05-16
SPEC: `SPEC-sps-hackathon.md`
Reviewer identity: `claude-opus-4-7` requested per `/opusolo`; runtime identity `insufficient_data`.

## Critical findings
**0 critical.**

## Major findings

**M1. Method mismatch is the most likely failure mode.**
The hackathon centres on formal methods (proof assistants, type systems, model checkers). Our submission must do more than honest-framing the gap; it must offer a *concrete* bridge artefact that resonates with formal-methods reviewers. Suggested bridge artefacts to consider for Phase 2:
- (a) Compile our closeout rule packs to a property specification language (TLA+, Alloy, or Z3 SMT). Demonstrate equivalence between regex match and a formal predicate.
- (b) Quantify what fraction of closeout-stage dark patterns regex catches vs. what would require formal verification. Frame as the empirical motivation for heavier methods.
- (c) Build a closeout-text type-checker that infers an "evidence-passed" type from the assistant's output; reject ill-typed closeouts.

Of these, (b) is the lowest-risk, most-aligned-to-existing-artefacts angle for a 3-day hackathon.

**M2. Registration URL extraction failed.**
The Luma URL `luma.com/4q2fnc39` is the most likely registration target but was not directly verified as the SPS hackathon page in this turn. Operator should sanity-check by visiting it before registering, or fall back to the Apart sprint page's "Sign Up" button.

**M3. Topic-fit framing risks underclaiming the existing work.**
The current Phase 1 idea-note framing pitches the hackathon submission as a "first-pass surface". Reviewers might miss that the underlying engine + benchmark + claim ledger are already substantive research-grade artefacts independent of the hackathon's formal-methods angle. The idea note should lead with the existing artefacts as evidence of execution capability, not as a tentative offering.

## Minor findings

**m1. Phase 2 is intentionally underspecified.**
Acceptable because the kickoff-day template is unknown. But operator should be aware that Phase 2 will need rapid replanning on May 22 once the template lands.

**m2. Operator bandwidth check is not formalised.**
The SPEC notes burnout risk but doesn't gate execution on operator capacity. Recommend an explicit op-check before Phase 2: if at any point during May 22-24 the operator wants to bail, the slice closes as `submitted-partial-or-withdrawn` cleanly.

**m3. Teammate-finding via Apart Discord is unverified.**
Apart's Discord existence is mentioned in past LessWrong posts but not confirmed in this turn's research. If operator wants teammates, they should find the Discord invite through the sprint's main page or the kickoff-day onboarding.

**m4. Prize money is not the leverage.**
The 5 prizes ($1K / $500 / $300 / $100 / $100) are small relative to the slice's true leverage, which is the Fellowship pipeline. The SPEC §10 already frames "win" as submission + Fellowship-application potential; this is correct.

**m5. The `apart-sps/` directory needs creating.**
On execution, agent creates `agent-closeout-bench/apart-sps/` as the working subdirectory. Existing `paper/uai-2026/`, `paper/uai-2026-sprint` branch, `.taste/strategic-pivot/` are all preserved.

## Improvement suggestions

1. **Add a "kickoff plan" snippet** to the SPEC that pre-commits to bridge artefact (b) above as the default Phase 2 plan, with (a) and (c) as backups depending on what the template invites.
2. **Reach out to one Apart-network contact pre-hackathon** if the operator has one — informal signal that we're submitting helps reviewer attention.
3. **Capture the existing artefacts in a 1-page "what we've already built" pre-pitch** for the idea note, so the bridge framing rests on demonstrated execution.
4. **Set an explicit decision point on May 21** (day before kickoff) — operator confirms registration, team status, and idea note final before the kickoff opens.

## Currentness source ledger

- Apart Secure Program Synthesis Hackathon page (verified live, 2026-05-16)
- Apart sprints index (verified live, 2026-05-16)
- LessWrong "Apply to Mentor SPS" post (verified, mentor recruitment angle)
- Submission template format (general Apart pattern, not SPS-specific): PDF per kickoff template
- Speaker / mentor names: explicit on the SPS page

Pending verification at Phase 2:
- Exact submission template fields
- Exact judging rubric for SPS-specific evaluation
- Whether Atlas Computing has its own preferred deliverable format

## Execution decision

**ALLOWED pending operator confirmation of**:
1. Slice scope acceptance (the bridge framing is honest but it is a strategic choice the operator should endorse).
2. Registration intent (operator commits to clicking through the Luma URL within the next 24-48 hours).
3. Solo vs team posture (or "decide later" — acceptable but should be settled by Phase 1 Task 1.1).

Confidence: medium. Downgrade reasons: kickoff template unknown until May 22; method-mismatch reviewer risk; concurrent operator load.

Block conditions (would flip ALLOWED → BLOCKED):
- Registration page reveals the hackathon is invitation-only or closed
- Operator decides not to commit the 3-day window
- Eligibility issue surfaces on registration

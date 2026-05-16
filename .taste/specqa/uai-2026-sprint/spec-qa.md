# Spec QA: SafeAI@UAI 2026 Workshop Paper Sprint

Run ID: `uai-2026-sprint`
Access date: 2026-05-16
SPEC reviewed: `paper/SPEC-paper-uai-2026.md`

## Reviewer Identity Status

- requested_reviewer: `claude-opus-4-7`
- proven_reviewer: `insufficient_data` (no `/status` check, no sentinel,
  no durable model-identity artifact in this session)
- reviewer_action: conduct inline review with downgraded confidence;
  do not claim Opus 4.7 reviewed.

## Critical Findings

**Status**: 0 critical findings that block execution.

## Major Findings

### M1: SOTA model identifiers in §6 Task 2 are not version-verified
The SPEC says "Claude Sonnet 4.6, GPT-5.x, Gemini 2.x" but does not pin
exact model IDs (e.g. `gpt-5.4-2026-XX`, `gemini-2.5-pro-2026-XX`).
Reviewers will ask which models judged. Required: pin exact API model
IDs in Task 2 Day 3 before running, log them in
`annotations/judge_metadata.json`. Live verification of current GPT and
Gemini model IDs needed at run time (knowledge cutoff is Jan 2026; May
2026 model identifiers may have shifted).

**Action**: when Task 2 starts, run live API model-listing to pick
current GA model IDs. Do not rely on training-data assumptions.

### M2: DarkBench precedent is load-bearing for honest κ; verify quote
The SPEC §3 C3 cites DarkBench's "low κ acceptable" precedent. Before
final paper, verify the DarkBench paper explicitly uses this framing —
the WebSearch snippet said "despite low Cohen's Kappa on some
dark pattern categories, indicating poor inter-rater agreement, the
summary statistics over models and dark patterns remain consistent."
This is paraphrase from a derivative source. Direct PDF quote needed
in `paper/uai-2026/source_ledger.md` before this argument appears in
the final paper.

**Action**: Day 1-2, fetch DarkBench ICLR 2025 PDF, extract the exact
sentence and page reference. Add to source ledger.

### M3: 4-page limit is tight for 6 sections + Threat Model + Limitations
The SPEC §6 Task 1 lists ~9 sections. Realistic 4-page budget:
- Abstract: 0.2 pg
- Intro: 0.5 pg
- Related Work: 0.6 pg
- Boundary Formalisation + Dataset: 1.0 pg
- Annotation + Results (κ): 0.8 pg
- Threat Model + Limitations: 0.6 pg
- Conclusion: 0.2 pg
- References: separate (workshop typically allows refs beyond limit)

Tight but feasible. Risk: each section will be compressed; reviewers
may flag any single section as too thin.

**Action**: write to outline first, do a one-page-budget pass on Day
5 before drafting prose, cut any section that exceeds budget.

## Minor Findings

### m1: Cost estimate in §8 Rollback uses unverified per-row price
`200 × 3 × $0.02 = $12` worst case. Current 2026 API prices for
Sonnet 4.6 / GPT-5.x / Gemini 2.x must be checked at run time. Likely
order of magnitude correct; should not be quoted as authoritative.

### m2: Workshop format/template still unknown
Risk R1 noted. Day 1 action: WebFetch the SafeAI@UAI 2026 submission
page, look for explicit LaTeX template link. If not found, default
to PMLR style.

### m3: §3 C7 "Submission logged" cannot be auto-verified by harness
This is correctly marked operator-only. Confirm: the harness must
NOT attempt OpenReview submission. Manual step only.

### m4: ICML 2026 Agents in the Wild deadline already past (May 8)
Out of scope but worth noting in `SUBMISSION_LOG.md` as rejected
venue. NeurIPS workshop Aug 29 is the v2 target.

### m5: SPEC doesn't state which `agent-closeout-bench` or
`llm-dark-patterns` repo branch hosts the paper sprint commits
Recommend: new branch `paper/uai-2026-sprint` on
`agent-closeout-bench` to isolate paper work from main benchmark
contract. Final merge after submission.

## Improvement Suggestions

1. Add a §11 "First-week checkpoint" listing what must be true by
   end of Day 5 to keep the 12-day window achievable. If checkpoint
   fails, switch to NeurIPS workshop fallback before sinking more
   effort.
2. Add `pre-commit` hook in `paper/uai-2026/` running `claim-gate.sh`
   on every paper-source commit (per §9 Risk mitigation).
3. Consider including the LDP project as a co-equal artifact in the
   paper (rather than just citing it). The "hook suite" angle
   strengthens the "infrastructure" framing and gives reviewers more
   to anchor on. Tradeoff: more scope = more 4-page pressure.
4. Decide upfront: single-author submission (operator) or co-author
   collaborator. Affects OpenReview profile setup.

## Currentness Source Ledger

- SafeAI@UAI 2026 deadline May 28 — verified 2026-05-16 via WebFetch
- NeurIPS 2026 E&D May 4/6 (past) — verified 2026-05-16
- NeurIPS 2026 workshops Aug 29 — verified 2026-05-16
- ICML 2026 Agents in the Wild May 8 (past) — verified 2026-05-16
- DarkBench ICLR 2025 low-κ precedent — verified via WebSearch snippet,
  PDF quote pending (see M2)
- ProbGuard arXiv:2508.00500 v3 March 2026 — verified
- AgentSpec arXiv:2503.18666 ICSE'26 April 2026 — verified
- Live API model IDs for Claude Sonnet 4.6, GPT-5.x, Gemini 2.x —
  pending (see M1)

## Execution Decision

**ALLOWED**: execution may proceed past the plan-mode checkpoint after
explicit operator approval. No critical findings. Three major findings
have concrete Day-1/Day-2 actions baked into the plan.

**Confidence**: medium. Downgrade reasons: 12-day window is tight,
model-identity proof not run, DarkBench precedent quote pending.

**Block conditions** (would flip ALLOWED → BLOCKED if discovered
during Day 1-2):
- SafeAI@UAI workshop template not available and PMLR fallback unclear
- Live API access blocked (no Claude/GPT/Gemini API credentials)
- DarkBench PDF does not actually contain the "low κ acceptable"
  framing in clear form

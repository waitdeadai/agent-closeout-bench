# /introspect pre-plan — Paper draft 2026-05-16

Run ID: `2026-05-16-paper-draft`
Subject: `paper/uai-2026/main.tex` at commit `779d8f4` + Table 1 skeleton (uncommitted)
Triggered by: completion of all draft sections, before /verify and PDF compile

## Findings

### CRITICAL — must fix before commit/push

**C1. Misstated origin of closeout texts (Abstract L26, Annotation §L116).**
Both passages say closeout texts "originate from Claude Code agents" and use this to justify the SPB concern. In fact, the v0.3 corpus is `deterministic_synthetic_positive`-generated per `data/<category>/{positives,negatives}.jsonl`, not transcripts from real Claude sessions. The records carry `model: deterministic-template-v1`, not a real model.

The honest framing: the synthetic templates encode lexical patterns observed in real Claude Code closeout text (that is what motivated the project), so a Claude judge may be biased toward or against phrasings stylistically resembling Anthropic-family outputs even though the text was not actually produced by Claude. SPB risk is present in a weaker, style-correlated form, not in the literal training-distribution form documented by \citet{spb2026}.

**Fix**: rewrite both passages to state the synthetic origin accurately, then describe the SPB risk as a style-correlation effect that the mitigations still address.

### MAJOR

**M1. Reference Engine §L153 unclear ("Where a faithful closeout would carry concrete evidence").**
The clause is hard to parse on first read and the antecedent of "where" is ambiguous. Rewrite for clarity.

**M2. Contribution (iii) in Intro phrases the DarkBench precedent loosely.**
"Follows the precedent set by DarkBench for honest $\kappa$ reporting" — DarkBench's specific contribution to the precedent is using LLM annotators with honest per-category $\kappa$ reporting even when low. Tighten the phrasing.

**M3. Conclusion §L: missing locked-test scope statement.**
"A v1.0 release with two independent human annotation passes, adjudication, agreement metrics, a frozen detector commit, and a locked-test evaluation is planned" — mirrors Gate 5 in `readiness_audit_2026-05-13.md`. Good as-is, but should explicitly say "performance numbers gated on Gate 5 completion".

### MINOR

**m1. Intro §L40 unbacked claim**: "different remediation paths than chat-surface or action-trace failures" — paper does not actually establish this. Soften to "and likely different remediation paths".

**m2. Closeout Boundary §L83 "scope was respected"** — agents don't always assert this. Replace with "that the work covered the requested scope".

**m3. refs.bib: SORRY-Bench full author list is `Xie, Tinghao and others`.** Acceptable for submission but should be filled before camera-ready.

**m4. Table 1 caption says "after the locked annotation run".** Wording is fine but "locked" overlaps with "locked-test" terminology. Consider "after the v0.3 LLM-judge annotation run is committed".

**m5. Page budget unmeasured.** Without `pdflatex` we cannot confirm ≤ 4 pages until Day 6. Current word count (2826) and typical SafeAI/UAI density suggest fit, but uncertainty remains.

### Assumption audit

A1. The reader recognises the "agentic coding assistant" framing. We do not define agentic coding assistant in the paper — relying on Claude Code being well-known. **Acceptable for a 4-page workshop paper at a safety venue; would need definition in a main-track submission.**

A2. The reader trusts Cohen's $\kappa$ as the right agreement metric for binary annotation on disjoint categories. **Standard convention; safe.**

A3. The reader accepts a pre-release paper. **Workshop scope is friendlier to this than main-track; consistent with SafeAI@UAI's "Foundations / Uncertainty / Interpretability / Engineering & Deployment" scope.**

### Evidence audit

E1. All 5 citations have verified authors and venues (`source_ledger.md`).
E2. DarkBench $\kappa=0.27$ claim is from a direct PDF quote on page 15.
E3. Self-preference bias citation (`arXiv:2604.22891`) has not had its full author list verified — TODO before camera-ready.
E4. ProbGuard/AgentSpec same-group differentiation: verified — both from Wang/Poskitt/Sun at SMU.

### Scope audit

S1. Paper makes no $F_1$ benchmark performance claim ✓
S2. Paper does not claim ACSP-CC as adopted standard ✓
S3. Paper does not claim prompt-injection immunity ✓
S4. Paper explicitly states it is pre-release ✓
S5. Paper notes English-only scope ✓

### Verification audit

V1. `claim-gate.sh` passes (verified after last edit)
V2. PDF compile: pending (no texlive locally)
V3. Cohen $\kappa$ pipeline: dry-run verified end-to-end with 20 records
V4. Table 1 cells correctly marked TBD pending real data

### Risk audit

R1. Pushing to public remote before UAI submission compromises double-blind anonymity. Acknowledged in `SUBMISSION_LOG.md`; partly mitigated by the underlying repo already being public. **Stance: accept the residual risk; workshop reviewers can search anyway, and the open-source benchmark is the contribution.**

R2. SPB framing as currently drafted (the C1 fix above) overstates the risk. Fixing now will strengthen the paper, not weaken it.

R3. ~$1.53 API spend for real annotation run is the next reversibility cliff. Pre-committed in SPEC §8, recomputed in source_ledger.md.

## Confidence after introspection

- Pre-introspection: **medium** (draft complete, claim-gate pass)
- Post-introspection: **medium**, **but with C1 fix required before next commit**
- Downgrade reason: one critical accuracy issue, three major clarifications, five minor edits

## Blocker decisions

| Decision | Status |
|---|---|
| Apply C1 fix immediately | **REQUIRED before next commit** |
| Apply M1, M2 fixes | recommended in same commit |
| Apply m1-m5 fixes | recommended same commit |
| Proceed to /verify after fix | yes |
| Proceed to LDP README + CI deprecation work | yes (independent of paper draft) |

## Outcome

ALLOWED with the C1 fix and recommended minor edits applied. /verify can run after the fix.

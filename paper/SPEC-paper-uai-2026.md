# SPEC: NeurIPS 2026 Workshop Paper (re-targeted from SafeAI@UAI 2026)

Access-date anchor for external claims: 2026-05-16.

## Re-target Decision — 2026-05-16T13:40-03:00

This sprint was originally targeted at SafeAI@UAI 2026 (deadline 2026-05-28 AoE). On 2026-05-16 the operator chose to defer the May 28 sprint and re-target to a NeurIPS 2026 workshop (contributions due ~2026-08-29 AoE per `neurips.cc/Conferences/2026/Dates`). The deferred timeline removes the operator API-keys + LaTeX-path blockers and adds room for human-adjudicated labels (per `paper/readiness_audit_2026-05-13.md` Gates 4-5). All draft work on this branch (`paper/uai-2026-sprint`) remains intact; the 4-page workshop draft expands to the new workshop's page allowance.

Target venue: NeurIPS 2026 Workshop (specific workshop TBD; accepted workshop list announced 2026-07-11 per `neurips.cc/Conferences/2026/Dates`).
Submission deadline: **~2026-08-29 AoE** (verify against the specific workshop's CFP once accepted workshops are listed).
Format: typically 6-9 pages plus references (varies by workshop), OpenReview.

## Original target (preserved for reference)

Target venue: SafeAI@UAI 2026 (Amsterdam, Aug 21, 2026).
Submission deadline: 2026-05-28 AoE (DEFERRED 2026-05-16).
Format: 4-page workshop paper, original-research track, OpenReview.

## 1. Problem Statement

AgentCloseoutBench (ACB) and the LLM Dark Patterns hook suite (LDP) are
publishable as pre-release benchmark infrastructure but currently lack a
single submission-ready artifact. This sprint produces a 4-page paper that
formalises closeout text as a safety boundary, releases the candidate
corpus and annotation protocol, and positions the work against
ProbGuard / AgentSpec / DarkBench without claiming final performance.

## 2. Research Claims (scope-locked)

Primary claim, unchanged from `SPEC.md` §1:

> To our knowledge, AgentCloseoutBench is the first benchmark for
> dark-pattern detection on agentic coding assistant closeout text at the
> Claude Code Stop/SubagentStop `last_assistant_message` boundary.

Engine claim, unchanged from readiness audit §"Scientific Claim Audit":

> Out-of-band deterministic enforcement at the agentic coding assistant
> closeout boundary makes specific dark-pattern and false-closeout
> mechanics observable, reproducible, and benchmarkable.

Differentiation claim (NEW, requires Related Work source ledger):

> Existing runtime monitors for LLM agents (ProbGuard, AgentSpec) target
> action-level execution traces; this work targets the orthogonal axis of
> closeout-text claim discipline at the assistant-message lifecycle
> surface.

Non-claims (forbidden under any rewording):

- Final benchmark scores. The paper reports κ on an LLM-as-judge sample
  and candidate-corpus diagnostics, not final human-gold performance.
- Universal agent benchmark.
- ACSP-CC as adopted standard or certification.
- Prompt-injection immunity.
- Production-ready safety solution.
- State-of-the-art robustness.
- Beating ProbGuard / AgentSpec on any metric — they measure a different
  surface.

## 3. Success Criteria

Each criterion is verifiable by a command, file inspection, or external
artifact check.

1. **Paper PDF exists at `paper/uai-2026/paper.pdf`** within 4 pages
   (excluding references, supplementary) and compiles cleanly from LaTeX.
   - Verify: `pdfinfo paper/uai-2026/paper.pdf | grep -i pages` returns
     `Pages: ≤ 4` for main content; full file may include refs.
2. **LLM-as-judge annotation script runs end-to-end** on a 200-row sample
   of the 800-row corpus, producing three judge-label files
   (`annotations/judge_claude.jsonl`, `annotations/judge_gpt.jsonl`,
   `annotations/judge_gemini.jsonl`).
   - Verify: each file has 200 rows, schema-valid against
     `annotations/judge_schema.json`.
3. **Cohen's κ computed honestly** across judge pairs and against
   candidate labels, written to `annotations/judge_agreement.json`.
   - Verify: file contains per-category pairwise κ for at least
     {claude-gpt, claude-gemini, gpt-gemini, ensemble-vs-candidate};
     low κ is acceptable per DarkBench (ICLR 2025) precedent.
4. **Related Work section cites ProbGuard, AgentSpec, DarkBench,
   HarmBench, AgentSpec, SORRY-Bench** with a differentiation paragraph
   distinguishing closeout-text from action-level monitoring.
   - Verify: `grep -E "ProbGuard|AgentSpec|DarkBench|HarmBench" paper/uai-2026/paper.tex`
     finds all five.
5. **Threat Model section** explicitly enumerates: lexical evasion, hook
   misconfiguration, runtime bypass, in-band vs out-of-band, evidence-marker
   limitations, synthetic-corpus artifacts.
   - Verify: section exists with all six items, checked by
     `grep -c "^\\\\item" paper/uai-2026/threat-model.tex` ≥ 6.
6. **Claim-ledger preflight passes** — no forbidden wording in paper
   source.
   - Verify: `bash paper/uai-2026/scripts/claim-gate.sh paper/uai-2026/`
     exits 0; scans for `standard`, `certified`, `certification`,
     `final score`, `final metric`, `SOTA`, `state-of-the-art`,
     `prompt-injection-proof`, `immune`, `production-ready` and confirms
     each occurrence is inside a clearly-marked non-claim or related-work
     citation.
7. **OpenReview submission record exists** as a separate manual step,
   logged in `paper/uai-2026/SUBMISSION_LOG.md` with OpenReview URL,
   submission timestamp, and abstract hash. This step is operator-only;
   the harness must not auto-submit.

## 4. Scope

### In scope
- 4-page workshop paper draft + LaTeX source under `paper/uai-2026/`
- LLM-as-judge annotation pipeline (Claude Sonnet 4.6, GPT-5.x, Gemini 2.x)
  on a 200-row sample of the existing 800-row candidate corpus
- Cohen's κ computation across judge pairs and vs. candidate labels
- Related Work section with verified citations to ProbGuard (arXiv:2508.00500),
  AgentSpec (arXiv:2503.18666), DarkBench (ICLR 2025), HarmBench
  (arXiv:2402.04249), SORRY-Bench
- Threat Model section enumerating limitations
- Claim-gate preflight script
- README update on `agent-closeout-bench` linking to the paper
  (only after submission)

### Out of scope
- Human annotation pass (defer to NeurIPS workshop v2, Aug 29 deadline)
- Final locked-test evaluation with `label_final` (gated by Gate 4/5 in
  `paper/readiness_audit_2026-05-13.md`)
- v4 semantic engine prototype (defer; not a paper-blocker)
- LDP README Threat Model section in `llm-dark-patterns` repo (do
  alongside paper but not blocker for paper submission)
- External outreach (HN, X, blog posts) — separate decision after
  submission
- CI deprecation PRs (`actions/checkout@v4`, `codeql-action@v3`) — fix
  this week as hygiene PR but not a paper-blocker
- Auto-submission to OpenReview (operator-only step)

## 5. Agent-Native Estimate

- **Estimate type**: agent-native wall-clock
- **Execution topology**: local + subagents (workstation 16 cores 32GB,
  recommended ceiling 6; effective lanes 1-2 for paper drafting, 1 for
  API-bound annotation runs)
- **Capacity evidence**: `scripts/parallel-capacity.sh --summary` reports
  workstation, 16 cores, 32GB RAM, recommended 6, default subagents.
  MAX_PARALLEL_AGENTS local ceiling is not the binding constraint;
  API rate limits and supervisor review capacity are.
- **Effective lanes**: 2 of ceiling 6
- **Critical path**:
  Day 1-2 (scope + outline) → Day 3-4 (annotation pipeline + API runs)
  → Day 5-6 (results tables + κ) → Day 7-8 (related work + threat model)
  → Day 9-10 (draft + internal review) → Day 11-12 (polish + submit)
- **Agent wall-clock**: optimistic 5 days / likely 9 days / pessimistic 12 days
- **Agent-hours**: ~30 hours total (drafting 12h, pipeline 6h, related
  work 4h, threat model 3h, polish 5h)
- **Human touch time**: 4-8 hours (read drafts, approve framing, final
  pass, manual OpenReview submission)
- **Calendar blockers**: API rate limits on Claude/GPT/Gemini (mostly
  parallelisable), OpenReview profile required (operator has one),
  deadline AoE 2026-05-28 means effective cutoff 2026-05-29 02:00 UTC.
  No CI queue or business-hours dependency.
- **Confidence**: medium
- **Downgrade reason**: 12 days is tight; threat model and related work
  require sharp claim discipline; first-time submission to this workshop
  introduces formatting unknowns
- **Human-equivalent baseline (secondary)**: ~2-3 weeks for a researcher
  pair, given existing draft material in `outline.md` and
  `readiness_audit_2026-05-13.md`

## 6. Implementation Plan

### Task 1: Paper scaffolding (Day 1-2)
Definition of Done:
- [ ] `paper/uai-2026/` directory created with LaTeX skeleton
- [ ] UAI/PMLR template applied (or workshop template if specified)
- [ ] Section stubs: Abstract, Intro, Related Work, Boundary
      Formalisation, Dataset, Annotation Protocol, Threat Model,
      Limitations, Conclusion
- [ ] `paper/uai-2026/claim-gate.sh` script copying logic from existing
      claim discipline
- [ ] `paper/uai-2026/SUBMISSION_LOG.md` stub
- [ ] Source ledger initialised with the 9 cited sources from
      DeepResearch turn

### Task 2: LLM-as-judge annotation pipeline (Day 3-4)
Definition of Done:
- [ ] Sample 200 rows from `data/` using deterministic seed; record in
      `annotations/sample_uai_2026.jsonl`
- [ ] Judge prompt template at `annotations/judge_prompt.md` with
      exact category definitions matching `SPEC.md` §2
- [ ] Annotation runner at `annotations/run_judges.py` that calls
      Claude Sonnet 4.6, GPT-5.x, Gemini 2.x via their respective APIs
- [ ] Schema validation script at `annotations/validate_judge_output.py`
- [ ] Dry run on 5 rows per judge passes
- [ ] Full run completes, producing three 200-row JSONL files

### Task 3: Agreement computation (Day 5)
Definition of Done:
- [ ] `annotations/compute_judge_agreement.py` produces
      `annotations/judge_agreement.json` with per-category pairwise κ
- [ ] Per-category breakdown shows where judges disagree most
- [ ] Comparison vs. candidate labels included
- [ ] Honest reporting: low κ is acceptable, not hidden

### Task 4: Related Work + differentiation (Day 6-7)
Definition of Done:
- [ ] Related Work section cites ProbGuard, AgentSpec, DarkBench,
      HarmBench, SORRY-Bench with year + venue + 1-sentence
      characterisation each
- [ ] Differentiation paragraph: closeout-text vs action-level vs
      probabilistic-prediction
- [ ] Boundary formalisation: define
      `Stop/SubagentStop.last_assistant_message` as the evaluation
      surface, contrast with chat-surface dark-pattern work
- [ ] All citations checked: each arXiv ID exists, each ICLR/ICSE/NeurIPS
      paper has correct year and venue

### Task 5: Threat Model + Limitations (Day 8)
Definition of Done:
- [ ] Threat Model enumerates 6 items: lexical evasion, hook
      misconfiguration, runtime bypass, in-band vs out-of-band,
      evidence-marker limitations, synthetic-corpus artifacts
- [ ] Limitations section integrates content from
      `LIMITATIONS.md` and readiness audit gaps
- [ ] No forbidden claims (run `claim-gate.sh`)

### Task 6: Draft polish + internal review (Day 9-10)
Definition of Done:
- [ ] Full paper compiles to PDF, ≤ 4 pages main content
- [ ] Abstract written, runs `claim-gate.sh` clean
- [ ] All citations resolve; references compile
- [ ] Internal /introspect pass on the draft

### Task 7: Submission prep (Day 11-12, operator-driven)
Definition of Done:
- [ ] Final PDF compiled
- [ ] Supplementary materials zipped (annotation script, judge output,
      agreement JSON, candidate diagnostics, license, dataset card)
- [ ] OpenReview submission completed by operator
- [ ] `SUBMISSION_LOG.md` updated with URL, timestamp, hash

## 7. Verification

| Criterion | Verification Method |
|---|---|
| C1: PDF ≤ 4 pages | `pdfinfo paper/uai-2026/paper.pdf` |
| C2: Three judge files | `wc -l annotations/judge_*.jsonl` |
| C3: κ JSON valid | `python3 annotations/validate_agreement.py` |
| C4: 5 citations present | `grep -E "ProbGuard\|AgentSpec\|DarkBench\|HarmBench\|SORRY-Bench" paper/uai-2026/paper.tex` |
| C5: Threat Model 6 items | manual section inspection + grep |
| C6: Claim-gate passes | `bash paper/uai-2026/claim-gate.sh` |
| C7: Submission logged | manual inspection of `SUBMISSION_LOG.md` |

`/verify` invocation at end of each task; `/introspect` before final
draft polish and before submission prep.

## 8. Rollback Plan

The work is local-only until OpenReview submission. Rollback by task:

1. **Pre-submission rollback**: `git revert` or `git reset` of paper
   commits; no external state changed.
2. **Annotation API spend rollback**: not financially recoverable,
   but bounded — 200 rows × 3 judges × ~$0.02 = ~$12 worst case.
   Tracked in `annotations/api_cost_log.md`.
3. **Post-submission rollback**: OpenReview allows withdrawing
   submissions before the review process completes. If a critical
   error is discovered, withdraw via OpenReview UI, fix, resubmit
   (if before deadline) or target NeurIPS workshop (Aug 29).
4. **Claim violation rollback**: if `claim-gate.sh` finds forbidden
   wording post-commit, immediate `git revert` of the offending
   commit; no public exposure until submission.

## 9. Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| Workshop format/template unknown | Medium | Day 1: fetch UAI workshop template; if unavailable, use PMLR default |
| API rate limits delay annotation | Low | 200 rows × 3 judges is small; spread over 2 days; cache responses |
| Claim drift in drafting | Medium | `claim-gate.sh` runs on every commit via pre-commit hook |
| Reviewers reject as "just hooks" | Medium-high | Frame as benchmark + boundary formalisation, not engine; cite ProbGuard/AgentSpec as orthogonal |
| 12 days insufficient | Medium | Fallback: target NeurIPS workshop Aug 29 with same materials |
| Forbidden claim slips into abstract | Low | `claim-gate.sh` + manual review before submission |

## 10. References (sprint source ledger, access 2026-05-16)

- SafeAI@UAI 2026 workshop CFP — https://safe-ai-workshop.github.io/uai-2026/
- NeurIPS 2026 E&D Track CFP — https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets
- NeurIPS 2026 workshops dates — https://neurips.cc/Conferences/2026/Dates
- DarkBench ICLR 2025 paper — https://proceedings.iclr.cc/paper_files/paper/2025/file/6f6421fbc2351067ef9c75e4bcd12af5-Paper-Conference.pdf
- ProbGuard / Pro²Guard — https://arxiv.org/abs/2508.00500
- AgentSpec — https://arxiv.org/abs/2503.18666
- HarmBench — https://arxiv.org/abs/2402.04249
- Prior outline — `paper/outline.md`
- Prior readiness audit — `paper/readiness_audit_2026-05-13.md`
- Benchmark contract — `SPEC.md`
- Claim ledger — `CLAIM_LEDGER.md`
- Limitations — `LIMITATIONS.md`

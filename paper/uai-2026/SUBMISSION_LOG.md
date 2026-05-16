# Submission Log — SafeAI@UAI 2026

Target venue: SafeAI@UAI 2026 (Amsterdam, Aug 21, 2026)
Submission deadline: 2026-05-28 AoE
Portal: https://openreview.net/group?id=auai.org/UAI/2026/Workshop/SafeAI
Review style: double-blind (per `safeai2026.cls`, anonymous by default)
Page limit: 4 (references and supplementary excluded)

## Pre-flight Checklist

- [ ] `bash claim-gate.sh paper/uai-2026/` exits 0
- [ ] PDF main content `pdfinfo main.pdf | grep Pages` reports ≤ 4 pages (excluding refs)
- [ ] `\documentclass{safeai2026}` is the base (NOT `[accepted]`) for submission version
- [ ] No author identity in the PDF (anonymous submission)
- [ ] No URLs that reveal identity (no `github.com/waitdeadai/...` URLs in submission PDF)
- [ ] References compile without error
- [ ] Source ledger entries all verified (`source_ledger.md`)
- [ ] DarkBench quote and Table 3 numbers verified against PDF (page 15)
- [ ] ProbGuard / AgentSpec arXiv IDs verified
- [ ] Five required citations present (DarkBench, HarmBench, ProbGuard, AgentSpec, SORRY-Bench)
- [ ] Threat Model section enumerates ≥ 6 items
- [ ] Abstract reads cleanly without mathematical notation
- [ ] Supplementary zip prepared (annotation script, judge output, agreement JSON, dataset card, license)

## Submission Record

- Status: NOT YET SUBMITTED
- OpenReview URL: (filled after submission)
- Submission timestamp (UTC): (filled after submission)
- PDF SHA256: (filled after submission)
- Abstract SHA256: (filled after submission)

## Withdrawal / Resubmission Plan

If submission contains a critical error discovered post-submission:

1. Withdraw via OpenReview UI before review process completes
2. Fix the error on `paper/uai-2026-sprint` branch
3. Re-submit if deadline still open, OR
4. Target NeurIPS 2026 workshop (Aug 29 deadline) with same materials

## Author Identity Policy

For the submission PDF:
- `\author{Anonymous Submission}` in `main.tex`
- No identifying URLs (no `github.com/waitdeadai`, no personal email)
- Supplementary materials hosted on anonymous repo or zipped inline
- Self-citations phrased in third person if applicable

For the camera-ready (only if accepted):
- Switch to `\documentclass[accepted]{safeai2026}` and fill in real author block

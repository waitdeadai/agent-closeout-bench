# Source Ledger — SafeAI@UAI 2026 Paper Sprint

Access date: 2026-05-16
Time anchor: 2026-05-16T01:34:32-03:00 (from minmaxing system clock)

All external claims in `main.tex` must trace to an entry here.

## Cited (must appear in `refs.bib`)

### S1. DarkBench (ICLR 2025 Oral)
- **Identifier**: arXiv:2503.10728 / ICLR 2025 proceedings paper
- **Authors (verified 2026-05-16)**: Esben Kran, Jord Nguyen, Akash Kundu, Sami Jawhar, Jinsuk Park, Mateusz Maria Jurewicz (Apart Research)
- **URL**: https://proceedings.iclr.cc/paper_files/paper/2025/file/6f6421fbc2351067ef9c75e4bcd12af5-Paper-Conference.pdf
- **HuggingFace dataset**: https://huggingface.co/datasets/apart/darkbench
- **GitHub**: https://github.com/apartresearch/darkbench
- **Local extracted text**: `/tmp/darkbench.txt` (page 15, lines 800-880)
- **Status**: verified, exact quote extracted

**Exact quote (page 15, paragraph above Table 3)**:
> Despite a low Cohen's Kappa on some dark pattern categories, indicating
> poor inter-rater agreement, the summary statistics over models and dark
> patterns remain consistent. See Table 3.

**Methodology facts verified from PDF and WebSearch**:
- Corpus: 660 prompts across 6 dark-pattern categories
- Categories: Anthropomorphization, User retention, Brand bias, Sycophancy, Harmful generation, Sneaking
- 3 LLM annotators: Claude 3.5 Sonnet (Anthropic, 2024), Gemini 1.5 Pro, GPT-4o
- 3 human annotators on 1680 examples
- Annotation collected via LimeSurvey
- Evaluated 14 models across 5 leading companies (OpenAI, Anthropic, Meta, Mistral, Google)
- Table 3 reports per-category Cohen's κ vs human annotators per LLM judge:
  | Category | Claude-3.5-Sonnet K | Gemini-1.5-Pro K | GPT-4o K |
  |---|---|---|---|
  | Anthropomorphization | 0.75 | 0.64 | 0.69 |
  | User retention | 0.62 | 0.72 | 0.66 |
  | Brand bias | 0.49 | 0.49 | 0.44 |
  | Sycophancy | 0.57 | 0.27 | 0.73 |
  | Harmful generation | 0.98 | 0.90 | 0.96 |
  | Sneaking | 0.56 | 0.46 | 0.42 |
  | Overall | 0.75 | 0.70 | 0.71 |
- Lowest per-category κ: 0.27 (Gemini-1.5-Pro on Sycophancy) — still published at ICLR 2025 Oral.

**Used in our paper at**: §Related Work (citation), §Annotation Protocol (methodology and honest-κ precedent).

### S2. HarmBench
- **Identifier**: arXiv:2402.04249
- **Authors (verified 2026-05-16)**: Mantas Mazeika, Long Phan, Xuwang Yin, Andy Zou, Zifan Wang, Norman Mu, Elham Sakhaee, Nathaniel Li, Steven Basart, Bo Li, David Forsyth, Dan Hendrycks (Center for AI Safety + collaborators)
- **URL**: https://arxiv.org/abs/2402.04249
- **GitHub**: https://github.com/centerforaisafety/HarmBench
- **Status**: identifier and authors verified

**Used in our paper at**: §Related Work — characterise as standardised red-teaming for refusal; 18 red-teaming methods × 33 target LLMs.

### S3. ProbGuard / Pro²Guard
- **Identifier**: arXiv:2508.00500 (v1 Aug 2025, v3 Mar 2026)
- **Authors (verified 2026-05-16)**: Haoyu Wang, Christopher M. Poskitt, Jiali Wei, Jun Sun
- **URL**: https://arxiv.org/abs/2508.00500
- **Status**: identifier, authors, and key claims verified.

**Note on author overlap with AgentSpec (S4)**: Wang, Poskitt, and Sun are co-authors on both ProbGuard and AgentSpec — this is a single research line at SMU. Our paper should treat the "action-level runtime enforcement" thread as one orthogonal line of work, not two independent competing lines.

**Verified claim** (via WebSearch result):
> ProbGuard is a proactive runtime monitoring framework for LLM agents that
> anticipates safety violations through probabilistic risk prediction.
> It abstracts agent executions into symbolic states and learns a Discrete-Time
> Markov Chain (DTMC) from execution traces.

**Used in our paper at**: §Related Work — characterise as action-level probabilistic monitor; differentiation paragraph (closeout-text axis vs action axis).

### S4. AgentSpec
- **Identifier**: arXiv:2503.18666 (ICSE'26, Rio de Janeiro, April 12--18, 2026)
- **Authors (verified 2026-05-16)**: Haoyu Wang, Christopher M. Poskitt, Jun Sun
- **URL**: https://arxiv.org/abs/2503.18666
- **GitHub**: https://github.com/haoyuwang99/AgentSpec
- **Status**: identifier, authors, venue verified.

**Verified claim** (via WebSearch result):
> AgentSpec is a lightweight domain-specific language for specifying and
> enforcing runtime constraints on LLM agents, with users defining structured
> rules that incorporate triggers, predicates, and enforcement mechanisms.

**Used in our paper at**: §Related Work — characterise as DSL for action-level pre-execution constraints; differentiation paragraph.

### S5. SORRY-Bench
- **Identifier**: arXiv:2406.14598 (ICLR 2025)
- **Authors (partially verified 2026-05-16)**: Tinghao Xie + 15 other authors from Princeton, Virginia Tech, Stanford, UC Berkeley, UIUC, U. Chicago. Full author list TODO before camera-ready.
- **URL**: https://arxiv.org/abs/2406.14598
- **OpenReview**: https://openreview.net/forum?id=YfKNaRktan
- **HuggingFace**: https://huggingface.co/datasets/sorry-bench/sorry-bench-202406
- **Status**: lead author and venue verified; full author list pending.

**Verified claim**:
> SORRY-Bench introduced a 45-class safety taxonomy (44 fine-grained
> categories in one version) across four high-level domains: Hate Speech
> Generation, Assistance with Crimes or Torts, Potentially Inappropriate
> Topics, and Potentially Unqualified Advice.

**Used in our paper at**: §Related Work — characterise as refusal taxonomy on chat outputs.

### S6. Self-Preference Bias in LLM-as-a-Judge (April 2026)
- **Identifier**: arXiv:2604.22891 (April 2026)
- **Authors**: TODO (verify before camera-ready)
- **URL**: https://arxiv.org/abs/2604.22891
- **Status**: identifier verified; key findings extracted.

**Verified claims** (via WebSearch April 2026):
> Self-Preference Bias (SPB) is a directional evaluative deviation where
> LLMs systematically favor or disfavor their own generated outputs during
> evaluation. Analysis of 20 mainstream models uncovered a counterintuitive
> pattern in which stronger model capabilities are often associated with
> larger SPB. Models such as GPT-4o and Claude 3.5 Sonnet systematically
> assign higher scores to their own outputs.

**Implication for our paper**:
Our closeout texts come from Claude Code agents (Anthropic family). Using
Claude Sonnet 4.6 as a judge introduces SPB risk. Mitigations to apply:
1. Hide model identity in the closeout text shown to the judge (strip
   "Claude" tokens where possible, normalise framework-specific phrasing)
2. Randomise the order of records in the prompt (per-record judgment,
   not pairwise)
3. Report cross-judge disagreement as an SPB indicator, especially when
   Claude Sonnet 4.6 agrees with the candidate label more often than GPT
   or Gemini do
4. Acknowledge SPB risk in the limitations section

**Used in our paper at**: §Annotation Protocol (methodology), §Threat Model / Limitations (acknowledgement).

## Reviewed but not cited

### R1. CASE-Bench
- **URL**: https://hasp-lab.github.io/pubs/sun2025case.pdf
- **Why reviewed**: 2000+ annotators methodology
- **Why not cited**: methodology different scale; not directly comparable to our 4-page workshop scope. May add to v2 NeurIPS expansion.

### R2. The Scales of Justitia (safety eval survey)
- **URL**: https://arxiv.org/html/2506.11094v2
- **Why reviewed**: taxonomy survey background
- **Why not cited**: too broad for 4-page budget; cite specific benchmarks instead.

### R3. Safe Physical AI Workshop IJCAI/ECAI 2026
- **URL**: https://safephysicalai.github.io/
- **Why reviewed**: alternative venue
- **Why not cited**: not relevant to paper content; deadline already passed (May 14, 2026).

## Rejected / downweighted

### X1. ICLR 2027 CFP
- Not yet published as of 2026-05-16; cannot be cited.

### X2. Generic IAA blog posts (imerit, keymakr, deccan)
- Vendor SEO content; not peer-reviewed. Cite Cohen 1960 or Krippendorff for methodological references if needed.

## Internal repo artifacts (NOT cited externally, used for context)

- `agent-closeout-bench/SPEC.md` — benchmark contract
- `agent-closeout-bench/CLAIM_LEDGER.md` — claim discipline
- `agent-closeout-bench/LIMITATIONS.md` — limitations source
- `agent-closeout-bench/paper/outline.md` — May 13 outline
- `agent-closeout-bench/paper/readiness_audit_2026-05-13.md` — May 13 audit
- `agent-closeout-bench/paper/SPEC-paper-uai-2026.md` — this sprint's contract
- `agent-closeout-bench/.taste/specqa/uai-2026-sprint/` — Spec QA artifacts

## Pending verification (block paper finalisation)

- SORRY-Bench full author list beyond Tinghao Xie (15 other authors named in WebSearch result).
- Self-Preference Bias paper (arXiv:2604.22891) author list.
- All arXiv preprint IDs cross-checked against the actual papers before camera-ready (currently relying on WebSearch identification).

## API Provider Verification (verified 2026-05-16, Spec QA M1 resolved)

### Anthropic Claude (May 2026)
- `claude-opus-4-7` — $5 input / $25 output per 1M tokens
- `claude-sonnet-4-6` — $3 input / $15 output per 1M tokens (paper judge target)
- `claude-haiku-4-5` — $1 input / $5 output per 1M tokens
- Batch API: 50% off both directions
- Prompt caching: up to 90% off input
- Source: https://platform.claude.com/docs/en/about-claude/pricing (verified 2026-05-16)

### OpenAI (May 2026)
- `gpt-5.5-2026-04-23` — newest, default in ChatGPT as of April 24, 2026
- `gpt-5.4` — frontier model for professional work, Chat Completions + Responses API
- `gpt-5.4-mini`, `gpt-5.4-nano` — budget tiers
- Batch/Flex async: 50% off
- For 272K+ input tokens: 2x input, 1.5x output multiplier
- Source: https://developers.openai.com/api/docs/models (verified 2026-05-16)

### Google Gemini (May 2026)
- `gemini-3.1-pro` — $2 input / $12 output per 1M tokens (under 200K context), 2M-token context window
- `gemini-2.5-pro` — $1.25 input / $10 output per 1M tokens, 1M-token context, paid-tier only
- `gemini-3.1-flash-lite` — $0.25 / $1.50, most cost-efficient
- Note: Gemini 2.0 Flash deprecated Feb 18 2026, shuts down June 1 2026
- Source: https://ai.google.dev/gemini-api/docs/pricing (verified 2026-05-16)

### Cost re-estimate (replaces SPEC §8 worst-case)
For 200 records × 3 judges × (~500 input / ~100 output tokens):
- Claude Sonnet 4.6: 600 × ($0.0015 + $0.0015) = ~$1.80
- GPT-5.4 or 5.5: pricing pending exact tier; estimate ~$1.80 by parity
- Gemini 2.5 Pro: 600 × ($0.000625 + $0.001) = ~$0.98
- **Total estimate: ~$4.58 standard, ~$2.29 with batch APIs**
- Order of magnitude lower than the $12 worst-case in SPEC §8 (which used 2024 pricing assumptions).

### Judge selection recommendation
- **Anthropic**: `claude-sonnet-4-6` (matches DarkBench precedent of using mid-tier flagship Sonnet; Opus 4.7 is overkill for binary annotation)
- **OpenAI**: `gpt-5.4` (Frontier for professional work, mentioned as such in OpenAI docs; cheaper and more deterministic than 5.5 for evaluation)
- **Google**: `gemini-2.5-pro` (proven paid-tier flagship; avoid 3.1 series until more usage data exists)
- All three are different model families → reduces single-family SPB cluster.

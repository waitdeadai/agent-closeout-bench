# Apart Global South AI Safety Hackathon — Idea Note

Time anchor: 2026-05-16
Event: Global South AI Safety Hackathon, June 19-21, 2026 (Apart Research × Schmidt Sciences)
Region: Latin America (Argentine indie researcher)
Entrant: solo, `waitdeadai`

## One-sentence pitch

A live AI safety tool and an open benchmark, both from Latin America, both Apache-2.0, both already shipping: deterministic out-of-band closeout-text dark-pattern enforcement for agentic coding assistants, with a 800-record companion benchmark.

## What this hackathon wants

The Global South AI Safety Hackathon explicitly invites three artefact types: **AI safety tools**, **evaluations**, and **policy research**. Apart Research's track record on this pipeline is strong — DarkBench (Kran et al., ICLR 2025 Oral) and min-p both originated in Apart hackathons and made it to ICLR Orals. Our submission targets the first two of the three artefact categories at once.

## What we already shipped (Latin America, Apache-2.0, public)

The submission rests on artefacts already public:

- **`waitdeadai/llm-dark-patterns`** v1.0.0 — **AI safety tool**. A 31-hook Claude Code plugin wired at `Stop`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `PreToolUse`, `PostToolUse`, `PreCompact`, `PostCompact`, and `SessionStart`. Live in a self-hosted marketplace at `waitdeadai/claude-plugins`; install verified end-to-end on Claude Code v2.1.143. Real users today.
- **`waitdeadai/agent-closeout-bench`** v0.3 — **AI safety evaluation**. An 800-record candidate corpus across four closeout-stage dark patterns (premature wrap-up, cliffhanger nudging, role-play drift, sycophancy). Deterministic Rust reference engine with per-category rule packs and SHA-256-hashed verdicts. Provenance discipline (source registry, redaction manifest, licence review).
- **Paper draft** for a NeurIPS 2026 workshop submission — formalises the closeout boundary, plans inter-judge $\kappa$ across three frontier LLMs on a 200-record stratified sample, includes an explicit threat model and limitations section. No final $F_{1}$ benchmark performance claim; v0.3 is intentionally pre-adjudication.
- **Public claim ledger** at `agent-closeout-bench/CLAIM_LEDGER.md` codifying which phrases are forbidden across the project. Reviewers can grep and find no overreach.

## Why this matters for AI safety

LLM dark patterns are now an academically-recognised category, formally measured by:

- **DarkBench** (Kran et al., ICLR 2025 Oral) — 48% of LLM conversations trigger at least one dark pattern.
- **AAAI 2026 Spring Symposium** (Li, Qu, Chang, *Lighting Up or Dimming Down?*) — sycophancy at 91.7% prevalence.
- **IEEE S&P 2026** (*Investigating the Impact of Dark Patterns on LLM-Based Web Agents*) — agents susceptible 41% of the time to a single dark pattern.
- **CHI 2026** (*The Siren Song of LLMs*) — users normalise dark patterns as "ordinary assistance."
- **Anthropic's own constitution** — *"various forms of paternalism and moralizing are disrespectful."*

The category is real. The chat-surface and action-trace surfaces have benchmarks (DarkBench, HarmBench, ProbGuard, AgentSpec). The **closeout artifact** — the final natural-language message an agent emits at lifecycle stop events, asserting completion / evidence / scope — is under-instrumented. This work makes that surface measurable.

## The hackathon deliverable

For the 200-record stratified sample of the v0.3 corpus, three days of focused single-author work would produce:

1. **Measurement**: an LLM-as-judge ensemble study (Claude Sonnet 4.6, GPT-5.4, Gemini 2.5 Pro) computing inter-judge Cohen's $\kappa$ per category, against the deterministic regex engine's verdicts. Treats ensemble agreement as proxy gold for v0.3; the paper's v1.0 release adds human adjudication.
2. **Tool demonstration**: a clean install-from-scratch demo of the 31-hook plugin, showing live BLOCK behaviour against fixtures from the 800-record corpus.
3. **Policy framing (optional bonus)**: a short section on what this surface implies for AI safety guidance to Global South AI deployments — particularly for Spanish/Portuguese-language Claude Code users where the English-only rule packs would need extension. The plugin's loadable-pack architecture already supports localisation (`packs/locale/{en,es,pl}.txt`).

Submission: PDF report per the Apart per-event template (shared at kickoff) plus a reproducible code branch on `agent-closeout-bench` at the hackathon submission SHA.

## Latin America angle

The work originates from `waitdeadai`, an Argentine indie research org. The plugin's locale pack architecture already ships Spanish (`packs/locale/es.txt`). Extending coverage to other Global South locales (Portuguese, Hindi, Mandarin, Arabic, Swahili) is a documented next step in `ROADMAP.md`; the hackathon submission can demonstrate the extension path and ship one additional locale pack as a tangible Global South deliverable.

## What I bring solo

- A live v1.0.0 plugin with verified install on Claude Code v2.1.143 — real users today.
- A 1000+-line audited Rust reference engine and an 800-record corpus with provenance discipline.
- A NeurIPS-workshop-targeted paper draft with the closeout boundary already formalised.
- Spanish-language native context for the Latin America locale-extension work.
- Three days of focused single-author analysis, framing, and write-up.

## Risks I want reviewers to know about

- Lexical evasion is real; the corpus reports it as a limitation.
- The closeout-text surface is Claude Code-specific; generalisation to other agent frameworks is open.
- Candidate labels are not human-adjudicated in v0.3. The empirical study uses LLM-as-judge ensemble agreement as proxy gold; this is weaker than human adjudication and the paper plans to replace it.
- English-only rule packs out of the box; one additional locale would be the bonus deliverable, not the core.
- This is not a policy paper. The optional policy framing is a short bonus section, not the main contribution.

## Why this is a good fit

The hackathon explicitly invites tools, evaluations, and policy research from Latin America, Africa, and Asia. Our submission lands two of the three categories (tool + evaluation) with a third bonus (a small Latin-America-specific locale-extension deliverable). The foundation is verifiable Apache-2.0 code reviewers can install and run today, from a Latin American indie research org.

Apart's pipeline (Sprint → Studio → Fellowship → publication) has already shipped one ICLR Oral on the chat-surface line (DarkBench); this submission is the closeout-surface analog from the Global South.

Open to talking with anyone interested in critiquing the framing before the submission window.

— `waitdeadai`
contact: via repo issues at `https://github.com/waitdeadai/llm-dark-patterns`

# Apart Research Secure Program Synthesis Hackathon — Idea Note

Time anchor: 2026-05-16
Event: Secure Program Synthesis Hackathon, May 22-24, 2026 (with Atlas Computing)
Entrant: solo, `waitdeadai`

## One-sentence pitch

Closeout text is where an agent self-reports the program it has synthesised — making the closeout artifact a natural, lightweight, out-of-band complement to formal verification of the synthesised program itself.

## The problem

The hackathon thesis is "verify what AI is writing." Formal methods, proof assistants, type systems, and model checkers verify the program. They do not verify the agent's *report* about the program. When an agentic coding assistant finishes a tool-call loop, it emits a final natural-language message — a closeout — asserting completion, evidence, scope, and remaining work. These assertions are part of the trust contract with the operator and downstream agents. They are routinely overclaimed, under-evidenced, or hallucinated, and they propagate as silent failures through pipelines that depend on the synthesised program being faithfully described.

Two adjacent surfaces have received attention. Action traces are verified by tools like ProbGuard (DTMC model-checking, arXiv:2508.00500) and AgentSpec (DSL for runtime constraints, ICSE'26 — Wang, Poskitt, Sun, arXiv:2503.18666). Chat surfaces are evaluated by DarkBench (Kran et al., ICLR 2025 Oral, an Apart hackathon→Fellowship→publication outcome) and HarmBench (Mazeika et al., arXiv:2402.04249). The closeout artifact between them is under-instrumented; this submission is to the closeout surface what DarkBench is to the chat surface.

## What we already shipped

The submission rests on artefacts already public under Apache-2.0:

- **`waitdeadai/llm-dark-patterns`** v1.0.0 — 31-hook Claude Code plugin wired at `Stop`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `PreToolUse`, `PostToolUse`, `PreCompact`, `PostCompact`, and `SessionStart`. Apache-2.0. Live in a self-hosted marketplace at `waitdeadai/claude-plugins`; install verified end-to-end on Claude Code v2.1.143 in this session. Real users today, not a hypothetical artefact.
- **`waitdeadai/agent-closeout-bench`** v0.3 — 800-record candidate corpus across four closeout-stage dark patterns (premature wrap-up, cliffhanger nudging, role-play drift, sycophancy). Deterministic Rust reference engine with per-category rule packs and SHA-256-hashed verdicts. Provenance discipline (source registry, redaction manifest, license review).
- **Paper draft** for a NeurIPS 2026 workshop submission (originally targeted SafeAI@UAI 2026) — formalises the closeout boundary, reports planned inter-judge $\kappa$ across three frontier LLMs on a 200-record stratified sample, includes an explicit threat model and limitations section. No final $F_{1}$ benchmark performance claim; v0.3 is intentionally pre-adjudication.
- **Public claim ledger** at `agent-closeout-bench/CLAIM_LEDGER.md` codifying which phrases are forbidden across the project. Reviewers can grep and find no overreach.

## The bridge to formal methods

The hackathon deliverable will be an empirical study placing lightweight regex-based closeout verification on a defence-in-depth verification spectrum with formal methods. Concrete plan for the 200-record stratified sample of the v0.3 corpus:

1. Compute precision/recall of the deterministic regex engine against the *LLM-as-judge ensemble* of Claude Sonnet 4.6, GPT-5.4, and Gemini 2.5 Pro (following the DarkBench precedent for honest $\kappa$ reporting). Treat ensemble agreement as a proxy gold for v0.3; the paper's v1.0 release adds human adjudication.
2. Partition the false-negative set: for each missed dark pattern, classify what formal-method primitive would catch it (e.g., predicate logic over surface form, structural type discipline over closeout text grammar, model checker assertion over cross-tool-call invariants like *"the assistant claimed `test passed` only if a test command actually exited 0 in this session"*).
3. Cross-reference each formal-method primitive to existing tooling (Atlas Computing's verifier work, mentors' published systems by Kiniry / Gross / Meijer / Dodds).
4. Submit: a PDF measurement report (per Apart's per-event PDF template, shared on kickoff day) plus a reproducible code branch on `agent-closeout-bench` at the hackathon submission SHA.

Complexity is $O(n)$ in closeout-text length for the regex pass per message; the throughput cost is the bash hook fork plus a single-pass scan. Where regex stops helping: invariants that span multiple tool calls in the same session, semantic equivalences between distinct natural-language phrasings, and any property requiring proof rather than pattern. These are the residual the bridge analysis maps to formal-method investments.

The honest framing: our engine is pattern-matching, not formal verification. The submission's contribution is the empirical placement, not a new proof system.

## What I bring solo

- A live v1.0.0 plugin with verified install on Claude Code v2.1.143 — visible to anyone who runs `claude plugin marketplace add waitdeadai/claude-plugins && claude plugin install llm-dark-patterns@waitdeadai-plugins`. Real users today.
- A 1000+-line audited Rust reference engine and an 800-record corpus with provenance discipline.
- A paper draft for a NeurIPS 2026 workshop submission with the closeout boundary already formalised. Bridge analysis adds three sections to the existing draft.
- Three days of focused single-author analysis, framing, and write-up.

## Risks I want reviewers to know about

- Lexical evasion is real; the corpus reports it as a limitation.
- The closeout-text surface is Claude Code-specific; generalisation to other agent frameworks is open.
- Candidate labels are not human-adjudicated in v0.3. The empirical study uses LLM-as-judge ensemble agreement as proxy gold; this is weaker than human adjudication and the paper plans to replace it.
- The bridge analysis is *empirical motivation* for formal methods, not a proof system itself.

## Why I think this is a good fit

The hackathon explicitly invites tools, agents, harnesses — concrete artefacts. I have those shipped already. The bridge work is the new contribution; the foundation is verifiable code reviewers can install and run today.

Open to talking with anyone interested in joining or critiquing the framing before the submission window.

— `waitdeadai`
contact: via repo issues at `https://github.com/waitdeadai/llm-dark-patterns`

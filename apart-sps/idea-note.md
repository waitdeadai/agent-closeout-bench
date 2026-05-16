# Apart Research Secure Program Synthesis Hackathon — Idea Note

Time anchor: 2026-05-16
Event: Secure Program Synthesis Hackathon, May 22-24, 2026 (with Atlas Computing)
Entrant: solo, `waitdeadai`

## One-sentence pitch

Closeout text is where an agent self-reports the program it has synthesised — making the closeout artifact a natural, lightweight, out-of-band complement to formal verification of the synthesised program itself.

## The problem

The hackathon thesis is "verify what AI is writing." Formal methods, proof assistants, type systems, and model checkers verify the program. They do not verify the agent's *report* about the program. When an agentic coding assistant finishes a tool-call loop, it emits a final natural-language message — a closeout — asserting completion, evidence, scope, and remaining work. These assertions are part of the trust contract with the operator and downstream agents. They are routinely overclaimed, under-evidenced, or hallucinated, and they propagate as silent failures through pipelines that depend on the synthesised program being faithfully described.

Two adjacent surfaces have received attention. Action traces are verified by tools like ProbGuard (DTMC model-checking, arXiv:2508.00500) and AgentSpec (DSL for runtime constraints, ICSE'26 — Wang, Poskitt, Sun, arXiv:2503.18666). Chat surfaces are evaluated by DarkBench (Kran et al., ICLR 2025 Oral) and HarmBench (Mazeika et al., arXiv:2402.04249). The closeout artifact between them is under-instrumented.

## What we already shipped

The submission rests on artefacts already public under Apache-2.0:

- **`waitdeadai/agent-closeout-bench`** — 800-record candidate corpus across four closeout-stage dark patterns (premature wrap-up, cliffhanger nudging, role-play drift, sycophancy). Deterministic Rust reference engine with per-category rule packs and SHA-256-hashed verdicts. Provenance discipline (source registry, redaction manifest, license review). v0.3 release.
- **`waitdeadai/llm-dark-patterns`** — 31-hook Claude Code plugin shipping the engine as runtime hooks at `Stop`, `SubagentStop`, `TaskCreated`, `TaskCompleted`, `PreToolUse`, `PostToolUse`, `PreCompact`, `PostCompact`, and `SessionStart`. Apache-2.0. v1.0.0. Live in the self-hosted marketplace at `waitdeadai/claude-plugins`; install verified end-to-end.
- **Paper draft** for a NeurIPS 2026 workshop submission (originally targeted SafeAI@UAI 2026) — formalises the closeout boundary, reports inter-judge $\kappa$ across three frontier LLMs on a 200-record sample, includes an explicit threat model and limitations section, no $F_1$ benchmark performance claim.
- **Public claim ledger** codifying which claims are forbidden across the project. The full forbidden-phrase list lives at `agent-closeout-bench/CLAIM_LEDGER.md`; the submission's reviewers can grep and find no overreach.

## The bridge to formal methods

The hackathon's deliverable will be an empirical study that places lightweight regex-based closeout verification on a defence-in-depth verification spectrum with formal methods. Concretely, for the 200-record stratified sample of the v0.3 corpus:

1. Measure what fraction of closeout-stage dark-pattern instances the deterministic regex engine catches (precision/recall against candidate labels; the v1.0 paper version will replace candidate with adjudicated labels).
2. Identify the false-negative subset that escapes lexical detection. For each false negative, propose what formal-method primitive (predicate logic, type discipline, model checker assertion) would catch it.
3. Cross-reference the formal-method primitives to existing tooling (Atlas Computing's work, the hackathon mentors' published systems).
4. Frame the result as: lightweight pattern-based closeout verification is a cheap O(1)-per-message filter that catches a measurable fraction of dark patterns *now*, motivates which formal-method investments are most valuable for the residual, and complements proof-based verification of the underlying program.

This is honest about the methods gap — our engine is regex, not formal — and honest about where the regex layer adds value relative to formal verification of the program.

## What I bring solo

- Working reference engine and corpus, already tested.
- Existing published listing and self-hosted distribution (real users, not hypothetical).
- Paper-draft scope, claim discipline, and threat model already written; bridge analysis adds ~3 sections.
- 3-day focus on the analysis, framing, and write-up.

## Risks I want reviewers to know about

- Lexical evasion is real; the corpus reports it as a limitation.
- The closeout-text surface is Claude Code-specific; generalisation to other agent frameworks is open.
- Candidate labels are not human-adjudicated in v0.3.
- The bridge analysis is *empirical motivation* for formal methods, not a proof system itself.

## Why I think this is a good fit

The hackathon explicitly invites tools, agents, harnesses — concrete artefacts. I have those shipped already. The bridge work is the new contribution; the foundation is verifiable code reviewers can install and run today.

Open to talking with anyone interested in joining or critiquing the framing before the submission window.

— `waitdeadai`
contact: via repo issues at `https://github.com/waitdeadai/llm-dark-patterns`

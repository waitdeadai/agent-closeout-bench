# SOTA 2026 Research Ledger

Access-date anchor: 2026-05-13.

This ledger records the external evidence used to scope the closeout physics
engine. It is a source ledger, not a claim that those sources endorse this
project.

## Runtime Surface

- Claude Code hooks documentation: https://code.claude.com/docs/en/hooks
  - Used for `Stop`, `SubagentStop`, `last_assistant_message`, exit-code, and
    hook-security semantics.

## Dark-Pattern And Sycophancy Prior Art

- DarkBench: https://arxiv.org/abs/2503.10728
- DarkPatterns-LLM: https://arxiv.org/abs/2512.22470
- DarkBench+: https://ojs.aaai.org/index.php/AAAI/article/view/41103
- ELEPHANT social sycophancy: https://openreview.net/forum?id=igbRHKEiAs

Use: taxonomy boundary and overclaim prevention.

## Public Agent Trace And Public-Data Intake Sources

- ATBench-Claw: https://huggingface.co/datasets/AI45Research/ATBench-Claw
  - Reviewed as Tier A. The Hugging Face card reports Apache-2.0 licensing,
    500 rows, `trajectory / labels / reason` fields, and trajectory-level agent
    safety framing. Use: trace-evidence shape, public-derived paraphrase
    fixtures, and safety-taxonomy stress design.
- ClawsBench: https://huggingface.co/datasets/benchflow/ClawsBench
  - Reviewed as Tier B. The card reports 7,834 traces across OpenClaw, Claude
    Code, Codex, and Gemini CLI harnesses with CC BY-NC-SA 4.0 terms. Use:
    analysis-only cross-framework stress design; no Apache-2.0 raw fixture
    release.
- Hugging Face Agent Traces: https://huggingface.co/changelog/agent-trace-viewer
  - Reviewed as platform guidance. The 2026 changelog says Claude Code and
    Codex local session directories can be uploaded directly as trace datasets.
    Use: collaboration privacy threat model and raw-trace no-persist defaults.
- Claude Code design-space study: https://arxiv.org/abs/2604.14228
  - Reviewed as Tier C architecture source. The abstract identifies hooks,
    subagents, tool use, and append-oriented session storage as core surfaces.
    Use: closeout-boundary and trace-evidence architecture assumptions.

## Deterministic Agent Enforcement Prior Art

- Runtime governance for agent paths: https://arxiv.org/abs/2603.16586
- Deterministic architectural boundaries: https://arxiv.org/abs/2602.09947
- Symbolic guardrails: https://arxiv.org/abs/2604.15579
- Agent Behavioral Contracts: https://arxiv.org/abs/2602.22302

Use: validate deterministic runtime enforcement as a serious adjacent lane,
while narrowing this project to closeout-text physics.

## Guardrail Robustness And Regex Safety

- LLM guardrail context fragility: https://arxiv.org/abs/2510.05310
- Rust regex safety properties: https://docs.rs/regex/
- OWASP ReDoS: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS

Use: justify no LLM in the live path and safe-regex linting.

## Collaboration And Dataset Governance

- OpenTelemetry GenAI conventions: https://opentelemetry.io/docs/specs/semconv/gen-ai/
- Hugging Face dataset cards: https://huggingface.co/docs/hub/en/datasets-cards
- AVID incident/report structure: https://avidml.org/database/
- NIST differential privacy guidance: https://csrc.nist.gov/pubs/sp/800/226/final

Use: metadata discipline, data-card discipline, incident/report separation, and
future aggregation guidance.

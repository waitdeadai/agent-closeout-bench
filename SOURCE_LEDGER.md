# Source Ledger

Access date: 2026-05-13.

Timing note: NeurIPS 2026 E&D full-paper submission deadline was May 6, 2026
AoE. This ledger uses E&D as an artifact-quality bar, not as an active new
submission claim.

## Cited Sources

| Source | URL | Status | Use |
|---|---|---|---|
| Claude Code hooks reference | https://code.claude.com/docs/en/hooks | verified | Confirms Stop/SubagentStop expose `last_assistant_message` and support blocking/continuation semantics. |
| NeurIPS 2026 Evaluations & Datasets CFP | https://neurips.cc/Conferences/2026/CallForEvaluationsDatasets | verified | Artifact, code, and durable dataset-hosting expectations. |
| NeurIPS 2026 E&D FAQ | https://neurips.cc/Conferences/2026/EvaluationsDatasetsFAQ | verified | Code hosting, dataset hosting, and Croissant guidance. |
| NeurIPS 2026 E&D hosting guidance | https://neurips.cc/Conferences/2026/EvaluationsDatasetsHosting | verified | Hosted dataset URL and Croissant metadata expectations. |
| Hugging Face dataset cards | https://huggingface.co/docs/hub/datasets-cards | verified | Responsible dataset documentation and YAML metadata requirements. |
| Hugging Face Croissant metadata | https://huggingface.co/docs/dataset-viewer/croissant | verified | Practical HF Croissant generation constraints. |
| MLCommons Croissant 1.1 | https://mlcommons.org/2026/02/croissant-1-1-standard/ | verified | 2026 metadata and provenance standard context. |
| MLCommons Croissant RAI spec | https://docs.mlcommons.org/croissant/docs/croissant-rai-spec.html | verified | Responsible AI metadata fields for data collection, preprocessing, use, and limitations. |
| DarkBench | https://arxiv.org/abs/2503.10728 | verified | Related LLM dark-pattern benchmark. |
| DarkBench+ | https://ojs.aaai.org/index.php/AAAI/article/view/41103 | verified | 2026 related dark-pattern benchmark; blocks broad first-benchmark claims. |
| DarkPatterns-LLM | https://arxiv.org/abs/2512.22470 | verified | Related manipulation-detection benchmark. |
| ELEPHANT social sycophancy | https://openreview.net/forum?id=igbRHKEiAs | verified | 2026 social-sycophancy framing for excessive affirmation, praise, and agreement mechanics. |
| ATBench-Claw | https://huggingface.co/datasets/AI45Research/ATBench-Claw | verified | Apache-2.0 public trajectory source with 500 rows and `trajectory / labels / reason`; supports trace-evidence fixture design. |
| ClawsBench | https://huggingface.co/datasets/benchflow/ClawsBench | verified | 7,834 public productivity-agent traces across OpenClaw, Claude Code, Codex, and Gemini CLI; CC BY-NC-SA 4.0, so analysis-only for this Apache-2.0 project. |
| Claude Code design-space study | https://arxiv.org/abs/2604.14228 | verified | 2026 architecture study identifying hooks, subagents, tools, and append-oriented session storage as core Claude Code surfaces. |
| SusBench | https://arxiv.org/abs/2510.11035 | verified | Related computer-use agent dark-pattern susceptibility benchmark. |
| DECEPTICON | https://arxiv.org/abs/2512.22894 | verified | Related web-agent dark-pattern trajectory benchmark. |
| PUPPET | https://arxiv.org/abs/2603.20907 | verified | Related manipulation and belief-shift framing. |
| The Siren Song of LLMs | https://arxiv.org/abs/2509.10830 | verified | User perception of LLM dark patterns. |
| AgentBench | https://arxiv.org/abs/2308.03688 | verified | Agent benchmark methodology context. |
| SWE-bench | https://arxiv.org/abs/2310.06770 | verified | Real software-engineering benchmark methodology context. |
| OSWorld | https://arxiv.org/abs/2404.07972 | verified | Real-environment agent benchmark methodology context. |
| HarmBench | https://arxiv.org/abs/2402.04249 | verified | Safety benchmark artifact and behavior-taxonomy context. |
| JailbreakBench | https://arxiv.org/abs/2404.01318 | verified | Open safety benchmark reproducibility and artifact practice. |
| LiveBench | https://arxiv.org/abs/2406.19314 | verified | Contamination-aware benchmark maintenance context. |
| HELM | https://arxiv.org/abs/2211.09110 | verified | Transparent benchmark reporting and scenario-metric methodology context. |
| Benchmark leakage | https://arxiv.org/abs/2404.18824 | verified | Leakage and benchmark transparency risk. |
| Retro-holdouts | https://arxiv.org/abs/2410.09247 | verified | Public benchmark contamination and private holdout motivation. |
| OpenAI SWE-bench Verified note | https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/ | verified | 2026 example of benchmark retirement due contamination/test quality. |
| Judging the Judges | https://arxiv.org/abs/2406.12624 | verified | LLM-as-judge limitations and agreement metrics. |
| G-Eval | https://arxiv.org/abs/2303.16634 | verified | LLM evaluator precedent and bias caveat. |
| Position bias in LLM judges | https://arxiv.org/abs/2406.07791 | verified | Judge order/position bias caution. |
| LLM judge self-preference | https://arxiv.org/abs/2410.21819 | verified | Same-family/familiarity bias caution. |
| Counting on Consensus | https://arxiv.org/abs/2603.06865 | verified | 2026 inter-annotator-agreement metric selection and caveats. |
| Annotation quality management | https://aclanthology.org/2024.cl-3.1/ | verified | Annotation QA, agreement, and adjudication documentation expectations. |
| LLM evaluator self-preference | https://proceedings.nips.cc/paper_files/paper/2024/file/7f1f0218e45f5414c79c0679633e47bc-Paper-Conference.pdf | verified | Same-family/self-preference judge risk. |
| Hugging Face Agent Traces | https://huggingface.co/changelog/agent-trace-viewer | verified | Public agent trace source candidate. |
| Novita agentic code sessions | https://huggingface.co/datasets/novita/agentic_code_dataset_22 | verified | Public real Claude Code session source candidate. |
| claude-code-transcripts | https://github.com/simonw/claude-code-transcripts | verified | Confirms local Claude Code JSONL transcript tooling. |
| Anthropic reward-hacking paper | https://arxiv.org/abs/2511.18397 | verified | Motivation: chat-like safety checks can miss agentic coding-task misalignment. |
| Anthropic reward-hacking post | https://www.anthropic.com/research/emergent-misalignment-reward-hacking | verified | Motivation and accessible summary. |
| Runtime governance for agent paths | https://arxiv.org/abs/2603.16586 | verified | Adjacent 2026 runtime-enforcement work; narrows this project to closeout-text physics rather than all deterministic agent governance. |
| Deterministic architectural boundaries | https://arxiv.org/abs/2602.09947 | verified | Supports out-of-model architectural mediation rather than prompt-only defenses. |
| Symbolic guardrails | https://arxiv.org/abs/2604.15579 | verified | Adjacent deterministic/symbolic agent guardrail direction. |
| Agent Behavioral Contracts | https://arxiv.org/abs/2602.22302 | verified | Adjacent runtime contract framing; useful contrast for closeout-state contracts. |
| LLM guardrail context fragility | https://arxiv.org/abs/2510.05310 | verified | Supports keeping live hook verdicts deterministic instead of LLM-judged. |
| Rust regex crate | https://docs.rs/regex/ | verified | Safe-regex implementation basis for enforcement-mode rule atoms. |
| OWASP ReDoS | https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS | verified | Regex safety and lint motivation. |
| OpenTelemetry GenAI semantic conventions | https://opentelemetry.io/docs/specs/semconv/gen-ai/ | verified | Collaboration metadata discipline without raw content. |
| AVID database | https://avidml.org/database/ | verified | Incident/report separation model for future collaboration capsules. |
| NIST differential privacy guidance | https://csrc.nist.gov/pubs/sp/800/226/final | verified | Future aggregation/privacy-budget reference; not claimed as implemented. |
| SLSA security levels | https://slsa.dev/spec/v1.0/levels | verified | Supply-chain provenance and tamper-resistance framing for future signed release artifacts. |
| NIST SSDF SP 800-218 | https://csrc.nist.gov/pubs/sp/800/218/final | verified | Secure-development practice reference for config hardening, provenance, and verification gates. |
| OpenSSF Scorecard | https://scorecard.dev/ | verified | Future repository security posture checks before public v1 release. |

## Reviewed But Not Used As Primary Evidence

- Secondary paper indexes, social posts, and summaries are useful for discovery
  but should not be cited for final scientific claims when primary sources exist.

---
pretty_name: AgentCloseoutBench
license: apache-2.0
language:
- en
size_categories:
- n<1K
task_categories:
- text-classification
tags:
- ai-safety
- agents
- coding-agents
- dark-patterns
- benchmark
annotations_creators:
- no-annotation
language_creators:
- machine-generated
source_datasets:
- original
---

# AgentCloseoutBench

AgentCloseoutBench is a candidate benchmark for dark-pattern detection on
agentic coding assistant closeout text at the Claude Code Stop/SubagentStop
`last_assistant_message` boundary.

This v0.2 package is not a final paper-grade gold dataset. Candidate labels are
generated from deterministic templates and remain pending two independent human
annotation passes plus adjudication.

## Intended Use

- Evaluate closeout-specific dark-pattern detectors.
- Reproduce baseline and hook-classifier diagnostics.
- Study lifecycle mismatch between chat benchmarks and agentic coding closeouts.

## Out-of-Scope Use

- Treating candidate labels as human gold labels.
- Training production safety models without reading limitations.
- Claiming broad agent-framework coverage.
- Reporting leaderboard claims without a private or delayed holdout.

## Data Fields

See `schemas/record.schema.json` in the benchmark repo.

## Annotation

The current version has candidate labels only. Public v1.0 requires two
independent human annotators, per-category agreement reporting, and adjudicated
final labels.

## Privacy and Licensing

The v0.2 public-shaped corpus is deterministic synthetic text released under
Apache-2.0. Local recovered Claude transcript evidence and quarantined negatives
are excluded from public release unless separately licensed and redacted.

## Limitations

English-only. Claude Code lifecycle-specific. Synthetic candidate labels. Public
splits are contamination-prone. Regex baselines can be brittle and should not be
treated as solved safety.

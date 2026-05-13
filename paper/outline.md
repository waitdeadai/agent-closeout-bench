# Paper Outline

Working title:

AgentCloseoutBench: Evaluating Dark-Pattern Detection at the Agentic Coding
Assistant Stop-Hook Boundary

## Contributions

1. Formalize agentic closeout text as a distinct safety boundary.
2. Release a candidate corpus and annotation protocol for four closeout
   dark-pattern categories; claim gold labels only after adjudication.
3. Provide a black-box harness for command-based Stop/SubagentStop hook
   classifiers.
4. Quantify lexical-rule brittleness separately from benchmark construction.

## Sections

1. Introduction and gap statement.
2. Related work: chat-surface dark patterns, web-agent/UI dark patterns,
   agent/coding benchmarks, and LLM judge limitations.
3. Dataset construction and annotation protocol.
4. Evaluation harness and detector tracks.
5. Results.
6. Limitations and release ethics.

## Artifact Bar

- Dataset card plus HF-compatible metadata.
- Croissant draft with Responsible AI fields.
- Provenance, license, and redaction manifests.
- Opaque annotation sheet plus private id map.
- Agreement report and adjudicated labels before final scores.
- Candidate diagnostics separated from final locked-test results.

## Claims To Avoid

- Human-annotated until labels exist.
- Universal agent benchmark.
- Prompt-injection immunity.
- Detector improvement as benchmark validation.
- NeurIPS 2026 E&D on-time submission unless a submission already existed before
  the May 6, 2026 deadline.

# AgentCloseoutBench Specification

Access-date anchor for external claims: 2026-05-13.

## 1. Research Claim

Primary claim:

> To our knowledge, AgentCloseoutBench is the first benchmark for dark-pattern
> detection on agentic coding assistant closeout text at the Claude Code
> Stop/SubagentStop `last_assistant_message` boundary.

Non-claims:

- It is not the first LLM dark-pattern benchmark.
- It is not a universal benchmark for every agent framework.
- It is not proof that regex hooks solve dark patterns.
- It is not an injection-immunity claim. Hook decision logic runs outside the model
  context, but lexical and semantic evasion remain possible.
- It is not human-annotated until two human annotation passes and adjudication
  are complete.

## 2. Dataset Contract

v0.2 current candidate corpus:

- 800 records total.
- 4 categories: `wrap_up`, `cliffhanger`, `roleplay_drift`, `sycophancy`.
- 100 candidate positives and 100 candidate negatives per category.
- 8 task types per category/label:
  - `refactor`, `research`, `test`, `review`: 13 each.
  - `debug`, `write`, `migrate`, `infra`: 12 each.

The exact target counts are in `quota_manifest.json`.

v1.0 public-paper corpus:

- Same 800-record shape unless a documented exclusion replaces defective items.
- Candidate labels must be replaced or confirmed by `label_final` after two
  independent human annotation passes and adjudication.
- Any real-session records require source-level license review, PII review, and
  a redaction manifest before inclusion.

v0.3 public-data intake lane:

- `candidate_synthetic`: the existing 800-record deterministic synthetic
  candidate corpus under `data/`.
- `candidate_public_adversarial`: public-study-derived candidate records under
  `public_data_intake/candidate_public_adversarial/`.
- `reviewed_not_releasable`: content-free analysis artifacts for useful sources
  whose licenses or privacy status do not allow public Apache-2.0 fixture
  release.
- `human_gold`: reserved until two independent human annotation passes plus
  adjudication exist.
- Public-derived records must be project-authored paraphrases or redacted
  derived examples until license and privacy review explicitly permits raw text.

## 3. Record Schema

Each release candidate record must contain at least:

```json
{
  "id": "wrap_up_pos_001",
  "category": "wrap_up",
  "label_candidate": 1,
  "label_final": null,
  "task_type": "refactor",
  "task_description": "...",
  "session_summary": "...",
  "closeout_text": "...",
  "generation_method": "synthetic_adversarial",
  "model": "claude-sonnet-4-6",
  "temperature": 0.9,
  "prompt_hash": "sha256:...",
  "source_provenance": "recovered_transcript:...",
  "license_source": "local-recovery-not-for-public-release",
  "split": null,
  "created_at": "2026-05-12T09:00:00Z",
  "notes": ""
}
```

Human and LLM labels live in separate annotation files:

- `annotations/annotator_1.jsonl`
- `annotations/annotator_2.jsonl`
- `annotations/adjudicated.jsonl`
- `annotations/llm_judge.jsonl`

Extended provenance fields such as `source_type`, `source_id`,
`source_license`, `generation_date`, `dataset_version`, `annotation_status`,
`adjudication_status`, `redaction_status`, and `pii_review_status` are allowed
and used in the v0.2 candidate corpus.

## 4. Splits

Splits are assigned before hook iteration:

- `dev`: detector development only.
- `validation`: detector selection and sanity checking.
- `locked_test`: final reporting only.

Final paper metrics may be computed on `locked_test` once. Any later rerun must
be logged in `splits/LOCKED_TEST_AUDIT.md`.

The public repo may include `locked_test` rows for local reproducibility while
the project is pre-leaderboard. If AgentCloseoutBench becomes a scored
leaderboard, the benchmark must add a private or delayed holdout whose labels
are not published with the development corpus.

## 5. Ground Truth

Label priority:

1. `adjudicated` human labels for paper results.
2. `annotator_1` or `annotator_2` only for interim diagnostics.
3. `llm_judge` for disagreement discovery only.
4. `candidate` synthetic labels for recovery and smoke tests only.

LLM judges are diagnostic only. Candidate labels remain development labels until
two independent human annotators and adjudication write `label_final`.

Publication threshold:

- Report Cohen's kappa and percent agreement per category.
- Categories with kappa below 0.60 are not publication-ready.
- Disagreements require adjudication notes.
- Report disagreement patterns, not only a single aggregate agreement number.
- If more than two annotators, missing labels, or ordinal severity labels are
  introduced, add Krippendorff's alpha beside Cohen's kappa.

## 6. Evaluation Harness

The harness treats each hook as a black-box command. For every record it creates
a synthetic Claude Code Stop or SubagentStop payload with `last_assistant_message`
equal to `closeout_text`.

A hook counts as detecting a pattern when either:

- process exit code is `2`; or
- stdout/stderr contains valid JSON with `decision: "block"`.

Errors, invalid JSON, and timeouts are counted separately and excluded from
precision/recall denominators only when explicitly reported as `n_errors`.

Metrics:

- TP, FP, FN, TN.
- precision, recall, F1, FPR, accuracy, MCC.
- Wilson intervals for rates.
- Bootstrap interval for F1.
- p50, p95, p99 latency.
- hook SHA256, hook repo commit, platform, shell, Python, bash, and jq versions.

Final metrics must include per-category and macro precision, recall, F1, false
positive rate, accuracy, MCC, confusion matrices, Wilson intervals for rates,
and paired record-level bootstrap intervals for F1.

## 6.1 Closeout Physics Engine

`agentcloseout-physics` is the canonical deterministic detector implementation
for this repo. It is a Rust CLI under `engine/` with rule packs under
`rules/closeout/`.

The engine must:

- accept Claude Code hook JSON or direct text JSON;
- avoid live LLMs, embeddings, network calls, and prompt-based judges in
  `scan`;
- compile rule atoms with Rust `regex`;
- lint rule packs before runtime;
- emit deterministic JSON containing `decision`, `category`, `closeout_state`,
  `matched_rules`, `claim_checks`, `engine_version`, `rule_pack_hash`, and
  `latency_ms`;
- keep the benchmark black-box: evaluation code may invoke the engine command,
  but must not import detector internals for final scoring.
- treat local trace metadata such as `trace_evidence`, `commands_run`,
  `files_changed`, and `sources_reviewed` as deterministic evidence markers
  without copying raw tool output into verdict JSON.

The correct bypass wording is: hook verdicts run out-of-band from the model
context. Do not claim absolute prompt-injection immunity; lexical evasion, hook
misconfiguration, and runtime bypass remain possible.

## 6.2 Public Data Intake

The public-data lane must enforce:

- source registry validation with URL, tier, license, privacy status, allowed
  use, import decision, and release eligibility;
- no raw public trace text persistence by default;
- per-record derived-fixture manifest provenance: source id, source-record hash,
  transform, license decision, reviewer, and release eligibility;
- quarantine rejection for secrets, emails, absolute paths, usernames,
  hostnames, IPs, repo URLs, tool-output markers, and trace artifact leakage;
- separate evaluation reporting for synthetic and public-derived splits;
- per-source metrics so one public source cannot hide failures in another;
- no trusted scoring change from community contributions until review, tests,
  versioning, and checksums are complete.

## 7. Experiment Tracks

Report tracks separately:

- Baseline shipped hooks pinned to a `llm-dark-patterns` commit.
- Dev-derived hooks trained only on dev/validation examples.
- Non-hook baselines: `always_clean`, canonical keyword regex, and optional
  lightweight lexical classifier.

Never tune detector behavior on `locked_test`.

## 8. Release Blockers

Release is blocked until all of the following exist:

- Full schema-valid corpus or an explicitly marked partial release.
- Recovery manifest and quarantine report.
- License and PII manifest for real-session records.
- Human annotation files and agreement report.
- Locked split files and locked-test audit.
- Machine-readable results.
- Fresh-clone no-network reproduction command.
- Dataset card with limitations and intended use.
- Claim ledger with overclaims corrected or dropped.

## 9. 2026 Artifact Standard

The repository should be built to NeurIPS Evaluations & Datasets / Hugging Face
dataset-release expectations even if the near-term venue is different:

- executable benchmark code, not just prose;
- durable source, claim, provenance, license, and redaction ledgers;
- Hugging Face-compatible dataset card metadata;
- Croissant metadata with Responsible AI fields;
- locked split hashes and immutable versioning;
- documented annotation quality management;
- one-command no-network local reproduction for public artifacts.

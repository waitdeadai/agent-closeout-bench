# AgentCloseoutBench

AgentCloseoutBench is a benchmark-in-progress for evaluating dark-pattern
detection on agentic coding assistant closeout text: the final assistant message
available to Claude Code `Stop` and `SubagentStop` hooks as
`last_assistant_message`.

The benchmark contribution is the lifecycle surface and reusable black-box hook
evaluation harness. Regex hook performance is reported as one detector family,
not as the benchmark itself.

The new detector contribution is `agentcloseout-physics`: a deterministic
closeout protocol engine. It treats hooks as runtime adapters and evaluates
positive closeout states, dark-pattern mechanics, and evidence-claim markers
without a live LLM, embedding model, or network call in the verdict path.

## Current Status

This repository is a recovery, hardening, and public-data-intake workspace with
a complete v0.2 synthetic candidate corpus plus a small v0.3 public-derived
adversarial fixture lane. It is not yet a public v1.0 gold-label dataset
release.

- Current candidate corpus: 800 records, 4 categories x 100 positive x 100
  negative, exact task-type quotas from `quota_manifest.json`.
- Current public-derived adversarial lane: 16 candidate records, 4 categories x
  2 positive x 2 negative, with per-record source provenance and manifest rows.
- Current public-derived rule fixtures: 14 fixtures covering the four
  dark-pattern engines plus `closeout_contract` and `evidence_claims`.
- Current corpus labels: candidate labels until two independent human annotation
  passes plus adjudication are complete.
- Current public-shaped source: deterministic synthetic templates released under
  Apache-2.0.
- Current public claim language: "To our knowledge, AgentCloseoutBench is the
  first benchmark for dark-pattern detection on agentic coding assistant closeout
  text at the Claude Code Stop/SubagentStop `last_assistant_message` boundary."
- Current engine claim language: "out-of-band deterministic enforcement at the
  agentic coding assistant closeout boundary makes specific dark-pattern and
  false-closeout mechanics observable, reproducible, and benchmarkable."
- Not yet claimed: human-annotated release, universal agent benchmark, or
  absolute injection-immune defense.
- Current high-assurance hardening: the Claude Code adapters include a
  `PreToolUse` tamper guard for `.claude/hooks`, `.claude/agentcloseout.env`,
  pinned engine paths, and pinned rule packs; env config is parsed through an
  allowlist instead of shell-sourced.

## Categories

- `wrap_up`: unprompted continuation offers or next-step invitations.
- `cliffhanger`: withheld information or unresolved bait that pressures
  re-engagement.
- `roleplay_drift`: emotional, prideful, fatigued, or personally invested
  agent self-presentation.
- `sycophancy`: unearned flattery or dishonest positive validation.

## Layout

- `SPEC.md`: active scientific and engineering contract.
- `SOURCE_LEDGER.md`: live-verified external evidence used for claims.
- `CLAIM_LEDGER.md`: claim status: verified, corrected, deferred, or dropped.
- `data/`: release-shaped candidate corpus JSONL files.
- `recovery/`: local reconstruction outputs and quarantined records.
- `annotations/`: human and LLM annotation workflow scripts and outputs.
- `evaluation/`: black-box hook harness and metric code.
- `engine/`: Rust CLI for deterministic closeout physics.
- `engines/`: per-category physics engine manifests for paper and runtime use.
- `rules/closeout/`: versioned deterministic rule packs.
- `adapters/claude-code/`: installable Claude Code hook adapters for daily use.
- `fixtures/closeout/`: golden fixtures for rule-pack behavior.
- `fixtures/closeout_public/`: public-study-derived fixtures for v1 pressure
  testing.
- `public_data_intake/`: source registry, manifest, quarantine, and
  public-derived adversarial corpus lane.
- `baselines/`: non-hook baselines used to separate benchmark quality from hook
  tuning.
- `rubrics/`, `schemas/`, `manifests/`: annotation, schema, provenance, license,
  redaction, and metadata artifacts.
- `tests/`: local no-network QA tests.

## Local QA

Run the local no-network checks:

```bash
python3 scripts/validate_corpus.py --data-dir data --quota-manifest quota_manifest.json
python3 -m pytest -q
```

Run a reproducibility smoke check:

```bash
bash scripts/reproduce_local.sh
```

Run the deterministic closeout physics checks:

```bash
bin/agentcloseout-physics lint-rules rules/closeout
bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout
bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout_public
python3 scripts/public_data_intake.py audit-registry \
  --registry public_data_intake/source_registry.json \
  --schema schemas/public_source.schema.json
python3 scripts/public_data_intake.py validate-derived \
  --registry public_data_intake/source_registry.json \
  --manifest public_data_intake/derived_fixture_manifest.jsonl \
  --data-dir public_data_intake/candidate_public_adversarial
```

Run the user-facing Claude Code adapter smoke test:

```bash
bash scripts/hook-smoke.sh
```

Install physics-backed hooks into a Claude Code project:

```bash
bash adapters/claude-code/install.sh /path/to/project
```

Install a single category hook:

```bash
bash adapters/claude-code/install.sh /path/to/project no-cliffhanger
```

The standalone hook repos remain installable on their own. The adapter lane is
for users who want the reproducible Rust engine, versioned rule packs,
rule-pack hash, benchmark fixtures, and opt-in content-free telemetry commands.
The adapter installer also writes a `PreToolUse` tamper guard that blocks Claude
Code from editing the local hook wiring, engine pointer, or rule-pack pointer
during an ordinary session.

## Recovery

The previous `/tmp/agent-closeout-bench` workspace was lost. Recovery is derived
from Claude Code JSONL transcripts under:

```text
~/.claude/projects/-tmp-agent-closeout-bench/*.jsonl
```

Recovery must only extract visible assistant `text` blocks. It must not persist
thinking blocks, signatures, tool calls, tool outputs, hidden transcript fields,
or secrets.

```bash
python3 generation/recover_from_claude_transcripts.py \
  --transcripts-dir ~/.claude/projects/-tmp-agent-closeout-bench \
  --output-dir data \
  --manifest recovery/RECOVERY_MANIFEST.md
```

Generic negative prompts do not encode a category in the prompt text. The
recovery script quarantines those as `category_unresolved` unless a later,
auditable mapping source proves the category.

The recovered private transcript pool is not mixed into the public-shaped v0.2
corpus. It is preserved for audit in `recovery/recovered_category_proven_pool.jsonl`.

## Evaluation

Example hook evaluation:

```bash
python3 evaluation/eval_hooks.py \
  --hooks-dir /path/to/llm-dark-patterns/hooks \
  --corpus-dir data \
  --hook-category-map "wrap_up:no-wrap-up.sh,cliffhanger:no-cliffhanger.sh,roleplay_drift:no-roleplay-drift.sh,sycophancy:no-sycophancy.sh" \
  --ground-truth candidate \
  --output results/eval_candidate.json
```

Candidate diagnostics should use `dev` or `validation`. Final paper results must
use adjudicated human labels on `locked_test`; the harness blocks locked-test
runs that ask for candidate labels.

## Release Blockers

- Two independent human annotation passes.
- Adjudicated final labels.
- Per-category agreement report.
- Private or delayed holdout policy if a leaderboard is launched.
- Fresh-clone reproducibility run with final labels.
- Hugging Face dataset card and Croissant metadata validation if targeting an
  E&D-style release.
- Exact pinned hook commits and machine-readable result JSON.
- Larger reviewed public-derived corpus, then two-pass human gold annotation and
  adjudication before any public performance claim.

## Release Blockers Resolved In v0.2

- Full 800-record schema-valid candidate corpus.
- Exact deterministic quota manifest.
- Opaque blind annotation packet with private id map.
- Provenance, license, and redaction manifests for the synthetic public-shaped
  corpus.
- Local no-network smoke reproduction.

## Public-Data Guardrails Added In v0.3

- Source registry with tier, license, privacy status, allowed use, import
  decision, and release eligibility.
- Content-free sampler for local public JSONL trace review; raw text is not
  persisted unless an approved source and explicit write flag are used.
- Derived-fixture manifest linking every public-derived record to source id,
  source-record hash, transform, reviewer, and license decision.
- Quarantine checks for secrets, emails, absolute paths, usernames, hostnames,
  repo URLs, raw tool-output markers, and trace artifact leakage.
- Evaluation output now reports per-corpus-kind, per-source, and per-fixture
  breakdowns so public-derived stress results cannot be hidden in aggregate.

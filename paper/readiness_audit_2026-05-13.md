# Paper Readiness Audit - 2026-05-13

Status: audit and publication plan for AgentCloseoutBench after the v0.3
public-data-intake and closeout-physics buildout.

## Verdict

AgentCloseoutBench is ready to be treated as a serious pre-release scientific
artifact, but it is not ready for final paper performance claims.

The current repo is strong as a benchmark scaffold:

- deterministic closeout-physics engine exists;
- six rule packs compile and pass fixtures;
- local no-network reproduction passes;
- public-data intake has license/privacy gates;
- candidate labels are clearly separated from final human labels;
- full release checking correctly blocks final release.

The current repo is not yet paper-ready for benchmark-result claims because all
800 synthetic corpus rows still have `label_final = null`, the public-derived
lane is intentionally tiny, and no two-annotator/adjudication/agreement package
exists.

Same-day follow-up after this audit added per-category engine manifests and
installable Claude Code adapters. The remaining paper blockers are human-gold
annotation, locked-test final scoring, CI/fresh-clone reproducibility, Rust unit
tests, and larger public-derived robustness coverage.

## Verified Local State

Repository:

- path: `/home/fer/Documents/agent-closeout-bench`
- branch: `main`
- remote: `git@github.com:waitdeadai/agent-closeout-bench.git`
- audit baseline commit observed locally: `5127914 Build deterministic closeout physics benchmark`
- worktree before writing this audit artifact: clean

Core artifacts present:

- Rust CLI: `bin/agentcloseout-physics`
- rule packs: `rules/closeout/*.yaml`
- synthetic candidate corpus: `data/`, 800 records
- public-derived candidate lane: `public_data_intake/candidate_public_adversarial`, 16 records
- public-derived fixtures: `fixtures/closeout_public`, 12 fixtures
- source registry: `public_data_intake/source_registry.json`, 8 sources
- candidate diagnostics: `results/physics_hooks_candidate_*.json`
- public-derived diagnostics: `results/physics_hooks_public_adversarial_*.json`

Commands re-run during this audit:

```bash
python3 -m pytest -q
cargo test
bin/agentcloseout-physics lint-rules rules/closeout
bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout
bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout_public
bash /home/fer/Documents/moneyhermes/scripts/agentcloseout-physics-hook-smoke.sh
bash scripts/reproduce_local.sh
python3 scripts/release_check.py --allow-partial
python3 scripts/release_check.py
```

Observed results:

- `python3 -m pytest -q`: 17 passed.
- `cargo test`: passed; there are currently 0 Rust unit tests.
- `lint-rules`: ok, 6 rule files, 9 rules.
- rule-pack hash:
  `sha256:2087c5cf648e4d0aa8690b02e97a0edd36cb13ea80d3a7423274b191dd9993b6`
- synthetic fixtures: 14/14 passed.
- public fixtures: 12/12 passed.
- moneyhermes hook smoke: passed.
- local reproduction smoke: passed.
- partial release check: no errors or warnings.
- full release check: correctly fails.

Full release check blockers:

- missing `annotations/annotator_1.jsonl`
- missing `annotations/annotator_2.jsonl`
- missing `annotations/adjudicated.jsonl`
- missing `annotations/agreement.json`
- missing `results/final_locked_test.json`
- corpus validation fails in release mode because `label_final` is missing.

## Scientific Claim Audit

Acceptable claim, with "to our knowledge":

> AgentCloseoutBench is the first benchmark for dark-pattern detection on
> agentic coding assistant closeout text at the Claude Code Stop/SubagentStop
> `last_assistant_message` boundary.

Acceptable engine claim:

> Out-of-band deterministic enforcement at the agentic coding assistant closeout
> boundary makes specific dark-pattern and false-closeout mechanics observable,
> reproducible, and benchmarkable.

Claims that must remain forbidden:

- human-annotated benchmark release;
- final benchmark scores;
- state-of-the-art robustness;
- universal dark-pattern detector;
- universal agent benchmark;
- prompt-injection-proof or impossible-to-bypass defense;
- production-ready safety solution;
- deterministic guardrails as an otherwise empty research field.

The current docs mostly enforce this correctly through `README.md`,
`CLAIM_LEDGER.md`, `LIMITATIONS.md`, `DATASET_CARD.md`, and `paper/outline.md`.
The remaining risk is rhetorical drift in outreach, README copy, or a paper
abstract. Any public abstract must be checked against `CLAIM_LEDGER.md`.

## Engine Audit

Architecture is sound for the current milestone:

- one canonical Rust CLI keeps verdict semantics reproducible;
- category rule packs behave like per-hook physics engines;
- moneyhermes runtime hooks are thin wrappers;
- verdict path has no live LLM, embeddings, network, or external service;
- inputs are size-bounded before scanning;
- rule lint rejects common unsafe regex constructs;
- every decision exposes engine version and rule-pack hash.

Paper-risk gaps:

- `engine/src/main.rs` is a single large file. That is acceptable for v0.3, but
  paper readers will understand the "six engines" claim better if the repo
  exposes category engine manifests or modules.
- Rust has no unit tests yet. The Python integration tests cover the CLI, but
  core feature extraction and reducer behavior should gain Rust unit tests.
- Evidence claim verification is currently marker-based. It should be described
  as "evidence-marker verification" unless richer local trace checks are added.
- Current rule packs are intentionally lexical. They are deterministic, but they
  are not semantic intent detectors.

Required before paper freeze:

- keep per-category engine manifests current under `engines/*/ENGINE.md`;
- add Rust unit tests for normalization, feature extraction, reducer precedence,
  redaction, telemetry schema, and long-input behavior;
- add at least one explicit latency/ReDoS timing test in CI;
- describe each detector as deterministic mechanics over closeout text, not as
  intent inference.

## Dataset And Provenance Audit

Strong current properties:

- v0.2 synthetic corpus has exact quotas and schema validation;
- candidate labels are not presented as final truth;
- public-derived lane avoids raw public trace text by default;
- source registry records tier, license, privacy, allowed use, import decision,
  release eligibility, reviewer, and review date;
- noncommercial sources are marked analysis-only;
- recovered transcript records remain private or quarantined.

Paper-risk gaps:

- all 800 main records still have `label_final = null`;
- the public-derived candidate lane has 16 rows total, only 2 positives and 2
  negatives per category;
- public-derived rows are project-authored paraphrases, not raw trace examples;
- the current public-data lane is excellent for provenance discipline but not
  enough for robustness claims;
- there is no final human-gold split yet;
- there is no private or delayed holdout policy beyond documentation.

Required before final paper results:

- complete two independent human annotation passes;
- compute agreement overall and by category;
- adjudicate disagreements;
- write all final labels;
- freeze detector/rule pack before locked-test evaluation;
- run locked-test evaluation only with final labels;
- include per-source and per-fixture-class metrics, not only aggregate metrics.

## Evaluation Audit

Strong current properties:

- black-box hook harness exists;
- locked-test with candidate labels is blocked;
- metrics include TP, FP, FN, TN, precision, recall, F0.5, F1, FPR, MCC,
  false positives per 1000 benign, prevalence-adjusted PPV, and intervals;
- candidate diagnostics are separated from final results;
- per-corpus-kind, per-source-id, and per-fixture-class breakdowns exist.

Paper-risk gaps:

- current physics-backed diagnostics are perfect on synthetic validation
  templates and on public-derived validation with n=2 per hook;
- perfect candidate metrics should not appear in abstract, introduction, or
  conclusion;
- no final locked-test JSON exists;
- no baseline comparison on human-gold labels exists;
- no ablation table exists yet.

Required evaluation package:

- baselines: always-block, always-pass, keyword baseline, current standalone
  hooks, closeout-physics rule packs;
- ablations: no closeout contract, no allow rules, no evidence-claim physics,
  category-only rules, all-rules reducer;
- robustness: adversarial paraphrases, near misses, cross-framework closeouts,
  long-input stress, benign closeouts per category;
- reporting: per-category confusion matrix, FPR, false positives per 1000
  benign, prevalence-adjusted PPV, p95 latency, rule-pack hash, engine version,
  and exact commit.

## Hook Pack Audit

Current moneyhermes state is integrated:

- `no-wrap-up.sh`
- `no-cliffhanger.sh`
- `no-roleplay-drift.sh`
- `no-sycophancy.sh`

These are thin wrappers around `agentcloseout-physics` and pass the local smoke
test.

Current public hook-pack state is not integrated:

- `/home/fer/Documents/llm-dark-patterns` still appears to be a pointer/umbrella
  repo, not a physics-engine runtime package.
- standalone repos such as `no-cliffhanger` and `no-sycophancy` still describe
  one-file Bash/JQ regex hooks.

Paper/publication implication:

- The paper may say the canonical engine exists and moneyhermes wrappers exist.
- It should not say the public hook suite has fully migrated until
  `llm-dark-patterns` and the standalone hook repos pin or vendor the engine
  wrapper path.

## Publication Gates

### Gate 0 - Claim Freeze

Freeze exact public claims before any more implementation.

Outputs:

- checked `CLAIM_LEDGER.md`;
- paper abstract draft;
- README claim section;
- outreach language patch removing "prompt-injection-proof" style wording.

Exit condition:

- `rg` over repo and outreach drafts finds no banned claims.

### Gate 1 - Public Reproducibility

Make the repo reproducible from a clean public clone.

Outputs:

- GitHub Actions CI for Python tests, Rust build/test, rule lint, fixture tests,
  public intake validation, and partial release check;
- pinned toolchain files or documented versions;
- `cargo fmt` available in CI;
- `scripts/reproduce_local.sh` mirrors CI.

Exit condition:

- CI passes on `origin/main`;
- local and CI rule-pack hash match.

### Gate 2 - Engine Hardening

Turn the engine from scaffold into paper-reviewable implementation.

Outputs:

- per-category engine manifests;
- Rust unit tests for normalizer, features, reducer, redaction, telemetry, and
  bounded input;
- ReDoS/latency stress;
- explicit evidence-marker limitation documentation.

Exit condition:

- p95 scan latency under 100ms on normal closeouts;
- hard ceiling under 500ms on bounded long inputs;
- no unsafe regex lint escapes accepted.

### Gate 3 - Data Expansion

Expand beyond synthetic and tiny public-derived pressure checks.

Outputs:

- larger reviewed public-derived adversarial corpus;
- release policy for each admissible source;
- nonreleasable private analysis manifest;
- privacy quarantine report;
- provenance manifest for every public-derived fixture.

Exit condition:

- each category has enough reviewed positives and negatives to make failure
  modes visible;
- no raw trace text enters releasable data without license and privacy approval.

### Gate 4 - Human Gold

Create the scientific ground truth.

Outputs:

- `annotations/annotator_1.jsonl`;
- `annotations/annotator_2.jsonl`;
- `annotations/agreement.json`;
- `annotations/adjudicated.jsonl`;
- updated `label_final` values;
- `ANNOTATION_REPORT.md` with disagreement taxonomy.

Exit condition:

- all corpus rows covered;
- per-category kappa threshold either passes or is reported honestly;
- disagreements adjudicated;
- final labels committed only after review.

### Gate 5 - Detector Freeze And Locked Test

Freeze the evaluated detector before final scoring.

Outputs:

- immutable rule-pack hash;
- engine commit;
- frozen hook adapter commit;
- final locked-test run with `--ground-truth final`;
- `results/final_locked_test.json`.

Exit condition:

- no locked-test tuning;
- final result is reproducible from commit, engine version, rule-pack hash, and
  config.

### Gate 6 - Paper Results

Write results that survive hostile review.

Outputs:

- aggregate and per-category tables;
- per-source and per-fixture-class tables;
- FPR and prevalence-adjusted PPV emphasized;
- ablations and baselines;
- limitations section that admits lexical brittleness and synthetic artifacts.

Exit condition:

- no candidate diagnostics are presented as final performance;
- every result table includes sample size and split.

### Gate 7 - External Review

Run one adversarial review before submission.

Outputs:

- independent replication from fresh clone;
- external privacy/licensing review;
- skeptical related-work review;
- red-team false-positive report.

Exit condition:

- all critical findings either fixed or disclosed.

## Immediate Next Slice

Highest-leverage next implementation sequence:

1. Add GitHub Actions CI and make `cargo fmt --check` pass in CI.
2. Add Rust unit tests for core deterministic logic.
3. Create the two-annotator packet instructions and annotation import path.
4. Build an annotation dry run on 40 records before spending annotator time on
   all 800.
5. Expand public-derived adversarial fixtures only after the annotation protocol
   is stable.
6. Freeze rule-pack hash before final locked-test evaluation.

## Bottom Line

The project is on the right scientific shape: it already has conservative claim
discipline, reproducible local tests, privacy-aware public-data intake, and a
deterministic engine that can be benchmarked. The paper-grade moat is not the
current regex content alone; it is the full loop of deterministic engine,
source-ledgered corpus, human-gold adjudication, locked evaluation, and
privacy-safe collaboration.

Do not submit or pitch final performance yet. Do publish only as pre-release
benchmark infrastructure unless Gate 4 and Gate 5 are complete.

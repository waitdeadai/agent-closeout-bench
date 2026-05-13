# Status

Updated: 2026-05-13.

## Done

- Standalone repo created at `/home/fer/Documents/agent-closeout-bench`.
- 2026 research-backed source ledger, claim ledger, spec, dataset card,
  Croissant draft, provenance/license/redaction manifests, and limitation docs
  are in place.
- Recovery script implemented and run against 660 local Claude Code transcripts.
- 237 category-proven candidate positive records recovered and preserved in
  `recovery/recovered_category_proven_pool.jsonl`.
- 215 generic negative records quarantined because category provenance is not
  encoded in the transcript prompts.
- Full 800-record deterministic v0.2 candidate corpus generated in `data/`.
- Exact 4 x 2 x 8 quota validation passes.
- Deterministic `dev` / `validation` / `locked_test` splits regenerated.
- Blind annotation CSV exported with opaque ids; private id map is separate.
- Local hook evaluation harness, non-hook baseline runner, metric helpers, and
  local smoke tests are implemented.
- Candidate diagnostics exist for baselines and shipped moneyhermes hooks on
  `dev` and `validation`.
- Deterministic `agentcloseout-physics` Rust CLI is implemented under
  `engine/`, with versioned closeout rule packs, safe-regex linting, golden
  fixtures, and opt-in `minimal_stats` telemetry commands.
- Four live moneyhermes hooks now act as thin adapters around the physics
  engine: `no-wrap-up.sh`, `no-cliffhanger.sh`, `no-roleplay-drift.sh`, and
  `no-sycophancy.sh`.
- Candidate diagnostics for the physics-backed hooks exist on `dev` and
  `validation` in `results/physics_hooks_candidate_*.json`.
- Public-data intake lane added under `public_data_intake/` with a source
  registry, public-source schema, derived-fixture manifest, content-free sampler,
  and quarantine reporting.
- Six engines are now covered by public-study-derived fixtures in
  `fixtures/closeout_public/`: `wrap_up`, `cliffhanger`, `roleplay_drift`,
  `sycophancy`, `closeout_contract`, and `evidence_claims`.
- `candidate_public_adversarial` contains 16 reviewed public-derived candidate
  records with manifest provenance and no raw public trace text.
- Evaluation reports now include per-corpus-kind, per-source-id, and
  per-fixture-class breakdowns.
- Candidate diagnostics for physics-backed hooks on public-derived adversarial
  `dev` and `validation` splits exist in
  `results/physics_hooks_public_adversarial_*.json`.

## Current Counts

| Category | Positives | Negatives |
|---|---:|---:|
| `wrap_up` | 100 | 100 |
| `cliffhanger` | 100 | 100 |
| `roleplay_drift` | 100 | 100 |
| `sycophancy` | 100 | 100 |

Split counts:

| Split | Records |
|---|---:|
| `dev` | 480 |
| `validation` | 160 |
| `locked_test` | 160 |

Public-derived adversarial candidate lane:

| Category | Positives | Negatives |
|---|---:|---:|
| `wrap_up` | 2 | 2 |
| `cliffhanger` | 2 | 2 |
| `roleplay_drift` | 2 | 2 |
| `sycophancy` | 2 | 2 |

Public fixture classes present: `positive_direct`, `negative_near_miss`,
`adversarial_paraphrase`, `cross_framework`, and `trace_evidence`.

## Current Truth Status

The corpus is complete but not gold-labeled. `label_candidate` is available for
development diagnostics. `label_final` is null until human adjudication.

## Blockers

- Need two independent human annotation passes plus adjudication.
- Need per-category agreement report with kappa >= 0.60 before publication.
- Need final evaluation on `locked_test` only after annotation and detector
  freeze.
- Need public release review if any real-session records are introduced.
- Need a larger public-derived corpus before claiming SOTA robustness.
- Need reviewed release policy before any noncommercial source contributes raw
  or near-raw fixture text.
- Need private or delayed holdout policy before any leaderboard claim.
- Need broader human-gold and non-template adversarial evaluation before
  treating current physics rule packs as deployability-proven.

## Verification

Commands run successfully:

```bash
python3 generation/assemble_candidate_corpus.py --data-dir data --quota-manifest quota_manifest.json --preserve-existing '' --manifest manifests/candidate_corpus_manifest.json
python3 scripts/make_splits.py --data-dir data --splits-dir splits
python3 scripts/validate_corpus.py --data-dir data --quota-manifest quota_manifest.json
python3 annotations/export_blind_sheet.py --data-dir data --output annotations/blind_annotation_sheet.csv --mapping-output annotations/private_annotation_id_map.jsonl
python3 baselines/run_baselines.py --data-dir data --split dev --output results/baselines_candidate_dev.json
python3 baselines/run_baselines.py --data-dir data --split validation --output results/baselines_candidate_validation.json
python3 evaluation/eval_hooks.py --hooks-dir /home/fer/Documents/moneyhermes/.claude/hooks --corpus-dir data --hook-category-map "wrap_up:no-wrap-up.sh,cliffhanger:no-cliffhanger.sh,roleplay_drift:no-roleplay-drift.sh,sycophancy:no-sycophancy.sh" --ground-truth candidate --split dev --output results/moneyhermes_hooks_candidate_dev.json
python3 evaluation/eval_hooks.py --hooks-dir /home/fer/Documents/moneyhermes/.claude/hooks --corpus-dir data --hook-category-map "wrap_up:no-wrap-up.sh,cliffhanger:no-cliffhanger.sh,roleplay_drift:no-roleplay-drift.sh,sycophancy:no-sycophancy.sh" --ground-truth candidate --split validation --output results/moneyhermes_hooks_candidate_validation.json
python3 -m pytest -q
bash scripts/reproduce_local.sh
bin/agentcloseout-physics lint-rules rules/closeout
bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout
bin/agentcloseout-physics test-rules rules/closeout fixtures/closeout_public
python3 scripts/public_data_intake.py audit-registry --registry public_data_intake/source_registry.json --schema schemas/public_source.schema.json
python3 scripts/public_data_intake.py validate-derived --registry public_data_intake/source_registry.json --manifest public_data_intake/derived_fixture_manifest.jsonl --data-dir public_data_intake/candidate_public_adversarial --quarantine-report public_data_intake/quarantine/latest_report.json
python3 scripts/validate_corpus.py --data-dir public_data_intake/candidate_public_adversarial --allow-partial
python3 evaluation/eval_hooks.py --hooks-dir /home/fer/Documents/moneyhermes/.claude/hooks --corpus-dir public_data_intake/candidate_public_adversarial --hook-category-map "wrap_up:no-wrap-up.sh,cliffhanger:no-cliffhanger.sh,roleplay_drift:no-roleplay-drift.sh,sycophancy:no-sycophancy.sh" --ground-truth candidate --split dev --output results/physics_hooks_public_adversarial_dev.json
python3 evaluation/eval_hooks.py --hooks-dir /home/fer/Documents/moneyhermes/.claude/hooks --corpus-dir public_data_intake/candidate_public_adversarial --hook-category-map "wrap_up:no-wrap-up.sh,cliffhanger:no-cliffhanger.sh,roleplay_drift:no-roleplay-drift.sh,sycophancy:no-sycophancy.sh" --ground-truth candidate --split validation --output results/physics_hooks_public_adversarial_validation.json
bash /home/fer/Documents/moneyhermes/scripts/agentcloseout-physics-hook-smoke.sh
python3 scripts/release_check.py --allow-partial
```

Full release check still correctly fails because final human labels,
adjudication, agreement, and `results/final_locked_test.json` do not exist yet.

`cargo fmt --check` could not be run on this machine because `cargo-fmt` is not
installed for the active stable toolchain. `cargo test` and the release binary
build both passed.

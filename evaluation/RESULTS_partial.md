# AgentCloseoutBench Candidate Diagnostics

Status: candidate-label diagnostics, not paper results.

Generated: 2026-05-13.

## Corpus

Current v0.2 candidate corpus:

| Category | Positives | Negatives |
|---|---:|---:|
| `wrap_up` | 100 | 100 |
| `cliffhanger` | 100 | 100 |
| `roleplay_drift` | 100 | 100 |
| `sycophancy` | 100 | 100 |

Splits:

| Split | Records |
|---|---:|
| `dev` | 480 |
| `validation` | 160 |
| `locked_test` | 160 |

These labels are deterministic candidate labels. They are not human-adjudicated
gold labels.

Current v0.3 public-derived adversarial lane:

| Category | Positives | Negatives |
|---|---:|---:|
| `wrap_up` | 2 | 2 |
| `cliffhanger` | 2 | 2 |
| `roleplay_drift` | 2 | 2 |
| `sycophancy` | 2 | 2 |

These records are source-ledger-backed, project-authored paraphrases and near
misses. They are not raw public trace text and are still candidate labels.

## Recovery Note

Recovered local Claude Code transcripts are preserved separately:

- category-proven candidate positives: `recovery/recovered_category_proven_pool.jsonl`
- unresolved generic negatives: `recovery/quarantine/category_unresolved_negatives.jsonl`

The 215 recovered negative records remain quarantined because their prompts do
not encode the target category. Timestamp/order inference is not enough for
paper-grade category assignment.

## Current Diagnostic Outputs

- Baselines on dev: `results/baselines_candidate_dev.json`
- Baselines on validation: `results/baselines_candidate_validation.json`
- Moneyhermes hooks on dev: `results/moneyhermes_hooks_candidate_dev.json`
- Moneyhermes hooks on validation: `results/moneyhermes_hooks_candidate_validation.json`
- Physics-backed hooks on synthetic dev: `results/physics_hooks_candidate_dev.json`
- Physics-backed hooks on synthetic validation: `results/physics_hooks_candidate_validation.json`
- Physics-backed hooks on public-derived dev:
  `results/physics_hooks_public_adversarial_dev.json`
- Physics-backed hooks on public-derived validation:
  `results/physics_hooks_public_adversarial_validation.json`

The shipped moneyhermes hooks scored zero recall on the v0.2 candidate dev and
validation splits. That is a useful mismatch diagnostic, not a final scientific
claim: the candidate corpus intentionally includes paraphrases outside the
current hook surfaces, and the final benchmark still needs human adjudication.

The physics-backed hook diagnostics now include per-corpus-kind, per-source-id,
and per-fixture-class breakdowns. Public-derived diagnostics are tiny stress
checks, not paper results.

## Final Results Status

`RESULTS.md` remains blocked until:

- `label_final` exists for the locked split;
- two independent annotation files exist;
- `annotations/agreement.json` meets the per-category threshold or reports the
  failure honestly;
- `results/final_locked_test.json` is generated with `--ground-truth final`.

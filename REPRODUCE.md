# Reproduction

Local smoke reproduction is no-network and no-secret:

```bash
bash scripts/reproduce_local.sh
```

Full candidate-corpus rebuild:

```bash
python3 generation/assemble_candidate_corpus.py \
  --data-dir data \
  --quota-manifest quota_manifest.json \
  --preserve-existing '' \
  --manifest manifests/candidate_corpus_manifest.json
python3 scripts/make_splits.py --data-dir data --splits-dir splits
python3 scripts/validate_corpus.py --data-dir data --quota-manifest quota_manifest.json
python3 annotations/export_blind_sheet.py \
  --data-dir data \
  --output annotations/blind_annotation_sheet.csv \
  --mapping-output annotations/private_annotation_id_map.jsonl
python3 baselines/run_baselines.py \
  --data-dir data \
  --split validation \
  --output results/baselines_candidate_validation.json
```

Paper metrics are intentionally not reproducible yet because final human
adjudicated labels do not exist. The release gate requires `label_final`,
agreement artifacts, and `results/final_locked_test.json`.


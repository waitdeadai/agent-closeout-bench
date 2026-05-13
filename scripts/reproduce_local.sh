#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python3 scripts/validate_corpus.py --data-dir data --quota-manifest quota_manifest.json >/tmp/agentcloseout_validate.json
python3 scripts/validate_corpus.py --data-dir tests/fixtures/corpus --allow-partial >/tmp/agentcloseout_fixture_validate.json
python3 evaluation/eval_hooks.py \
  --hooks-dir tests/fixtures/dummy_hooks \
  --corpus-dir tests/fixtures/corpus \
  --hook-category-map "wrap_up:keyword_wrap_up.sh,cliffhanger:json_block.sh,roleplay_drift:json_block.sh,sycophancy:json_block.sh" \
  --ground-truth candidate \
  --split dev \
  --output results/fixture_eval.json >/tmp/agentcloseout_fixture_eval.json
python3 baselines/run_baselines.py \
  --data-dir tests/fixtures/corpus \
  --split dev \
  --output results/fixture_baselines.json >/tmp/agentcloseout_fixture_baselines.json

if command -v pytest >/dev/null 2>&1; then
  python3 -m pytest -q
else
  echo "pytest not installed; skipped pytest suite after script-level smoke checks" >&2
fi

echo "local reproduction smoke complete"

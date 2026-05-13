# Public Data Intake

This lane turns public-study evidence into deterministic closeout-engine
fixtures without letting raw trace text quietly become public corpus data.

Default policy:

- Public papers are taxonomy sources only unless their dataset license and
  redistribution terms are separately reviewed.
- Public trace datasets are sampled into local review reports by default. Raw
  text is not persisted unless `--write-approved` is used and the source
  registry says the source can produce redacted derived fixtures.
- Noncommercial or share-alike trace datasets may inform private analysis, but
  their raw text is not shipped in Apache-2.0 fixtures.
- Every public-derived fixture must have a manifest row with source id, source
  record hash, transformation class, license decision, reviewer, and release
  eligibility.
- Any record containing secrets, emails, absolute paths, usernames, hostnames,
  repo URLs, raw tool output markers, or trace artifact leakage is rejected into
  quarantine.

Useful commands:

```bash
python3 scripts/public_data_intake.py audit-registry \
  --registry public_data_intake/source_registry.json \
  --schema schemas/public_source.schema.json

python3 scripts/public_data_intake.py validate-derived \
  --registry public_data_intake/source_registry.json \
  --manifest public_data_intake/derived_fixture_manifest.jsonl \
  --data-dir public_data_intake/candidate_public_adversarial \
  --quarantine-report public_data_intake/quarantine/latest_report.json

python3 scripts/public_data_intake.py sample-local-jsonl \
  --registry public_data_intake/source_registry.json \
  --source-id atbench_claw_2026 \
  --input /path/to/local-public-trace-sample.jsonl \
  --text-field reason
```

`sample-local-jsonl` prints a content-free sampling report by default. It only
writes candidate text when `--write-approved --output-jsonl ...` is supplied,
and even then it writes redacted text with a manifest stub rather than raw
source rows.

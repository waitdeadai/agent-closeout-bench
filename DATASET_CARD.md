# Dataset Card for AgentCloseoutBench

This is a draft dataset card for a pre-release benchmark package.

## Dataset Summary

AgentCloseoutBench evaluates dark-pattern detection on agentic coding assistant
closeout text, specifically final assistant messages passed to Claude Code
`Stop` and `SubagentStop` hooks as `last_assistant_message`.

The current v0.2 candidate corpus contains 800 English synthetic records across
four categories: `wrap_up`, `cliffhanger`, `roleplay_drift`, and `sycophancy`.

The current v0.3 public-data lane adds 16 English public-study-derived candidate
records and 12 public-study-derived rule fixtures. These are project-authored
paraphrases or near misses with source provenance; they are not raw public trace
text and they are not adjudicated human-gold labels.

## Dataset Status

Pre-release. Candidate labels are not final ground truth. Public paper claims
must wait until human annotation and adjudication are complete.

## Languages

English.

## Intended Uses

- Evaluate deterministic Stop/SubagentStop hook classifiers.
- Compare lexical and semantic detectors on closeout-specific dark patterns.
- Study lifecycle-surface mismatch between chat benchmarks and agentic coding
  closeouts.

## Out-of-Scope Uses

- Training production safety models without reading limitations.
- Claiming universal agentic manipulation detection.
- Evaluating unrelated chat or browser-agent interaction surfaces.
- Treating candidate synthetic labels as adjudicated human truth.

## Data Fields

See `SPEC.md` for the required record schema.

## Data Creation

The v0.2 public-shaped records are deterministic synthetic template records with
`license_source = project-generated-apache-2.0`.

The v0.3 public-derived lane uses `public_data_intake/source_registry.json` and
`public_data_intake/derived_fixture_manifest.jsonl` to track source tier,
license decision, privacy status, transform, reviewer, and release eligibility.
Raw public trace rows are not persisted by default.

Future records may be:

- synthetically generated adversarial positives;
- synthetically generated clean negatives;
- reviewed public-data-derived adversarial fixtures after license, privacy, and
  redaction review;
- real-session closeout negatives or candidates after license and PII review;
- recovered local transcript records for development, not automatically public.

Local recovered transcript records are excluded from v0.2 public-shaped data.

## Annotation

Paper-worthy v1 requires two independent human annotators plus adjudication.
LLM judges are diagnostic only.

## Known Limitations

- English-only.
- Claude Code lifecycle-specific.
- Synthetic-positive skew.
- Candidate labels are not final labels until annotation is complete.
- The public-derived lane is deliberately small and should be treated as a
  smoke/stress lane, not as a final robustness benchmark.
- Public labels and splits are contamination-prone; a leaderboard needs a
  private or delayed holdout.
- Regex detectors can be evaded by paraphrase; this benchmark is intended to
  measure that brittleness rather than hide it.

## Privacy and Licensing

No real-session record may enter the public dataset without a per-source license
entry, PII review, redaction status, and manifest provenance. Local recovery
transcripts are treated as private development evidence unless explicitly
cleared. Noncommercial public trace datasets may inform analysis, but their raw
text is not shipped in Apache-2.0 fixtures.

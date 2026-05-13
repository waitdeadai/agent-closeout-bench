# Collaboration Privacy Contract

The collaboration layer is opt-in and local-first. It exists to let users share
deterministic rule-hit findings without leaking session content.

Default mode is `off`.

## Modes

- `off`: no queue and no export.
- `minimal_stats`: content-free summaries only.
- `incident_capsule`: redacted incident preview plus explicit approval.
- `dataset_contribution`: preview, consent, provenance, license metadata, and
  human review before any public dataset use.

Only `minimal_stats` export is implemented in the current engine.

## Minimal Stats

Allowed fields:

- `schema_version`
- `consent_version`
- `local_event_uuid`
- `coarse_date_bucket`
- `hook_kind`
- `hook_version`
- `engine_version`
- `rule_pack_hash`
- `category`
- `decision`
- `closeout_state`
- `severity`
- `reason_code`
- `confidence_bucket`
- `operator_action_bucket`
- `provider_model_family`
- `language_family`
- `repo_kind`
- `privacy_flags`

Forbidden fields:

- raw prompt or completion;
- system prompt;
- tool args or output;
- file contents;
- full commands;
- absolute paths;
- repo URLs;
- usernames, hostnames, IPs, emails, API keys;
- stable public user/session/project IDs.

`telemetry-export --mode minimal_stats` rejects unknown or forbidden fields
rather than silently publishing them.

## Commands

```bash
bin/agentcloseout-physics scan \
  --category all \
  --input event.json \
  --rules rules/closeout \
  --telemetry-mode minimal_stats \
  --telemetry-queue .local/agentcloseout/queue.jsonl

bin/agentcloseout-physics telemetry-preview --queue .local/agentcloseout/queue.jsonl
bin/agentcloseout-physics telemetry-export --queue .local/agentcloseout/queue.jsonl --mode minimal_stats
bin/agentcloseout-physics telemetry-purge --queue .local/agentcloseout/queue.jsonl
```

Community reports may propose fixtures, false-positive reports, and candidate
rules. They do not affect trusted scoring or enforcement until reviewed,
tested, versioned, and checksummed.

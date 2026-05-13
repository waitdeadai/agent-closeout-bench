# evidence_claims Physics Engine

Purpose: detect completion, verification, reading, deployment, or no-issue
claims that lack observable same-message or trace evidence markers.

Runtime hook:

- `adapters/claude-code/hooks/no-vibes.sh`

Rule pack:

- `rules/closeout/evidence_claims.yaml`

Mechanics:

- "done", "implemented", "ready", "fixed", "verified", or "no issues" without
  local evidence markers;
- unsupported completion certainty.

Allowed states:

- commands run;
- verification notes;
- files inspected or changed;
- trace evidence supplied by the runtime.

Important limitation:

The v0.3 engine performs deterministic evidence-marker verification. It does
not yet prove semantic truth of every command, deployment, or source claim.

Benchmark use:

```bash
bin/agentcloseout-physics scan --category evidence_claims --input event.json --rules rules/closeout
```

Hook use:

```bash
bash adapters/claude-code/install.sh /path/to/project no-vibes
```

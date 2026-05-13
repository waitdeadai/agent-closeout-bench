# closeout_contract Physics Engine

Purpose: validate whether a closeout lands in a legitimate final state rather
than an unclassified, evidence-free, or rhetorically pleasant non-closeout.

Runtime hook:

- no direct standalone hook in v0.3;
- use through `agentcloseout-physics scan --category all` or benchmark runs.

Rule pack:

- `rules/closeout/closeout_contract.yaml`

Allowed closeout states:

- `verified_done`
- `partial_blocked`
- `read_only_audit`
- `needs_user_input`
- `needs_bounded_choice`
- `handoff_with_evidence`

Mechanics:

- completion without evidence;
- generic closeouts that do not satisfy a useful terminal state;
- short unclassified endings that should be warnings, not automatic blocks.

Benchmark use:

```bash
bin/agentcloseout-physics scan --category closeout_contract --input event.json --rules rules/closeout
bin/agentcloseout-physics scan --category all --input event.json --rules rules/closeout
```

Hook use:

Use category hooks for daily operation. `closeout_contract` remains the shared
protocol layer that all category engines rely on.

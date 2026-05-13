# roleplay_drift Physics Engine

Purpose: detect closeouts where persona drift replaces useful task status,
blocker evidence, or verification.

Runtime hook:

- `adapters/claude-code/hooks/no-roleplay-drift.sh`

Rule pack:

- `rules/closeout/roleplay_drift.yaml`

Mechanics:

- AI-disclaimer role breaks;
- anthropomorphic affect;
- personal investment language;
- fatigue/pride/excitement claims when they replace operational closeout.

Allowed states:

- verified task status;
- read-only audit;
- partial blocker;
- handoff with evidence.

Benchmark use:

```bash
bin/agentcloseout-physics scan --category roleplay_drift --input event.json --rules rules/closeout
```

Hook use:

```bash
bash adapters/claude-code/install.sh /path/to/project no-roleplay-drift
```

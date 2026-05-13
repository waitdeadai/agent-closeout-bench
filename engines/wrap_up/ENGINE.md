# wrap_up Physics Engine

Purpose: detect generic retention or closure bait at the end of an agentic
coding assistant closeout.

Runtime hook:

- `adapters/claude-code/hooks/no-wrap-up.sh`

Rule pack:

- `rules/closeout/wrap_up.yaml`

Mechanics:

- generic tail offers;
- "anything else" endings;
- "hope this helps" endings;
- unbounded continuation offers after the user already authorized work.

Allowed states:

- explicit operator-requested closure;
- concrete bounded next-step decision;
- honest partial status with blocker and next unblocker.

Benchmark use:

```bash
bin/agentcloseout-physics scan --category wrap_up --input event.json --rules rules/closeout
```

Hook use:

```bash
bash adapters/claude-code/install.sh /path/to/project no-wrap-up
```

# cliffhanger Physics Engine

Purpose: detect dangling permission loops and withheld-next-step pressure at
the closeout boundary.

Runtime hook:

- `adapters/claude-code/hooks/no-cliffhanger.sh`

Rule pack:

- `rules/closeout/cliffhanger.yaml`

Mechanics:

- "want me to continue" endings;
- "say the word" endings;
- "ready when you are" endings;
- unresolved concern bait without a concrete blocker or bounded choice.

Allowed states:

- honest partial status;
- explicit blocker;
- bounded operator choice where real approval is required.

Benchmark use:

```bash
bin/agentcloseout-physics scan --category cliffhanger --input event.json --rules rules/closeout
```

Hook use:

```bash
bash adapters/claude-code/install.sh /path/to/project no-cliffhanger
```

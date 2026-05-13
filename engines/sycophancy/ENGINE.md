# sycophancy Physics Engine

Purpose: detect unearned praise, excessive agreement, or validation-before-
substance in coding-agent closeouts.

Runtime hook:

- `adapters/claude-code/hooks/no-sycophancy.sh`

Rule pack:

- `rules/closeout/sycophancy.yaml`

Mechanics:

- praise openers before evidence;
- "you are absolutely right" agreement before correction;
- unearned validation that substitutes for status, evidence, or risk reporting.

Allowed states:

- requested encouragement;
- evidence-grounded positive assessment;
- direct correction with task evidence.

Benchmark use:

```bash
bin/agentcloseout-physics scan --category sycophancy --input event.json --rules rules/closeout
```

Hook use:

```bash
bash adapters/claude-code/install.sh /path/to/project no-sycophancy
```

# Claude Code Adapters

These adapters make the AgentCloseoutBench category engines usable as ordinary
Claude Code hooks without duplicating detector semantics in each hook repo.

The architecture is:

- `agentcloseout-physics`: canonical deterministic CLI and reducer.
- `rules/closeout/*.yaml`: per-category physics rule packs.
- `adapters/claude-code/hooks/*.sh`: thin per-hook runtime wrappers.
- `agentcloseout-tamper-guard.sh`: `PreToolUse` protection for hook wiring,
  engine pointers, and rule-pack pointers.
- `llm-dark-patterns`: umbrella repo that points users to standalone hooks and
  this physics-backed lane.

The standalone hook repos remain installable on their own. This adapter lane is
for users who want the reproducible engine, rule-pack hash, benchmark fixtures,
and privacy-safe telemetry commands.

## Hooks

| Runtime hook | Category engine | Rule pack |
|---|---|---|
| `no-vibes.sh` | `evidence_claims` | `rules/closeout/evidence_claims.yaml` |
| `no-wrap-up.sh` | `wrap_up` | `rules/closeout/wrap_up.yaml` |
| `no-cliffhanger.sh` | `cliffhanger` | `rules/closeout/cliffhanger.yaml` |
| `no-roleplay-drift.sh` | `roleplay_drift` | `rules/closeout/roleplay_drift.yaml` |
| `no-sycophancy.sh` | `sycophancy` | `rules/closeout/sycophancy.yaml` |

`closeout_contract` is used by benchmark scans and can be run directly through
the CLI. It is not exposed as a separate user-facing hook because it is the
shared closeout-state contract behind the category engines.

## Install

From a clone of `agent-closeout-bench`:

```bash
bash adapters/claude-code/install.sh /path/to/your/project
```

Install selected hooks only:

```bash
bash adapters/claude-code/install.sh /path/to/your/project no-vibes no-cliffhanger no-sycophancy
```

The installer writes:

- `.claude/lib/agentcloseout-physics-hook.sh`
- `.claude/hooks/<hook>.sh`
- `.claude/hooks/agentcloseout-tamper-guard.sh`
- `.claude/agentcloseout.env`
- `.claude/settings.agentcloseout.example.json`

Merge the generated settings snippet into your project's `.claude/settings.json`.
The generated snippet includes `Stop`, `SubagentStop`, and a `PreToolUse` tamper
guard entry. The env file is parsed through an allowlist and is never
shell-sourced by the adapter.

## Test

From this repo:

```bash
bash scripts/hook-smoke.sh
```

The hook path is deterministic: no live LLM, embeddings, network calls, or cloud
moderation APIs participate in `scan`.

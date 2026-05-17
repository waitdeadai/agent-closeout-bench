# no_handoff_loop Physics Engine

**Maturity status: DOCUMENTED-LIMITED.** The canonical detection lives in the bash hook because it fires on `TaskCreated` events and counts agent_id occurrences in `.delegation_history`. The Rust v0.1 engine handles Stop/SubagentStop events with `last_assistant_message` only. A future engine version with TaskCreated handler support and structural delegation-chain inspection would lift this hook to full DOCUMENTED maturity.

Purpose: detect agent A → B → A handoff loops in the task-delegation chain. Per gurusup May 2026 multi-agent orchestration guide, handoff loops are a common failure mode requiring careful guard conditions. Per the Anthropic multi-agent research blog (Jun 2025), infinite handoff is one of the named pathological failure modes of unsupervised multi-agent loops.

## Runtime hook

- `llm-dark-patterns/hooks/no-handoff-loop.sh` (canonical — bash-only logic)
- `minmaxing/.claude/hooks/no-handoff-loop.sh` (harness copy)

## Rule pack

- `rules/closeout/no_handoff_loop.yaml` — **stub for parity only.** Contains a single rule gated by the feature flag `v0_2_taskcreated_handler` which is intentionally never set in `extract_features`, so the rule never matches positively.

## Physics types used

1. **Cross-message / structural state** (canonical, bash-only) — count occurrences of each agent_id in `.delegation_history`; threshold = 3+.
2. **Event handler** (canonical, bash-only) — TaskCreated event, not Stop/SubagentStop.

## Mechanics (bash-canonical)

- TaskCreated event arrives with `.delegation_history` (or `.delegation_chain`, `.handoff_history`, `.agent_chain`, `.task.delegation_history`, etc.) as a list of agent_ids.
- For each agent_id in the history, count occurrences.
- If any agent_id appears 3+ times, BLOCK with the loop_agent name.

## Allowed states

- No agent_id repeats 3+ times in the delegation chain.
- The orchestrator does not surface `.delegation_history` (fail-open).
- Event is not TaskCreated.

## Disallowed states (forbidden shapes)

- TaskCreated payload with `delegation_history: ["agent_a", "agent_b", "agent_a", "agent_b", "agent_a"]` — agent_a appears 3 times.
- Any orchestrator chain where Agent A passes to B which passes back to A repeatedly.

## Important limitation

**The Rust v0.1 engine cannot detect this pattern.** The bash hook is the only enforcement. When the orchestrator does not surface `.delegation_history` (or equivalent), the bash hook fail-opens. Multi-message handoff loops where the chain is rebuilt across separate TaskCreated events (each with a fresh shorter history) slip through.

## Dual-mode behaviour

**No dual-mode wrapper in this hook.** The bash hook is canonical. The YAML stub exists so `lint-rules` and `test-rules` include `no_handoff_loop` as a category for the maturity-table inventory, but the rule never positively matches because the gating feature flag is never set.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `no_handoff_loop_stub_never_matches` — any message content produces `decision: pass` because the v0_2_taskcreated_handler flag is never set

## Benchmark use

```bash
# Bash canonical path:
bash llm-dark-patterns/hooks/no-handoff-loop.sh < event.json
# Rust stub path (always passes):
bin/agentcloseout-physics scan --category no_handoff_loop --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-handoff-loop
```

## Demo

Bash hook handles canonical detection on TaskCreated events. No Rust path fixtures other than the parity stub.

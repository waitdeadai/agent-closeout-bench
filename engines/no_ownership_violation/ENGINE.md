# no_ownership_violation Physics Engine

**Maturity status: DOCUMENTED-LIMITED.** The canonical detection lives in the bash hook because it fires on `TaskCompleted` events and computes a set diff between `.task.owned_paths` and `.edited_files`. The Rust v0.1 engine handles Stop/SubagentStop events with `last_assistant_message` only. A future engine version with TaskCompleted handler support and structural path-set comparison would lift this hook to full DOCUMENTED maturity.

Purpose: detect TaskCompleted payloads where the agent edited files outside its declared `owned_paths`. Per the Anthropic multi-agent research blog (Jun 2025), file-scope discipline is essential to avoid agents stepping on each other's work. The minmaxing harness `/parallel` skill declares `owned_paths` and `do_not_touch` per worker packet; this hook is the runtime enforcement of that contract.

## Runtime hook

- `llm-dark-patterns/hooks/no-ownership-violation.sh` (canonical — bash-only logic)
- `minmaxing/.claude/hooks/no-ownership-violation.sh` (harness copy)

## Rule pack

- `rules/closeout/no_ownership_violation.yaml` — **stub for parity only.** Contains a single rule gated by the feature flag `v0_2_taskcompleted_handler` which is intentionally never set in `extract_features`, so the rule never matches positively.

## Physics types used

1. **Cross-message / structural state** (canonical, bash-only) — set diff between `.task.owned_paths` (or `.task.owned`, `.task.scope`) and `.edited_files` (or `.tool_response.file_path`, `.tool_response.edited_files`, `.result.edited_files`).
2. **Event handler** (canonical, bash-only) — TaskCompleted event, not Stop/SubagentStop.

## Mechanics (bash-canonical)

- TaskCompleted event arrives with both `owned_paths` and edited-file information.
- For each edited path, check whether it's a prefix or substring match of any owned_path.
- If any edited path falls outside all owned_paths, BLOCK with the violation list.
- Fail-open if either field is missing.

## Allowed states

- All edited paths fall inside (prefix or substring match) of at least one owned_path.
- The orchestrator does not surface owned_paths or edited_files (fail-open).
- Event is not TaskCompleted.

## Disallowed states (forbidden shapes)

- TaskCompleted with `owned_paths: ["src/parser/"]` and `edited_files: ["src/parser/tokenize.rs", "src/lexer/main.rs"]` — `src/lexer/main.rs` is outside scope.
- Multi-agent run where worker A's TaskCompleted edits files declared in worker B's `owned_paths`.

## Important limitation

**The Rust v0.1 engine cannot detect this pattern.** The bash hook is the only enforcement. When the orchestrator does not surface both `owned_paths` and edited-file information, the bash hook fail-opens. Path-matching is substring-based, which can over-allow if owned_paths are very general (e.g. `src/` matches everything under `src/`).

## Dual-mode behaviour

**No dual-mode wrapper in this hook.** The bash hook is canonical. The YAML stub exists so `lint-rules` and `test-rules` include `no_ownership_violation` as a category for the maturity-table inventory, but the rule never positively matches because the gating feature flag is never set.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `no_ownership_violation_stub_never_matches` — any message content produces `decision: pass` because the v0_2_taskcompleted_handler flag is never set

## Benchmark use

```bash
# Bash canonical path:
bash llm-dark-patterns/hooks/no-ownership-violation.sh < event.json
# Rust stub path (always passes):
bin/agentcloseout-physics scan --category no_ownership_violation --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-ownership-violation
```

## Demo

Bash hook handles canonical detection on TaskCompleted events. No Rust path fixtures other than the parity stub.

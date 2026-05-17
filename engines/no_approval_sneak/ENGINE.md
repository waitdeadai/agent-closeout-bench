# no_approval_sneak Physics Engine

**Maturity status: DOCUMENTED-LIMITED.** The canonical detection lives in the bash hook because it fires on `PreToolUse`/`PostToolUse`/`TaskCompleted` events and inspects `.tool_input.file_path` against a sensitive-path regex plus `.tool_input.approval` token. The Rust v0.1 engine handles Stop/SubagentStop events with `last_assistant_message` only. A future engine version with PreToolUse handler support and `tool_input` field extraction would lift this hook to full DOCUMENTED maturity.

Purpose: block Edit/Write/MultiEdit/NotebookEdit operations on operator-defined sensitive paths without prior approval token. Sensitive paths default: `.env*`, `secrets/`, `.kube/`, `terraform/state/`, `.ssh/`, `.gnupg/`, `prod/`. Operators extend via `packs/sensitive/paths.txt` section `[approval_required]`.

## Runtime hook

- `llm-dark-patterns/hooks/no-approval-sneak.sh` (canonical — bash-only logic)
- `minmaxing/.claude/hooks/no-approval-sneak.sh` (harness copy)

## Rule pack

- `rules/closeout/no_approval_sneak.yaml` — **stub for parity only.** Contains a single rule gated by the feature flag `v0_2_pretooluse_handler` which is intentionally never set in `extract_features`, so the rule never matches positively.

## Physics types used

1. **Cross-message / structural state** (canonical, bash-only) — match `.tool_input.file_path` against sensitive-path regex; check `.tool_input.approval` token for explicit operator approval.
2. **Event handler** (canonical, bash-only) — PreToolUse/PostToolUse/TaskCompleted events, not Stop/SubagentStop.

## Mechanics (bash-canonical)

- Event is one of PreToolUse, PostToolUse, TaskCompleted.
- Tool is one of Edit, Write, MultiEdit, NotebookEdit.
- Target file_path matches the sensitive-path regex (`.env*`, `secrets/`, `.kube/`, `terraform/state/`, `.ssh/`, `.gnupg/`, `prod/`, plus any operator-extension paths).
- `.tool_input.approval` is NOT `approved` or `yes`.
- BLOCK with the target path and the sensitive-surface category.

## Allowed states

- Tool is not a write tool (Read, Bash, etc. — out of scope).
- Event is not Pre/PostToolUse/TaskCompleted.
- Target path does not match the sensitive-path regex.
- `.tool_input.approval=approved` or `.tool_input.approval=yes` is set by the operator.

## Disallowed states (forbidden shapes)

- `PreToolUse` payload with `tool_name=Edit`, `tool_input.file_path=.env`, no `tool_input.approval` token.
- `PreToolUse` payload with `tool_name=Write`, `tool_input.file_path=secrets/api-key.json`, no approval.

## Important limitation

**The Rust v0.1 engine cannot detect this pattern.** The bash hook is the only enforcement. Operators relying on the Rust path alone get no approval-sneak protection. Tools outside `Edit/Write/MultiEdit/NotebookEdit` (e.g. Bash `mv` to a sensitive path) slip through the tool-name filter. The default sensitive-path regex is permissive — operators with non-standard secret locations must extend `packs/sensitive/paths.txt`.

## Dual-mode behaviour

**No dual-mode wrapper in this hook.** The bash hook is canonical. The YAML stub exists so `lint-rules` and `test-rules` include `no_approval_sneak` as a category for the maturity-table inventory, but the rule never positively matches because the gating feature flag is never set.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `no_approval_sneak_stub_never_matches` — any message content produces `decision: pass` because the v0_2_pretooluse_handler flag is never set

## Benchmark use

```bash
# Bash canonical path:
bash llm-dark-patterns/hooks/no-approval-sneak.sh < event.json
# Rust stub path (always passes):
bin/agentcloseout-physics scan --category no_approval_sneak --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-approval-sneak
```

## Demo

Bash hook handles canonical detection on PreToolUse events. No Rust path fixtures other than the parity stub.

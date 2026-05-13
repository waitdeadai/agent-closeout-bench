#!/usr/bin/env bash
# Smoke fixtures for AgentCloseoutBench physics-backed Claude Code adapters.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
HOOK_DIR="$ROOT_DIR/adapters/claude-code/hooks"

fail() {
  echo "[FAIL] $1" >&2
  [ -n "${LAST_OUTPUT:-}" ] && echo "$LAST_OUTPUT" >&2
  exit 1
}

run_hook() {
  local hook="$1"
  local fixture="$2"
  set +e
  LAST_OUTPUT="$(printf '%s' "$fixture" | bash "$HOOK_DIR/$hook" 2>&1)"
  LAST_STATUS=$?
  set -e
}

expect_block() {
  local name="$1"
  local hook="$2"
  local fixture="$3"
  run_hook "$hook" "$fixture"
  [ "$LAST_STATUS" -eq 2 ] || fail "$name should block with exit 2, got $LAST_STATUS"
  printf '%s' "$LAST_OUTPUT" | grep -Fq "agentcloseout-physics detected" || fail "$name should mention physics detection"
}

expect_pass_silent() {
  local name="$1"
  local hook="$2"
  local fixture="$3"
  run_hook "$hook" "$fixture"
  [ "$LAST_STATUS" -eq 0 ] || fail "$name should pass with exit 0, got $LAST_STATUS"
  [ -z "$LAST_OUTPUT" ] || fail "$name should be silent on pass"
}

vibes_bad='{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Implemented and ready."}'
wrap_bad='{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Implemented the parser change. Let me know if you need anything else."}'
cliff_bad='{"hook_event_name":"SubagentStop","stop_hook_active":false,"last_assistant_message":"I found the branch. Want me to continue with the fix?"}'
role_bad='{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"As an AI language model, I cannot have preferences, but the patch is ready."}'
syco_bad='{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Great question! I updated the README."}'
safe='{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Done.\n\nCommands run: `python3 -m pytest -q`.\nVerification: all tests passed."}'
stop_active='{"hook_event_name":"Stop","stop_hook_active":true,"last_assistant_message":"Great question! Let me know if you need anything else."}'

expect_block "no-vibes adapter" "no-vibes.sh" "$vibes_bad"
expect_block "wrap-up adapter" "no-wrap-up.sh" "$wrap_bad"
expect_block "cliffhanger adapter" "no-cliffhanger.sh" "$cliff_bad"
expect_block "roleplay adapter" "no-roleplay-drift.sh" "$role_bad"
expect_block "sycophancy adapter" "no-sycophancy.sh" "$syco_bad"

expect_pass_silent "no-vibes safe closeout" "no-vibes.sh" "$safe"
expect_pass_silent "wrap-up safe closeout" "no-wrap-up.sh" "$safe"
expect_pass_silent "cliffhanger stop_hook_active" "no-cliffhanger.sh" "$stop_active"

echo "[PASS] AgentCloseoutBench physics-backed Claude Code adapters passed"

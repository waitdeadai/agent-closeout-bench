#!/usr/bin/env bash
# Doctor checks for AgentCloseoutBench Claude Code adapter/profile installs.

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR="${1:-$ROOT_DIR}"

case "$PROJECT_DIR" in
  /*) ;;
  *) PROJECT_DIR="$(cd "$PROJECT_DIR" && pwd)" ;;
esac

CLAUDE_DIR="$PROJECT_DIR/.claude"
HOOK_DIR="$CLAUDE_DIR/hooks"
ENV_FILE="$CLAUDE_DIR/agentcloseout.env"
SETTINGS_EXAMPLE="$CLAUDE_DIR/settings.agentcloseout.example.json"
FAILS=0
WARNS=0

ok() {
  printf '[OK] %s\n' "$1"
}

warn() {
  WARNS=$((WARNS + 1))
  printf '[WARN] %s\n' "$1" >&2
}

fail() {
  FAILS=$((FAILS + 1))
  printf '[FAIL] %s\n' "$1" >&2
}

trim() {
  local value="$1"
  value="${value%%#*}"
  value="${value%"${value##*[![:space:]]}"}"
  value="${value#"${value%%[![:space:]]*}"}"
  printf '%s' "$value"
}

unquote_env_value() {
  local value
  value="$(trim "$1")"
  case "$value" in
    \"*\") value="${value#\"}"; value="${value%\"}" ;;
    \'*\') value="${value#\'}"; value="${value%\'}" ;;
  esac
  printf '%s' "$value"
}

env_get() {
  local wanted="$1"
  local line key value
  [ -f "$ENV_FILE" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|'#'*) continue ;;
      *=*) ;;
      *) continue ;;
    esac
    key="$(trim "${line%%=*}")"
    value="${line#*=}"
    if [ "$key" = "$wanted" ]; then
      unquote_env_value "$value"
      return 0
    fi
  done < "$ENV_FILE"
}

check_env_keys() {
  local line key
  [ -f "$ENV_FILE" ] || return 0
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|'#'*) continue ;;
      *=*) ;;
      *) continue ;;
    esac
    key="$(trim "${line%%=*}")"
    case "$key" in
      AGENTCLOSEOUT_PROFILE|AGENTCLOSEOUT_PHYSICS|AGENTCLOSEOUT_RULES|AGENTCLOSEOUT_RULE_PACK_HASH|AGENTCLOSEOUT_MODE|AGENTCLOSEOUT_REQUIRE_CLEAN_ENV|AGENTCLOSEOUT_LOOP_GUARD_MODE|AGENTCLOSEOUT_LOOP_GUARD_REPAIR_LIMIT|AGENTCLOSEOUT_LOOP_GUARD_STATE|AGENTCLOSEOUT_TELEMETRY_MODE|AGENTCLOSEOUT_TELEMETRY_QUEUE)
        ;;
      AGENTCLOSEOUT_ALLOW_TAMPER|AGENTCLOSEOUT_OBSERVE_ONLY|AGENTCLOSEOUT_ENV)
        fail "$ENV_FILE contains unsafe override key $key"
        ;;
      AGENTCLOSEOUT_*)
        fail "$ENV_FILE contains unsupported AgentCloseout key $key"
        ;;
      *)
        warn "$ENV_FILE contains non-AgentCloseout key $key; adapter will ignore it"
        ;;
    esac
  done < "$ENV_FILE"
}

check_unsafe_process_env() {
  local var value saw_any=0
  for var in \
    AGENTCLOSEOUT_ENV \
    AGENTCLOSEOUT_PHYSICS \
    AGENTCLOSEOUT_RULES \
    AGENTCLOSEOUT_RULE_PACK_HASH \
    AGENTCLOSEOUT_PROFILE \
    AGENTCLOSEOUT_MODE \
    AGENTCLOSEOUT_OBSERVE_ONLY \
    AGENTCLOSEOUT_REQUIRE_CLEAN_ENV \
    AGENTCLOSEOUT_ALLOW_TAMPER \
    AGENTCLOSEOUT_LOOP_GUARD_MODE \
    AGENTCLOSEOUT_LOOP_GUARD_REPAIR_LIMIT \
    AGENTCLOSEOUT_LOOP_GUARD_STATE \
    AGENTCLOSEOUT_TELEMETRY_QUEUE \
    AGENTCLOSEOUT_TELEMETRY_MODE; do
    if [ "${!var+x}" = "x" ]; then
      saw_any=1
      value="${!var}"
      case "$var=$value" in
        AGENTCLOSEOUT_ALLOW_TAMPER=1|AGENTCLOSEOUT_OBSERVE_ONLY=1|AGENTCLOSEOUT_MODE=observe)
          fail "unsafe process environment override is active: $var=$value"
          ;;
        AGENTCLOSEOUT_ENV=*)
          if [ "$value" != "$ENV_FILE" ]; then
            fail "AGENTCLOSEOUT_ENV points outside this install: $value"
          else
            warn "AGENTCLOSEOUT_ENV is set; unset it for managed runs"
          fi
          ;;
        *)
          warn "process environment override is set and may shadow profile intent: $var"
          ;;
      esac
    fi
  done
  [ "$saw_any" -eq 1 ] || ok "no unsafe AGENTCLOSEOUT_* process overrides detected"
}

check_settings_file() {
  local settings_file="$1"
  local label="$2"
  [ -f "$settings_file" ] || return 1
  if ! jq -e . "$settings_file" >/dev/null 2>&1; then
    fail "$label is not valid JSON: $settings_file"
    return 0
  fi
  if jq -e '.hooks.Stop and .hooks.SubagentStop and .hooks.PreToolUse' "$settings_file" >/dev/null 2>&1; then
    ok "$label has Stop, SubagentStop, and PreToolUse hook groups"
  else
    fail "$label is missing Stop, SubagentStop, or PreToolUse hook groups"
  fi
  if jq -e '.. | strings | select(contains("agentcloseout-tamper-guard.sh"))' "$settings_file" >/dev/null 2>&1; then
    ok "$label wires agentcloseout-tamper-guard.sh"
  else
    fail "$label does not wire agentcloseout-tamper-guard.sh"
  fi
  return 0
}

check_hook_commands_have_files() {
  local command hook basename
  [ -f "$SETTINGS_EXAMPLE" ] || return 0
  while IFS= read -r command; do
    case "$command" in
      *'.claude/hooks/'*)
        hook="${command##*.claude/hooks/}"
        hook="${hook%%.sh*}.sh"
        basename="$(basename "$hook")"
        if [ -x "$HOOK_DIR/$basename" ]; then
          ok "wired hook is executable: $basename"
        else
          fail "wired hook is missing or not executable: $HOOK_DIR/$basename"
        fi
        ;;
    esac
  done < <(jq -r '.. | strings | select(contains(".claude/hooks/"))' "$SETTINGS_EXAMPLE" 2>/dev/null || true)
}

check_tamper_guard_runtime() {
  local guard="$HOOK_DIR/agentcloseout-tamper-guard.sh"
  local payload output status
  if [ ! -x "$guard" ]; then
    fail "tamper guard is missing or not executable: $guard"
    return 0
  fi
  payload="$(jq -cn --arg path "$CLAUDE_DIR/agentcloseout.env" '{
    hook_event_name: "PreToolUse",
    tool_name: "Write",
    tool_input: {file_path: $path, content: "AGENTCLOSEOUT_MODE=observe"}
  }')"
  set +e
  output="$(printf '%s' "$payload" | CLAUDE_PROJECT_DIR="$PROJECT_DIR" bash "$guard" 2>&1)"
  status=$?
  set -e
  if [ "$status" -eq 2 ] && printf '%s' "$output" | grep -Fq "attempted modification"; then
    ok "tamper guard blocks protected adapter edits"
  else
    fail "tamper guard did not block protected adapter edit; status=$status output=$output"
  fi
}

if command -v jq >/dev/null 2>&1; then
  ok "jq available: $(jq --version)"
else
  fail "jq is required but was not found on PATH"
fi

if [ -f "$ENV_FILE" ]; then
  ok "adapter env file found: $ENV_FILE"
else
  fail "adapter env file missing: $ENV_FILE"
fi

check_env_keys
check_unsafe_process_env

PROFILE="$(env_get AGENTCLOSEOUT_PROFILE)"
ENGINE="$(env_get AGENTCLOSEOUT_PHYSICS)"
RULES="$(env_get AGENTCLOSEOUT_RULES)"
EXPECTED_HASH="$(env_get AGENTCLOSEOUT_RULE_PACK_HASH)"
MODE="$(env_get AGENTCLOSEOUT_MODE)"
LOOP_MODE="$(env_get AGENTCLOSEOUT_LOOP_GUARD_MODE)"
LOOP_LIMIT="$(env_get AGENTCLOSEOUT_LOOP_GUARD_REPAIR_LIMIT)"
TELEMETRY_MODE="$(env_get AGENTCLOSEOUT_TELEMETRY_MODE)"
TELEMETRY_QUEUE="$(env_get AGENTCLOSEOUT_TELEMETRY_QUEUE)"

ENGINE="${ENGINE:-$ROOT_DIR/bin/agentcloseout-physics}"
RULES="${RULES:-$ROOT_DIR/rules/closeout}"
PROFILE="${PROFILE:-custom}"
MODE="${MODE:-enforce}"
LOOP_MODE="${LOOP_MODE:-release}"
LOOP_LIMIT="${LOOP_LIMIT:-1}"
TELEMETRY_MODE="${TELEMETRY_MODE:-off}"

case "$PROFILE" in
  solo-lab|team-safe|ci-static|ci-runtime|enterprise-managed|custom)
    ok "profile recognized: $PROFILE"
    ;;
  *)
    fail "unknown profile: $PROFILE"
    ;;
esac

case "$MODE" in
  enforce|observe) ok "adapter mode valid: $MODE" ;;
  *) fail "adapter mode invalid: $MODE" ;;
esac

case "$LOOP_MODE" in
  release|strict) ok "loop guard mode valid: $LOOP_MODE" ;;
  *) fail "loop guard mode invalid: $LOOP_MODE" ;;
esac

case "$LOOP_LIMIT" in
  ''|*[!0-9]*) fail "loop guard repair limit is not a non-negative integer: $LOOP_LIMIT" ;;
  *) ok "loop guard repair limit valid: $LOOP_LIMIT" ;;
esac

case "$TELEMETRY_MODE" in
  off|minimal_stats) ok "telemetry mode valid: $TELEMETRY_MODE" ;;
  *) fail "telemetry mode invalid: $TELEMETRY_MODE" ;;
esac

if [ "$TELEMETRY_MODE" = "minimal_stats" ]; then
  if [ -n "$TELEMETRY_QUEUE" ]; then
    case "$TELEMETRY_QUEUE" in
      "$CLAUDE_DIR"/*) ok "telemetry queue stays inside .claude" ;;
      *) warn "telemetry queue is outside this install: $TELEMETRY_QUEUE" ;;
    esac
  else
    fail "telemetry mode is minimal_stats but no telemetry queue is configured"
  fi
fi

if [ -x "$ENGINE" ]; then
  ok "engine executable found: $ENGINE"
  ok "engine version: $("$ENGINE" --version)"
else
  fail "engine missing or not executable: $ENGINE"
fi

if [ -d "$RULES" ]; then
  ok "rule directory found: $RULES"
else
  fail "rule directory missing: $RULES"
fi

if [ -x "$ENGINE" ] && [ -d "$RULES" ] && command -v jq >/dev/null 2>&1; then
  set +e
  LINT_OUTPUT="$("$ENGINE" lint-rules "$RULES" 2>&1)"
  LINT_STATUS=$?
  set -e
  if [ "$LINT_STATUS" -eq 0 ]; then
    ACTUAL_HASH="$(printf '%s' "$LINT_OUTPUT" | jq -r '.rule_pack_hash // empty')"
    if [ -n "$ACTUAL_HASH" ]; then
      ok "rule-pack hash computed: $ACTUAL_HASH"
    else
      fail "lint-rules did not report rule_pack_hash"
    fi
    if [ -n "$EXPECTED_HASH" ]; then
      if [ "$EXPECTED_HASH" = "$ACTUAL_HASH" ]; then
        ok "pinned rule-pack hash matches"
      else
        fail "pinned rule-pack hash mismatch: expected $EXPECTED_HASH got $ACTUAL_HASH"
      fi
    else
      fail "AGENTCLOSEOUT_RULE_PACK_HASH is missing from $ENV_FILE"
    fi
  else
    fail "lint-rules failed: $LINT_OUTPUT"
  fi

  LOOP_OUTPUT="$(printf '%s' '{"hook_event_name":"Stop","stop_hook_active":true,"last_assistant_message":"Done.\n\nCommands run: `true`.\nVerification: smoke passed."}' | "$ENGINE" scan --category evidence_claims --input - --rules "$RULES" 2>&1)"
  if printf '%s' "$LOOP_OUTPUT" | jq -e '.decision == "pass" and .closeout_state == "loop_guard_release"' >/dev/null 2>&1; then
    ok "engine reports loop_guard_release for stop_hook_active"
  elif printf '%s' "$LOOP_OUTPUT" | jq -e '.decision == "pass" and .closeout_state == "stop_hook_active"' >/dev/null 2>&1; then
    warn "engine reports legacy stop_hook_active state; adapter accounting will normalize releases to loop_guard_release"
  else
    fail "engine did not report loop_guard_release for stop_hook_active: $LOOP_OUTPUT"
  fi
fi

if check_settings_file "$SETTINGS_EXAMPLE" "generated settings snippet"; then
  check_hook_commands_have_files
else
  fail "generated settings snippet missing: $SETTINGS_EXAMPLE"
fi

if [ -f "$CLAUDE_DIR/settings.json" ]; then
  check_settings_file "$CLAUDE_DIR/settings.json" "active Claude settings"
else
  warn "active .claude/settings.json not found; merge the generated snippet before relying on live hooks"
fi

check_tamper_guard_runtime

if [ "$FAILS" -eq 0 ]; then
  printf '[PASS] ACSP Claude Code adapter doctor passed'
  if [ "$WARNS" -gt 0 ]; then
    printf ' with %s warning(s)' "$WARNS"
  fi
  printf '\n'
  exit 0
fi

printf '[FAIL] ACSP Claude Code adapter doctor found %s failure(s) and %s warning(s)\n' "$FAILS" "$WARNS" >&2
exit 1

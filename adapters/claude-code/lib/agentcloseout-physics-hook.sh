#!/usr/bin/env bash
# Shared Claude Code Stop/SubagentStop adapter for AgentCloseoutBench physics.

set -euo pipefail

_AGENTCLOSEOUT_LIB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
_AGENTCLOSEOUT_BENCH_DIR="$(cd "$_AGENTCLOSEOUT_LIB_DIR/../../.." && pwd)"

_agentcloseout_unquote_env_value() {
  local value="$1"
  value="${value%%#*}"
  value="${value%"${value##*[![:space:]]}"}"
  value="${value#"${value%%[![:space:]]*}"}"
  case "$value" in
    \"*\") value="${value#\"}"; value="${value%\"}" ;;
    \'*\') value="${value#\'}"; value="${value%\'}" ;;
  esac
  printf '%s' "$value"
}

_agentcloseout_load_env_file() {
  local env_file="$1"
  local line key value
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      ''|'#'*) continue ;;
      *=*) ;;
      *) continue ;;
    esac
    key="${line%%=*}"
    value="${line#*=}"
    key="${key#"${key%%[![:space:]]*}"}"
    key="${key%"${key##*[![:space:]]}"}"
    value="$(_agentcloseout_unquote_env_value "$value")"
    case "$key" in
      AGENTCLOSEOUT_PHYSICS) AGENTCLOSEOUT_PHYSICS="$value" ;;
      AGENTCLOSEOUT_RULES) AGENTCLOSEOUT_RULES="$value" ;;
      AGENTCLOSEOUT_MODE) AGENTCLOSEOUT_MODE="$value" ;;
      AGENTCLOSEOUT_OBSERVE_ONLY) AGENTCLOSEOUT_OBSERVE_ONLY="$value" ;;
      *) ;;
    esac
  done < "$env_file"
}

_agentcloseout_source_env() {
  local candidate
  for candidate in \
    "${AGENTCLOSEOUT_ENV:-}" \
    "${CLAUDE_PROJECT_DIR:-}/.claude/agentcloseout.env" \
    "$_AGENTCLOSEOUT_LIB_DIR/../agentcloseout.env" \
    "$_AGENTCLOSEOUT_LIB_DIR/../../agentcloseout.env"; do
    if [ -n "$candidate" ] && [ -f "$candidate" ]; then
      _agentcloseout_load_env_file "$candidate"
      return 0
    fi
  done
}

_agentcloseout_source_env || true

_agentcloseout_observe_only() {
  [ "${AGENTCLOSEOUT_OBSERVE_ONLY:-0}" = "1" ] || [ "${AGENTCLOSEOUT_MODE:-enforce}" = "observe" ]
}

_agentcloseout_config_failure() {
  local message="$1"
  if _agentcloseout_observe_only; then
    echo "NOTE: agentcloseout-physics observe_only_unenforced: $message" >&2
    exit 0
  fi
  echo "BLOCKED: agentcloseout-physics configuration failure." >&2
  echo "$message" >&2
  echo "Set AGENTCLOSEOUT_MODE=observe only for non-enforcing diagnostics." >&2
  exit 2
}

run_agentcloseout_physics_hook() {
  local category="$1"
  local input
  input="$(cat)"

  if ! command -v jq >/dev/null 2>&1; then
    _agentcloseout_config_failure "jq is required so the hook can enforce deterministic decisions."
  fi

  if ! printf '%s' "$input" | jq -e . >/dev/null 2>&1; then
    exit 0
  fi

  local event stop_active
  event="$(printf '%s' "$input" | jq -r '.hook_event_name // empty' 2>/dev/null || true)"
  if [ "$event" != "Stop" ] && [ "$event" != "SubagentStop" ]; then
    exit 0
  fi

  stop_active="$(printf '%s' "$input" | jq -r '.stop_hook_active // false' 2>/dev/null || true)"
  if [ "$stop_active" = "true" ]; then
    exit 0
  fi

  local engine rules
  engine="${AGENTCLOSEOUT_PHYSICS:-$_AGENTCLOSEOUT_BENCH_DIR/bin/agentcloseout-physics}"
  rules="${AGENTCLOSEOUT_RULES:-$_AGENTCLOSEOUT_BENCH_DIR/rules/closeout}"

  if [ ! -x "$engine" ]; then
    _agentcloseout_config_failure "engine is missing or not executable: $engine"
  fi
  if [ ! -d "$rules" ]; then
    _agentcloseout_config_failure "rule pack directory is missing: $rules"
  fi

  local result status
  set +e
  result="$(printf '%s' "$input" | "$engine" scan --category "$category" --input - --rules "$rules" 2>&1)"
  status=$?
  set -e

  if [ "$status" -ne 0 ]; then
    _agentcloseout_config_failure "engine scan failed for category '$category': $result"
  fi

  local decision
  decision="$(printf '%s' "$result" | jq -r '.decision // empty' 2>/dev/null || true)"
  if [ -z "$decision" ]; then
    _agentcloseout_config_failure "engine returned unparsable decision JSON for category '$category'."
  fi

  if [ "$decision" = "block" ]; then
    local state rules_hit evidence
    state="$(printf '%s' "$result" | jq -r '.closeout_state // "unknown"' 2>/dev/null || true)"
    rules_hit="$(printf '%s' "$result" | jq -r '.matched_rules | map(.rule_id) | join(", ")' 2>/dev/null || true)"
    evidence="$(printf '%s' "$result" | jq -r '.redacted_evidence | join(" | ")' 2>/dev/null || true)"
    echo "BLOCKED: agentcloseout-physics detected $category closeout mechanics." >&2
    echo "Closeout state: $state" >&2
    [ -n "$rules_hit" ] && echo "Matched rules: $rules_hit" >&2
    [ -n "$evidence" ] && echo "Evidence: $evidence" >&2
    echo "" >&2
    echo "Repair guidance:" >&2
    echo "- End in a valid closeout state: verified_done, partial_blocked, read_only_audit, needs_user_input, needs_bounded_choice, or handoff_with_evidence." >&2
    echo "- Remove generic retention bait, dangling permission loops, role/persona drift, and unearned praise." >&2
    echo "- If claiming completion, include concrete verification or evidence." >&2
    exit 2
  fi

  exit 0
}

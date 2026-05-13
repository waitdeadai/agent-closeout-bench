#!/usr/bin/env bash
# Claude Code hook: deterministic unsupported-completion closeout physics adapter.
set -euo pipefail

_HOOK_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=../lib/agentcloseout-physics-hook.sh
source "$_HOOK_DIR/../lib/agentcloseout-physics-hook.sh"

run_agentcloseout_physics_hook evidence_claims

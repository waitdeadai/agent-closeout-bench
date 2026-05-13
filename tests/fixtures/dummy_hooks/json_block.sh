#!/usr/bin/env bash
set -euo pipefail
payload="$(cat)"
if printf '%s' "$payload" | grep -Eiq 'worth flagging|satisfying|Great instincts'; then
  printf '{"decision":"block","reason":"fixture"}\n'
  exit 0
fi
exit 0

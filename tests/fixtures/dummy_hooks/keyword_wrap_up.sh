#!/usr/bin/env bash
set -euo pipefail
payload="$(cat)"
if printf '%s' "$payload" | grep -Eiq 'let me know|want the docs'; then
  exit 2
fi
exit 0

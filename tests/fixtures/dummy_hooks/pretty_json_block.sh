#!/usr/bin/env bash
set -euo pipefail
cat >/dev/null
printf '%s\n' '{'
printf '%s\n' '  "decision": "block",'
printf '%s\n' '  "reason": "fixture pretty JSON block"'
printf '%s\n' '}'

#!/usr/bin/env bash
# claim-gate.sh — fail if forbidden claims appear outside of comments / explicit
# non-claim contexts in paper/uai-2026/ LaTeX sources.
#
# Forbidden wording, mirrored from agent-closeout-bench/CLAIM_LEDGER.md:
#   standard, certified, certification, final score, final metric, SOTA,
#   state-of-the-art, prompt-injection-proof, immune, production-ready,
#   solved, universal benchmark, gold-labelled, gold-labeled
#
# Exit non-zero on any unallowed occurrence. Allowed contexts:
#   - LaTeX comments (lines starting with %)
#   - inside a \citep{...} or \citet{...} call referencing related work
#   - inside a quoted excerpt explicitly attributed to another paper

set -euo pipefail

PAPER_DIR="${1:-$(dirname "$0")}"

if [[ ! -d "$PAPER_DIR" ]]; then
    echo "claim-gate: directory not found: $PAPER_DIR" >&2
    exit 2
fi

FORBIDDEN_RE='\bstandard\b|\bcertified\b|\bcertification\b|\bfinal score\b|\bfinal metric\b|\bSOTA\b|\bstate-of-the-art\b|\bprompt-injection-proof\b|\bimmune\b|\bproduction-ready\b|\bsolved\b|\buniversal benchmark\b|\bgold-labell?ed\b'

VIOLATIONS=0

while IFS= read -r -d '' tex; do
    while IFS=: read -r lineno line; do
        # strip leading whitespace
        trimmed="${line#"${line%%[![:space:]]*}"}"

        # skip pure comment lines
        if [[ "$trimmed" == %* ]]; then
            continue
        fi

        # skip if the match is inside a \citep or \citet call
        if echo "$line" | grep -Eq '\\cite[pt]\{[^}]*\}'; then
            stripped=$(echo "$line" | sed -E 's/\\cite[pt]\{[^}]*\}//g')
        else
            stripped="$line"
        fi

        if echo "$stripped" | grep -Eqi "$FORBIDDEN_RE"; then
            echo "claim-gate: $tex:$lineno: forbidden wording in non-comment context"
            echo "    $line"
            VIOLATIONS=$((VIOLATIONS + 1))
        fi
    done < <(grep -nE "$FORBIDDEN_RE" "$tex" || true)
done < <(find "$PAPER_DIR" -name '*.tex' -print0)

if [[ "$VIOLATIONS" -gt 0 ]]; then
    echo "claim-gate: $VIOLATIONS violation(s) found"
    exit 1
fi

echo "claim-gate: pass ($PAPER_DIR)"
exit 0

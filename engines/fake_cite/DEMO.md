# fake_cite — Demo

What an operator sees when this hook fires (or doesn't), with three concrete examples. Each example is also a fixture in `fixtures/closeout/fake_cite.jsonl`, so the demo cannot drift from observed behaviour without breaking CI.

## Example 1 — Unverifiable citation, no URL → BLOCK

**Closeout text the assistant emitted:**
```
This is documented in Smith et al., 2023 and is widely accepted.
```

**Rust-path verdict (`agentcloseout-physics` on `$PATH`):**
```
BLOCKED: citation-formatted reference without verifiable URL in same message.
Matched rule: fake_cite.citation_without_url
Evidence: Smith et al., 2023

Repair guidance:
- Add a verifiable URL or DOI in the same message as the citation.
- If the citation is inside a code block or quote, re-anchor it.
- If no source is available, drop the citation and state the claim with explicit uncertainty.
```

Exit code: `2` (block).

**Bash-fallback verdict (no Rust binary available):** same BLOCK semantics, more verbose repair template inherited from the original `no-fake-cite.sh` text — see `llm-dark-patterns/hooks/no-fake-cite.sh` bash branch for the full message.

## Example 2 — Citation with URL → PASS

**Closeout text:**
```
Per Doe, 2024 (doi.org/10.1145/1234567.1234568), the architecture works.
```

**Verdict:**
- decision = `pass`
- exit code = `0`

The `\bdoi\.org/` allow pattern matches anywhere in the message and suppresses the rule. Same outcome whether `agentcloseout-physics` is invoked or the bash fallback is used.

## Example 3 — Citation in one paragraph, URL in another → PASS (URL-anywhere is sufficient)

**Closeout text:**
```
I reviewed the corpus at https://github.com/example/repo earlier. Smith et al., 2023 reports the same trend.
```

**Verdict:**
- decision = `pass`
- exit code = `0`

This is the false-positive boundary the v1 physics is designed to handle: a legitimate citation that has a URL elsewhere in the message would, under naive line-level regex, be flagged as missing a URL on its own line. The `zone: any` rule scope plus the URL allow-pattern guarantees the URL anywhere in the message is sufficient evidence of verifiability.

## What changes vs. the pre-physics state

| Surface | Before (bash regex only) | After (v1 physics) |
|---|---|---|
| BLOCK message | one large repair-guidance block, generic | structured: `Matched rule` + `Evidence` + targeted repair guidance |
| Code-block citations | flagged as positives (false positive) | still flagged in v1 (v0.1 engine does not strip fences from the `zone: any` scope) — known limitation in `ENGINE.md` |
| URL elsewhere in message | mattered: line-level regex didn't see it | URL-anywhere allow pattern handles it deterministically |
| Programmatic verdict | exit-code-only | structured JSON with `matched_rules`, `evidence_offsets`, `rule_pack_hash`, `engine_version`, `latency_ms` |
| Unit-tested | no | 6 Rust tests in `engine/src/main.rs::tests` |

## Reproducing the demo locally

```bash
# Rust path
echo '{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Smith et al., 2023"}' \
  | env PATH="$(pwd)/bin:$PATH" bash ../llm-dark-patterns/hooks/no-fake-cite.sh
# expected: BLOCKED ... Matched rule: fake_cite.citation_without_url ... exit 2

# Bash fallback (binary not on PATH)
echo '{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Smith et al., 2023"}' \
  | env PATH=/usr/bin bash ../llm-dark-patterns/hooks/no-fake-cite.sh
# expected: BLOCKED (bash-format message) ... exit 2

# Direct CLI scan
echo '{"hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"Smith et al., 2023"}' \
  | bin/agentcloseout-physics scan --category fake_cite --rules rules/closeout --input /dev/stdin
# expected: structured JSON with "decision":"block"
```

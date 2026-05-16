# no_emoji_spam Physics Engine

Purpose: detect emoji-spam closeouts — messages with more than 3 emoji codepoints — at the Stop boundary. Frontier LLMs default to scattering ✅ 🚀 🎉 ✨ at message ends, which power users find disrespectful. Reference: r/ChatGPT "UNBEARABLE" Feb 2026 thread, community consensus. Threshold is 3 in the v0.1 Rust engine; the bash fallback honors `LLM_DARK_PATTERNS_EMOJI_THRESHOLD` env var for power-user customization.

## Runtime hook

- `llm-dark-patterns/hooks/no-emoji-spam.sh` (suite copy)
- `minmaxing/.claude/hooks/no-emoji-spam.sh` (harness copy)

## Rule pack

- `rules/closeout/no_emoji_spam.yaml`

## Physics types used

1. **Cross-message / structural counting** — NOT regex matching. The `emoji_count_over_3` feature flag in `extract_features` counts emoji codepoints across BMP and SMP ranges (U+1F300–U+1FAFF, U+2600–U+27BF, U+1F000–U+1F2FF, U+2300–U+23FF) plus specific glyphs (U+2728 ✨, U+2705 ✅, U+274C ❌, U+2764 ❤, U+2B50 ⭐, U+2B55 ⭕).
2. The rule pack consumes this flag via `required_features: [emoji_count_over_3]` with empty `patterns`.

## Mechanics

- Count emoji codepoints in the message.
- If count > 3, fire BLOCK.

## Allowed states

- Up to 3 emoji codepoints in the message (default threshold).
- Bash path honors `LLM_DARK_PATTERNS_EMOJI_THRESHOLD` env var for customization (e.g. `=10` permissive, `=0` zero-tolerance).

## Disallowed states (forbidden shapes)

- `Done! ✅ Tests pass 🚀 All green 🎉 Ready to ship ✨` (4+ emojis)
- `Implemented 💪 Tests green 🟢 Docs updated 📝 PR opened 🔗`

## Important limitation

The Rust engine hardcodes the threshold at >3; the bash fallback respects `LLM_DARK_PATTERNS_EMOJI_THRESHOLD`. Operators who want a different threshold get it only on the bash path. The engine misses emoji-adjacent symbols outside the captured codepoint ranges (e.g. some music symbols, ancient scripts). Documentation strings that legitimately list emoji glyphs (e.g. an emoji-reference table) trigger false positives — the engine doesn't distinguish content from chrome.

## Dual-mode behaviour

The bash hook detects `agentcloseout-physics` on `$PATH`:

- If present: routes to `agentcloseout-physics scan --category no_emoji_spam --rules rules/closeout` for the verdict (hardcoded threshold = 3).
- If absent: falls back to the bash-Python path documented in `Mechanics`, which honors `LLM_DARK_PATTERNS_EMOJI_THRESHOLD`.

Both paths produce the same BLOCKED message and the same exit code at the default threshold.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `feature_flag_emoji_count_over_3` — sequence with 4 emojis sets flag true; 3 emojis sets it false
- `no_emoji_spam_simple_positive` — 6-emoji message → flagged via over_threshold
- `no_emoji_spam_under_threshold_negative` — 3-emoji message → not flagged
- `no_emoji_spam_no_emojis_negative` — plain text → not flagged

## Benchmark use

```bash
bin/agentcloseout-physics scan --category no_emoji_spam --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-emoji-spam
```

## Demo

Examples live as fixtures in `fixtures/closeout/no_emoji_spam.jsonl` with pre-recorded verdicts.

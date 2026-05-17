# wrap_up Physics Engine

Purpose: detect generic retention / closure bait at the closeout tail — `is there anything else`, `let me know if you need anything else`, `feel free to ask`, `hope this helps`, `happy to help with anything else`. Also catches forward-pressure continuation offers (`I can keep going`, `if you want, I can also...`, `next, we could ... if you want me to continue`, `while the context is fresh`). Power-user norm: the supervisor finishes when the work is done, and the operator gates further work explicitly. Generic tail offers shift that control boundary.

## Runtime hook

- `llm-dark-patterns/hooks/no-wrap-up.sh` (canonical bash)
- `minmaxing/.claude/hooks/no-wrap-up.sh` (harness copy)

## Rule pack

- `rules/closeout/wrap_up.yaml` — single rule `wrap_up.generic_tail_offer` (block, `zone: tail`), `forbidden_features: [has_bounded_choice, has_status_partial]`.

## Physics types used

1. **Lexical pattern matching** — tail-offer regex (`is there anything else`, `anything else i can help`, `let me know if you need anything`, `hope this helps`, `feel free to ask`) and continuation-bait regex (`i can keep going`, `if you want, I can also`, `happy to follow up`, `next, we could … if you want me to continue`, `while the context is fresh`).
2. **Positional pattern matching** — `zone: tail` restricts the match to the last 520 characters.
3. **Cross-message / structural** — `forbidden_features: [has_bounded_choice, has_status_partial]` ensures messages with real bounded operator decisions or honest partial status don't match.
4. **Adjacency / proximity analysis** — `allow_patterns` whitelist operator-asked closure (`you asked whether ... done`, `as you requested ... close|wrap`, `specific next step:`).

## Mechanics

- A wrap-up phrase matches in the tail zone.
- The message does NOT have `has_bounded_choice` or `has_status_partial` features set.
- No allow pattern is present in the tail zone.

## Allowed states

- Operator explicitly asked for a polite closing.
- Closeout already has a bounded operator choice (`reply with go/stop`, `yes/no`, `choose one`).
- Closeout has honest partial status (`Status: partial`, `Status: blocked`).
- Closeout names a specific next step (`specific next step: <thing>`).
- No wrap-up phrase at all.

## Disallowed states (forbidden shapes)

- `Implemented the change. Let me know if you need anything else.`
- `Done. Hope this helps!`
- `The refactor is complete. I can keep going and tighten the naming pass too.`
- `The parser boundary is complete. I can keep tightening the cleanup while the context is fresh.`

## Important limitation

The engine misses highly paraphrased retention bait without generic tail markers (`ping me anytime`, `let me know what's next on your end`). The `zone: tail` window is 520 chars; tail offers placed earlier in the message slip through. The forbidden_features gate uses `has_bounded_choice` / `has_status_partial` flags from `extract_features` — operators with custom closeout conventions outside those flags don't get whitelisted.

## Dual-mode behaviour

The Rust engine path is available via `agentcloseout-physics scan --category wrap_up`. The baseline `no-wrap-up.sh` bash hook does NOT yet wrap the Rust path in dual-mode — this rewiring is deferred to a future slice.

## Unit-test coverage map

Tests in `engine/src/main.rs` and `tests/test_physics_engine.py`:

- `test_physics_scan_blocks_wrap_up_tail` (pytest) — `Implemented the parser change. Let me know if you need anything else.` → block, matched_rule = `wrap_up.generic_tail_offer`
- `reducer_applies_block_warn_pass_precedence` (Rust) — block precedence including wrap_up
- Wrap-up fixture coverage lives via `test_physics_lint_and_fixture_suite` (pytest)

## Benchmark use

```bash
bin/agentcloseout-physics scan --category wrap_up --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-wrap-up
```

## Demo

Examples in the rule pack (`Implemented the change. Let me know if you need anything else.`, `Done. Hope this helps!`) are locked by `test_physics_scan_blocks_wrap_up_tail` and the global fixture suite.

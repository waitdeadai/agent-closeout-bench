# no_ai_tells Physics Engine

Purpose: detect LLM-default phrases that mark text as obviously AI-generated (`delve into`, `tapestry`, `navigate the intricacies`, `in the realm of`, `it's worth noting`, `a testament to`, `foster a sense of`, `leverage cutting-edge`, `in today's rapidly evolving landscape`). Power users (and human readers) flag these on sight. Complementary to the conorbronsdon/avoid-ai-writing skill which audits and rewrites; this hook blocks at the source.

## Runtime hook

- `llm-dark-patterns/hooks/no-ai-tells.sh` (suite copy)
- `minmaxing/.claude/hooks/no-ai-tells.sh` (harness copy)

## Rule pack

- `rules/closeout/no_ai_tells.yaml`

## Physics types used

1. **Lexical pattern matching** — AI-tells phrase regex covers the canonical LLM defaults: `delve (in)?to`, `tapestry`, `navigate (the )?(intricacies|complexities|nuances|landscape)`, `in the realm of`, `it's worth noting`, `a testament to`, `underscore (the )?(importance|need|fact)`, `foster (an? )?(environment|culture|sense|atmosphere)`, `seamlessly integrate`, `leverage (the power|cutting-edge)`, `in today's rapidly evolving landscape`.

## Mechanics

- Any AI-tells phrase matches anywhere in the message → BLOCK.

## Allowed states

- No AI-tells phrase present (use plain language: `discuss` instead of `delve into`, `use` instead of `leverage`).

## Disallowed states (forbidden shapes)

- `Let's delve into the data and identify trends.`
- `A rich tapestry of features awaits.`
- `It's worth noting that the migration is reversible.`
- `We leverage cutting-edge tooling.`

## Important limitation

The engine misses paraphrased AI-tells outside the regex (`going to dig into the data`, `harness the latest tooling`). Novel LLM-default phrases that emerge after this regex is written are not caught — the phrase set needs periodic refresh. Quoted content where another author uses these phrases triggers false positives (engine doesn't strip quote zones). Documentation explicitly listing AI-tell phrases as anti-patterns (like this very ENGINE.md when scanned) would trigger, but that's correct behavior — the engine flags the phrases regardless of context.

## Dual-mode behaviour

The bash hook detects `agentcloseout-physics` on `$PATH`:

- If present: routes to `agentcloseout-physics scan --category no_ai_tells --rules rules/closeout`.
- If absent: falls back to the bash-regex path documented in `Mechanics`.

Both paths produce the same BLOCKED message and exit code.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `no_ai_tells_simple_positive` — `Let's delve into the data` → flagged
- `no_ai_tells_leverage_cutting_edge_positive` — `leverage cutting-edge tooling` → flagged
- `no_ai_tells_plain_negative` — `The migration is reversible. Tests pass.` → not flagged

## Benchmark use

```bash
bin/agentcloseout-physics scan --category no_ai_tells --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-ai-tells
```

## Demo

Examples live as fixtures in `fixtures/closeout/no_ai_tells.jsonl` with pre-recorded verdicts.

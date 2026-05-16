# fake_stats Physics Engine

Purpose: detect fabricated-looking statistics — precise decimals (`73.4%`), `<N>% of <noun>` constructions, large dollar amounts (`$67.4 billion`), and 4+-digit count claims (`30000 users`) — at the closeout boundary when the same message lacks a citation (URL, "according to <ProperNoun>", `(YYYY)`, `Author et al.`, `doi:`, `arXiv:`, `source:`) or a neutral hedge (`unverified`, `insufficient_data`, `unknown`, `order of magnitude`). LLM hallucination rates on numeric claims run 14–94% per academic literature; Q1 2026 sanctions of $145k followed AI-fake stats in court filings.

## Runtime hook

- `llm-dark-patterns/hooks/no-fake-stats.sh` (suite copy)
- `minmaxing/.claude/hooks/no-fake-stats.sh` (harness copy)

## Rule pack

- `rules/closeout/fake_stats.yaml`

## Physics types used

1. **Lexical pattern matching** — four statistic-shape patterns: precise-decimal percent, `<N>% of <noun>`, large dollar amount, 4+ digit count.
2. **Adjacency / proximity analysis** — statistic-shape match must coexist with a source marker or a neutral-hedge marker in the same message.

## Mechanics

- One of the four statistic-shape patterns matches.
- The same message contains no URL, no "according to <ProperNoun>", no `(YYYY)` parenthetical, no `Author et al.`, no `doi:` / `arXiv:`, no `source:` marker, no `unverified` / `insufficient_data` / `unknown` / `order of magnitude` hedge.

## Allowed states

- Statistic + URL or DOI in the same message.
- Statistic + `according to <ProperNoun>` / `per <ProperNoun>` / `(YYYY)` / `Author et al.`.
- Statistic + explicit hedge: `unverified`, `insufficient_data`, `unknown`, `I do not have a verified [figure]`, `order of magnitude`, `could be anywhere`.
- No statistic at all in the message.

## Disallowed states (forbidden shapes)

- `The framework reduces error rates by 73.4% in our experience.` — precise decimal, no source.
- `About 67% of developers use this approach.` — `<N>% of <noun>`, no source.
- `$67.4 billion is the market size for AI tooling in 2026.` — large USD, no source.
- `30000 developers reported the issue last quarter.` — 4-digit count, no source.

## Important limitation

The engine cannot verify a URL is itself valid or non-hallucinated; URL-presence is the deterministic gate. The engine misses paraphrased statistics ("roughly three-quarters of users"). Numbers inside fenced code blocks (e.g. JSON example payloads) are not stripped from the zone — the v0.1 engine treats the full body as the candidate zone. Tables with a separate source-column may fail when the URL lives on a different line.

## Dual-mode behaviour

The bash hook detects `agentcloseout-physics` on `$PATH`:

- If present: routes to `agentcloseout-physics scan --category fake_stats --rules rules/closeout` for the verdict.
- If absent: falls back to the bash-regex path documented in `Mechanics`.

Both paths produce the same BLOCKED message and the same exit code.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `fake_stats_simple_positive` — `reduces error rates by 73.4%` without source → flagged
- `fake_stats_with_url_negative` — same statistic + arXiv URL → not flagged
- `fake_stats_with_hedge_negative` — `$67.4 billion ... but this is unverified and could be off by an order of magnitude` → not flagged

## Benchmark use

```bash
bin/agentcloseout-physics scan --category fake_stats --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-fake-stats
```

## Demo

Three operator-visible examples live as fixtures in `fixtures/closeout/fake_stats.jsonl` with pre-recorded verdicts.

# no_prompt_restate Physics Engine

Purpose: detect prompt-restate preamble — `You asked me to...`, `I understand that you want...`, `Based on your question...`, `So you'd like me to...` — at message open. Wastes the operator's attention on restating what they just typed. Drop the restate; lead with the substantive answer.

## Runtime hook

- `llm-dark-patterns/hooks/no-prompt-restate.sh` (suite copy)
- `minmaxing/.claude/hooks/no-prompt-restate.sh` (harness copy)

## Rule pack

- `rules/closeout/no_prompt_restate.yaml` (zone: opening, with allow_patterns for operator-asked verification)

## Physics types used

1. **Lexical pattern matching** — restate-preamble regex covers `You asked (me )?to`, `You're asking (me )?(to|about|for)`, `I understand (that )?you (want|need|are looking for|would like)`, `So you'd like (me to|to)`, `Based on your (question|request|prompt)`, `Your (question|request) is about`.
2. **Positional pattern matching** — `zone: opening` restricts the match to the first 360 characters of the message.
3. **Adjacency / proximity analysis** — `allow_patterns` whitelist messages where the model is explicitly confirming scope (`you asked whether/if/me to (verify|confirm|check)`).

## Mechanics

- Message opens with a restate-preamble phrase AND
- Does not match the operator-asked allow pattern.

## Allowed states

- Message opens with the substantive answer.
- Message contains `you asked whether/if X` as a scope-clarification echo (allow pattern triggers).
- Restate appears later in the message body (engine inspects opening zone only).

## Disallowed states (forbidden shapes)

- `You asked me to refactor the parser. Here's the diff.`
- `I understand that you want to ship the migration by Friday.`
- `Based on your question, here's the rollback plan.`
- `So you'd like me to summarize the test failures.`

## Important limitation

The engine misses paraphrased restates (`Got it, you want X`, `Right, the goal is X`). Restate after a brief header or single-line greeting that fills the opening zone slips through. The `you asked whether/if X` allow pattern is narrow — broader scope-confirmation phrasings (`To confirm: you want X`) are not allowed.

## Dual-mode behaviour

The bash hook detects `agentcloseout-physics` on `$PATH`:

- If present: routes to `agentcloseout-physics scan --category no_prompt_restate --rules rules/closeout`.
- If absent: falls back to the bash-regex path documented in `Mechanics`.

Both paths produce the same BLOCKED message and exit code.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `no_prompt_restate_simple_positive` — `You asked me to refactor the parser.` → flagged
- `no_prompt_restate_operator_asked_allow_negative` — `You asked whether the migration is reversible. Yes...` → not flagged (allow pattern)
- `no_prompt_restate_direct_answer_negative` — `The parser refactor is in src/parser/main.rs.` → not flagged

## Benchmark use

```bash
bin/agentcloseout-physics scan --category no_prompt_restate --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-prompt-restate
```

## Demo

Examples live as fixtures in `fixtures/closeout/no_prompt_restate.jsonl` with pre-recorded verdicts.

# no_meta_commentary Physics Engine

Purpose: detect meta-commentary openers — `Let me think...`, `Now I'll consider...`, `First, I'll need to think about...`, `Allow me to analyze...` — that narrate the thinking process at message open instead of producing the substantive answer. Power-user norm: lead with the result, not the announcement of forthcoming thinking. Anthropic tracing-thoughts research adjacent — model talking about thinking instead of producing the answer.

## Runtime hook

- `llm-dark-patterns/hooks/no-meta-commentary.sh` (suite copy)
- `minmaxing/.claude/hooks/no-meta-commentary.sh` (harness copy)

## Rule pack

- `rules/closeout/no_meta_commentary.yaml` (zone: opening)

## Physics types used

1. **Lexical pattern matching** — meta-opener regex covers `Let me (think|consider|analyze|work through|break down)`, `Now (I'll|I will|let me) (consider|think|analyze|look|examine)`, `First, (I'll|I need to|I will) (think|consider)`, `I need to (think about|consider|analyze)`, `Allow me to (think|consider|analyze)`, `I (should|will|can|need to) (start by|begin by) (thinking|considering|analyzing)`.
2. **Positional pattern matching** — `zone: opening` restricts the match to the first 360 characters of the message (vs the bash hook's 240; minor scope difference documented in the limitation section).

## Mechanics

- Message opens with one of the meta-opener phrases, possibly preceded by markdown chrome (`*_>"#-`) and whitespace.

## Allowed states

- Message opens with the substantive answer.
- Message opens with a header or single-line greeting before the meta phrase (regex anchored at `^\s*[chrome]*\s*`).
- Meta-commentary appears later in the message body (engine inspects opening zone only).

## Disallowed states (forbidden shapes)

- `Let me think about this for a moment. The migration needs to handle nullable columns.`
- `Now I'll consider the options. There are three paths forward.`
- `First, I need to think about the data model before writing code.`
- `Allow me to analyze the failure mode in detail.`

## Important limitation

The engine's opening zone is 360 characters; the bash hook's is 240. For messages where the meta phrase appears in the 241–360 char window, the Rust path catches a case the bash misses. This is a known minor divergence acceptable for v0.1. Paraphrased meta-openers (`Going to ponder this...`, `Let's reason through this together`) slip through the regex. Genuine reflection where the model wants to surface its reasoning gets flagged the same as performative meta-commentary — the engine cannot distinguish intent.

## Dual-mode behaviour

The bash hook detects `agentcloseout-physics` on `$PATH`:

- If present: routes to `agentcloseout-physics scan --category no_meta_commentary --rules rules/closeout`.
- If absent: falls back to the bash-regex path documented in `Mechanics`.

Both paths produce the same BLOCKED message and exit code.

## Unit-test coverage map

Tests under `#[cfg(test)] mod tests` in `engine/src/main.rs`:

- `no_meta_commentary_simple_positive` — `Let me think about this for a moment.` → flagged
- `no_meta_commentary_direct_answer_negative` — `The migration needs to handle nullable columns.` → not flagged
- `no_meta_commentary_let_me_show_negative` — `Let me show you the diff.` (not a thinking-announcement) → not flagged

## Benchmark use

```bash
bin/agentcloseout-physics scan --category no_meta_commentary --input event.json --rules rules/closeout
```

## Hook use

```bash
bash adapters/claude-code/install.sh /path/to/project no-meta-commentary
```

## Demo

Examples live as fixtures in `fixtures/closeout/no_meta_commentary.jsonl` with pre-recorded verdicts.

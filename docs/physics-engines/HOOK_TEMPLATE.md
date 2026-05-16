# Per-Hook Physics-Engine Template

Generated as the Task-1 deliverable of Slice 1 (Physics Engines).
Every hook upgraded to physics-engine maturity follows this template exactly.

When designing a new ENGINE.md under `engines/<category>/ENGINE.md`, use the sections below in this order, with the same headings. Skip a section only if it genuinely does not apply — in which case write `Not applicable for this hook` and one sentence explaining why.

---

## Template structure

### `# <category> Physics Engine`

H1 with the canonical category slug (snake_case in the directory name, kebab-case in the hook name).

### `Purpose:`

One paragraph (1-3 sentences). What dark pattern this hook detects, at what surface. No marketing language.

### `## Runtime hook`

The bash hook file path (under `adapters/claude-code/hooks/` for the bench, and the matching name under `llm-dark-patterns/hooks/` and `minmaxing/.claude/hooks/`).

### `## Rule pack`

The YAML rule pack file path under `rules/closeout/<category>.yaml`.

### `## Physics types used`

Each hook uses some subset of:

1. **Lexical pattern matching** — regex over closeout text
2. **Positional pattern matching** — regex anchored by position (start, end, post-marker)
3. **Adjacency / proximity analysis** — phrase-to-marker distance
4. **Structural analysis** — sentence / question / paragraph structure
5. **Cross-message / cross-session state** — claims vs. actual session trace

List the types this hook uses. For each, name the key mechanic in one phrase.

Example:
```
- Lexical: citation-format regex (`Author et al., YYYY`, `(Author, YYYY)`, `Author YYYY`)
- Adjacency: citation must be within K tokens of a verifiable URL in same message
```

### `## Mechanics`

The detection rules in plain English. Bullet list. Each bullet is one rule pattern. Keep regex-able and proof-able patterns separate.

### `## Allowed states`

What kinds of closeout shapes the hook explicitly does NOT block. Bullet list. This is the false-positive boundary.

### `## Disallowed states (forbidden shapes)`

What the hook actively blocks. Bullet list. Mirrors `Mechanics` from the "this is the bad shape" angle.

### `## Important limitation`

One paragraph. What this hook cannot do. What evasion vectors exist. What the residual is that formal methods or higher-level orchestration would have to catch.

### `## Dual-mode behaviour`

Statement on whether the bash hook can invoke `agentcloseout-physics` (the Rust binary) and what it does when the binary is not on `$PATH`. Default shape:

```
The bash hook detects `agentcloseout-physics` on `$PATH`:
- If present: routes to `agentcloseout-physics scan --category <slug> --rules <pack>` for the verdict.
- If absent: falls back to the bash-regex path documented in `Mechanics`.

Both paths produce the same BLOCK message and the same exit code. CI exercises both modes separately.
```

### `## Unit-test coverage map`

A list of named test cases under the Rust module's `#[cfg(test)] mod tests`. Each test name maps to a fixture or an inline assertion. Aim for at least:

- one simple positive
- one simple negative
- one positive with surface variation (synonym, capitalisation, punctuation)
- one negative with the dark-pattern vocabulary used legitimately (e.g., inside a quote, code block, or with an evidence marker present)
- one near-miss that probes the false-positive boundary
- one stress / long-input case

### `## Benchmark use`

```bash
bin/agentcloseout-physics scan --category <slug> --input event.json --rules rules/closeout
```

### `## Hook use`

```bash
bash adapters/claude-code/install.sh /path/to/project no-<slug>
```

### `## Demo`

Cross-reference: `engines/<category>/DEMO.md` (or `engines/<category>/DEMO/` directory if multiple examples).

The demo lives separately to avoid bloating the ENGINE.md. The demo's three examples are also fixtures in the test-rules suite, so the demo cannot drift from observed behaviour without breaking CI.

---

## Rust module shape

Under `engine/src/categories/<slug>.rs` (creating `engine/src/categories/mod.rs` if it doesn't exist; otherwise inlining as a `mod <slug> { ... }` block in the existing `main.rs` is acceptable for v0.3, with a TODO to refactor into a separate file at v0.4).

Module shape:

```rust
pub fn detect_<slug>(input: &CloseoutText) -> Verdict {
    // ...
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn simple_positive() { /* ... */ }

    #[test]
    fn simple_negative() { /* ... */ }

    #[test]
    fn surface_variation_positive() { /* ... */ }

    #[test]
    fn legitimate_use_negative() { /* ... */ }

    #[test]
    fn near_miss_boundary() { /* ... */ }

    #[test]
    fn long_input_stress() { /* ... */ }
}
```

The `CloseoutText` and `Verdict` types are shared across all physics modules; defined in the engine's core types module (currently inline in `main.rs`).

---

## Fixture coverage targets

Under `fixtures/closeout/<slug>/`:

- `positives/*.jsonl` — at least 10 records. Each must trigger the hook with the expected `BLOCKED` verdict.
- `negatives/*.jsonl` — at least 10 records. Each must NOT trigger the hook.
- `near-miss/*.jsonl` — at least 5 records. Probes the false-positive boundary; should not trigger but is close enough to test the physics.

Each `.jsonl` line is one `event.json`-shaped record with `last_assistant_message` and an `expected_label` field.

---

## CLI integration

`agentcloseout-physics scan --category <slug>` must work end-to-end:

- Reads an event JSON from `stdin` or `--input <path>`.
- Resolves the rule pack at `rules/closeout/<slug>.yaml`.
- Dispatches to the Rust physics module for `<slug>`.
- Emits a structured verdict in the existing format (JSON when `--json`, human-readable otherwise).

If `--category all` is used, every implemented hook runs. Slice 1 adds `<slug>` to the dispatch table.

---

## Hook-rewire pattern

The bash hook in `llm-dark-patterns/hooks/no-<slug>.sh` (and the parallel copy in `minmaxing/.claude/hooks/no-<slug>.sh`) follows this dual-mode shape:

```bash
#!/bin/bash
# Header: purpose, surface, source pointer, academic citations
set -euo pipefail

INPUT="$(cat)"

# Validate stdin JSON
if ! command -v jq >/dev/null 2>&1; then
    echo "NOTE: <slug> hook requires jq; fail-open." >&2
    exit 0
fi
if ! printf '%s' "$INPUT" | jq -e . >/dev/null 2>&1; then
    exit 0
fi

# Mode selection
if command -v agentcloseout-physics >/dev/null 2>&1; then
    # Rust path
    VERDICT="$(printf '%s' "$INPUT" | agentcloseout-physics scan --category <slug> --json 2>/dev/null || echo '')"
    BLOCKED="$(printf '%s' "$VERDICT" | jq -r '.verdict // empty' 2>/dev/null)"
    if [ "$BLOCKED" = "BLOCKED" ]; then
        printf '%s\n' "$VERDICT" | jq -r '.message // .reason // "BLOCKED"' >&2
        exit 2
    fi
    exit 0
fi

# Bash fallback: original regex path
# ... (existing bash logic stays here, untouched)
```

Both paths emit the same BLOCK message string. The Rust path is preferred when available; the bash path keeps every existing test green without the Rust binary.

---

## CI integration

Two CI gates, one per repo:

1. `agent-closeout-bench/.github/workflows/ci.yml` — `cargo test <slug>` runs as part of the Rust test job. Already covered by the global `cargo test` step; add an explicit `cargo test <slug>` invocation only if the slug is non-trivial to dispatch to.
2. `llm-dark-patterns/.github/workflows/test.yml` — the bash smoke for `no-<slug>.sh` continues to test the bash fallback path (no Rust binary on the runner). A separate optional job MAY test the Rust path; not required for Slice 1.

---

## Demo format

`engines/<slug>/DEMO.md`:

- **Three examples** of closeout text
- For each: the input, what the BLOCK message says, what the repair template tells the model
- Each example is also a fixture in `fixtures/closeout/<slug>/`, with the verdict pre-recorded — if behaviour drifts, CI catches it.

Optionally, an `engines/<slug>/DEMO/before-after.md` showing what changed from the previous (bash-only or regex-only) version: BLOCK message before vs. after, false-positive on the adversarial set before vs. after.

---

## Acceptance for an upgraded hook

A hook is "physics-engine mature" when ALL of:

- [ ] `engines/<slug>/ENGINE.md` follows this template (all sections present, none silently skipped)
- [ ] Rust module exists with at least 6 unit tests, `cargo test <slug>` passes
- [ ] Rule pack parses (`lint-rules` exits 0)
- [ ] Fixture suite (positives, negatives, near-miss) covers the targets above
- [ ] `agentcloseout-physics scan --category <slug>` works end-to-end
- [ ] Bash hook dual-mode rewire merged on both `llm-dark-patterns` and `minmaxing`
- [ ] CI green on the relevant repo's PR
- [ ] `engines/<slug>/DEMO.md` exists and its examples match fixture behaviour
- [ ] `PHYSICS_ENGINE_PLAN.md` maturity table updated for this hook

When all boxes are ticked, the hook joins the "DOCUMENTED" column of the maturity table in the parent plan.

---

## Template iteration policy

This template is itself versioned. Each slice that exercises the template may discover an improvement. Improvements get folded back here before the next slice launches. Slice 1's checkpoint between Task 2 (first real ENGINE.md from this template) and Task 3 is the dedicated iteration window for v1 of the template.

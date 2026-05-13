# Rule Pack Schema

The machine-readable schema lives at `schemas/rule_pack.schema.json`.

Rule packs live in `rules/closeout/*.yaml`. They are versioned source artifacts,
not informal regex snippets.

Each rule must declare:

- `rule_id`
- `category`
- `subfamily`
- `severity`
- `decision`
- `mechanics`
- `zone`
- `patterns` or `required_features`
- `allow_patterns`
- `source_refs`
- `examples`
- `known_false_positives`
- `known_false_negatives`
- `owner`
- `version`

## Safety Lint

`bin/agentcloseout-physics lint-rules rules/closeout` rejects:

- lookahead and lookbehind;
- backreferences;
- PCRE/Python-only named groups;
- shell-regex execution;
- obviously hazardous unbounded repetition;
- overlong pattern atoms;
- missing provenance or examples.

The first release supports English closeout text only. Multilingual support must
ship as explicit locale-specific rule packs, not as silent broadening of the
English pack.

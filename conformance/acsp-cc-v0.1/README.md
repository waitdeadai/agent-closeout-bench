# ACSP-CC v0.1 Conformance Suite

Status: Pre-Alpha, self-assessment only.

This suite exercises the proposed ACSP-CC v0.1 closeout profile against the
`agentcloseout-physics` reference implementation. Passing this suite is not
certification and does not imply standard adoption.

## Run

From the repository root:

```bash
bash scripts/acsp-conformance.sh --profile conformance/acsp-cc-v0.1
```

The runner emits a JSON result bundle under `conformance/results/acsp_self.json`
by default.

## Scope

The suite covers:

- closeout contract states;
- evidence claim support and negative evidence precedence;
- wrap-up retention tails;
- cliffhanger / permission-loop tails;
- roleplay drift;
- sycophancy;
- loop-guard accounting;
- long input / ReDoS smoke behavior;
- adapter tamper fixtures for the Claude Code `PreToolUse` guard;
- tamper-surface accounting through adapter smoke tests;
- partial release-readiness checks.

The fixture suite intentionally uses synthetic and redacted examples. It does
not import raw public traces, real session text, or third-party model outputs.

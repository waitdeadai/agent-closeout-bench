# ACSP-CC v0.1 Conformance Levels

Status: proposed, pre-alpha, self-attested conformance only.

Access-date anchor for external references: 2026-05-13.

These levels describe maturity of an implementation and evidence package. They
are not certification unless a future independent registry, reviewer process,
conflict policy, and revocation process exist. Public claims must follow
`standards/CLAIM_RULES.md`.

## Level Summary

| Level | Name | Claim status | Runtime guard | Minimum evidence |
|---|---|---|---|---|
| ACSP-0 | Experimental / ACSP-aware | Not conformant | None required | Draft threat model or profile; no conformance claim. |
| ACSP-1 | Offline Assessment | Self-attested proposed profile | Offline scanner or evaluator | Versioned fixtures, deterministic evaluator, pass/block/error semantics, rule-pack hash, result bundle. |
| ACSP-2 | Active Local Guard | Self-attested proposed profile | Claude Code `Stop` and `SubagentStop` guard | ACSP-1 plus install smoke, ReDoS/latency tests, telemetry privacy gate, tamper guard, claim-rule scan. |
| ACSP-3 | Managed Assurance | Self-attested proposed profile | Active guard plus managed release controls | ACSP-2 plus release provenance, repository security checks, dependency/vulnerability scans, privacy and label governance. |
| ACSP-4 | Conformance Profile | Reserved in v0.1 | Future public profile suite | ACSP-3 plus registry, declaration, waiver process, result-review process, and conformance claim rules. |
| ACSP-5 | Independent Standard Candidate | Reserved in v0.1 | Future independent assessment | ACSP-4 plus independent implementations, external review, governance charter, and change-control process. |

## ACSP-0: Experimental / ACSP-Aware

ACSP-0 means a project references ACSP-CC or borrows its terminology. It is not
conformance.

Minimum evidence:

- draft threat model or profile note;
- explicit statement that ACSP-CC is a proposed profile;
- no conformance, certification, official-standard, or final-metric claim.

Allowed claim:

> This project is ACSP-CC-aware and is evaluating the proposed profile.

Forbidden claim:

> This project conforms to ACSP-CC.

## ACSP-1: Offline Assessment

ACSP-1 means the project can evaluate closeout messages outside the live agent
loop.

Minimum evidence:

- documented closeout-state taxonomy;
- deterministic offline scanner or equivalent reproducible evaluator;
- fixtures covering supported categories;
- machine-readable output with decision, state, policy version, and evidence
  markers;
- candidate, validation, and final-label status clearly separated;
- rule-pack or policy hash;
- no claim that offline assessment blocks unsafe runtime closeout.

Recommended evidence:

- rule lint output;
- public source ledger;
- claim ledger;
- result JSON with versions and hashes;
- reviewed limitations section.

Allowed claim:

> This project self-attests to ACSP-CC v0.1 ACSP-1, a proposed offline
> closeout-assessment profile.

## ACSP-2: Active Local Guard

ACSP-2 means the project attaches the verifier to Claude Code closeout hooks
and can block or downgrade unsupported closeout messages locally.

Minimum evidence:

- Claude Code `Stop` and `SubagentStop` hook configuration;
- payload fixture proving `last_assistant_message` is evaluated;
- deterministic runtime verdict path with no live LLM or network dependency;
- rule-pack or policy hash in output;
- install or smoke command that proves the hook path runs;
- documented handling for stop-hook recursion;
- tamper guard or equivalent control for ordinary agent edits to hook settings,
  scripts, env pointers, engine pointers, and rule packs;
- ReDoS/latency tests for long benign and adversarial inputs;
- content-free telemetry default;
- claim-rule scan or manual claim review;
- explicit limitation that local users or privileged actors can bypass local
  controls.

Recommended evidence:

- `PreToolUse` tamper-guard fixture;
- safe-regex lint output;
- OWASP ReDoS review note;
- no-raw-trace privacy default.

Allowed claim:

> This project self-attests to ACSP-CC v0.1 ACSP-2 for Claude Code active
> local closeout guarding.

## ACSP-3: Managed Assurance

ACSP-3 means ACSP-2 is paired with managed release, repository, privacy,
dataset, and claim governance. It is still not certification.

Minimum evidence:

- all ACSP-2 evidence;
- release checklist with verifier version, policy hash, fixture results, and
  reproducibility command;
- NIST SSDF-informed secure-development practices for protected surfaces,
  review, vulnerability response, and release retention;
- SLSA-informed provenance or build-integrity evidence for released verifier
  artifacts where feasible;
- OpenSSF Scorecard-style repository hygiene checks or documented equivalent;
- dependency and CI-token hardening plan;
- rule contribution review workflow;
- privacy and redaction review for traces;
- candidate-label, human-label, adjudication, split, and locked-test governance
  when benchmark claims are made;
- claim ledger or equivalent public overclaim control.

Recommended evidence:

- signed or otherwise verifiable releases;
- independent reviewer notes;
- fixture coverage report by category;
- public source ledger with access dates;
- vulnerability disclosure policy;
- SBOM or dependency inventory when release artifacts are distributed.

Allowed claim:

> This project self-attests to ACSP-CC v0.1 ACSP-3 managed assurance. This is
> not official certification.

## ACSP-4: Conformance Profile

ACSP-4 is reserved. No project may claim ACSP-4 under ACSP-CC v0.1.

Future ACSP-4 would require at least:

- all ACSP-3 evidence;
- a public conformance suite;
- a machine-readable conformance declaration;
- waiver and exception rules;
- public result-review criteria;
- claim text rules tied to profile version and result digest.

Allowed claim:

> ACSP-CC ACSP-4 is reserved and unavailable in v0.1.

## ACSP-5: Independent Standard Candidate

ACSP-5 is reserved. No project may claim ACSP-5 under ACSP-CC v0.1.

Future ACSP-5 would require at least:

- all ACSP-4 evidence;
- independent assessor criteria;
- at least two independent implementations passing the same suite;
- conflict-of-interest policy;
- evidence retention rules;
- revocation or expiration rules;
- external standards or governance process;
- clear separation from vendor endorsement.

Allowed claim:

> ACSP-CC ACSP-5 is reserved and unavailable in v0.1.

## Named Profiles

| Profile | Required control families |
|---|---|
| ACSP-Core | `Stop` / `SubagentStop` closeout contract, wrap-up, cliffhanger, roleplay drift, sycophancy. |
| ACSP-Core+Evidence | ACSP-Core plus evidence claims and negative-evidence precedence. |
| ACSP-RegexSafe | ACSP-Core plus input bounds, regex safety lint, ReDoS/latency tests. |
| ACSP-Agentic | ACSP-Core+Evidence plus subagent closeout semantics, loop-guard accounting, tamper guard, agent-spawn policy notes. |
| ACSP-SupplyChain | ACSP-Agentic plus CI, release evidence manifests, dependency/security scans, artifact digests. |
| ACSP-Conformance | Public conformance declaration, result bundle, waivers, reproduction command, and claim-rule compliance. |

## Current Reference Target

`agent-closeout-bench` targets ACSP-0/1 public proposal status immediately and
implements candidate ACSP-2 gates. It MUST continue to fail full release checks
until human-gold annotation, adjudication, final locked-test results, and
release approvals exist.

## Evidence Retention

Self-attestation evidence SHOULD be retained with:

- date of assessment;
- assessor or maintainer identity;
- repository commit or release tag;
- verifier and rule-pack hashes;
- commands run;
- result artifact paths;
- known gaps;
- claim text approved for publication.

## Research And Standards Anchors

- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Claude Code security: https://code.claude.com/docs/en/security
- NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA v1.0 security levels: https://slsa.dev/spec/v1.0/levels
- OpenSSF Scorecard: https://scorecard.dev/
- OWASP ReDoS: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS

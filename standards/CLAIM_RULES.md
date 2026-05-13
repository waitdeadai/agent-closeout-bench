# ACSP-CC v0.1 Claim Rules

Status: mandatory claim discipline for the proposed ACSP-CC v0.1 profile.

Access-date anchor for external references: 2026-05-13.

These rules govern how projects may describe ACSP-CC, AgentCloseoutBench,
detectors, adapters, datasets, benchmarks, and conformance. They are designed to
prevent standards-washing, certification-washing, benchmark overclaiming, and
unsupported safety claims.

## Required Status Language

Every public ACSP-CC claim MUST preserve these facts:

- ACSP-CC v0.1 is a proposed profile.
- Conformance is self-attested unless a future independent assessment process
  exists.
- ACSP-CC is not an official standard.
- ACSP-CC is not certification by Anthropic, OpenAI, Hugging Face, NIST,
  OpenSSF, SLSA, OWASP, AAAI, arXiv, or any other cited source.
- ACSP-CC does not certify a model, agent, repository, hook, or organization as
  secure.

Preferred short phrase:

> ACSP-CC v0.1 is a proposed, self-attested closeout security profile, not an
> official standard or certification.

## Allowed Wording

- `proposed Agent Closeout Security Profile for Claude Code`
- `ACSP-CC v0.1 pre-alpha`
- `reference implementation`
- `self-attested candidate conformance result`
- `self-attested ACSP-CC v0.1 ACSP-1`
- `self-attested ACSP-CC v0.1 ACSP-2`
- `self-attested ACSP-CC v0.1 ACSP-3`
- `benchmarked against ACSP-Core v0.1 fixtures`
- `candidate-label diagnostic results`
- `candidate synthetic results`
- `public-derived adversarial fixtures`
- `human-gold labels pending`
- `full release gate intentionally blocks until annotation/adjudication/final locked-test artifacts exist`

Allowed novelty language for AgentCloseoutBench only when the source and claim
ledgers remain consistent:

> To our knowledge, AgentCloseoutBench is the first benchmark for dark-pattern
> detection on agentic coding assistant closeout text at the Claude Code
> `Stop`/`SubagentStop` `last_assistant_message` boundary.

## Forbidden Wording Before Gates Exist

- `ACSP certified`
- `certified`
- `world standard`
- `official standard`
- `production security boundary`
- `prompt-injection-proof`
- `injection immune`
- `cannot be bypassed`
- `guarantees truthful closeout`
- `guarantees implementation correctness`
- `guarantees tests passed`
- `guarantees production readiness`
- `human-annotated corpus`
- `human-gold benchmark result`
- `final scientific performance`
- `universal agent benchmark`
- `universal dark-pattern defense`
- `SOTA result` without a source-ledger entry, exact dataset, exact split, and
  final labels

## Gate-Dependent Wording

| Wording | Minimum gate |
|---|---|
| `benchmarked against ACSP-Core v0.1` | ACSP-1 result bundle. |
| `candidate ACSP-2 implementation` | Active guard, conformance runner, privacy gate, ReDoS test, tamper guard, release partial gate, claim-rule scan. |
| `supply-chain verifiable release` | ACSP-3 with signed or provenanced artifacts and dependency scans. |
| `conformance profile` | Future ACSP-4 registry, declaration, waiver, and reviewer process. |
| `standard candidate` | Future ACSP-5 independent review, governance charter, change-control process, and at least two independent implementations. |
| `final benchmark performance` | Human-gold labels, adjudication, agreement report, frozen detector, final locked-test run. |

## Evidence Required By Claim Type

| Claim type | Minimum evidence |
|---|---|
| ACSP-1 | Offline scanner, fixtures, machine-readable outputs, versioned policy, candidate/final label status. |
| ACSP-2 | ACSP-1 evidence plus Claude Code `Stop` and `SubagentStop` install proof, `last_assistant_message` fixture, rule/policy hash, active guard smoke, tamper-boundary evidence. |
| ACSP-3 | ACSP-2 evidence plus release checklist, provenance or build-integrity evidence, repo security checklist, privacy governance, claim ledger, vulnerability-response path. |
| Deterministic verdict | Code or command evidence showing no live LLM, embedding, network moderation, or prompt judge in runtime verdict. |
| Tamper guard | Protected path list and `PreToolUse` fixture proving ordinary agent edits are blocked. |
| Safe regex | Rule lint output, rejected unsafe constructs, bounded input policy, ReDoS review note. |
| Candidate benchmark result | Dataset version, split, candidate-label disclosure, detector version, command, result JSON. |
| Human-gold benchmark result | Two independent annotation passes, adjudication, agreement report, frozen detector, locked-test audit, result JSON. |
| Trace-derived artifact | Source license, privacy decision, PII/redaction review, provenance manifest, release eligibility. |

## Required Caveats

### Out-Of-Band Verdict Caveat

Use:

> The closeout verdict runs out-of-band from the model context, so prompt text
> cannot directly rewrite the detector's decision procedure.

Pair it with:

> This is not prompt-injection immunity. Lexical evasion, semantic evasion,
> hook misconfiguration, local tampering, and runtime bypass remain possible.

### Evidence Marker Caveat

Use:

> Evidence markers satisfy the closeout-text contract. They do not independently
> prove that the command, deployment, or production system succeeded.

### Candidate Label Caveat

Use:

> Candidate labels are development labels until independent human annotation
> and adjudication are complete.

### Trace Privacy Caveat

Use:

> Raw traces are sensitive by default and require source-license, consent,
> privacy, PII, and redaction review before release.

## Source-Reference Rules

Public claims SHOULD include source references when they rely on current or
external facts. References MUST be refreshed before a new profile release.

Required references by topic:

- Claude Code hook mechanics: Claude Code hooks reference and permissions docs.
- Claude Code security posture: Claude Code security docs.
- Secure-development governance: NIST SSDF.
- Build provenance: SLSA.
- Repository hygiene: OpenSSF Scorecard.
- Regex safety: OWASP ReDoS.
- Dark-pattern benchmark context: DarkBench, DarkPatterns-LLM, and DarkBench+.
- Agent trajectory benchmark context: ATBench and ATBench-Claw.
- Public trace tooling context: Hugging Face Agent Trace Viewer.

## Correction Procedure

When an overclaim is found:

1. Mark the claim as `corrected`, `dropped`, or `deferred`.
2. Preserve the old wording if needed for audit.
3. Write the replacement wording.
4. Identify the evidence gap.
5. Update public docs before further promotion.
6. If result artifacts were affected, regenerate or clearly supersede them.

## Public Draft Rule

Simon/Hacker News/paper/outreach drafts MUST be checked against this file before
publication. If a sentence sounds stronger than the evidence bundle, rewrite it
as a candidate, proposed-profile, or self-attested claim.

## Approved Claim Templates

### ACSP-1

> This project self-attests to ACSP-CC v0.1 ACSP-1, a proposed offline
> closeout-assessment profile. This is not official certification.

### ACSP-2

> This project self-attests to ACSP-CC v0.1 ACSP-2 for Claude Code active local
> closeout guarding. It evaluates closeout text at `Stop` and `SubagentStop`
> and is not official certification.

### ACSP-3

> This project self-attests to ACSP-CC v0.1 ACSP-3 managed assurance, pairing
> active local closeout guarding with release, repository, privacy, and claim
> governance. This is not official certification.

### Benchmark Candidate Result

> These are candidate-label diagnostic results for development and should not
> be read as final benchmark scores.

### Benchmark Final Result

> These are final locked-test results over adjudicated labels for the stated
> dataset version and detector version.

This final-result template is prohibited until the required human-gold evidence
exists.

## Reference URLs

- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Claude Code security: https://code.claude.com/docs/en/security
- Claude Code permissions: https://code.claude.com/docs/en/permissions
- NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA v1.0 security levels: https://slsa.dev/spec/v1.0/levels
- OpenSSF Scorecard: https://scorecard.dev/
- OWASP ReDoS: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS
- DarkBench: https://arxiv.org/abs/2503.10728
- DarkPatterns-LLM: https://arxiv.org/abs/2512.22470
- DarkBench+: https://ojs.aaai.org/index.php/AAAI/article/view/41103
- ATBench: https://arxiv.org/abs/2604.02022
- ATBench-Claw: https://huggingface.co/datasets/HeySig/ATBench-Claw
- Hugging Face Agent Trace Viewer: https://huggingface.co/changelog/agent-trace-viewer

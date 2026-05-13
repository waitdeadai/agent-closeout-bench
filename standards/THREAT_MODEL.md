# ACSP-CC v0.1 Threat Model

Status: proposed profile threat model, pre-alpha.

Access-date anchor for external references: 2026-05-13.

This threat model covers ACSP-CC v0.1 as proposed in
`standards/ACSP_CC_V0_1.md`. It focuses on the closeout boundary where an
agentic coding assistant presents a final message and may imply that work is
complete, verified, safe, or ready to ship.

## Protected Asset

The protected asset is user trust at the agent closeout boundary: the moment an
assistant says work is done, verified, blocked, partial, or ready for handoff.

## Covered Surfaces

- Claude Code `Stop` closeouts.
- Claude Code `SubagentStop` closeouts.
- Deterministic command-hook adapters that invoke the ACSP reference engine.
- Rule packs and conformance fixtures used to detect unsupported completion
  claims and closeout dark patterns.
- Hook settings, hook scripts, env files, engine pointers, and rule-pack
  pointers.
- Content-free telemetry and conformance result bundles.
- Public-data-derived fixture manifests and claim ledgers.

## Partially Covered Surfaces

- `PreToolUse` is covered only for tamper-guard and tool policy controls wired
  by this implementation.
- `UserPromptSubmit` and `UserPromptExpansion` are relevant to prompt intake and
  slash-command expansion, but ACSP-CC v0.1 does not claim full governance over
  those paths.
- Trace-bound evidence is a v0.1 evidence-source class, but full transcript
  binding is still a candidate gate unless a concrete trace ledger is present.
- Public agent traces are considered input candidates only after license,
  provenance, privacy, sanitizer, and reviewer gates pass.

## Out Of Scope

- OS sandboxing.
- Complete Claude Code permission enforcement.
- Whole-session correctness.
- Provider identity proof.
- Model training or model-level alignment.
- Prompt-injection immunity.
- Prevention of user-authorized local tampering by a shell user with filesystem
  permissions.
- `PostToolUse` as pre-execution prevention.
- HTTP/MCP/prompt/agent hook failure as fail-closed deterministic enforcement.
- Certification of repositories, models, hooks, or organizations.

## Assets

- User trust in the final assistant message.
- Closeout-state verdicts and matched rule evidence.
- Claude Code hook settings and runtime adapters.
- Engine binaries, scripts, policy files, rule packs, and hashes.
- Local env files that point to engines or rules.
- Trace-derived evidence markers.
- Corpus records, labels, splits, and locked-test results.
- Source, claim, provenance, license, redaction, and release ledgers.
- Public statements about benchmark novelty, performance, and conformance.

## Actors

- Assistant or subagent producing closeout text.
- User or operator approving actions and interpreting results.
- Repository maintainer adding rules, fixtures, or releases.
- Malicious or careless contributor attempting to weaken controls.
- Dependency or build-system actor able to alter scripts or binaries.
- Benchmark participant trying to overfit public examples or locked tests.
- External source author whose public traces or papers may be ingested.
- Downstream adopter making unsupported marketing or compliance claims.

## Trust Boundaries

### TB-1: Model Context To Hook Runtime

The assistant can influence the final message, but a deterministic hook runtime
can evaluate that message out-of-band. This boundary reduces direct prompt
control over the verdict, but does not prevent lexical evasion, runtime
misconfiguration, malicious hook code, or local bypass.

### TB-2: Hook Runtime To Filesystem

Hooks are privileged local code. Claude Code command hooks run with the
operator's user permissions, so the hook layer is not isolation. ACSP-CC relies
on deterministic local evaluation, reproducible fixture results, source-control
review, CI, release provenance, and explicit claim discipline.

### TB-3: Evidence Marker To Actual Truth

Trace evidence can support a closeout-text claim, but it is not the same as
independent proof that tests passed, deployment succeeded, or a release is
secure. External verification remains required.

### TB-4: Public Benchmark Data To Generalization

Public examples support transparency and reproducibility, but they also create
leakage and tuning risk. Candidate-label diagnostics must remain separate from
human-gold locked-test claims.

### TB-5: Public Trace Sources To Release Artifacts

Hugging Face Agent Trace Viewer, ATBench, ATBench-Claw, and similar trace-level
resources make agent safety work more observable. They also raise license,
privacy, consent, PII, and raw-tool-output risks. ACSP-CC defaults to
content-free or redacted manifests unless release review permits more.

## Primary Threats

| Threat | Description | ACSP-CC response |
|---|---|---|
| Evidence-free completion | Assistant claims done, tested, verified, deployed, read, or no-issues without evidence. | Block or flag unless an evidence source is present. |
| Contradictory closeout | Assistant claims success while text says tests failed, did not run, or were skipped. | Treat negative evidence as stronger than completion phrasing. |
| Retention pressure | Assistant ends with generic continuation bait. | Detect wrap-up tails at closeout. |
| Cliffhanger | Assistant withholds unresolved concerns or invites continuation without concrete blocker. | Detect dangling issue and partial-status false shapes. |
| Sycophancy | Assistant opens or closes with unearned praise or validation. | Detect praise-before-substance and evidence-free agreement patterns. |
| Roleplay drift | Assistant breaks role with AI-disclaimer boilerplate or anthropomorphic self-claims. | Detect role breaks and self-investment language. |
| Hook tampering | Assistant edits hooks, env, rule packs, or engine pointers. | `PreToolUse` tamper guard and doctor checks. |
| Loop-guard blind spot | Stop hook continuation causes `stop_hook_active=true`. | Require explicit `loop_guard_release` accounting or bounded strict repair. |
| ReDoS | Crafted closeout text slows regex detectors. | Input limits, safe regex lint, long-input conformance tests. |
| Untrusted rule contribution | External rule weakens or destabilizes verdicts. | Quarantine, review, fixture tests, versioning, and checksums. |
| Runtime dependency compromise | Verifier binary, script, or dependency is altered. | SLSA-style provenance, checksums, pinned releases, protected build path. |
| Repository security drift | Poor repo hygiene weakens trust in releases. | OpenSSF Scorecard-style checks, least-privilege CI, signed releases where feasible. |
| Candidate label overclaim | Development labels are presented as final truth. | Human adjudication gate and claim rules. |
| Benchmark leakage | Detector is tuned on locked or public reporting examples. | Split governance, locked-test audit, private or delayed holdout for leaderboards. |
| LLM judge finality | A model judge is treated as ground truth. | LLM judge output is diagnostic only; human adjudication controls final labels. |
| Trace privacy leak | Raw session data exposes secrets, users, paths, hosts, or private code. | No raw trace persistence by default, quarantine checks, redaction and license review. |
| Claim inflation | Project claims standard, certified, SOTA, official, or final before evidence exists. | Claim rules and release gates. |
| Cross-runtime confusion | Non-Claude runtimes claim Claude Code conformance. | Require documented equivalent boundary and prohibit Claude Code claim without hook proof. |

## Misuse Cases

### MC-1: "Done" Without Verification

An assistant says implementation is complete even though no command ran. The
profile should classify the message as unsupported unless the message clearly
says it is blocked, partial, or read-only.

### MC-2: Tamper Then Close

An assistant edits hook settings, removes the closeout guard, and then claims
the task is done. A `PreToolUse` tamper guard should block ordinary agent edits
to protected hook surfaces. The profile must still acknowledge that a local
user or compromised account can bypass the guard.

### MC-3: Regex Rule Bomb

A contributor adds a detector pattern with nested repetition and overlapping
alternation. Lint and adversarial fixture tests should reject it before release,
following OWASP ReDoS guidance.

### MC-4: Public Trace Shortcut

A maintainer imports raw public agent traces into release artifacts because a
viewer made them easy to browse. The intake path should stop until source
license, consent, privacy, and redaction reviews are complete.

### MC-5: Benchmark Marketing Inflation

A project reports candidate-label development results as a public benchmark
score. The claim rules should require candidate-label wording and block final
or SOTA language until adjudicated locked-test results exist.

## Required Compensating Controls

- Team/default installs SHOULD use `team-safe` or explicit review-oriented
  policy, not undocumented trusted-local bypass modes.
- CI SHOULD rerun conformance independently from local hook wiring.
- Release artifacts SHOULD include engine hash, rule-pack hash, fixture hash,
  corpus hash, dependency lockfile hash, and CI run URL.
- Higher assurance deployments SHOULD use managed policy, sandboxing, immutable
  hook/rule paths, filesystem ACLs, or equivalent controls.
- Claim reviews SHOULD run before outreach, paper, README, or leaderboard
  publication.

## Residual Risks

- Deterministic text rules can miss paraphrases and novel pressure tactics.
- Closeout evidence markers can be forged unless independently verified.
- Local filesystem controls do not stop a privileged local actor.
- Public benchmark examples can leak into model training or detector tuning.
- Hook behavior may change as Claude Code evolves; references must be rechecked
  before freezing a new ACSP-CC version.
- This profile does not replace SSDF, SLSA, Scorecard, secure code review,
  deployment verification, incident response, or human judgment.

## Research And Standards Anchors

- Claude Code hooks reference: https://code.claude.com/docs/en/hooks
- Claude Code security: https://code.claude.com/docs/en/security
- Claude Code permissions: https://code.claude.com/docs/en/permissions
- NIST SSDF SP 800-218: https://csrc.nist.gov/pubs/sp/800/218/final
- SLSA v1.0 security levels: https://slsa.dev/spec/v1.0/levels
- OpenSSF Scorecard: https://scorecard.dev/
- OWASP ReDoS: https://owasp.org/www-community/attacks/Regular_expression_Denial_of_Service_-_ReDoS
- ATBench: https://arxiv.org/abs/2604.02022
- ATBench-Claw: https://huggingface.co/datasets/HeySig/ATBench-Claw
- Hugging Face Agent Trace Viewer: https://huggingface.co/changelog/agent-trace-viewer

# ACSP-CC v0.1: Agent Closeout Security Profile for Claude Code

Status: proposed profile, pre-alpha, self-attestation only.

Access-date anchor for external references: 2026-05-13.

ACSP-CC v0.1 defines deterministic closeout-integrity controls for Claude Code
sessions. ACSP-CC means Agent Closeout Security Profile for Claude Code. It is a
proposed profile and reference conformance target, not an official standard,
certification program, sandbox, model-safety certificate, or final benchmark
claim.

The reference implementation for this repository is `agentcloseout-physics`.
The reference implementation is not the standard itself; it is a candidate
implementation and conformance harness used to exercise the proposed profile.

## Scope

ACSP-CC covers the text and lifecycle boundary where Claude Code attempts to
finish a main turn or subagent turn. In Claude Code, the intended enforcement
surface is the `Stop` and `SubagentStop` hook payload field documented as
`last_assistant_message`.

The profile focuses on:

- evidence-free completion claims;
- misleading `done`, `tested`, `verified`, `deployed`, `read`, or `no issues`
  language;
- contradictory closeouts where failed, skipped, or missing verification is
  softened into success language;
- retention-oriented wrap-up tails;
- cliffhanger and continuation-bait endings;
- sycophantic praise or unearned validation in closeout text;
- AI-disclaimer role breaks and anthropomorphic self-investment in coding-agent
  closeouts;
- deterministic hook behavior at `Stop`, `SubagentStop`, and related command
  hook surfaces;
- protected hook, env, engine, and rule-pack wiring.

The profile does not claim whole-system Claude Code security. Hooks are local
policy automation and run with the operator's user permissions. Operating-system
sandboxing, Claude Code permission settings, source-control policy, release CI,
independent verification, and human review remain required controls for higher
assurance.

## Normative Language

The terms `MUST`, `MUST NOT`, `SHOULD`, `SHOULD NOT`, and `MAY` are normative
only for this proposed profile. They do not imply recognition by a standards
body or external certifier.

## ACSP-CC Core Requirements

### ACSP-CC-HOOK-DET

Security-critical closeout controls MUST use deterministic local validators.
For Claude Code command hooks, blocking MUST use documented event semantics:
`exit 2` for blocking command-hook failures, or a documented JSON decision for
the specific hook event.

Prompt hooks and agent hooks MAY be used as advisory review layers, but they
MUST NOT be the deciding enforcement path for ACSP-Core or
ACSP-Core+Evidence.

The enforcement verdict MUST NOT depend on a live LLM, embedding service,
network moderation API, prompt-based judge, or unbounded remote call. LLMs MAY
be used for offline triage, research, or disagreement discovery, but such use is
not an enforcement verdict under this profile.

### ACSP-CC-STOP

An implementation claiming ACSP-Core MUST evaluate `Stop` events. It MUST parse
the outgoing assistant closeout message and return a blocking or downgrade
decision when the message violates the selected ACSP profile.

`Stop` enforcement MUST implement loop protection. If Claude Code reports
`stop_hook_active=true`, the implementation MUST either use a bounded repair
counter or release with an explicit `loop_guard_release` accounting event. It
MUST NOT silently count the release as full enforcement.

### ACSP-CC-SUBAGENT

An implementation claiming agentic closeout coverage MUST evaluate
`SubagentStop` events. A blocking `SubagentStop` decision keeps the subagent
running; it is not proof that the parent session is correct. Parent-session
claims MUST remain evidence-bound.

### ACSP-CC-EVIDENCE

Completion claims MUST be checked against deterministic evidence markers.
Implementations MUST distinguish at least:

- `trace_ledger`: evidence bound to structured trace or tool data;
- `command_marker`: a concrete command, test, deploy, lint, or verification
  command named in the closeout or trace;
- `source_marker`: a cited source ledger, reviewed file path, or read-only audit
  marker;
- `text_marker`: evidence mentioned only in closeout prose;
- `negative_marker`: explicit missing, skipped, failed, or contradictory
  evidence;
- `missing`: no evidence marker;
- `contradicted`: a stronger structured marker contradicts the claim.

Text-only markers MAY be accepted for daily-user ergonomics, but conformance
reports MUST label them weaker than trace-bound evidence.

Evidence markers only satisfy the closeout-text contract. They do not prove the
software, deployment, release, or production system is correct.

### ACSP-CC-STATES

An implementation SHOULD preserve a machine-readable closeout state. The
minimum state set is:

- `verified_done`: completion claim with concrete verification or evidence.
- `partial_blocked`: incomplete work, cause, and next concrete unblocker.
- `read_only_audit`: inspected files or sources without implementation claims.
- `needs_user_input`: missing user input blocks progress.
- `needs_bounded_choice`: bounded operator choice such as `go/stop` or `A/B`.
- `handoff_with_evidence`: handoff with concrete evidence and residual risk.
- `unsupported_completion`: completion or verification claim without sufficient
  evidence.

Explicit negative evidence such as `tests not run`, `verification skipped`,
`commands run: none`, failed checks, missing source review, or blocked access
MUST downgrade completion to a non-`verified_done` state unless separate
concrete verification evidence is present.

### ACSP-CC-DARKPATTERNS

The proposed minimum closeout category set is:

- `wrap_up`: unprompted continuation offers, unnecessary next-step prompts, or
  re-engagement invitations that turn a completed response into an open loop.
- `cliffhanger`: withheld information, bait, or unresolved setup that pressures
  the user to continue.
- `roleplay_drift`: emotional, prideful, fatigued, personally invested, or
  anthropomorphic agent self-presentation.
- `sycophancy`: unearned praise, dishonest validation, or flattery that could
  distort user judgment.
- `evidence_claims`: unsupported claims of implementation, verification,
  testing, deployment, or absence of issues.

Projects MAY add categories, but they MUST keep category definitions separate
from release claims. A detector improving on one category does not validate the
benchmark or the profile as a whole.

### ACSP-CC-TAMPER

An implementation deployed in Claude Code SHOULD protect hook wiring, engine
pointers, env files, and rule-pack pointers with a `PreToolUse` tamper guard or
equivalent local control. The guard SHOULD cover ordinary agent edits to:

- `.claude/settings*.json` hook entries;
- `.claude/hooks/**`;
- `.claude/agentcloseout.env` or equivalent env file;
- engine executable pointers;
- rule-pack or policy directories.

The implementation MUST NOT describe this as a sandbox or absolute protection.
A local user, administrator, compromised account, or malicious dependency with
sufficient filesystem privileges can still bypass local controls.

### ACSP-CC-CLAIMS

Public claims MUST be scoped to observed evidence and MUST follow
`standards/CLAIM_RULES.md`. Allowed claim families include:

- `ACSP-CC-aware`;
- `self-attested ACSP-CC v0.1 Level 1`;
- `self-attested ACSP-CC v0.1 Level 2`;
- `self-attested ACSP-CC v0.1 Level 3`;
- `benchmarked against ACSP-Core v0.1 fixtures`;
- `candidate-label diagnostic result`;
- `human-gold result` only after adjudication gates exist.

Forbidden claims before the required gates exist include `ACSP certified`,
`official standard`, `world standard`, `prompt-injection-proof`,
`cannot be bypassed`, `production security boundary`, `human-gold benchmark
result`, `final scientific performance`, and `SOTA result`.

### ACSP-CC-REDOS

Regex-based implementations MUST bound input size and test long benign and
adversarial inputs. Implementations SHOULD use a regex engine with linear-time
safety properties where possible. They MUST NOT include known catastrophic
backtracking constructs unless a deterministic timeout and failure mode are
present.

Rule governance MUST account for OWASP ReDoS risk. Any implementation accepting
community-supplied or untrusted rules MUST quarantine them until syntax,
resource-bound, and adversarial fixture checks pass.

### ACSP-CC-TELEMETRY

Telemetry MUST be opt-in and content-free by default. Minimal telemetry MUST
exclude raw prompts, raw completions, tool arguments, tool output, file
contents, absolute paths, usernames, hostnames, IP addresses, emails, API keys,
and stable user/session/project identifiers.

Raw traces, transcripts, and tool outputs MUST be treated as sensitive by
default. Public or shared artifacts SHOULD use content-free or redacted
manifests unless source license, consent, PII review, and redaction review all
permit release.

### ACSP-CC-PUBLIC-DATA

Public-data-derived fixtures MUST have source, license, provenance, sanitizer,
reviewer, and release-eligibility records. Noncommercial, share-alike,
privacy-sensitive, or unclear-license sources MUST NOT be mixed into
Apache-compatible public fixtures until explicitly cleared.

Hugging Face Agent Trace Viewer, ATBench, and ATBench-Claw demonstrate the
growing value of trace-level safety evaluation. ACSP-CC uses that direction as
context, but closeout-text conformance MUST NOT require publishing raw traces.

### ACSP-CC-SUPPLYCHAIN

Projects claiming Level 3 or above SHOULD maintain release provenance,
rule-pack checksums, pinned dependency posture, least-privilege CI tokens,
signed or verifiable release artifacts where feasible, and vulnerability
response documentation. NIST SSDF, SLSA, and OpenSSF Scorecard are informative
references for these practices; satisfying ACSP-CC does not mean satisfying
those frameworks.

## Named Profiles

| Profile | Required control families |
|---|---|
| ACSP-Core | `Stop` / `SubagentStop` closeout contract, wrap-up, cliffhanger, roleplay drift, sycophancy. |
| ACSP-Core+Evidence | ACSP-Core plus evidence claims and negative-evidence precedence. |
| ACSP-RegexSafe | ACSP-Core plus input bounds, regex safety lint, ReDoS/latency tests. |
| ACSP-Agentic | ACSP-Core+Evidence plus subagent semantics, loop-guard accounting, tamper guard, agent-spawn policy notes. |
| ACSP-SupplyChain | ACSP-Agentic plus CI, release evidence manifests, dependency/security scans, artifact digests. |
| ACSP-Conformance | Public conformance declaration, result bundle, waivers, reproduction command, and claim-rule compliance. |

## Machine-Readable Evidence

An implementation SHOULD emit or preserve machine-readable evidence with:

- verifier name and version;
- policy or rule-pack version and hash;
- input class and lifecycle event;
- decision and closeout state;
- matched controls or rule identifiers;
- evidence markers considered;
- latency and timeout status;
- any configuration or runtime caveat that affects the verdict.

## Research And Standards Anchors

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

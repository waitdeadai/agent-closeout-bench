# ACSP-CC v0.1 Control Crosswalk

Status: informative crosswalk for a proposed profile.

Access-date anchor for external references: 2026-05-13.

This crosswalk maps ACSP-CC controls to adjacent references. It is not a claim
that ACSP-CC satisfies NIST SSDF, SLSA, OpenSSF Scorecard, OWASP, Anthropic,
Hugging Face, DarkBench, DarkPatterns-LLM, DarkBench+, ATBench, or
ATBench-Claw. It is a traceability aid for implementers and reviewers.

## Crosswalk Table

| ACSP control | Claude Code hook semantics | NIST SSDF reference | SLSA / supply-chain reference | OpenSSF Scorecard reference | OWASP / research anchor |
|---|---|---|---|---|---|
| ACSP-CC-HOOK-DET | Command hooks, event JSON, exit `2`, documented JSON decisions. | Secure implementation, verification, and vulnerability-response practice families. | Build and result provenance for validator artifacts. | Dangerous-Workflow and Token-Permissions checks inform repo hardening. | Runtime verdict is deterministic; LLM judge output is diagnostic only. |
| ACSP-CC-STOP | `Stop` can block stopping and feed reason back; `last_assistant_message` is the inspected field. | Verification criteria and recurrence prevention. | Result bundle binds profile, rules, fixtures, and engine. | CI-Tests where adopted. | Closeout manipulation context from DarkBench, DarkPatterns-LLM, and DarkBench+. |
| ACSP-CC-SUBAGENT | `SubagentStop` keeps subagent running but is not parent proof. | Review and verification governance. | Trace and result manifests for agentic runs. | Branch-Protection and Code-Review checks where adopted. | Agent trajectory safety context from ATBench and ATBench-Claw. |
| ACSP-CC-EVIDENCE | Closeout text plus optional trace, command, source, and negative evidence fields. | Executable verification evidence and release criteria. | Provenance for result and corpus transforms. | Pinned-Dependencies and Dependency-Update-Tool where adopted. | Evidence-free completion and overreliance risks. |
| ACSP-CC-STATES | Stop/SubagentStop output preserves `verified_done`, `partial_blocked`, `read_only_audit`, and unsupported states. | Security requirements and review criteria. | Result artifact digests. | CI-Tests where adopted. | Supports closeout-specific benchmark reproducibility. |
| ACSP-CC-DARKPATTERNS | Closeout text is inspected for wrap-up, cliffhanger, roleplay drift, sycophancy, and evidence claims. | Misuse-case and abuse-case review discipline. | N/A | N/A | DarkBench, DarkPatterns-LLM, and DarkBench+ define adjacent LLM dark-pattern landscape. |
| ACSP-CC-TAMPER | `PreToolUse` can guard ordinary edits to hooks, settings, env, engine, and rules. | Protection of code/configuration and release integrity. | Tamper-resistant release artifacts and provenance goals. | Token-Permissions, Signed-Releases, Branch-Protection where adopted. | Must not claim sandbox or injection immunity. |
| ACSP-CC-REDOS | Bounded command-hook input and rule lint. | Input validation and safe implementation. | Reproducible long-input fixture results. | Fuzzing where adopted. | OWASP ReDoS. |
| ACSP-CC-TELEMETRY | Hook telemetry emitted only in content-free/minimal-stats mode by default. | Data-protection and logging discipline. | Content-free event manifests. | Security-Policy where adopted. | HF Agent Trace Viewer shows trace utility; ACSP keeps raw traces private by default. |
| ACSP-CC-PUBLIC-DATA | Public fixtures require source, license, provenance, sanitizer, reviewer, and release decisions. | Third-party component and supplier governance. | Corpus shard hashes and source manifests. | License and OpenSSF best-practice checks where adopted. | ATBench, ATBench-Claw, HF Agent Trace Viewer; license and privacy caveats remain. |
| ACSP-CC-CLAIMS | Claims constrained to observed profile evidence and gates. | Secure release criteria and supplier communication. | Release attestation and result digests. | Signed-Releases where enabled. | Scientific benchmark claim discipline and overclaim prevention. |
| ACSP-CC-SUPPLYCHAIN | Release evidence for engine, rules, fixtures, corpus, and results. | Protect software, verify release integrity, respond to vulnerabilities. | SLSA provenance and tamper-resistance goals. | Scorecard automated security checks. | ACSP conformance does not equal SLSA, SSDF, or Scorecard compliance. |

## Control Notes

### Claude Code Hooks And Security

Claude Code hooks are the implementation surface for ACSP-CC in Claude Code.
The relevant reference points are:

- `Stop` and `SubagentStop` events expose the final assistant message for
  closeout evaluation.
- `PreToolUse` can be used to block ordinary tool calls before they execute.
- Hook code is security-sensitive because it executes commands in the local
  environment.
- Permissions and sandboxing are complementary; hooks do not create an
  absolute sandbox.

ACSP-CC therefore requires active closeout guards to prove hook wiring, but it
also requires claim language that acknowledges local bypass and configuration
risk.

### NIST SSDF

NIST SSDF is an informative secure-development reference. ACSP-CC borrows its
general discipline around requirements, secure implementation, protection of
software and configuration, verification, release integrity, and vulnerability
response. ACSP-CC conformance does not establish SSDF compliance.

### SLSA

SLSA v1.0 focuses on build provenance and increasing protection against
tampering of the build, provenance, and artifact. ACSP-CC uses SLSA as a
reference for verifier binaries, rule-pack release artifacts, and reproducible
release evidence. ACSP-CC does not assign SLSA levels.

### OpenSSF Scorecard

OpenSSF Scorecard is an automated OSS security-risk assessment tool. ACSP-CC
uses it as a reference for repository hygiene, dependency posture, token
permissions, packaging, and signed release checks. A Scorecard result does not
prove closeout safety.

### OWASP ReDoS

OWASP ReDoS documents regular-expression denial-of-service risk. ACSP-CC uses
it to justify bounded inputs, safe regex engines, rule linting, and quarantine
for untrusted rule contributions.

### Benchmark And Trace References

DarkBench, DarkPatterns-LLM, and DarkBench+ establish adjacent LLM dark-pattern
benchmark context. They prevent broad first-benchmark claims and motivate
clearer category boundaries.

ATBench and ATBench-Claw establish adjacent trajectory-level agent safety
evaluation context. They motivate trace evidence and action-centric failure
analysis, while ACSP-CC remains narrower: closeout-text safety at the Claude
Code closeout boundary.

Hugging Face Agent Trace Viewer demonstrates that Claude Code, Codex, and other
agent traces can be uploaded and browsed as datasets. ACSP-CC treats that as a
useful research direction, not permission to publish raw traces without review.

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

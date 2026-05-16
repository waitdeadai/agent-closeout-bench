# Strategic Pivot — 2026-05-16

Outer route: `/opussonnet`
Inner contract: workflow
Mode: read-and-recommend (no mutation outside this artifact and a follow-up SPEC)
Time anchor: 2026-05-16T12:19:25-03:00 (Saturday)
Trigger: operator request "I want the engines to be a moat and focus on other things, identifying the highest leverage path we can take from now"

## 1. UAI sprint checkpoint — paused at Day 2 of 12

The SafeAI@UAI 2026 paper sprint is paused at a clean checkpoint, not abandoned. Resume costs are bounded.

State on `paper/uai-2026-sprint` branch at HEAD `ea9ea69`:
- 9 paper sections drafted, 0 TODO markers, claim-gate passes (3016 words, ~2400 prose).
- Table 1 skeleton with TBD cells; populates automatically from `annotations/judge_agreement.json` when real judge data exists.
- Annotation pipeline scaffolded end-to-end (sampler, judge driver with `--dry-run` / `--use-real-api`, schema, validator, kappa computer). Verified on 20-row dry data.
- LeveragePath audit at `.taste/leveragepath/2026-05-16-uai-sprint-context/leveragepath.md`.
- /introspect run at `.taste/introspect/2026-05-16-paper-draft/introspect.md` — one critical SPB-framing fix applied.
- /verify run at `.taste/verify/2026-05-16-paper-draft/verify.md` — 3 PASS, 3 BLOCKED on operator, 1 not started.

Resume requirements:
- Operator-only: API keys (~$1.53 spend), LaTeX install or Overleaf, OpenReview submission.
- Autonomous: 1-3 hours of polish + the κ table populate when judge data exists.

Deadline: 2026-05-28 AoE (12 days from now). Resume window is wide.

Fallback: if the May 28 deadline is missed, the same materials redirect to NeurIPS workshop (Aug 29, 3.5 months). The work is not deadline-fragile.

## 2. Engines locked as moat

The deterministic engine and benchmark scaffolding shipped over the last week constitute the technical moat. Locking means: no more architecture changes, no v4 semantic engine rebuild, no scope creep on the engine itself. Future work consumes the engine; it does not modify it.

Locked artifacts:
- `agent-closeout-bench/engine/` — Rust reference engine, rule-pack hashing, deterministic verdicts.
- `agent-closeout-bench/rules/closeout/*.yaml` — per-category rule packs, hash `sha256:2087c5cf648e4d0aa8690b02e97a0edd36cb13ea80d3a7423274b191dd9993b6`.
- `agent-closeout-bench/data/` — 800-record candidate corpus with provenance discipline.
- `agent-closeout-bench/CLAIM_LEDGER.md` — forbidden-wording discipline, codified.
- `llm-dark-patterns/hooks/*.sh` — 11 bundled hooks already passing CI on main.
- `llm-dark-patterns/.claude-plugin/plugin.json` — already exists, ready for marketplace submission.
- Open-core Apache-2.0 licensing on both repos.

What "moat" means in this context:
- First-mover claim on the closeout-text safety surface.
- Open-source under the `waitdeadai` org, which is the canonical authorship trail (paper-grade Git history, claim ledger, source registry).
- Deterministic out-of-band design = adversarial copies cannot just "fine-tune harder"; they have to ship a different architecture.
- The companion paper (UAI workshop submission target) is the academic citation hook.

Defence posture:
- No patent / trademark work — heavy, slow, and inconsistent with the open-core posture.
- No license change — Apache-2.0 stays.
- Distribution lock through official channels = the moat reinforcement (see §3).

## 3. Highest-leverage path from here (deepresearch-backed, 2026-05-16)

### Path candidates (RICE-ranked, ceiling ten on each axis)

| # | Move | R | I | C | E (hr) | RICE | Tags |
|---|------|---|---|---|--------|------|------|
| Z1 | Anthropic plugin marketplace submission (`clau.de/plugin-directory-submission` + `claude-plugins-community`) | 10 | 9 | 7 | 6 | **105** | auto, mass, evergreen, reversible |
| Z2 | Anthropic AI Safety Fellows application (rolling cohort, next batch after July 2026) | 4 | 10 | 5 | 16 | **12.5** | manual, community, time-sensitive, reversible |
| Z3 | UK AISI Alignment Project grant (£27M to 60 projects, up to £1M individual) | 6 | 10 | 4 | 32 | **7.5** | manual, community, cycle-bound, reversible |
| Z4 | Anthropic Verified badge upgrade (after Z1 lands) | 9 | 10 | 5 | 8 | **56** | auto-then-review, mass, evergreen, reversible |
| Z5 | Windsurf Cascade Hooks port | 5 | 6 | 6 | 24 | **7.5** | auto, mass, evergreen, reversible |
| Z6 | NeurIPS workshop paper (Aug 29) | 7 | 8 | 8 | 60 | **7.5** | auto, community, time-sensitive, reversible |
| Z7 | Apart Research Lab Fellowship application | 6 | 9 | 4 | 12 | **18** | manual, community, cycle-bound, reversible |

Recompute under "engines as moat" weighting (where distribution > academic credit):
- Z1 dominates by a wide margin; the second-place move is **Z4** (Anthropic Verified badge), which is unlocked by Z1.

### Recommended path: **Z1 → Z4 → Z2 → Z6 (parallel with UAI resume)**

#### Z1. Anthropic plugin marketplace submission (this slice)
Submission portal: `clau.de/plugin-directory-submission` (verified 2026-05-16 via Anthropic plugin marketplace documentation).

Two destinations:
- `claude-plugins-community` — community marketplace, read-only mirror, accepts third-party submissions.
- `claude-plugins-official/external_plugins/` — Anthropic-managed directory, where third-party plugins from partners (Supabase, Firebase, Discord, Telegram) live.

Two tiers:
- Standard listing — automated review (basic security scan, plugin shape validation).
- **Anthropic Verified badge** — additional quality and safety review by Anthropic.

Why this is the highest-leverage move:
1. Distribution to every Claude Code user. Anthropic shipped the marketplace in late 2025; growth is steep.
2. Trust pyramid favours us. CVE-2026-21852 (CVSS 7.5, January 2026) and recent Pluto Security analysis surfaced "Trust Pyramid Issues" where operators must trust a stack of plugin + MCP + skills + hooks + binaries without integrity-rooted authorship boundaries. Our shape (deterministic, no MCP, no auto-loading skills, paper-grade claim ledger, redactable Apache-2.0 source) is the *opposite* of the trust-erosion concern. We have a reviewer-friendly story.
3. Anthropic Verified badge upgrade after standard listing is the credibility moat. It's an explicit "Anthropic reviewed this for quality and safety" signal — exactly the badge a dark-patterns hook suite benefits from.
4. The plugin.json file already exists in `llm-dark-patterns/.claude-plugin/`. The submission packaging is mostly checklist work.
5. Compatible with the UAI sprint — marketplace submission is non-anonymous and lives in the `waitdeadai` org, which is already public. No double-blind conflict.

Effort breakdown for Z1:
- Verify plugin.json against the current marketplace schema and CLI validation.
- Verify all 11 bundled hooks comply with the marketplace security guidance.
- Read `https://claude.com/plugins/security-guidance` end-to-end and fix any non-compliances.
- Submit via `clau.de/plugin-directory-submission` for the community marketplace.
- Submit via `platform.claude.com/plugins/submit` for the official marketplace (or whatever Anthropic's flow currently routes to).
- Log the submission in a `MARKETPLACE_SUBMISSION_LOG.md` with timestamps and reviewer feedback.

Reversibility: full. Submissions can be withdrawn before approval. If the marketplace rejects or asks for changes, the changes are local to the existing public repo.

#### Z4. Anthropic Verified badge (follow-on)
Triggered after Z1 lands as a standard listing. Submission process is implicit in the marketplace docs; details fetched live when Z1 review is in flight.

#### Z2. Anthropic Fellows application (parallel, slower clock)
The April 26 deadline for the July 2026 cohort is past, but applications are rolling. Prepare the materials now, submit for the next cohort window.
- Anthropic Fellows program details: $3,850/wk stipend, ~$15K/month compute credit, 4 months, direct mentorship.
- Eligibility favourable: no PhD required, prior ML experience not required.
- Topic fit: perfect (alignment-tagged work on a Claude Code surface).
- Likely "next cohort" timing: rolling basis means an Oct/Nov 2026 start is plausible; verify when application slot opens.

#### Z6. UAI sprint resume → NeurIPS workshop expansion
Once Z1 lands and Z2 is in motion, resume the UAI sprint (May 28 deadline) if API keys are provisioned. If May 28 is missed, the same materials route to NeurIPS workshop (Aug 29). Two-shot academic path with no extra work.

### Deferred (not zero leverage, but lower priority for the immediate slice)
- **Z3 UK AISI Alignment Project**: high impact but the application is heavy (16-32 hours of writing) and the next round timing is uncertain. Slot in after Z1 + Z2 prep.
- **Z5 Windsurf Cascade Hooks port**: useful as cross-platform proof but Windsurf user base is smaller than Claude Code and the porting work is non-trivial.
- **Z7 Apart Research Lab Fellowship**: parallel academic path; sequence after Z2 because Z2 is the higher-prestige Anthropic-direct path.

### Deliberately not on the list
- **NIST CAISI engagement**: too slow, no clear hook for us yet.
- **Google.org AI Impact Challenge**: less perfect topic fit; not safety-specific enough.
- **Patent or trademark work**: inconsistent with open-core posture.
- **Direct customer outreach / paid SaaS**: premature; needs the marketplace listing first.

## 4. Proposed next slice contract

Slice scope: **Z1. Anthropic plugin marketplace submission for `llm-dark-patterns`** as a single bounded deliverable. AgentCloseoutBench remains a benchmark repo, not a plugin.

Tentative SPEC structure (to be written in detail under `/opussonnet --inner-contract workflow` after operator approves the slice direction):

- **Deliverable**: One marketplace submission live in `claude-plugins-community` and, if the path supports, an `external_plugins/` directory PR to `claude-plugins-official`.
- **Success criteria**: submission record exists with confirmation ID, plugin install command verified end-to-end on a clean Claude Code install, no automated review failures.
- **Agent-Native Estimate**:
  - estimate type: agent-native
  - agent_wall_clock: optimistic 3 hr / likely 6 hr / pessimistic 10 hr
  - agent_hours: ~5 hr (validation + packaging + submission form fill)
  - human_touch_time: 30 min (operator approves the submission form, captures the confirmation URL)
  - calendar_blockers: Anthropic review queue (unknown ETA — could be hours, could be weeks)
  - critical_path: read security guidance → validate plugin.json → verify hooks → submit → log
  - confidence: medium (downgrade: marketplace submission process is documented but live-verification details on the exact form fields haven't been touched yet)
- **Out of scope**: AgentCloseoutBench marketplace submission, Windsurf port, Fellows application, paper resume work.

## 5. What "focus on other things" means concretely

After this slice closes:
- The UAI paper sprint becomes a passive critical-path item — operator provisions API keys when ready, paper resumes against the May 28 deadline.
- The plugin marketplace listing becomes the durable distribution moat.
- Time freed up goes to: Fellows application prep (Z2), Z6 NeurIPS workshop polish, and Z3 AISI Alignment Project research if calendar opens.

## 6. Decision required from operator

To proceed past plan-mode auto-approval gate:
1. Approve **Z1 as the next slice** (marketplace submission for `llm-dark-patterns`)?
2. Or pick a different path from §3 / propose your own?
3. Or pause everything for the day?

Once approved, I write the detailed SPEC under `llm-dark-patterns/SPEC-marketplace-submission.md`, run `/specqa`, and start execution.

## Coverage

- WebSearch queries this turn: 5 (Anthropic marketplace, AI safety funding, Cursor/Windsurf/Aider, Fellows program, security-guidance + dark-patterns mention check)
- RICE scoring: 7 candidates ranked
- Time anchor: 2026-05-16T12:19:25-03:00 (verified live)
- All claims sourced; no pretrained-memory bluff on rules/pricing/deadlines.

## Sources (verified 2026-05-16)

- [Anthropic plugin marketplace docs](https://claude.com/plugins)
- [Anthropic plugin submission portal](https://clau.de/plugin-directory-submission) (canonical short link from marketplace docs)
- [claude-plugins-official repo](https://github.com/anthropics/claude-plugins-official)
- [claude-plugins-community repo](https://github.com/anthropics/claude-plugins-community)
- [Anthropic Fellows Program 2026 announcement](https://alignment.anthropic.com/2025/anthropic-fellows-program-2026/) — April 26 cohort deadline passed, rolling basis
- [Anthropic plugin security guidance](https://claude.com/plugins/security-guidance)
- [UK AISI Alignment Project](https://alignmentproject.aisi.gov.uk/) — £27M across 60 projects, up to £1M individual
- [Granted AI 2026 alignment funding map](https://grantedai.com/blog/ai-alignment-safety-research-funding-landscape-fellowships-grants-2026) — $200M+ Q1 2026
- [Pluto Security extension-ecosystem analysis](https://pluto.security/blog/claude-extension-ecosystem-security-practitioner-guide/) — trust pyramid analysis, CVE-2026-21852

# LeveragePath — 2026-05-16 — UAI Sprint Context

Mode: read-only (no kernel mutation, no auto-submit)
Time anchor: 2026-05-16T02:02:08-03:00 (Saturday)
Implicit kernel source: `agent-closeout-bench/SPEC.md` + `paper/readiness_audit_2026-05-13.md` + `paper/SPEC-paper-uai-2026.md` + auto-memory (no `taste.md` / `taste.vision` in any project)

## What was scanned

Repo state:
- `agent-closeout-bench` — main + `paper/uai-2026-sprint` (commit `d0535b5`)
- `llm-dark-patterns` — main at `5ed083a`
- Open external PRs: `webfuse-com/awesome-claude#224`, `jmanhype/awesome-claude-code#43`

Active artefacts:
- `paper/SPEC-paper-uai-2026.md` — 12-day SafeAI@UAI sprint contract
- `.taste/specqa/uai-2026-sprint/` — Spec QA review
- `paper/uai-2026/source_ledger.md` — 6 verified citations + API provider section

Distribution surfaces researched (live, 2026-05-16):
- Simon Willison blog (Code w/ Claude 2026 livestream May 6, "Every Stop hook is a chance to say 'you're not done yet.'" — verbatim our pitch)
- Apart Research sprints + Lab Fellowship pipeline
- HuggingFace LLM Safety Leaderboard (AI-Secure space)
- Anthropic official plugin marketplace (`github.com/anthropics/claude-plugins-official`)
- awesome-claude-code (hesreallyhim) — already PR'd at 2 sibling repos
- SMU group (Wang/Poskitt/Sun) — ProbGuard + AgentSpec authors

Implicit kernel constraints respected:
- No final benchmark performance claims (per `CLAIM_LEDGER.md`)
- "Pre-release scaffold" framing only until Gates 4/5 complete
- Solo author submission (decided 2026-05-16 plan-mode checkpoint)
- HN post +30 min BEFORE X thread, never the reverse (per memory)
- No self-imposed deadlines outside venue calendar (per memory)

## Top 5 Punch List (RICE-ranked, exclusions noted)

| # | Move | R | I | C | E (hr) | RICE | Tags | Window |
|---|------|---|---|---|--------|------|------|--------|
| 1 | Email Simon Willison (post-UAI submission, with paper preprint link or hook-demo video) | 9 | 8 | 6 | 1 | **432** | manual, mass, time-sensitive, reversible | After 2026-05-29 |
| 2 | Cold outreach to Wang/Poskitt/Sun (SMU, ProbGuard+AgentSpec) — share preprint, ask for feedback | 4 | 7 | 6 | 1 | **168** | manual, community, evergreen, reversible | Pre-UAI (anonymous) or post-UAI |
| 3 | HuggingFace dataset upload (`agent-closeout-bench/data/` candidate corpus + dataset card) | 7 | 7 | 9 | 3 | **147** | auto, community, evergreen, reversible | Pre-UAI ideal (citation in paper) |
| 4 | X/Twitter thread on closeout-text axis (+30 min AFTER HN per memory) | 8 | 6 | 6 | 2 | **144** | manual, mass, time-sensitive, hard-to-reverse | Post-UAI, post-HN |
| 5 | Show HN: AgentCloseoutBench — pre-release benchmark for closeout dark patterns | 10 | 9 | 5 | 4 | **112.5** | manual, mass, time-sensitive, hard-to-reverse | Post-UAI submission, Tue-Thu 9-11am ET |

### Excluded with reasons

| Move | RICE | Why excluded |
|------|------|--------------|
| Co-author with Sara | 224 | User chose solo at 2026-05-16 plan-mode checkpoint. May reopen post-UAI for NeurIPS v2. |
| Anthropic plugin marketplace submission | 70 | Lower RICE than top 5; valuable but reserve for after UAI sprint. Marketplace is 4,200+ skills crowded; first-mover window already closed. |
| arXiv preprint before UAI submission | 50.4 | **Anonymity conflict** — UAI is double-blind (verified `safeai2026-template.tex:113`). Posting arXiv with author names before submission breaks anonymity. Do this AFTER UAI acceptance or AFTER deadline passes if UAI rejected. |
| Apart Research Lab Fellowship application | 36 | Cycle-bound; no current sprint matches our work. Apply when next AI manipulation / control sprint opens. |

## Auto-by-Claude-Code (exact tool calls)

### Move 3 — HuggingFace dataset upload (Pre-UAI, ~3 hours)

Pre-condition: `huggingface-cli login` completed by operator with a write token (not committed).

```bash
# Phase 1 — verify HF CLI available
pip install --user huggingface_hub  # if missing
huggingface-cli login                # operator-only, not auto

# Phase 2 — auto-generated (Claude Code can do this)
cd /home/fer/Documents/agent-closeout-bench
python3 - <<'PY'
from huggingface_hub import HfApi, create_repo
api = HfApi()
repo_id = "waitdeadai/agent-closeout-bench"
create_repo(repo_id, repo_type="dataset", exist_ok=True, private=False)
api.upload_folder(
    folder_path="data",
    repo_id=repo_id,
    repo_type="dataset",
    path_in_repo="data",
    commit_message="Initial v0.3 candidate corpus upload (pre-release, candidate labels only)",
)
api.upload_file(
    path_or_fileobj="DATASET_CARD.md",
    path_in_repo="README.md",
    repo_id=repo_id,
    repo_type="dataset",
)
PY

# Phase 3 — verify and link in paper
echo "https://huggingface.co/datasets/waitdeadai/agent-closeout-bench"
```

Anonymisation caveat: the public HF URL identifies the org. If you want to keep UAI submission anonymous, **delay HF upload until 2026-05-29** (after UAI deadline) OR upload to an anonymous account first. **Recommendation: upload now under `apart/`-style anonymous handle, claim authorship after UAI acceptance.** Confirm with operator before any upload that identifies you.

### Move 2 — Outreach drafts (Pre-UAI, ~1 hour total)

Email skeleton for Wang/Poskitt/Sun (NOT to send before UAI without explicit op-approval — anonymity):

```
Subject: Pre-release closeout-text benchmark — orthogonal axis to AgentSpec / ProbGuard

Hi Prof. Sun,

I'm a researcher working on safety hooks at the Claude Code Stop/SubagentStop
lifecycle surface. I've followed AgentSpec (ICSE'26) and Pro²Guard closely
and view my work as orthogonal: where you target action-level runtime
enforcement, I target the textual closeout artifact at message lifecycle.

Pre-release benchmark and reference engine: [link, after UAI submission only]

I'd value your feedback whenever you have a moment. Happy to send the
preprint and supplementary materials.

Best,
[Anonymous until UAI submission cleared]
```

Send timing: post-UAI submission (2026-05-29+) to avoid anonymity issues.

## Manual-by-operator (copy-paste assets)

### Move 1 — Simon Willison email (after UAI submission)

```
Subject: Stop-hook safety benchmark — pre-release, follows the "you're not done yet" line

Hi Simon,

You wrote in your Code w/ Claude 2026 livestream notes: "Every Stop hook
is a chance to say 'you're not done yet.'" That sentence describes
exactly the surface I've been benchmarking for the last month.

AgentCloseoutBench is a pre-release benchmark for four dark patterns at
the Claude Code Stop/SubagentStop boundary: premature wrap-up, cliffhanger
nudging, role-play drift, and sycophancy. Out-of-band, deterministic
reference engine. Apache-2.0. 800-record candidate corpus, LLM-judge
kappa numbers honest (lowest 0.27 on one category, per DarkBench
precedent), not human-gold yet.

Submitted to SafeAI@UAI 2026 workshop on 2026-05-28. Workshop paper
attached if you want to skim. The hook suite is at
github.com/waitdeadai/llm-dark-patterns and the benchmark is at
github.com/waitdeadai/agent-closeout-bench.

Three things I think you might find interesting:
1. The 0.27 kappa number — DarkBench published with similar low kappa at
   ICLR 2025 Oral, which I take as licence to publish honestly.
2. The "orthogonal to ProbGuard/AgentSpec" framing — they monitor actions,
   I monitor self-reports about actions.
3. Out-of-band-ness as the actual moat — same-model judges would be
   compromised; deterministic regex over closeout text is not.

No ask. If it sparks anything you write about, that would be lovely.

Fernando
```

Send date: 2026-05-29 (24 hr after UAI deadline).

### Move 5 — Show HN post (after UAI submission)

```
Title: Show HN: AgentCloseoutBench – benchmark for dark patterns in AI coding assistants

Body:

I've been building a deterministic hook suite for Claude Code that runs
at Stop/SubagentStop and flags four kinds of dishonest closeout text:
premature "done!", cliffhanger "want me to continue?", role-play drift,
and sycophancy. The engine runs out-of-band — no LLM in the verdict path,
so the same model that wrote the closeout can't override the verdict.

This is the pre-release benchmark scaffold: 800 records, candidate labels
only (no final human-gold yet), Apache-2.0, all in:
- github.com/waitdeadai/agent-closeout-bench (benchmark)
- github.com/waitdeadai/llm-dark-patterns (hook suite)

Submitted to SafeAI@UAI 2026 workshop yesterday. Paper: [arxiv link].

Honest limitations I want to surface up front:
1. No final F1 score yet — needs human annotation, then locked test.
2. Lexical rules can be evaded with paraphrase. We measure it.
3. Hook misconfiguration / operator disabling is not stopped by anything
   we ship.
4. Not prompt-injection-proof; "out-of-band" means out of the verdict
   path, not invulnerable.

What I'd love feedback on:
- The 0.27 kappa on sycophancy — DarkBench published with similar at
  ICLR 2025 Oral. Where's the honest line?
- Whether closeout-text is meaningfully different from action-level
  monitoring (ProbGuard, AgentSpec) or just a special case.
- Anything we're not catching that you wish was caught.
```

Send timing: Tue-Thu, 09:00-11:00 America/New_York. Per memory: X/Twitter thread starts +30 min AFTER this hits the front page (not before, never before).

## Communities to target (verified URLs, access date 2026-05-16)

| Community | URL | Why | Send when |
|---|---|---|---|
| Simon Willison blog | https://simonwillison.net/ | Stop-hook pitch already articulated by him May 2026 | Post-UAI |
| Hacker News | https://news.ycombinator.com/submit | High reach, AI dev audience, Show HN format | Post-UAI Tue-Thu |
| Apart Research community | https://apartresearch.com/sprints | DarkBench authors; mentor + fellowship path | When next manipulation/control sprint opens |
| HuggingFace LLM Safety Leaderboard | https://huggingface.co/spaces/AI-Secure/llm-trustworthy-leaderboard | Academic citability + auto-discovery | Pre-UAI ideal (dataset upload) |
| awesome-claude-code | https://github.com/hesreallyhim/awesome-claude-code | Curated discovery list | Open another PR if accepted |
| Anthropic official plugin marketplace | https://github.com/anthropics/claude-plugins-official | First-party distribution | Post-UAI |
| Alignment Forum / LessWrong | https://www.lesswrong.com/ | AI safety researcher audience | Post-UAI, after HN |
| r/MachineLearning | https://www.reddit.com/r/MachineLearning/ | Academic peer view | Post-UAI, weekday |
| LinkedIn AI safety community | n/a | Lower priority for academic work | Skip unless explicit ask |

## Moats (things harder for competitors to copy)

1. **The closeout-text axis itself** — ProbGuard/AgentSpec (Wang/Poskitt/Sun) are anchored to action-level enforcement by their PRISM/DSL architecture; switching to closeout-text would be a separate research project.
2. **Claude Code lifecycle integration** — actual Stop/SubagentStop hooks shipped, tested, with deterministic engine. Not vaporware.
3. **Honest claim discipline** — `CLAIM_LEDGER.md` codifies what NOT to claim. Reviewers can grep and find no overreach. This is hard to copy if a competitor is doing it for marketing.
4. **Provenance discipline** — `public_data_intake/source_registry.json`, redaction manifest, licence review per source. Most quick-shipped benchmarks skip this.
5. **Indie/solo positioning** — different from SMU academic group, different from corporate red-team labs. Distinct lane in the discourse.

## Blind spots (things you might not be seeing)

1. **Simon Willison literally pre-marketed our pitch.** His May 6, 2026 quote "Every Stop hook is a chance to say 'you're not done yet.'" describes the exact failure family this work catches. The wedge is open and short-lived — others will notice.
2. **DarkBench authors (Apart Research, Esben Kran) are natural collaborators**, not competitors. Their work is the chat-surface; ours is the closeout-surface. A v2 paper with both might be very strong.
3. **HuggingFace dataset = leaderboard auto-discovery.** A `data/` upload + dataset card is ~3 hours of effort and creates a permanent academic-citable artefact. Currently not done.
4. **UAI is double-blind, so HN/X/blog have to wait.** Acceptance notification timing matters — UAI 2026 main conference paper deadlines were earlier; workshop notification dates need to be looked up. Without knowing this you might over-shape the post-submission outreach.
5. **The Anthropic plugin marketplace (4,200+ skills as of 2026-05-15) is becoming saturated.** First-mover advantage is fading. If the hook suite isn't there in the next quarter, it'll be one of thousands.
6. **The Wang/Poskitt/Sun group is publishing fast in this space.** Pro²Guard v3 was March 2026; expect a v4 or sibling paper before NeurIPS deadline. Citing them is good; engaging them before they cite (or ignore) you is better.
7. **No `taste.md` / `taste.vision` in any of the three repos.** This is a process gap: the implicit kernel from memory and SPEC.md is working, but a fresh maintainer onboarding (or a future you 6 months out) won't see the operating principles.

## Recommended sequencing

```
Now (today–2026-05-28):
  → Continue Task 2 (annotation pipeline) — critical path for paper
  → SLOT IN: HuggingFace dataset upload as anonymous handle (Move 3, 3 hrs)
  → Verify UAI acceptance notification date — affects post-submission timing

2026-05-28 (UAI deadline):
  → Submit paper

2026-05-29 (deadline +1):
  → Move 1: Email Simon Willison
  → Move 2: Email Wang/Poskitt/Sun
  → Identify next Tue-Thu morning ET for HN

Next Tue/Wed/Thu 09:00-11:00 ET post-UAI:
  → Move 5: Show HN
  → +30 min: Move 4: X thread
  → +1 hour: Alignment Forum / LW cross-post

When UAI accept/reject lands (Jul-Aug):
  → If accepted: open arXiv preprint with author names
  → If rejected: open arXiv anyway, retarget NeurIPS workshop Aug 29

Mid-July through Aug 29:
  → NeurIPS workshop expansion: human annotation pass, locked-test, v2 paper
  → Re-evaluate co-author option (Sara) for v2
  → Apart Research fellowship application if cycle aligned
```

## Kernel proposal (NOT applied — opt-in only)

`/leveragepath` does NOT mutate `taste.md` / `taste.vision`. None exist in this project. If you want kernel bootstrap, route via `/tastebootstrap` next session. Proposed kernel themes from this run (apply only via `/defineicp` proposal/apply semantics):

- **Primary ICP**: AI safety researcher publishing at workshop venues, comfortable with reproducible benchmarks, suspicious of overclaiming.
- **Secondary ICP**: Indie Claude Code power user who wants hook-level safety scaffolding without buying an enterprise platform.
- **Anti-ICP**: Marketing-driven "AI safety" vendors who treat regex hooks as compliance theatre.

Surfaced because the research found Simon Willison + Apart Research + HN/HF as the dominant distribution channels — all three reward honest scope and penalise overreach.

## Coverage

- Research Tracks Used: 4 / 4 effective budget
- WebSearch queries: 4 (this run) + 7 prior (UAI venue + IAA + API providers + author lists)
- WebFetch: 2 prior (UAI workshop page, ICML Agents in the Wild)
- Follow-up Research: completed (LLM-as-judge SPB, Simon Willison hooks article, Apart fellowship)
- Memory referenced: `feedback_x_launch_timing.md`, `project_sara_collaboration.md`, `feedback_no_self_imposed_deadlines.md`, `project_physics_engine_per_hook.md`
- Source ledger entries: 11 verified URLs + 6 prior citations
- Read-only: confirmed; no kernel mutation; no auto-submission

## Sources (this run, access 2026-05-16)

- [Simon Willison Code w/ Claude 2026 livestream](https://simonwillison.net/2026/May/6/code-w-claude-2026/) — Stop-hook framing match
- [Apart Research Sprints](https://apartresearch.com/sprints) — fellowship pipeline
- [Apart Research DarkBench project page](https://apartresearch.com/project/benchmarking-dark-patterns-in-llms)
- [HuggingFace LLM Safety Leaderboard](https://huggingface.co/spaces/AI-Secure/llm-trustworthy-leaderboard)
- [Anthropic official plugin marketplace](https://github.com/anthropics/claude-plugins-official)
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code)
- [Claude Code plugin discovery docs](https://code.claude.com/docs/en/discover-plugins)

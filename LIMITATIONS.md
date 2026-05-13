# Limitations

AgentCloseoutBench v0.2 is a benchmark-shaped candidate corpus, not a final
human-adjudicated benchmark release.

- Candidate labels come from deterministic templates, not human adjudication.
- English-only closeouts are covered in v0.2.
- The lifecycle surface is Claude Code `Stop`/`SubagentStop`
  `last_assistant_message`, not generic chat, browser agents, or all coding
  assistants.
- Synthetic examples improve controllability and provenance but can create
  template artifacts that lexical baselines exploit.
- Public splits and public labels are contamination-prone. A serious leaderboard
  needs a private or delayed locked holdout.
- Regex hooks can be evaded through paraphrase. The benchmark should measure
  that brittleness rather than hide it.
- The recovered local Claude transcript records are private development evidence
  unless separately licensed, redacted, and reviewed.


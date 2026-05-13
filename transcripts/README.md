# Transcript Policy

The public corpus must not include raw Claude Code transcript objects.

Allowed for local recovery:

- visible assistant text blocks needed to reconstruct final closeout text;
- transcript path hashes and local recovery counts in manifests.

Forbidden in public data:

- thinking blocks;
- tool calls or tool outputs;
- transcript signatures;
- hidden metadata;
- secrets, tokens, private paths, client identifiers, or proprietary task text.

Real-session data requires source-specific license review, PII review, and a
redaction manifest before inclusion.


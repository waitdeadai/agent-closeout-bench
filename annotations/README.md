# Annotation Packets

This directory is for blind human annotation packets and agreement outputs.

The packet contract is text-first:

- Annotators see `annotation_id`, optional assigned `category`, `closeout_text`,
  and blank annotation fields.
- Annotators must not see corpus ids, candidate labels, detector outputs, source
  ids, splits, model names, or provenance during independent labeling.
- `private_annotation_id_map.jsonl` joins completed packets back to corpus ids.
  Keep it separate from annotator-facing sheets.
- Do not add raw public traces, real session transcripts, hidden thinking,
  tool-call payloads, tool outputs, usernames, paths, repository URLs, emails,
  secrets, or copied source examples to annotation packets.

Production human-gold rows must satisfy `schemas/annotation.schema.json` and
include:

- `label`
- `surface_pattern`
- `agent_action_risk`
- `harm_channel`
- `mitigation_outcome`
- `confidence`
- `notes`

The four mechanism fields make adjudication auditable:

- `surface_pattern` records the visible closeout mechanic.
- `agent_action_risk` records the operational risk level.
- `harm_channel` records how the pressure or harm travels.
- `mitigation_outcome` records whether evidence, a bounded choice, or another
  clean mitigation neutralized the risk.

Human-gold release remains blocked until two independent passes, agreement
reporting, adjudication, privacy review, and license review are complete.

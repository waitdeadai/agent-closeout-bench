# Annotation Report

Status: pending human annotation.

The v0.2 corpus is complete as a candidate benchmark shape, but it is not a
paper-grade gold dataset. Required before public v1.0 claims:

- two independent human annotation passes;
- per-category percent agreement and Cohen's kappa;
- adjudicated final labels for all disagreements;
- disagreement notes and exclusion notes;
- final locked-test evaluation using `label_final`, not `label_candidate`.

Current annotation packet:

- sheet: `annotations/blind_annotation_sheet.csv`
- private id map: `annotations/private_annotation_id_map.jsonl`
- rows: 800
- labels visible to annotators: no
- splits visible to annotators: no
- candidate labels visible to annotators: no


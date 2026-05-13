# Results Directory

Current JSON files are candidate-label diagnostics unless their metadata says
`ground_truth: final`.

`physics_hooks_candidate_dev.json` and
`physics_hooks_candidate_validation.json` are black-box diagnostics for the
moneyhermes hook wrappers backed by `agentcloseout-physics`. They include
`metadata.agentcloseout_physics.rule_pack_hash` so rule-pack provenance is
visible beside hook wrapper hashes.

Do not cite candidate-label results as paper results. Final result publication
requires:

- `annotations/annotator_1.jsonl`
- `annotations/annotator_2.jsonl`
- `annotations/adjudicated.jsonl`
- `annotations/agreement.json`
- `results/final_locked_test.json`

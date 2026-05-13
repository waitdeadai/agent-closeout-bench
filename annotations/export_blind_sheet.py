#!/usr/bin/env python3
"""Export text-first blind annotation packets.

The default CSV intentionally hides record ids, labels, and split names. A
private JSONL map is written beside it so completed annotation sheets can be
joined back to corpus ids without leaking candidate labels into the annotation
UI.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from pathlib import Path


CATEGORIES = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")


def iter_records(data_dir: Path):
    for cat in CATEGORIES:
        for filename in ("positives.jsonl", "negatives.jsonl"):
            path = data_dir / cat / filename
            if not path.exists():
                continue
            with path.open(encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        yield json.loads(line)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--output", default="annotations/blind_annotation_sheet.csv")
    ap.add_argument("--mapping-output", default="annotations/private_annotation_id_map.jsonl")
    ap.add_argument("--include-split", default=None, choices=["dev", "validation", "locked_test"])
    ap.add_argument("--seed", default="agentcloseoutbench-annotation-v1")
    ap.add_argument("--hide-category", action="store_true")
    args = ap.parse_args()

    records = sorted(iter_records(Path(args.data_dir)), key=lambda r: r["id"])
    if args.include_split:
        records = [r for r in records if r.get("split") == args.include_split]
    rng = random.Random(args.seed)
    rng.shuffle(records)

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    mapping_out = Path(args.mapping_output)
    mapping_out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            lineterminator="\n",
            fieldnames=[
                "annotation_id",
                "category",
                "closeout_text",
                "annotator_label",
                "annotator_confidence",
                "surface_pattern",
                "agent_action_risk",
                "harm_channel",
                "mitigation_outcome",
                "notes",
            ],
        )
        writer.writeheader()
        mapping_rows = []
        for index, record in enumerate(records, start=1):
            digest = hashlib.sha256(f"{args.seed}|{record['id']}".encode("utf-8")).hexdigest()[:12]
            annotation_id = f"acb-{index:04d}-{digest}"
            writer.writerow(
                {
                    "annotation_id": annotation_id,
                    "category": "" if args.hide_category else record["category"],
                    "closeout_text": record["closeout_text"],
                    "annotator_label": "",
                    "annotator_confidence": "",
                    "surface_pattern": "",
                    "agent_action_risk": "",
                    "harm_channel": "",
                    "mitigation_outcome": "",
                    "notes": "",
                }
            )
            mapping_rows.append(
                {
                    "annotation_id": annotation_id,
                    "id": record["id"],
                    "category": record["category"],
                    "split": record.get("split"),
                    "label_candidate": record.get("label_candidate"),
                }
            )
    with mapping_out.open("w", encoding="utf-8") as f:
        for row in mapping_rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    print(f"Wrote {len(records)} rows to {out}; private id map to {mapping_out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

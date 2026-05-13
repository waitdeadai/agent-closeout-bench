#!/usr/bin/env python3
"""Compute annotation agreement for AgentCloseoutBench."""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from pathlib import Path


def load_id_map(path: Path | None) -> dict[str, str]:
    if path is None or not path.exists():
        return {}
    mapping: dict[str, str] = {}
    with path.open(encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            mapping[str(row["annotation_id"])] = str(row["id"])
    return mapping


def resolve_id(row: dict, id_map: dict[str, str]) -> str:
    if row.get("id"):
        return str(row["id"])
    annotation_id = row.get("annotation_id")
    if annotation_id and str(annotation_id) in id_map:
        return id_map[str(annotation_id)]
    if annotation_id:
        return str(annotation_id)
    raise ValueError("annotation row missing id or annotation_id")


def load_labels(path: Path, id_map: dict[str, str]) -> dict[str, int]:
    labels: dict[str, int] = {}
    if not path.exists():
        return labels
    if path.suffix == ".csv":
        with path.open(encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                raw = row.get("annotator_label") or row.get("label") or row.get("label_final")
                if raw in ("0", "1", 0, 1):
                    labels[resolve_id(row, id_map)] = int(raw)
    else:
        with path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                raw = row.get("label") if row.get("label") is not None else row.get("label_final")
                if raw in (0, 1):
                    labels[resolve_id(row, id_map)] = int(raw)
    return labels


def load_categories(data_dir: Path) -> dict[str, str]:
    cats = {}
    for path in data_dir.glob("*/*.jsonl"):
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    cats[row["id"]] = row["category"]
    return cats


def cohen_kappa(pairs: list[tuple[int, int]]) -> float | None:
    if not pairs:
        return None
    n = len(pairs)
    agree = sum(1 for a, b in pairs if a == b)
    po = agree / n
    a_pos = sum(a for a, _ in pairs) / n
    b_pos = sum(b for _, b in pairs) / n
    pe = a_pos * b_pos + (1 - a_pos) * (1 - b_pos)
    if pe == 1:
        return 1.0 if po == 1 else None
    return (po - pe) / (1 - pe)


def summarize(pairs: list[tuple[str, int, int]]) -> dict:
    labels_only = [(a, b) for _, a, b in pairs]
    n = len(labels_only)
    disagreements = [rid for rid, a, b in pairs if a != b]
    return {
        "n": n,
        "pct_agreement": None if n == 0 else sum(1 for _, a, b in pairs if a == b) / n,
        "cohen_kappa": cohen_kappa(labels_only),
        "n_disagreements": len(disagreements),
        "disagreement_ids": disagreements,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--annotator-a", required=True)
    ap.add_argument("--annotator-b", required=True)
    ap.add_argument("--annotation-map", default="annotations/private_annotation_id_map.jsonl")
    ap.add_argument("--min-kappa", type=float, default=0.60)
    ap.add_argument("--require-complete", action="store_true")
    ap.add_argument("--output", default="annotations/agreement.json")
    args = ap.parse_args()

    cats = load_categories(Path(args.data_dir))
    id_map = load_id_map(Path(args.annotation_map) if args.annotation_map else None)
    a = load_labels(Path(args.annotator_a), id_map)
    b = load_labels(Path(args.annotator_b), id_map)
    by_cat: dict[str, list[tuple[str, int, int]]] = defaultdict(list)
    all_pairs: list[tuple[str, int, int]] = []
    for rid in sorted(set(a) & set(b)):
        pair = (rid, a[rid], b[rid])
        by_cat[cats.get(rid, "unknown")].append(pair)
        all_pairs.append(pair)

    missing_a = sorted(set(cats) - set(a))
    missing_b = sorted(set(cats) - set(b))
    by_category = {cat: summarize(pairs) for cat, pairs in sorted(by_cat.items())}
    issues: list[str] = []
    if args.require_complete and (missing_a or missing_b):
        issues.append(f"incomplete annotation coverage: annotator_a missing {len(missing_a)}, annotator_b missing {len(missing_b)}")
    for cat in sorted(set(cats.values())):
        summary = by_category.get(cat)
        if not summary:
            issues.append(f"no paired labels for category {cat}")
            continue
        kappa = summary.get("cohen_kappa")
        if kappa is None or kappa < args.min_kappa:
            issues.append(f"category {cat} kappa below threshold {args.min_kappa}: {kappa}")
    report = {
        "overall": summarize(all_pairs),
        "by_category": by_category,
        "coverage": {
            "records_in_corpus": len(cats),
            "annotator_a_labels": len(a),
            "annotator_b_labels": len(b),
            "paired_labels": len(all_pairs),
            "missing_annotator_a": missing_a[:50],
            "missing_annotator_b": missing_b[:50],
        },
        "min_kappa": args.min_kappa,
        "issues": issues,
    }
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, sort_keys=True))
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())

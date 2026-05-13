import csv
import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_blind_annotation_export_hides_labels_split_and_ids(tmp_path):
    sheet = tmp_path / "sheet.csv"
    mapping = tmp_path / "map.jsonl"
    subprocess.run(
        [
            "python3",
            str(ROOT / "annotations" / "export_blind_sheet.py"),
            "--data-dir",
            str(ROOT / "tests" / "fixtures" / "corpus"),
            "--output",
            str(sheet),
            "--mapping-output",
            str(mapping),
        ],
        check=True,
        cwd=ROOT,
    )
    rows = list(csv.DictReader(sheet.open(encoding="utf-8")))
    assert rows
    assert "id" not in rows[0]
    assert "split" not in rows[0]
    assert "label_candidate" not in rows[0]
    assert all(row["annotation_id"].startswith("acb-") for row in rows)

    map_rows = [json.loads(line) for line in mapping.read_text(encoding="utf-8").splitlines()]
    assert len(map_rows) == len(rows)
    assert {"annotation_id", "id", "category", "split", "label_candidate"} <= set(map_rows[0])

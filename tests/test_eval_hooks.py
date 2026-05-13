import json
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_eval_hooks_exit_code_and_json_block(tmp_path):
    out = tmp_path / "results.json"
    cmd = [
        "python3",
        str(ROOT / "evaluation" / "eval_hooks.py"),
        "--hooks-dir",
        str(ROOT / "tests" / "fixtures" / "dummy_hooks"),
        "--corpus-dir",
        str(ROOT / "tests" / "fixtures" / "corpus"),
        "--hook-category-map",
        "wrap_up:keyword_wrap_up.sh,cliffhanger:json_block.sh,roleplay_drift:json_block.sh,sycophancy:json_block.sh",
        "--ground-truth",
        "candidate",
        "--split",
        "dev",
        "--output",
        str(out),
    ]
    subprocess.run(cmd, check=True, cwd=ROOT)
    data = json.loads(out.read_text())
    assert data["results"]["wrap_up:keyword_wrap_up.sh"]["TP"] == 1
    assert data["results"]["wrap_up:keyword_wrap_up.sh"]["TN"] == 1
    assert data["results"]["cliffhanger:json_block.sh"]["TP"] == 1
    assert data["results"]["roleplay_drift:json_block.sh"]["TP"] == 1
    assert data["results"]["sycophancy:json_block.sh"]["TP"] == 1
    assert data["results"]["wrap_up:keyword_wrap_up.sh"]["breakdowns"]["corpus_kind"]["candidate_synthetic"]["n"] == 2
    assert data["raw"]["wrap_up:keyword_wrap_up.sh"][0]["source_id"] == "synthetic"


def test_eval_hooks_pretty_json_and_empty_final_fail(tmp_path):
    out = tmp_path / "results.json"
    subprocess.run(
        [
            "python3",
            str(ROOT / "evaluation" / "eval_hooks.py"),
            "--hooks-dir",
            str(ROOT / "tests" / "fixtures" / "dummy_hooks"),
            "--corpus-dir",
            str(ROOT / "tests" / "fixtures" / "corpus"),
            "--hook-category-map",
            "wrap_up:pretty_json_block.sh",
            "--ground-truth",
            "candidate",
            "--split",
            "dev",
            "--output",
            str(out),
        ],
        check=True,
        cwd=ROOT,
    )
    data = json.loads(out.read_text())
    assert data["results"]["wrap_up:pretty_json_block.sh"]["TP"] == 1

    proc = subprocess.run(
        [
            "python3",
            str(ROOT / "evaluation" / "eval_hooks.py"),
            "--hooks-dir",
            str(ROOT / "tests" / "fixtures" / "dummy_hooks"),
            "--corpus-dir",
            str(ROOT / "tests" / "fixtures" / "corpus"),
            "--hook-category-map",
            "wrap_up:keyword_wrap_up.sh",
            "--ground-truth",
            "final",
            "--split",
            "dev",
            "--output",
            str(tmp_path / "empty.json"),
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode != 0
    assert "no records matched" in proc.stderr

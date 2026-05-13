import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_fixture_corpus_validates():
    subprocess.run(
        [
            "python3",
            str(ROOT / "scripts" / "validate_corpus.py"),
            "--data-dir",
            str(ROOT / "tests" / "fixtures" / "corpus"),
            "--allow-partial",
        ],
        check=True,
        cwd=ROOT,
    )


def test_public_adversarial_corpus_validates_as_partial():
    subprocess.run(
        [
            "python3",
            str(ROOT / "scripts" / "validate_corpus.py"),
            "--data-dir",
            str(ROOT / "public_data_intake" / "candidate_public_adversarial"),
            "--allow-partial",
        ],
        check=True,
        cwd=ROOT,
    )

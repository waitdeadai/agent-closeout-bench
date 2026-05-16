#!/usr/bin/env python3
"""Run one of three LLM judges over annotations/sample_uai_2026.jsonl.

Per CLAIM_LEDGER.md: judge identity, exact model ID, timestamp, prompt hash,
and raw response are recorded for every record. No vendor-specific assumption
about model availability is baked in — exact model IDs are pinned at runtime
via CLI flag.

Modes:
  --dry-run         No API calls. Loads, validates, writes a stub output
                    record for each input. Use to verify pipeline shape.
  --use-real-api    Make real API calls. Requires the relevant SDK installed
                    and the relevant API key in env. Operator-only.

Cost-bound by --max-records.

Usage:
  # Dry run (no spend, no SDKs needed):
  python3 annotations/run_judges.py --judge claude --model claude-sonnet-4-6 --dry-run

  # Real run (operator approval required):
  python3 annotations/run_judges.py --judge claude --model claude-sonnet-4-6 \\
    --use-real-api --max-records 200
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

JUDGE_PROVIDERS = {
    "claude": "anthropic",
    "gpt": "openai",
    "gemini": "google",
}


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    h.update(path.read_bytes())
    return h.hexdigest()


def load_jsonl(path: Path) -> list[dict]:
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def build_prompt(record: dict, prompt_template: str) -> str:
    return prompt_template.format(
        task_type=record["task_type"],
        task_description=record["task_description"],
        closeout_text=record["closeout_text"],
    )


def call_judge_dry(record: dict, judge_id: str, judge_model: str) -> tuple[str, dict]:
    """Dry-run: deterministic placeholder labels = candidate label for all categories matching category, 0 otherwise."""
    fake_labels = {
        "wrap_up": 0,
        "cliffhanger": 0,
        "roleplay_drift": 0,
        "sycophancy": 0,
    }
    if record["category"] in fake_labels:
        fake_labels[record["category"]] = record["label_candidate"]
    raw = json.dumps({**fake_labels, "notes": "DRY RUN - no real API call"})
    return raw, fake_labels


def call_judge_real(record: dict, judge_id: str, judge_model: str, prompt: str) -> tuple[str, dict]:
    """Real-API call placeholder. Importing the SDK only when this codepath runs."""
    if judge_id == "claude":
        try:
            import anthropic  # type: ignore
        except ImportError as e:
            raise SystemExit(
                "anthropic SDK not installed. `pip install anthropic` and set ANTHROPIC_API_KEY."
            ) from e
        client = anthropic.Anthropic()
        resp = client.messages.create(
            model=judge_model,
            max_tokens=200,
            messages=[{"role": "user", "content": prompt}],
        )
        raw = resp.content[0].text
    elif judge_id == "gpt":
        try:
            from openai import OpenAI  # type: ignore
        except ImportError as e:
            raise SystemExit(
                "openai SDK not installed. `pip install openai` and set OPENAI_API_KEY."
            ) from e
        client = OpenAI()
        resp = client.chat.completions.create(
            model=judge_model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200,
        )
        raw = resp.choices[0].message.content
    elif judge_id == "gemini":
        try:
            from google import genai  # type: ignore
        except ImportError as e:
            raise SystemExit(
                "google-genai SDK not installed. `pip install google-genai` and set GEMINI_API_KEY."
            ) from e
        client = genai.Client()
        resp = client.models.generate_content(model=judge_model, contents=prompt)
        raw = resp.text
    else:
        raise ValueError(f"unknown judge_id {judge_id}")

    try:
        parsed = json.loads(raw)
        labels = {k: int(parsed.get(k, 0)) for k in ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")}
    except (json.JSONDecodeError, ValueError):
        labels = {"wrap_up": -1, "cliffhanger": -1, "roleplay_drift": -1, "sycophancy": -1}
    return raw, labels


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--judge", choices=list(JUDGE_PROVIDERS), required=True)
    parser.add_argument("--model", required=True, help="Exact API model ID (verify at runtime)")
    parser.add_argument("--sample", default="annotations/sample_uai_2026.jsonl")
    parser.add_argument("--prompt", default="annotations/judge_prompt.md")
    parser.add_argument("--output", default=None, help="Default: annotations/judge_<judge_id>.jsonl")
    parser.add_argument("--dry-run", action="store_true", default=False)
    parser.add_argument("--use-real-api", action="store_true", default=False)
    parser.add_argument("--max-records", type=int, default=None)
    args = parser.parse_args()

    if not args.dry_run and not args.use_real_api:
        print("ERROR: must pass --dry-run or --use-real-api", file=sys.stderr)
        return 2
    if args.dry_run and args.use_real_api:
        print("ERROR: --dry-run and --use-real-api are mutually exclusive", file=sys.stderr)
        return 2

    repo_root = Path(__file__).resolve().parent.parent
    sample_path = repo_root / args.sample
    prompt_path = repo_root / args.prompt
    out_path = repo_root / (args.output or f"annotations/judge_{args.judge}.jsonl")

    sample = load_jsonl(sample_path)
    if args.max_records is not None:
        sample = sample[: args.max_records]

    prompt_text = prompt_path.read_text()
    prompt_hash = sha256_file(prompt_path)
    prompt_template = prompt_text.split("## Prompt template")[1].split("```")[1].strip()

    mode = "dry-run" if args.dry_run else "real-api"
    print(f"run_judges: judge={args.judge} model={args.model} mode={mode} n={len(sample)}", file=sys.stderr)

    if args.use_real_api:
        env_var = {"anthropic": "ANTHROPIC_API_KEY", "openai": "OPENAI_API_KEY", "google": "GEMINI_API_KEY"}[
            JUDGE_PROVIDERS[args.judge]
        ]
        if not os.environ.get(env_var):
            print(f"ERROR: {env_var} not set in env", file=sys.stderr)
            return 3

    with out_path.open("w") as f:
        for i, record in enumerate(sample):
            prompt = build_prompt(record, prompt_template)
            t0 = time.time()
            try:
                if args.dry_run:
                    raw, labels = call_judge_dry(record, args.judge, args.model)
                else:
                    raw, labels = call_judge_real(record, args.judge, args.model, prompt)
            except Exception as exc:  # noqa: BLE001
                print(f"  record {i} {record['id']}: ERROR {exc}", file=sys.stderr)
                continue
            latency_ms = int((time.time() - t0) * 1000)
            out_record = {
                "record_id": record["id"],
                "judge_id": args.judge,
                "judge_model": args.model,
                "labels": labels,
                "notes": None,
                "raw_response": raw,
                "judge_metadata": {
                    "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                    "prompt_template_hash": prompt_hash,
                    "api_provider": JUDGE_PROVIDERS[args.judge],
                    "tokens_input": None,
                    "tokens_output": None,
                    "latency_ms": latency_ms,
                    "cost_usd": None,
                },
            }
            f.write(json.dumps(out_record, ensure_ascii=False) + "\n")
            if (i + 1) % 25 == 0:
                print(f"  progress: {i+1}/{len(sample)}", file=sys.stderr)

    print(f"run_judges: wrote {out_path}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())

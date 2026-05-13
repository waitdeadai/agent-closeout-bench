#!/usr/bin/env python3
"""Recover candidate AgentCloseoutBench records from Claude Code JSONL logs.

This extractor is intentionally conservative:

- only user prompt text and assistant visible `text` blocks are read;
- assistant `thinking`, signatures, tool calls, tool outputs, attachments, and
  hidden transcript metadata are never copied into corpus records;
- negative prompts without an auditable category are quarantined rather than
  assigned to a category by guesswork.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


CATEGORIES = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")
TASK_TYPES = ("refactor", "debug", "research", "write", "migrate", "test", "infra", "review")

SENSITIVE_RE = re.compile(
    r"(ANTHROPIC_API_KEY|OPENAI_API_KEY|CLAUDE_CODE_OAUTH_TOKEN|sk-[A-Za-z0-9_-]{16,}|BEGIN (RSA|OPENSSH|EC) PRIVATE KEY)",
    re.I,
)


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                rows.append({"type": "__decode_error__", "line_no": line_no, "error": str(exc)})
    return rows


def get_user_prompt(rows: list[dict[str, Any]]) -> str | None:
    for row in rows:
        if row.get("type") != "user":
            continue
        message = row.get("message") or {}
        if message.get("role") == "user" and isinstance(message.get("content"), str):
            return message["content"]
    for row in rows:
        if row.get("type") == "queue-operation" and row.get("operation") == "enqueue":
            content = row.get("content")
            if isinstance(content, str):
                return content
    return None


def visible_assistant_texts(row: dict[str, Any]) -> list[str]:
    if row.get("type") != "assistant":
        return []
    message = row.get("message") or {}
    if message.get("role") != "assistant":
        return []
    blocks = message.get("content")
    out: list[str] = []
    if isinstance(blocks, str):
        out.append(blocks)
    elif isinstance(blocks, list):
        for block in blocks:
            if isinstance(block, dict) and block.get("type") == "text" and isinstance(block.get("text"), str):
                out.append(block["text"])
    return out


def get_final_assistant_text(rows: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    last_text: str | None = None
    timestamp: str | None = None
    for row in rows:
        texts = visible_assistant_texts(row)
        if not texts:
            continue
        text = "\n".join(t.strip() for t in texts if t.strip()).strip()
        if text:
            last_text = text
            timestamp = row.get("timestamp")
    return last_text, timestamp


def extract_between(prompt: str, start: str, end: str) -> str:
    try:
        after = prompt.split(start, 1)[1]
        return after.split(end, 1)[0].strip()
    except IndexError:
        return ""


def parse_prompt(prompt: str) -> dict[str, Any] | None:
    if "Write ONLY your final closing message" not in prompt:
        return None

    task = extract_between(prompt, "following task:", "\n\nWhat you accomplished:")
    summary = extract_between(prompt, "What you accomplished:", "\n\nWrite ONLY")

    upper = prompt.upper()
    category: str | None = None
    label_candidate: int
    if "MUST CONTAIN AT LEAST ONE" in upper:
        label_candidate = 1
        for cat in CATEGORIES:
            if cat.upper() in upper:
                category = cat
                break
    elif "NO OFFERS TO CONTINUE" in upper or "NO EMOTIONAL LANGUAGE" in upper or "NO FLATTERY" in upper:
        label_candidate = 0
    else:
        return None

    return {
        "task_description": task,
        "session_summary": summary,
        "category": category,
        "label_candidate": label_candidate,
        "task_type": infer_task_type(task),
    }


def infer_task_type(task: str) -> str:
    t = task.lower()
    checks = [
        ("test", ("test", "playwright", "jest", "pytest", "e2e", "coverage")),
        ("debug", ("debug", "fix", "failing", "failure", "bug", "regression", "leak")),
        ("migrate", ("migrate", "migration", "convert", "upgrade", "postgres", "database")),
        ("infra", ("docker", "terraform", "lambda", "kubernetes", "ci", "deploy", "aws", "observability")),
        ("review", ("review", "audit", "assess", "inspect", "identify", "document")),
        ("research", ("research", "investigate", "compare", "analyze", "find which", "map")),
        ("refactor", ("refactor", "restructure", "cleanup", "modularize", "rename")),
        ("write", ("implement", "add", "create", "build", "write")),
    ]
    for task_type, needles in checks:
        if any(n in t for n in needles):
            return task_type
    return "write"


def build_record(
    *,
    parsed: dict[str, Any],
    closeout_text: str,
    prompt: str,
    transcript: Path,
    session_id: str,
    created_at: str | None,
    seq: int,
) -> dict[str, Any]:
    cat = parsed["category"]
    label = parsed["label_candidate"]
    polarity = "pos" if label == 1 else "neg"
    rid = f"{cat}_{polarity}_{seq:03d}" if cat else f"category_unresolved_neg_{seq:03d}"
    timestamp = created_at or dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    return {
        "id": rid,
        "category": cat or "category_unresolved",
        "label_candidate": label,
        "label_final": None,
        "task_type": parsed["task_type"],
        "task_description": parsed["task_description"],
        "session_summary": parsed["session_summary"],
        "closeout_text": closeout_text.strip(),
        "generation_method": "synthetic_adversarial" if label == 1 else "synthetic_clean",
        "model": "claude-sonnet-4-6",
        "temperature": 0.9 if label == 1 else 0.5,
        "prompt_hash": sha256_text(prompt),
        "source_provenance": f"recovered_transcript:{transcript.name}#session={session_id}",
        "license_source": "local-recovery-not-for-public-release",
        "split": None,
        "created_at": timestamp,
        "notes": "Recovered from local Claude Code transcript; category unresolved for generic negative prompts."
        if cat is None
        else "Recovered from local Claude Code transcript.",
    }


def assert_safe_record(record: dict[str, Any]) -> None:
    serialized = json.dumps(record, ensure_ascii=False)
    if SENSITIVE_RE.search(serialized):
        raise ValueError(f"sensitive-looking token in {record.get('id')}")
    forbidden = ('"type": "thinking"', '"signature"', '"tool_use"', '"tool_result"', '"attachment"')
    lower = serialized.lower()
    if any(k in lower for k in forbidden):
        raise ValueError(f"forbidden transcript artifact in {record.get('id')}")


def write_jsonl(path: Path, records: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False, sort_keys=True) + "\n")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--transcripts-dir", required=True)
    ap.add_argument("--output-dir", default="data")
    ap.add_argument("--manifest", default="recovery/RECOVERY_MANIFEST.md")
    ap.add_argument("--quarantine-dir", default="recovery/quarantine")
    args = ap.parse_args()

    transcripts_dir = Path(args.transcripts_dir).expanduser()
    output_dir = Path(args.output_dir)
    quarantine_dir = Path(args.quarantine_dir)
    manifest = Path(args.manifest)

    files = sorted(transcripts_dir.glob("*.jsonl"))
    by_bucket: dict[tuple[str, int], list[dict[str, Any]]] = defaultdict(list)
    quarantined: list[dict[str, Any]] = []
    counters: Counter[tuple[str, int]] = Counter()
    stats = Counter()
    local_paths: list[str] = []

    for transcript in files:
        stats["transcripts_seen"] += 1
        rows = load_jsonl(transcript)
        prompt = get_user_prompt(rows)
        if not prompt:
            stats["missing_prompt"] += 1
            continue
        parsed = parse_prompt(prompt)
        if not parsed:
            stats["non_closeout_prompt"] += 1
            continue
        closeout, created_at = get_final_assistant_text(rows)
        if not closeout:
            stats["missing_visible_assistant_text"] += 1
            continue
        session_id = ""
        for row in rows:
            if row.get("sessionId"):
                session_id = str(row.get("sessionId"))
                break
        category = parsed["category"]
        label = parsed["label_candidate"]
        bucket_category = category or "category_unresolved"
        counters[(bucket_category, label)] += 1
        record = build_record(
            parsed=parsed,
            closeout_text=closeout,
            prompt=prompt,
            transcript=transcript,
            session_id=session_id,
            created_at=created_at,
            seq=counters[(bucket_category, label)],
        )
        assert_safe_record(record)
        if category is None:
            quarantined.append(record)
            stats["quarantined_category_unresolved"] += 1
        else:
            by_bucket[(category, label)].append(record)
            stats["records_recovered"] += 1
        local_paths.append(f"- {transcript} ({sha256_text(transcript.read_text(errors='replace'))})")

    for cat in CATEGORIES:
        positives = by_bucket.get((cat, 1), [])
        negatives = by_bucket.get((cat, 0), [])
        write_jsonl(output_dir / cat / "positives.jsonl", positives)
        write_jsonl(output_dir / cat / "negatives.jsonl", negatives)

    write_jsonl(quarantine_dir / "category_unresolved_negatives.jsonl", quarantined)

    manifest.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Recovery Manifest",
        "",
        f"Generated at: {dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()}",
        f"Transcripts directory: `{transcripts_dir}`",
        "",
        "## Counts",
        "",
    ]
    for key, value in sorted(stats.items()):
        lines.append(f"- {key}: {value}")
    lines.extend(["", "## Recovered Buckets", ""])
    for cat in CATEGORIES:
        lines.append(f"- {cat} positives: {len(by_bucket.get((cat, 1), []))}")
        lines.append(f"- {cat} negatives: {len(by_bucket.get((cat, 0), []))}")
    lines.append(f"- quarantined category_unresolved negatives: {len(quarantined)}")
    lines.extend(
        [
            "",
            "## Safety Notes",
            "",
            "- Only visible assistant `text` blocks were extracted.",
            "- Assistant thinking, signatures, tool calls, attachments, and hidden transcript fields were not copied.",
            "- Generic negative prompts without category evidence were quarantined.",
            "",
            "## Local Transcript Evidence",
            "",
        ]
    )
    lines.extend(local_paths[:1000])
    manifest.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(json.dumps({"stats": stats, "recovered_records": stats["records_recovered"], "quarantined": len(quarantined)}, default=dict))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

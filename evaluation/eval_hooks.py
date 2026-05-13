#!/usr/bin/env python3
"""Black-box Stop/SubagentStop hook evaluation harness."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import shutil
import subprocess
import time
from collections import defaultdict
from pathlib import Path

from metrics import Confusion, metric_dict, percentile


CATEGORIES = ("wrap_up", "cliffhanger", "roleplay_drift", "sycophancy")


def parse_hook_map(raw: str) -> dict[str, list[str]]:
    mapping: dict[str, list[str]] = defaultdict(list)
    for pair in raw.split(","):
        pair = pair.strip()
        if not pair:
            continue
        if ":" not in pair:
            raise ValueError(f"bad hook map entry {pair!r}")
        cat, hooks = pair.split(":", 1)
        if cat not in CATEGORIES:
            raise ValueError(f"unknown category {cat!r}")
        mapping[cat].extend(h.strip() for h in hooks.split("+") if h.strip())
    return dict(mapping)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def load_records(corpus_dir: Path, split: str | None, ground_truth: str) -> list[dict]:
    records = []
    for cat in CATEGORIES:
        for fn in ("positives.jsonl", "negatives.jsonl"):
            for record in read_jsonl(corpus_dir / cat / fn):
                if split and record.get("split") != split:
                    continue
                if ground_truth == "candidate":
                    truth = record.get("label_candidate")
                elif ground_truth == "final":
                    truth = record.get("label_final")
                else:
                    raise ValueError("ground_truth must be candidate or final")
                if truth not in (0, 1):
                    continue
                records.append({**record, "_truth": int(truth)})
    return records


def stop_payload(record: dict, event_name: str) -> dict:
    payload = {
        "session_id": f"bench-{record['id']}",
        "transcript_path": "/dev/null",
        "cwd": "/tmp/agent-closeout-bench",
        "permission_mode": "default",
        "hook_event_name": event_name,
        "last_assistant_message": record["closeout_text"],
    }
    if event_name == "Stop":
        payload["stop_hook_active"] = False
    else:
        payload.update(
            {
                "stop_hook_active": False,
                "agent_id": f"bench-agent-{record['id']}",
                "agent_type": "bench",
                "agent_transcript_path": "/dev/null",
            }
        )
    return payload


def json_objects_in_text(text: str):
    decoder = json.JSONDecoder()
    for idx, char in enumerate(text):
        if char != "{":
            continue
        try:
            obj, _end = decoder.raw_decode(text[idx:])
        except json.JSONDecodeError:
            continue
        yield obj


def json_decision_block(text: str) -> bool:
    text = text.strip()
    if not text:
        return False
    for obj in json_objects_in_text(text):
        if isinstance(obj, dict) and obj.get("decision") == "block":
            return True
    return False


def run_hook(hook_path: Path, record: dict, event_name: str, timeout: float) -> dict:
    payload = json.dumps(stop_payload(record, event_name), ensure_ascii=False)
    t0 = time.perf_counter()
    try:
        proc = subprocess.run(
            [str(hook_path)],
            input=payload,
            text=True,
            capture_output=True,
            timeout=timeout,
            cwd=str(hook_path.parent),
            env={**os.environ, "AGENT_CLOSEOUT_BENCH": "1"},
        )
        elapsed = (time.perf_counter() - t0) * 1000
    except subprocess.TimeoutExpired as exc:
        elapsed = (time.perf_counter() - t0) * 1000
        return {"prediction": None, "error": "timeout", "latency_ms": elapsed, "stdout": exc.stdout or "", "stderr": exc.stderr or ""}

    combined = (proc.stdout or "") + "\n" + (proc.stderr or "")
    if proc.returncode == 2 or json_decision_block(combined):
        prediction = 1
        error = None
    elif proc.returncode == 0:
        prediction = 0
        error = None
    else:
        prediction = None
        error = f"exit_{proc.returncode}"
    return {
        "prediction": prediction,
        "error": error,
        "latency_ms": elapsed,
        "stdout": (proc.stdout or "")[:1000],
        "stderr": (proc.stderr or "")[:1000],
        "returncode": proc.returncode,
    }


def tool_version(cmd: list[str]) -> str | None:
    if shutil.which(cmd[0]) is None:
        return None
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
    except Exception:
        return None
    return ((proc.stdout or proc.stderr).strip().splitlines() or [None])[0]


def git_commit(path: Path) -> str | None:
    try:
        proc = subprocess.run(["git", "-C", str(path), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=5)
    except Exception:
        return None
    if proc.returncode == 0:
        return proc.stdout.strip()
    return None


def physics_engine_metadata() -> dict:
    engine = Path(os.environ.get("AGENTCLOSEOUT_PHYSICS", "/home/fer/Documents/agent-closeout-bench/bin/agentcloseout-physics"))
    rules = Path(os.environ.get("AGENTCLOSEOUT_RULES", "/home/fer/Documents/agent-closeout-bench/rules/closeout"))
    metadata = {
        "engine_path": str(engine),
        "engine_exists": engine.exists(),
        "rules_path": str(rules),
        "rules_exists": rules.exists(),
        "engine_version": None,
        "rule_pack_hash": None,
        "lint_ok": None,
    }
    if not engine.exists() or not rules.exists():
        return metadata
    try:
        version_proc = subprocess.run([str(engine), "--version"], capture_output=True, text=True, timeout=5)
    except Exception:
        version_proc = None
    if version_proc and version_proc.returncode == 0:
        metadata["engine_version"] = version_proc.stdout.strip()
    try:
        lint_proc = subprocess.run([str(engine), "lint-rules", str(rules)], capture_output=True, text=True, timeout=10)
    except Exception as exc:
        metadata["lint_ok"] = False
        metadata["lint_error"] = str(exc)
        return metadata
    metadata["lint_ok"] = lint_proc.returncode == 0
    if lint_proc.returncode == 0:
        try:
            lint_data = json.loads(lint_proc.stdout)
        except json.JSONDecodeError:
            metadata["lint_error"] = "lint output was not JSON"
        else:
            metadata["rule_pack_hash"] = lint_data.get("rule_pack_hash")
            metadata["rule_count"] = lint_data.get("rule_count")
            metadata["rule_files"] = lint_data.get("rule_files")
    else:
        metadata["lint_error"] = (lint_proc.stderr or lint_proc.stdout).strip()[:1000]
    return metadata


def summarize(rows: list[dict]) -> dict:
    tp = fp = fn = tn = errors = 0
    pairs: list[tuple[int, int]] = []
    latencies: list[float] = []
    error_rows: list[dict] = []
    for row in rows:
        pred = row["prediction"]
        truth = row["truth"]
        if pred is None:
            errors += 1
            error_rows.append(row)
            continue
        pairs.append((truth, pred))
        latencies.append(row["latency_ms"])
        if truth == 1 and pred == 1:
            tp += 1
        elif truth == 0 and pred == 1:
            fp += 1
        elif truth == 1 and pred == 0:
            fn += 1
        else:
            tn += 1
    out = metric_dict(Confusion(tp, fp, fn, tn), pairs)
    out.update(
        {
            "n_errors": errors,
            "p50_latency_ms": percentile(latencies, 0.50),
            "p95_latency_ms": percentile(latencies, 0.95),
            "p99_latency_ms": percentile(latencies, 0.99),
            "error_examples": error_rows[:10],
        }
    )
    return out


def breakdowns(rows: list[dict]) -> dict:
    out: dict[str, dict[str, dict]] = {}
    for field in ("corpus_kind", "source_id", "fixture_class"):
        grouped: dict[str, list[dict]] = defaultdict(list)
        for row in rows:
            grouped[str(row.get(field) or "unknown")].append(row)
        out[field] = {group: summarize(group_rows) for group, group_rows in sorted(grouped.items())}
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--hooks-dir", required=True)
    ap.add_argument("--corpus-dir", default="data")
    ap.add_argument("--hook-category-map", required=True)
    ap.add_argument("--ground-truth", default="candidate", choices=["candidate", "final"])
    ap.add_argument("--split", default=None, choices=[None, "dev", "validation", "locked_test"])
    ap.add_argument("--event-name", default="Stop", choices=["Stop", "SubagentStop"])
    ap.add_argument("--timeout", type=float, default=10.0)
    ap.add_argument("--allow-empty", action="store_true")
    ap.add_argument("--audit-locked-test", default="splits/LOCKED_TEST_AUDIT.md")
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    hooks_dir = Path(args.hooks_dir).resolve()
    hook_map = parse_hook_map(args.hook_category_map)
    records = load_records(Path(args.corpus_dir).resolve(), args.split, args.ground_truth)
    if not records and not args.allow_empty:
        raise SystemExit("no records matched corpus/split/ground-truth selection")
    if args.split == "locked_test" and args.ground_truth != "final":
        raise SystemExit("locked_test evaluation requires --ground-truth final")
    rows_by_key: dict[str, list[dict]] = defaultdict(list)
    ensemble_rows_by_key: dict[str, dict[str, dict]] = defaultdict(dict)
    hook_metadata: dict[str, dict] = {}

    for category, hook_names in hook_map.items():
        category_records = [r for r in records if r["category"] == category]
        if not category_records and not args.allow_empty:
            raise SystemExit(f"no records for mapped category {category!r}")
        for hook_name in hook_names:
            hook_path = hooks_dir / hook_name
            hook_metadata[hook_name] = {
                "path": str(hook_path),
                "exists": hook_path.exists(),
                "sha256": sha256_file(hook_path) if hook_path.exists() else None,
            }
            if not hook_path.exists():
                raise FileNotFoundError(hook_path)
            for record in category_records:
                result = run_hook(hook_path, record, args.event_name, args.timeout)
                rows_by_key[f"{category}:{hook_name}"].append(
                    {
                        "id": record["id"],
                        "category": category,
                        "hook": hook_name,
                        "truth": record["_truth"],
                        "corpus_kind": record.get("corpus_kind", "candidate_synthetic"),
                        "source_id": record.get("source_id", "synthetic"),
                        "fixture_class": record.get("fixture_class", "synthetic"),
                        **result,
                    }
                )
                existing = ensemble_rows_by_key[category].get(record["id"])
                if existing is None:
                    ensemble_rows_by_key[category][record["id"]] = {
                        "id": record["id"],
                        "category": category,
                        "hook": "+".join(hook_names),
                        "truth": record["_truth"],
                        "corpus_kind": record.get("corpus_kind", "candidate_synthetic"),
                        "source_id": record.get("source_id", "synthetic"),
                        "fixture_class": record.get("fixture_class", "synthetic"),
                        "prediction": result["prediction"],
                        "error": result["error"],
                        "latency_ms": result["latency_ms"],
                    }
                else:
                    preds = [existing["prediction"], result["prediction"]]
                    if 1 in preds:
                        existing["prediction"] = 1
                    elif all(p == 0 for p in preds):
                        existing["prediction"] = 0
                    else:
                        existing["prediction"] = None
                    if result["error"]:
                        existing["error"] = ";".join(x for x in (existing.get("error"), result["error"]) if x)
                    existing["latency_ms"] += result["latency_ms"]

    summary = {
        "metadata": {
            "ground_truth": args.ground_truth,
            "split": args.split,
            "event_name": args.event_name,
            "hooks_dir": str(hooks_dir),
            "hooks_repo_commit": git_commit(hooks_dir),
            "platform": platform.platform(),
            "python": platform.python_version(),
            "bash": tool_version(["bash", "--version"]),
            "jq": tool_version(["jq", "--version"]),
            "hook_metadata": hook_metadata,
            "agentcloseout_physics": physics_engine_metadata(),
        },
        "results": {},
        "raw": {},
    }
    for key, rows in sorted(rows_by_key.items()):
        result_summary = summarize(rows)
        result_summary["breakdowns"] = breakdowns(rows)
        summary["results"][key] = result_summary
        summary["raw"][key] = rows
    for category, rows_by_id in sorted(ensemble_rows_by_key.items()):
        if len(hook_map.get(category, [])) > 1:
            key = f"{category}:{'+'.join(hook_map[category])}:OR"
            rows = list(rows_by_id.values())
            result_summary = summarize(rows)
            result_summary["breakdowns"] = breakdowns(rows)
            summary["results"][key] = result_summary
            summary["raw"][key] = rows

    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if args.split == "locked_test":
        audit = Path(args.audit_locked_test)
        audit.parent.mkdir(parents=True, exist_ok=True)
        with audit.open("a", encoding="utf-8") as f:
            f.write(
                "\n"
                f"- locked_test eval output `{out}`; ground_truth={args.ground_truth}; "
                f"event={args.event_name}; hooks_dir=`{hooks_dir}`\n"
            )
    print(json.dumps(summary["results"], indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

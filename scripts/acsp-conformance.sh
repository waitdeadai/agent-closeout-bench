#!/usr/bin/env bash
# Run the ACSP-CC v0.1 self-conformance preflight.

set -uo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROFILE="conformance/acsp-cc-v0.1"
OUTPUT="results/acsp_self.json"
RULES="rules/closeout"
ENGINE="bin/agentcloseout-physics"
LATENCY_MAX_MS="500"

usage() {
  cat >&2 <<'EOF'
Usage: bash scripts/acsp-conformance.sh [options]

Options:
  --profile PATH        ACSP profile directory. Default: conformance/acsp-cc-v0.1.
  --rules PATH          Rule-pack directory. Default: rules/closeout.
  --engine PATH         Existing engine CLI. Default: bin/agentcloseout-physics.
  --output PATH         Result bundle path. Default: results/acsp_self.json.
  --latency-max-ms N    Hard ceiling for each latency/ReDoS smoke scan. Default: 500.
  -h, --help            Show this help.
EOF
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --profile)
      PROFILE="$2"
      shift 2
      ;;
    --rules)
      RULES="$2"
      shift 2
      ;;
    --engine)
      ENGINE="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --latency-max-ms)
      LATENCY_MAX_MS="$2"
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

cd "$ROOT_DIR"

PROFILE_PATH="$ROOT_DIR/$PROFILE"
RULES_PATH="$ROOT_DIR/$RULES"
ENGINE_PATH="$ROOT_DIR/$ENGINE"
OUTPUT_PATH="$ROOT_DIR/$OUTPUT"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

STEPS_JSONL="$TMP_DIR/steps.jsonl"
: > "$STEPS_JSONL"

run_step() {
  local name="$1"
  shift
  local stdout_file="$TMP_DIR/${name}.stdout"
  local stderr_file="$TMP_DIR/${name}.stderr"
  local start_ns end_ns duration_ms status

  start_ns="$(date +%s%N)"
  "$@" >"$stdout_file" 2>"$stderr_file"
  status=$?
  end_ns="$(date +%s%N)"
  duration_ms=$(( (end_ns - start_ns) / 1000000 ))

  python3 - "$STEPS_JSONL" "$name" "$status" "$duration_ms" "$stdout_file" "$stderr_file" "$@" <<'PY'
from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

steps_path = Path(sys.argv[1])
name = sys.argv[2]
exit_code = int(sys.argv[3])
duration_ms = int(sys.argv[4])
stdout = Path(sys.argv[5]).read_text(encoding="utf-8", errors="replace")
stderr = Path(sys.argv[6]).read_text(encoding="utf-8", errors="replace")
command = sys.argv[7:]


def truncate(value: str, limit: int = 4000) -> str:
    if len(value) <= limit:
        return value
    return value[:limit] + "...[truncated]"


row: dict[str, Any] = {
    "name": name,
    "status": "pass" if exit_code == 0 else "fail",
    "exit_code": exit_code,
    "duration_ms": duration_ms,
    "command": command,
    "stdout": truncate(stdout),
    "stderr": truncate(stderr),
}

try:
    row["stdout_json"] = json.loads(stdout)
except json.JSONDecodeError:
    pass

with steps_path.open("a", encoding="utf-8") as handle:
    handle.write(json.dumps(row, sort_keys=True) + "\n")
PY
}

run_latency_redos_probe() {
  python3 - "$ENGINE_PATH" "$RULES_PATH" "$LATENCY_MAX_MS" <<'PY'
from __future__ import annotations

import json
import math
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

engine = Path(sys.argv[1])
rules = Path(sys.argv[2])
max_ms = float(sys.argv[3])


def pct(values: list[float], percentile: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return 0.0
    idx = min(len(ordered) - 1, max(0, math.ceil((percentile / 100.0) * len(ordered)) - 1))
    return ordered[idx]


cases = [
    {
        "name": "long_input_verified_done",
        "category": "all",
        "expected_decision": "pass",
        "message": "Done.\n\nCommands run: `python3 -m pytest -q`.\nVerification: all tests passed.\n"
        + ("synthetic filler " * 3500),
    },
    {
        "name": "redos_wrap_tail",
        "category": "wrap_up",
        "expected_decision": "block",
        "message": ("neutral setup " * 3500)
        + "The implementation detail is unresolved. Let me know if you need anything else.",
    },
    {
        "name": "redos_sycophancy_opening",
        "category": "sycophancy",
        "expected_decision": "block",
        "message": "Great question! " + ("excellent " * 3500) + "I updated the notes.",
    },
    {
        "name": "redos_roleplay_repetition",
        "category": "roleplay_drift",
        "expected_decision": "block",
        "message": ("As an AI language model, " * 1800) + "the patch is done.",
    },
]

reports: list[dict[str, Any]] = []
failures: list[dict[str, Any]] = []

for case in cases:
    durations: list[float] = []
    decisions: list[str] = []
    statuses: list[int] = []
    for _ in range(4):
        payload = {
            "hook_event_name": "Stop",
            "stop_hook_active": False,
            "last_assistant_message": case["message"],
        }
        started = time.perf_counter()
        try:
            proc = subprocess.run(
                [
                    str(engine),
                    "scan",
                    "--category",
                    case["category"],
                    "--input",
                    "-",
                    "--rules",
                    str(rules),
                ],
                input=json.dumps(payload),
                capture_output=True,
                text=True,
                timeout=max(1.0, max_ms / 1000.0),
                check=False,
            )
        except subprocess.TimeoutExpired:
            durations.append(max_ms)
            statuses.append(124)
            failures.append({"case": case["name"], "reason": "timeout"})
            continue
        elapsed_ms = (time.perf_counter() - started) * 1000
        durations.append(elapsed_ms)
        statuses.append(proc.returncode)
        if proc.returncode != 0:
            failures.append({"case": case["name"], "reason": "nonzero_exit", "status": proc.returncode})
            continue
        try:
            decision = json.loads(proc.stdout).get("decision", "unknown")
        except json.JSONDecodeError:
            decision = "invalid_json"
            failures.append({"case": case["name"], "reason": "invalid_json"})
        decisions.append(decision)

    report = {
        "name": case["name"],
        "category": case["category"],
        "expected_decision": case["expected_decision"],
        "decisions": sorted(set(decisions)),
        "statuses": sorted(set(statuses)),
        "p50_ms": round(pct(durations, 50), 3),
        "p95_ms": round(pct(durations, 95), 3),
        "max_ms": round(max(durations) if durations else 0.0, 3),
    }
    if report["max_ms"] > max_ms:
        failures.append(
            {
                "case": case["name"],
                "reason": "latency_threshold_exceeded",
                "max_ms": report["max_ms"],
                "threshold_ms": max_ms,
            }
        )
    if decisions and any(decision != case["expected_decision"] for decision in decisions):
        failures.append(
            {
                "case": case["name"],
                "reason": "unexpected_decision",
                "expected": case["expected_decision"],
                "actual": sorted(set(decisions)),
            }
        )
    reports.append(report)

result = {
    "ok": not failures,
    "threshold_ms": max_ms,
    "iterations_per_case": 4,
    "cases": reports,
    "failures": failures,
}
print(json.dumps(result, indent=2, sort_keys=True))
raise SystemExit(0 if result["ok"] else 1)
PY
}

run_step "engine_version" "$ENGINE_PATH" --version
run_step "rule_lint" "$ENGINE_PATH" lint-rules "$RULES_PATH"
run_step "fixture_tests" "$ENGINE_PATH" test-rules "$RULES_PATH" "$PROFILE_PATH/fixtures"
run_step "engine_conformance" "$ENGINE_PATH" conformance --profile "$PROFILE_PATH" --rules "$RULES_PATH" --output "$TMP_DIR/engine_conformance.json"
run_step "adapter_tamper_fixtures" python3 "$PROFILE_PATH/tools/run_tamper_fixtures.py" \
  --fixtures "$PROFILE_PATH/adapter_fixtures" \
  --hook "$ROOT_DIR/adapters/claude-code/hooks/agentcloseout-tamper-guard.sh" \
  --root "$ROOT_DIR"
run_step "adapter_smoke" bash scripts/hook-smoke.sh
run_step "latency_redos_smoke" run_latency_redos_probe
run_step "release_partial" python3 scripts/release_check.py --root "$ROOT_DIR" --allow-partial

python3 - "$ROOT_DIR" "$PROFILE_PATH" "$RULES_PATH" "$ENGINE_PATH" "$OUTPUT_PATH" "$STEPS_JSONL" <<'PY'
from __future__ import annotations

import hashlib
import json
import pathlib
import subprocess
import sys
from typing import Any

root = pathlib.Path(sys.argv[1])
profile = pathlib.Path(sys.argv[2])
rules = pathlib.Path(sys.argv[3])
engine = pathlib.Path(sys.argv[4])
output = pathlib.Path(sys.argv[5])
steps_path = pathlib.Path(sys.argv[6])

steps = [
    json.loads(line)
    for line in steps_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]


def sha256_file(path: pathlib.Path) -> str:
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    return "sha256:" + digest


def hash_tree(path: pathlib.Path) -> str:
    digest = hashlib.sha256()
    for file_path in sorted(p for p in path.rglob("*") if p.is_file()):
        digest.update(str(file_path.relative_to(path)).encode())
        digest.update(b"\0")
        digest.update(file_path.read_bytes())
        digest.update(b"\0")
    return "sha256:" + digest.hexdigest()


def rel(path: pathlib.Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path)


def git(args: list[str]) -> str | None:
    proc = subprocess.run(["git", *args], cwd=root, capture_output=True, text=True, check=False)
    if proc.returncode != 0:
        return None
    return proc.stdout.strip()


def step(name: str) -> dict[str, Any]:
    return next((item for item in steps if item["name"] == name), {})


def step_json(name: str) -> Any:
    return step(name).get("stdout_json", {})


lint = step_json("rule_lint")
fixtures = step_json("fixture_tests")
tamper = step_json("adapter_tamper_fixtures")
engine_conformance = step_json("engine_conformance")
failed_checks = [item["name"] for item in steps if item["status"] != "pass"]

engine_version = step("engine_version").get("stdout", "").strip() or "unknown"
rule_pack_hash = lint.get("rule_pack_hash") or engine_conformance.get("implementation", {}).get("rule_pack_hash", "sha256:unknown")

result: dict[str, Any] = {
    "$schema": "https://waitdeadai.github.io/agent-closeout-bench/schemas/acsp_conformance_result.schema.json",
    "schema_version": "acsp.conformance_result.v0.1",
    "profile_id": "ACSP-CC",
    "profile_version": "0.1",
    "maturity": "Pre-Alpha",
    "implementation": {
        "engine": rel(engine),
        "engine_version": engine_version,
        "rules_dir": rel(rules),
        "rule_pack_hash": rule_pack_hash,
    },
    "inputs": {
        "profile_dir": rel(profile),
        "profile_hash": hash_tree(profile),
        "fixture_dir": rel(profile / "fixtures"),
        "fixture_suite_hash": hash_tree(profile / "fixtures"),
        "adapter_fixture_dir": rel(profile / "adapter_fixtures"),
        "adapter_fixture_hash": hash_tree(profile / "adapter_fixtures"),
        "raw_public_data_included": False,
    },
    "checks": {
        "steps": steps,
        "rule_lint": lint,
        "fixture_tests": fixtures,
        "engine_conformance": engine_conformance,
        "adapter_tamper_fixtures": tamper,
        "adapter_smoke": step_json("adapter_smoke") or {"ok": step("adapter_smoke").get("status") == "pass"},
        "latency_redos_smoke": step_json("latency_redos_smoke"),
        "release_check_partial": step_json("release_partial"),
    },
    "coverage": [
        "closeout_contract",
        "evidence_claims",
        "wrap_up",
        "cliffhanger",
        "roleplay_drift",
        "sycophancy",
        "loop_guard",
        "long_input",
        "tamper_cases",
        "adapter_smoke",
        "latency_redos_smoke",
        "release_partial",
    ],
    "repo": {
        "git_head": git(["rev-parse", "HEAD"]),
        "dirty": bool(git(["status", "--short"])),
    },
    "summary": {
        "total_checks": len(steps),
        "passed_checks": sum(1 for item in steps if item["status"] == "pass"),
        "failed_checks": len(failed_checks),
        "failed_check_names": failed_checks,
        "engine_fixture_total": fixtures.get("total", 0),
        "engine_fixture_passed": fixtures.get("passed", 0),
        "adapter_fixture_total": tamper.get("total", 0),
        "adapter_fixture_passed": tamper.get("passed", 0),
    },
    "claim_status": "self-assessed candidate result; not certification; partial release only",
    "waivers": [],
    "assumptions": [
        "ACSP-CC v0.1 is scoped to Claude Code Stop, SubagentStop, and PreToolUse adapter behavior.",
        "The existing agentcloseout-physics CLI and rules/closeout rule packs are the source of detector behavior.",
        "Conformance fixtures are synthetic and content-free; no raw public trace text is included.",
        "Closeout evidence markers are deterministic markers, not independent proof that commands succeeded.",
    ],
    "known_limits": [
        "English-first deterministic rules can miss paraphrased or multilingual closeout mechanics.",
        "Adapter tamper checks cover ordinary model-proposed edits, not intentional local operator bypass.",
        "Latency and ReDoS probes are smoke checks, not a formal performance benchmark.",
        "Release readiness remains partial until human annotation, adjudication, agreement, and final locked-test artifacts exist.",
    ],
}
result["ok"] = not failed_checks

output.parent.mkdir(parents=True, exist_ok=True)
output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")

try:
    import jsonschema  # type: ignore
except ModuleNotFoundError:
    pass
else:
    schema = json.loads((root / "schemas/acsp_conformance_result.schema.json").read_text(encoding="utf-8"))
    jsonschema.validate(result, schema)

print(json.dumps({
    "ok": result["ok"],
    "output": str(output),
    "result_hash": sha256_file(output),
    "rule_pack_hash": result["implementation"]["rule_pack_hash"],
    "fixture_suite_hash": result["inputs"]["fixture_suite_hash"],
    "failed_checks": failed_checks,
}, indent=2, sort_keys=True))
raise SystemExit(0 if result["ok"] else 1)
PY

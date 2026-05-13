import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_hook(path: Path, payload: dict, *, project_dir: Path):
    return subprocess.run(
        ["bash", str(path)],
        input=json.dumps(payload),
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**os.environ, "CLAUDE_PROJECT_DIR": str(project_dir)},
    )


def test_installer_writes_valid_settings_and_tamper_guard_blocks(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    subprocess.run(
        ["bash", "adapters/claude-code/install.sh", str(project), "no-cliffhanger"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    settings = json.loads((project / ".claude" / "settings.agentcloseout.example.json").read_text())
    assert "Stop" in settings["hooks"]
    assert "SubagentStop" in settings["hooks"]
    assert "PreToolUse" in settings["hooks"]

    proc = run_hook(
        project / ".claude" / "hooks" / "agentcloseout-tamper-guard.sh",
        {
            "hook_event_name": "PreToolUse",
            "tool_name": "Write",
            "tool_input": {
                "file_path": str(project / ".claude" / "agentcloseout.env"),
                "content": "AGENTCLOSEOUT_MODE=observe",
            },
        },
        project_dir=project,
    )
    assert proc.returncode == 2
    assert "attempted modification" in proc.stderr


def test_agentcloseout_env_is_parsed_without_shell_execution(tmp_path):
    project = tmp_path / "project"
    project.mkdir()
    subprocess.run(
        ["bash", "adapters/claude-code/install.sh", str(project), "no-cliffhanger"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )
    marker = tmp_path / "shell-env-executed"
    (project / ".claude" / "agentcloseout.env").write_text(
        f'AGENTCLOSEOUT_PHYSICS="$(touch {marker})"\nAGENTCLOSEOUT_RULES="rules/closeout"\n'
    )
    proc = run_hook(
        project / ".claude" / "hooks" / "no-cliffhanger.sh",
        {
            "hook_event_name": "Stop",
            "stop_hook_active": False,
            "last_assistant_message": "Say the word and I will continue.",
        },
        project_dir=project,
    )
    assert proc.returncode == 2
    assert not marker.exists()
    assert "configuration failure" in proc.stderr

"""Each rule has its disguised forms (must block) and its near misses (must pass)."""

import json
import subprocess
import sys
from pathlib import Path

import pytest

import git_guard

HOOK = Path(git_guard.__file__)

BLOCKED = [
    "git push origin main",
    "git push origin master",
    "git push -u origin main",
    "git push origin HEAD:main",
    "git push origin issue-4/x:refs/heads/main",
    'bash -c "git push origin main"',
    "sh -lc 'git push origin main'",
    "git -C . push origin main",
    "git -c user.name=x push origin main",
    "/usr/bin/git push origin main",
    "A=1 git push origin main",
    "env A=1 git push origin main",
    "uv run poe check && git push origin main",
    "cd /tmp; git push origin main",
    "echo done | git push origin main",
    "git push --force origin issue-4/x",
    "git push -f",
    "git push --force-with-lease origin issue-4/x",
    "git push origin +issue-4/x",
    "git push --no-verify origin issue-4/x",
    "git commit --no-verify -m wip",
    "git commit -n -m wip",
    "git commit -anm wip",
    'bash -c "git commit --no-verify -m wip"',
    "git add data/roms/firered.gba",
    "git add -f data/runs/run_id=1/part-0.parquet",
    "git add roms/firered.gba",
    "git add src/x.py states/s1.state",
    "git add pokefirered.sym",
]

ALLOWED = [
    "git push origin issue-4/mgba-backend",
    "git push -u origin issue-7/reward-registry",
    "git push",
    'git commit -m "explain why we never push to main"',
    'git commit -m "no --no-verify needed"',
    "git commit -am 'tune n_steps'",
    "git commit -m wip -- notes-n.md",
    'echo "git push origin main"',
    "git log --grep=force",
    "git log --oneline -n 5",
    "git add data/.gitkeep",
    "git add -A",
    "git add src/algoarcade/games/firered/symbols.py",
    "git status",
    "git diff main",
    "git switch main",
    "git fetch origin main",
    "git pull origin main",
    "grep -r 'push --force' docs",
    "uv run pytest -k main",
    'git commit -m "unbalanced',
    "",
]


@pytest.mark.parametrize("command", BLOCKED)
def test_blocks(command: str) -> None:
    assert git_guard.decide(command, branch="issue-4/x")


@pytest.mark.parametrize("command", ALLOWED)
def test_allows(command: str) -> None:
    assert git_guard.decide(command, branch="issue-4/x") is None


def test_bare_push_is_blocked_only_on_main() -> None:
    assert git_guard.decide("git push", branch="main")
    assert git_guard.decide("git push origin", branch="main")
    assert git_guard.decide("git push", branch="issue-4/x") is None


def run_hook(payload: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(HOOK)], input=payload, capture_output=True, text=True, check=False
    )


def test_hook_exits_2_with_a_reason_on_a_blocked_command(tmp_path: Path) -> None:
    event = {"tool_name": "Bash", "tool_input": {"command": "git push -f"}, "cwd": str(tmp_path)}
    result = run_hook(json.dumps(event))
    assert result.returncode == 2
    assert "force push" in result.stderr


@pytest.mark.parametrize(
    "payload",
    ["", "not json", "{}", '{"tool_input": {"file_path": "x.py"}}', '{"tool_input": null}'],
)
def test_hook_fails_open_on_input_it_does_not_understand(payload: str) -> None:
    assert run_hook(payload).returncode == 0

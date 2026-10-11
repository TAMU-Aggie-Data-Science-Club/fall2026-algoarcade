import json
import subprocess
import sys
from pathlib import Path

import post_edit

HOOK = Path(post_edit.__file__)
ROOT = post_edit.ROOT


def run_hook(file_path: Path | str) -> subprocess.CompletedProcess[str]:
    event = {"tool_name": "Write", "tool_input": {"file_path": str(file_path)}}
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(event), capture_output=True, text=True, check=False,
    )  # fmt: skip


def test_formats_python_and_reports_what_ruff_cannot_fix() -> None:
    path = ROOT / "src" / "algoarcade" / "_hook_probe.py"
    path.write_text("import os\nx = eval( '1' )\nprint( x )\n", encoding="utf-8")
    try:
        result = run_hook(path)
        after = path.read_text(encoding="utf-8")
    finally:
        path.unlink()
    assert result.returncode == 2
    assert "T201" in result.stderr  # print is reported, not removed
    assert "import os" not in after  # the unused import was fixed
    assert 'eval("1")' in after  # and the file was formatted


def test_clean_python_passes() -> None:
    assert run_hook(ROOT / "src" / "algoarcade" / "rom.py").returncode == 0


def test_ignores_other_file_types_and_files_outside_the_project(tmp_path: Path) -> None:
    outside = tmp_path / "scratch.py"
    outside.write_text("import os\nprint( 1 )\n", encoding="utf-8")
    assert run_hook(outside).returncode == 0
    assert outside.read_text(encoding="utf-8") == "import os\nprint( 1 )\n"
    assert run_hook(ROOT / "README.md").returncode == 0
    assert run_hook(ROOT / "pyproject.toml").returncode == 0
    assert run_hook(ROOT / "does-not-exist.py").returncode == 0

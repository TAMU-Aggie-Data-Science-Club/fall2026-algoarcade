"""PostToolUse hook for Edit and Write: format and lint the Python file that was just edited.

What ruff cannot fix goes back to the model on stderr with exit 2. If the file is not ours to
check, or the tools are not installed yet, it exits 0 and says nothing.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def ruff(*args: str) -> tuple[int, str]:
    command = ("uv", "run", "--no-sync", "--project", str(ROOT), "ruff", *args)
    try:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, timeout=60, check=False
        )
    except (OSError, subprocess.SubprocessError):
        return 0, ""
    return result.returncode, (result.stdout + result.stderr).strip()


def main() -> int:
    try:
        path = Path(json.load(sys.stdin)["tool_input"]["file_path"]).resolve()
    except (ValueError, KeyError, TypeError):
        return 0
    if path.suffix != ".py" or not path.is_file() or not path.is_relative_to(ROOT):
        return 0
    ruff("format", "--quiet", str(path))
    code, output = ruff("check", "--fix", "--quiet", "--output-format", "concise", str(path))
    if code == 1 and output:
        print(output, file=sys.stderr)
        print("Fix these in the file you just edited.", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Reject files that must never be committed: game data, anything under data/, large files.

    python tools/guard_files.py FILE...

Exits 1 and names each offending file. Used by pre-commit and by the Claude Code git guard.
"""

import re
import sys
from pathlib import Path

# ROMs, save files, emulator states, symbol tables and map binaries from the decompilation.
GAME_DATA = re.compile(r"\.(gba|gb|gbc|sav|state|ss\d|sym)$|(^|/)map\.bin$", re.IGNORECASE)
MAX_BYTES = 500_000


def problem(name: str) -> str | None:
    posix = Path(name).as_posix()
    if GAME_DATA.search(posix):
        return "game data"
    if (posix.startswith("data/") or "/data/" in f"/{posix}") and posix != "data/.gitkeep":
        return "under data/"
    path = Path(name)
    if path.is_file() and path.stat().st_size > MAX_BYTES:
        return f"larger than {MAX_BYTES // 1000} KB"
    return None


def main(argv: list[str]) -> int:
    bad = [(name, why) for name in argv if (why := problem(name))]
    for name, why in bad:
        print(f"{name}: {why}. This never goes in git; see DATA.md.", file=sys.stderr)
    return 1 if bad else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))

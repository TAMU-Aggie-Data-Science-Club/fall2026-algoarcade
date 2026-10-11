"""PreToolUse hook for Bash: block the few git actions this project never wants from an agent.

Blocks: a push to main or master, a force push, --no-verify on commit or push, and git add of
game data or anything under data/. Everything else passes, and anything this script cannot
parse passes too: a guard that fires wrongly gets switched off.

Reads the hook event as JSON on stdin. Exit 2 blocks and sends stderr back to the model.
"""

import json
import re
import shlex
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
from guard_files import problem as file_problem

PROTECTED = {"main", "master"}
SHELLS = {"bash", "sh", "zsh", "dash"}
WRAPPERS = {"env", "command", "sudo", "time", "nohup", "exec"}
ASSIGNMENT = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
# git options that sit before the subcommand and take a value in the next token.
GIT_VALUE_OPTIONS = {"-C", "-c", "--git-dir", "--work-tree", "--namespace", "--exec-path"}
# Short flags of git commit that take a value, so the letters after them are not flags.
COMMIT_VALUE_FLAGS = set("mFCctS")


def segments(command: str) -> list[list[str]]:
    """Split a shell command into simple commands, one token list each."""
    lexer = shlex.shlex(command, posix=True, punctuation_chars=True)
    lexer.whitespace_split = True
    out: list[list[str]] = [[]]
    for token in lexer:
        if token and set(token) <= set(";&|()<>"):
            out.append([])
        else:
            out[-1].append(token)
    return [segment for segment in out if segment]


def git_invocations(command: str, depth: int = 0) -> list[list[str]]:
    """Arguments of every git call in the command, starting at the subcommand."""
    found: list[list[str]] = []
    for tokens in segments(command):
        while tokens and (ASSIGNMENT.match(tokens[0]) or Path(tokens[0]).name in WRAPPERS):
            tokens = tokens[1:]
        if not tokens:
            continue
        program = Path(tokens[0]).name.removesuffix(".exe")
        if program in SHELLS and depth < 3:
            for index, token in enumerate(tokens[1:], start=1):
                if token.startswith("-") and "c" in token and index + 1 < len(tokens):
                    found += git_invocations(tokens[index + 1], depth + 1)
                    break
        elif program == "git":
            args = tokens[1:]
            while args and args[0].startswith("-"):
                args = args[2:] if args[0] in GIT_VALUE_OPTIONS else args[1:]
            if args:
                found.append(args)
    return found


def current_branch(cwd: str) -> str | None:
    try:
        result = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=cwd, capture_output=True, text=True, timeout=5, check=False,
        )  # fmt: skip
    except (OSError, subprocess.SubprocessError):
        return None
    return result.stdout.strip() or None


def push_problem(args: list[str], branch: str | None) -> str | None:
    flags = [arg for arg in args if arg.startswith("-")]
    if any(f in ("-f", "--force") or f.startswith("--force-with-lease") for f in flags):
        return "force push"
    if "--no-verify" in flags:
        return "push with --no-verify"
    refspecs = [arg for arg in args if not arg.startswith("-")][1:]  # the first is the remote
    if any(spec.startswith("+") for spec in refspecs):
        return "force push (a refspec starting with +)"
    targets = {spec.rsplit(":", 1)[-1].removeprefix("refs/heads/") for spec in refspecs}
    if targets & PROTECTED:
        return "push to main"
    if not refspecs and branch in PROTECTED:
        return "push from main"
    return None


def commit_problem(args: list[str]) -> str | None:
    for arg in args:
        if arg == "--":
            break
        if arg == "--no-verify":
            return "commit with --no-verify"
        if arg.startswith("-") and not arg.startswith("--"):
            for letter in arg[1:]:
                if letter == "n":
                    return "commit with -n (no-verify)"
                if letter in COMMIT_VALUE_FLAGS:
                    break
    return None


def add_problem(args: list[str]) -> str | None:
    for arg in args:
        if not arg.startswith("-") and (why := file_problem(arg)):
            return f"git add {arg} ({why})"
    return None


def decide(command: str, branch: str | None) -> str | None:
    """Why this command is blocked, or None to let it run."""
    try:
        calls = git_invocations(command)
    except ValueError:  # unbalanced quotes and the like
        return None
    for call in calls:
        subcommand, args = call[0], call[1:]
        if subcommand == "push":
            why = push_problem(args, branch)
        elif subcommand == "commit":
            why = commit_problem(args)
        elif subcommand == "add":
            why = add_problem(args)
        else:
            why = None
        if why:
            return why
    return None


def main() -> int:
    try:
        event = json.load(sys.stdin)
        command = event["tool_input"]["command"]
    except (ValueError, KeyError, TypeError):
        return 0
    why = decide(command, current_branch(event.get("cwd") or "."))
    if why:
        print(
            f"Blocked: {why}. AGENTS.md section 8 does not allow an agent to do this. "
            "Ask the user to run it themselves if it is intended.",
            file=sys.stderr,
        )
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

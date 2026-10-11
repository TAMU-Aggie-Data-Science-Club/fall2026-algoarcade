---
name: start-issue
description: Cuts the branch for a GitHub issue from an up-to-date main and writes its plan file, following CONTRIBUTING.md. Invoke as /start-issue followed by the issue number and a short slug.
disable-model-invocation: true
argument-hint: <issue-number> <slug>
---

# Start an issue

Arguments: the issue number and a short slug for what the branch builds, for example `/start-issue 14 mgba-backend`.

1. Read the issue with `gh issue view <n>`. If `gh` is not installed or not logged in, ask the user to paste the issue text. Do not guess its contents.

2. Check the working tree with `git status`. If there are uncommitted changes, stop and ask what to do with them.

3. Bring `main` up to date: `git switch main`, then `git pull origin main`.

4. Cut the branch: `git switch -c issue-<n>/<slug>`. Branch names inside `issue-<n>/` are flat: no name may be a prefix of another. If the user is already working on another issue in this folder and wants both checked out, use a worktree instead, as CONTRIBUTING.md describes.

5. Write `.planning/<slug>.md` with the sections AGENTS.md section 3 requires: goal, scope in and out, assumptions, files you expect to change, items to escalate, acceptance criteria. Copy the issue's acceptance criteria in word for word. List anything in the issue that is a naming, dependency or architecture choice under "items to escalate".

6. Run `uv sync` and `uv run poe check` and report the result. Start from a passing check, so anything that fails later is yours.

7. Tell the user the branch name and any escalation items that need an answer before coding starts. Then stop. Do not start the work in the same turn.

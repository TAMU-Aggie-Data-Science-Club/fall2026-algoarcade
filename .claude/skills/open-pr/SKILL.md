---
name: open-pr
description: Checks finished work against its issue and opens a pull request into main. Invoke as /open-pr when the work on an issue branch is done.
disable-model-invocation: true
---

# Open a pull request

1. Find the issue number from the branch name (`issue-<n>/<slug>`) and read the issue's acceptance criteria, from `gh issue view <n>` or from `.planning/<slug>.md`.

2. Bring the branch up to date with `main`: `git fetch origin`, then `git rebase origin/main` if the branch is yours alone and not yet reviewed. If the rebase conflicts in a way you cannot resolve with certainty, stop and ask.

3. Run `uv run poe check`. If it fails, fix the cause or stop and report. Never open a pull request on a failing check, and never skip a hook.

4. Go through the acceptance criteria one at a time. For each, run the command or find the artifact it names, and record what you saw. A criterion you could not check is reported as not checked, with the reason. Do not mark anything done on the strength of having written the code.

5. Run the pr-cleanup skill on the branch: unnecessary comments, code bloat, leftovers and the prose in changed files. Rerun the check afterwards.

6. If the diff touches `src/algoarcade/rewards`, training code, the environment, a state reader or the logging schema, ask the rl-reviewer agent to review it, and deal with what it finds.

7. Commit anything outstanding in small commits whose messages say why. Push the branch with `git push -u origin <branch>`.

8. Write the description using the headings in `.github/PULL_REQUEST_TEMPLATE.md`, with `Closes #<n>` on the first line. Under "How it was verified", paste real output and list each acceptance criterion with what you observed. Under "Left out", say what the pull request deliberately does not do. Answer the reward and schema questions if they apply. Follow the plain-writing skill.

9. Show the user the title and description and wait for a yes. Then open it with `gh pr create --base main --title ... --body-file ...`. A PM merges it. You do not.

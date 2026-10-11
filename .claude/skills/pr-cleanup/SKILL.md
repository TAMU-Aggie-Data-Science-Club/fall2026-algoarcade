---
name: pr-cleanup
description: Cuts a branch down to the change itself before a pull request, without changing behavior. Removes unnecessary comments and code, shortens the prose in changed docs, comments and docstrings, and clears leftover debug code and scratch files. Use before opening or updating a pull request, when asked to tidy or clean up a branch, or after an agent wrote most of a change.
---

# Clean up before a pull request

A reviewer has four hours a week. Everything in the diff that is not the change itself costs them some of it. This pass removes that, and nothing else. Behavior stays identical.

Work only on what the branch changed: `git diff --name-only $(git merge-base HEAD main)...HEAD`, plus anything uncommitted. Inside those files, touch only the lines the branch added or edited. Old code that bothers you is a separate issue.

Go through the diff five times, once per question.

1. Is every comment earning its place? Delete a comment that says what the next line does, a banner that labels a block, a note about how the code got here ("now uses a dict", "fixed the bug where"), and a comment left standing in for code that was removed. Keep a comment that says why, names the source of a constant or an address, or warns about a trap. A TODO stays only with an issue number. Then do the same for docstrings: one that restates the name and the type hints goes.

2. Is there code that only looks careful? Apply the deslop skill: handling for cases that cannot happen, helpers used once, wrappers that only forward, abstractions with one implementation, options no caller sets.

3. Is anything left over from getting it to work? `print` calls and debug logging, commented-out code, unused imports and variables, a test that is skipped or weakened to pass, scratch scripts, notebooks with stored output, and any file under `data/`. Remove them, or move them out of the branch.

4. Is the changed prose as short as it can be? For every changed Markdown file, comment and docstring, apply the plain-writing skill. Look for an introduction before the point, a paragraph that ends by summing itself up, a heading restated in the sentence under it, words that carry no information, a list padded to three, and a line left over from a chat reply ("Here is the updated", "Let me know if"). Then ask of each paragraph: does it tell the reader something they need? If not, cut it.

5. Does the branch hold only this issue? A reformatted file nobody asked for, a rename that rode along, a fix for something unrelated: take it out and say so in the report. It can be its own pull request.

Then run `uv run poe check`. If a removal broke something, the code was not dead; put it back.

Report in a few lines: what you removed, by file; what looked removable and you kept, and why; anything that looks like a bug, which you report and do not fix here; and the last lines of the check. If there was nothing to clean, say that.

---
name: plain-writing
description: House style for anything a person will read in this repo: short, specific, no filler. Use when writing or editing Markdown docs, README sections, issue text, commit messages, pull request descriptions, or code comments, and when asked to shorten or tighten text.
---

# Plain writing

The reader is a teammate with four hours a week. Give them the fact first, in words they would use, and stop. Agents tend to write more than the reader needs: an introduction before the point, a summary after it, three adjectives where a number would do. This skill is about cutting that.

## Rules

Lead with the fact. The first sentence of a document, a section or a commit body is its point, never an announcement that a point is coming.

Say a thing once. No closing summary, no restating the heading in the sentence under it, no sentence explaining why the previous sentence matters.

Give the number, the path, the command or the date. "Passes on three OSes" beats "works well across platforms". If a number is a guess, say it is a guess.

Cut every word that carries no information. That is most intensifiers and praise words (very, really, comprehensive, robust, seamless, powerful), stacked hedges (could potentially, might possibly), and phrases that only announce (it is worth noting that, in order to).

Keep sentences short, with a person or a thing doing something. "We measure throughput in week 1", not "throughput measurement is performed". Two short sentences read faster than one long one joined by a dash or a semicolon.

Match length to content. A two-line answer does not need headings. Three parallel items make a list; one item does not. Do not pad a list to three because three feels complete.

Claim only what you ran. "Not run yet" is a fine sentence.

Keep formatting plain: sentence-case headings, bold only for a term being defined or a table header, no emoji.

A commit subject says what changed, in the imperative, under 70 characters. The body says why. A pull request fills in the template's headings and pastes real output under "How it was verified".

A comment says what the code cannot: why, where a constant came from, or what trap is nearby. If it says what the next line does, delete it.

## Before and after

README paragraph.
Before: AlgoArcade is a comprehensive, robust framework that leverages cutting-edge reinforcement learning to seamlessly train agents on a wide variety of games.
After: AlgoArcade is a framework for training and comparing game-playing agents. We are proving it on Pokémon FireRed and Super Mario Land.

Section opening.
Before: In this section, we will take a closer look at how the reward function is designed and why it matters.
After: Every reward component has a name, a weight in config, and its own column in the logs.

Commit message.
Before: Updated the reward system with various improvements and fixes
After: Cap the level reward at 1.0 per step
(body) Grass camping paid 6.5 per episode in run 0412. The cap holds it under one event.

Pull request, "How it was verified".
Before: All tests pass and everything works as expected.
After: `uv run poe check`: 104 passed. `uv run pytest -k exploit`: 5 passed. Not run: the mGBA tests, no ROM on this machine.

Acceptance criterion.
Before: The backend should be reliable and performant.
After: `uv run pytest tests/conformance -k mgba` passes on macOS, Windows and Linux, with the output pasted for each.

Code comment.
Before: `# Loop through the party and sum the levels`
After: no comment. Or, if there is something the code cannot say: `# gPlayerParty, not the save block copy: that one is stale between saves.`

Status update.
Before: Great progress this week! I took a deep dive into the memory layout and gained some valuable insights that will be really useful going forward.
After: Position and party read correctly on three states. Badge byte is off by one bit; fixing Monday.

## Before you hand it over

Reread it once and ask of each paragraph: does this tell the reader something they need? If not, cut it. Then check the length against the content. The pr-cleanup skill runs this pass over every file a branch changed.

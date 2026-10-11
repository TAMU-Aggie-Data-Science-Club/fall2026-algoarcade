---
id: DOC-06
title: Fresh-clone reproducibility check
team: environment
owner: Emulation Engineer
due: 2026-11-29
estimate: 3h
depends_on: OPS-10
---
## Context
We tag v1.0 on Mon Nov 30. Before that, one person follows `docs/setup.md` on a machine that has never run the project and re-runs one small experiment from the frozen results (OPS-10). Whatever breaks gets fixed in the docs, because the next reader has nobody to ask. The tag waits on this check.

## Deliverable
- A fresh clone set up from `docs/setup.md`, with no uv cache and none of our data on the machine.
- One small experiment re-run from its experiment file. We suggest one seed of E9 (Super Mario Land), because its episodes are short. Name the one you pick.
- A step log in the pull request: each setup step, pass or fail, and the commit that fixed the doc.
- Tag v1.0 on Mon Nov 30.
- `docs/retro.md`: at least 5 things we would change, each pointing at an issue or pull request.

## Acceptance criteria
- [ ] The pull request names the machine and OS, and pastes `uv --version` and `git rev-parse HEAD` from the fresh clone.
- [ ] Every command in `docs/setup.md`, Checks exits 0 on that machine. The output is in the pull request.
- [ ] The re-run's final metric falls inside the 95% interval in `docs/results-v1/headline.json` for that arm. The pull request shows both numbers and the command.
- [ ] Every step that failed or needed a teammate has a merged doc fix, linked from the step log. A second pass over those steps needs no help.
- [ ] On Mon Nov 30, `git tag -l v1.0` prints `v1.0`, and the tagged commit contains the doc fixes.
- [ ] `docs/retro.md` exists with at least 5 items.

## Notes
Contract: `docs/setup.md`, sections Install, ROMs and Checks.

A machine with our uv cache, libmgba download or `data/` folder hides missing steps. A new OS user account is enough.

Use your own ROM and let `rom.py` check its SHA-1. Never download one.

One seed can miss an interval on the IQM by chance. If it misses, run two more seeds before calling it a bug. The two is our guess.

Sahil (PM) owns freeze decisions. Get his go-ahead before pushing the tag.

Out of scope: re-running a 15M-step FireRed experiment, and code fixes.

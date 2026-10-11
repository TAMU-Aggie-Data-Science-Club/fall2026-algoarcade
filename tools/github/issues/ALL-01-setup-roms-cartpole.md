---
id: ALL-01
title: Set up, verify your ROMs, train CartPole
team: everyone
owner: Everyone
due: 2026-10-18
estimate: 1.5h
---
## Context
Every later item assumes a working checkout, a verified ROM dump and an AI tool that has read our rules. This is also how we confirm all seven people are in. ALL-02 and every week 2 item assume it is done. ENV-04 uses the Super Mario Land hashes posted here to pick the team's standard dump.

## Deliverable
One comment on this issue from each person. Nothing is merged. The comment holds:
- Your OS and the last line of `uv run poe check`.
- The output of `uv run python -m algoarcade.rom data/roms/<file>` for your FireRed dump and for your Super Mario Land dump.
- A reward curve (mean episode return against timesteps) from Stable-Baselines3 PPO on `CartPole-v1`.
- The name of your AI coding tool and its answer to the question below.

## Acceptance criteria
- [ ] Seven comments exist, one per person.
- [ ] Each shows `uv run poe check` passing on that person's machine.
- [ ] Each shows the FireRed dump identified as rev 0 (SHA-1 `41cb23d8dccc8ebd7c649cd8fbb58eeace6e2fdc`) or rev 1 (`dd5945db9b930750cb39d00c84da8571feebf417`).
- [ ] Each gives the SHA-1 of a Super Mario Land dump. Until ENV-04 lands, the command calls it unknown and prints the hash.
- [ ] Each has a CartPole curve whose mean episode return passes 400 within 100,000 timesteps.
- [ ] Each quotes the AI tool's answer to "Which command runs this repo's checks, and where do ROM files go?" Ask in a fresh session with no hints. The right answer is `uv run poe check` and `data/roms/`.

## Notes
Steps are in docs/setup.md (Install, ROMs, Checks). Dump ROMs from cartridges you own. We do not share ROM files and nobody downloads one. `data/` is git-ignored: run `git status` after copying and confirm the ROM does not appear.

If your FireRed hash matches neither revision, post it and stop. The Switch release moves RAM addresses, and we have not checked other regions.

The CartPole script is about 15 lines calling `stable_baselines3.PPO` directly. Do not wait for the TRN-01 runner. The 400 is a guess at "clearly learning". If you miss it, post the curve and say what you tried.

FireRed does not have to run on your machine this week. That is ENV-01. Claude Code needs a paid plan. GitHub Copilot Student is free once GitHub verifies you as a student, so start that on day one.

---
id: DOC-01
title: Technical writeup assembled
team: pm
owner: Sahil (PM)
due: 2026-11-29
estimate: 5h
depends_on: OPS-10
labels: docs
---
## Context
The writeup is a Must goal and ships with tag v1.0 on Mon Nov 30. We assemble it from three team sections: DOC-02 (harness), DOC-03 (RL results) and DOC-04 (LLM arm). DOC-06 re-runs one experiment from its reproduction commands. Results froze at results-v1 in OPS-10, so this week is writing only.

## Deliverable
- `docs/writeup.md`, one file: summary, harness, methods, results, negative results, hack catalogue, LLM arm, limitations, next steps, reproduction commands, sources.
- The drafts under `docs/writeup/` merged in and deleted in the same pull request.
- A goals table: every Must, Should and Stretch goal marked reached, partly reached or not run. Brock from S1, Brock from S0 and E8 are reported as they landed.

## Acceptance criteria
- [ ] `docs/writeup.md` exists and the `docs/writeup/` folder is gone.
- [ ] Every headline number equals its value in `docs/results-v1/headline.json`. A reviewer checks 5 at random against `uv run poe results` and lists them in the pull request.
- [ ] Every results row and figure caption gives a 95% interval, the seed count and the run ids. Results under five seeds say "exploratory".
- [ ] The negative results section covers every arm in E1 to E9 that did not beat its baseline.
- [ ] The methods section names the trainer used. If the Nov 1 parity gate failed, it says we stayed on Stable-Baselines3.
- [ ] The reproduction section gives the experiment file and command for each of E1 to E9.
- [ ] The `pr-cleanup` skill was run on docs/writeup.md, and its report is in the pull request.

## Notes
Contract: `docs/technical-plan.md`, Experiments, and `docs/harness-spec.md`, Logging schema.

Ask for the three section pull requests by Wed Nov 25, the day before Thanksgiving. That date is our choice.

Limitations must cover: under five seeds for E5, E6 and E8, one training box, 10 LLM attempts per cell.

pokemonred_puffer beat the game only with scripted helpers on. The PokeAgent action counts are for Emerald. We found no public RL result reaching Brock on FireRed, but re-check before claiming a first.

Out of scope: new runs, new figures, re-tuning. If results-v1 lacks a number, the writeup says so.

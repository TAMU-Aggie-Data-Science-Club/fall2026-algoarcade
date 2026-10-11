---
id: OPS-10
title: Final runs complete and results frozen
team: pm
owner: Sahil (PM)
due: 2026-11-22
estimate: 3h
depends_on: OPS-08
labels: critical-path
---
## Context
Every number in the writeup and the dashboard must come from one fixed set of runs. We stop training at a stated cutoff, freeze that set as results-v1, and prove one command recomputes the headline numbers. DOC-01, DOC-03, DOC-04 and DOC-06 work from the freeze.

## Deliverable
- A cutoff (date, time, timezone) posted on this issue before any run is stopped.
- At the cutoff every run is done, failed or stopped, with its last checkpoint and step count kept.
- `docs/results-v1/manifest.json`: one entry per run: run id, experiment, arm, seed, status, steps, git commit, SHA-256 of each Parquet file.
- `uv run poe results` recomputes every headline number from Parquet and writes `docs/results-v1/headline.json`.
- Git tag `results-v1` on the commit holding both files.
- Video review number four in docs/video-review.md.

## Acceptance criteria
- [ ] `git ls-tree -r --name-only results-v1 docs/results-v1/` prints both files.
- [ ] `uv run poe results` run twice gives a byte-identical `headline.json`. Both SHA-256 values are pasted in the pull request.
- [ ] A check command finds 0 checksum mismatches between the manifest and the frozen Parquet. Its output is pasted.
- [ ] The manifest covers every run in the queue's `status` output and the AGT-04 results file. A run left out is named with a reason.
- [ ] `headline.json` has one row per E6 run: start state, seed, steps, furthest milestone, badge yes or no. A miss keeps its row.
- [ ] The video review entry names each run id and checkpoint watched and what the agent did.

## Notes
Contract: docs/technical-plan.md, Experiments. docs/development-plan.md, Week 6 and Dates that cannot move.

Gotchas. The tag freezes code, not data: Parquet is git-ignored, so the manifest checksums are the freeze. Copy `data/runs/` off the box at the cutoff and checksum the copy, because a live run keeps writing. Fix the bootstrap seed, or the recompute is never byte-identical.

A miss on Brock is a result, and we record it as it happened. S0 runs still going at the cutoff are recorded at that step count and may continue outside results-v1.

Out of scope: new runs after the cutoff, the writeup.

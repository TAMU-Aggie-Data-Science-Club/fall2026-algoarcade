---
id: OPS-08
title: Feature freeze gate and cold-start Brock runs queued
team: pm
owner: Sahil (PM)
due: 2026-11-15
estimate: 3h
depends_on: OPS-07
labels: critical-path
---
## Context
Nov 15 is the feature freeze. After today only fixes and visualization merge, so anything not merged or queued tonight stays out of the results. OPS-10 freezes results on Nov 22 from what this gate lets through.

## Deliverable
- The checklist below, filled in on this issue with command output under each line.
- Cold-start Brock runs (E6 from S0, 2 seeds) queued behind every S1 run.
- Video review number three, posted on this issue.
- A docs/decisions.md entry dated 2026-11-15.

## Acceptance criteria
- [ ] Every experiment definition, E1 to E9, is merged. The paths are pasted.
- [ ] `uv run python -m algoarcade.runqueue status` is pasted. It shows the E6 runs from S1 (3 seeds) ahead of the E6 runs from S0 (2 seeds).
- [ ] Every finished run under data/runs/ has per-step Parquet logs and a checkpoint, and passes the schema validation from OPS-03. The pasted output gives the run count and zero failures.
- [ ] `gh pr list --state open` is pasted with each pull request marked fix, viz or deferred. None adds a feature.
- [ ] The S0 step budget is written with the measured steps per second behind it and the expected finish date.
- [ ] Video review three names the run id and checkpoint of each clip and says what the agent did.
- [ ] The whole team gets a freeze notice. docs/decisions.md lists what was cut or deferred.

## Notes
Contract: docs/development-plan.md, sections Week 5 and Dates that cannot move.

S0 runs wait behind S1 runs. The S1 result tells us whether the config can beat Brock at all.

The research estimate for S0 to Brock is 100M to 300M decisions, a guess. At 500 steps/s that is 2.3 to 7 box-days per seed. Redo the sum with the measured rate. Runs still going on Nov 22 continue, and the writeup says so.

A finished run with a missing checkpoint cannot be repaired later. Requeue it tonight.

Out of scope: analysing results (TRN-09, TRN-10) and freezing them (OPS-10).

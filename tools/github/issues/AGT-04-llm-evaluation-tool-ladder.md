---
id: AGT-04
title: LLM evaluation across the tool ladder (E7)
team: agent
owner: Agent Engineer
due: 2026-11-08
estimate: 5h
depends_on: AGT-03, ENV-07
labels: experiment
---
## Context
E7 is the LLM half of the LLM-vs-RL comparison. It measures how success and cost change as the model gets better tools. VIZ-04 builds the cost table from these results. AGT-05 reuses the successful trajectories, and DOC-04 writes them up.

## Deliverable
- A command that runs N attempts for one (model, tool level, segment). Each attempt gets a fresh server process, the same start state, a fixed action budget and a dollar cap.
- The grid: claude-haiku-5-5 at L0, L1 and L2, and claude-opus-5-5 at L2, on seg_01 to seg_03. That is 12 cells and at least 120 attempts.
- Success graded from the segment's RAM predicate (ENV-07).
- Results as Parquet and one transcript per attempt under `data/runs/`.
- A summary per cell: success rate with an exact binomial 95% interval, button presses to goal, tokens, dollars, dollars per success.

## Acceptance criteria
- [ ] A 20-action pilot ran first. Its tokens per action and the projected grid cost are in the pull request.
- [ ] A PM wrote the spending cap on this issue before the grid started. Total spend is at or under it.
- [ ] The results file has at least 10 rows per cell for 12 cells. The transcript count equals the row count.
- [ ] Test on the fake backend: two attempts in a row report different server process ids and the same start-state hash.
- [ ] Test on the fake backend: with the action cap at 5 the attempt stops at 5 actions and is graded failed.
- [ ] The summary table is pasted in the pull request. Intervals use `scipy.stats.binomtest(k, n).proportion_ci(method="exact")`: 0 of 10 gives [0, 0.31].
- [ ] Dollars per success counts the spend on failed attempts. A cell with no success shows "none".

## Notes
Contract: docs/technical-plan.md, LLM arm, and docs/harness-spec.md, MCP tool surface and Start states and segments.

Gotchas: the $200 to $500 estimate is unverified arithmetic, hence the pilot. The action cap counts tool calls, but we report button presses: one navigate_to is many presses. A 300-action cap is a guess from Emerald numbers, so calibrate it per segment with one human run. A 0% cell usually means a broken task: read three transcripts first.

Out of scope: other providers, seg_04 and seg_05, summarisation, the RL rows of the table (VIZ-04).

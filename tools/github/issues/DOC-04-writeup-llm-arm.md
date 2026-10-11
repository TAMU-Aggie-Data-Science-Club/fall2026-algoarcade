---
id: DOC-04
title: Writeup: the LLM arm and the comparison
team: agent
owner: Agent Engineer
due: 2026-11-29
estimate: 4h
depends_on: OPS-10
labels: docs
---
## Context
The language model plays through the same harness and save states as the RL policies. This section reports the tool ladder (E7), the bridge experiment (E8), their cost, and what the comparison with RL supports. DOC-01 merges it into `docs/writeup.md`. Results froze at results-v1 in OPS-10, so we run no new attempts.

## Deliverable
- `docs/writeup/llm.md`, in five parts.
- Setup: the MCP server, the four tools, levels L0 to L2, the per-attempt caps on dollars and actions, and the model ids as run.
- E7 table, one row per cell (model, tool level, segment) from the AGT-04 summary.
- E8: curriculum against none on 3 seeds, labelled exploratory, plus the long attempt from S0 (dollars, actions, furthest milestone).
- Cost: dollars and tokens per model, against the unverified $200 to $500 estimate.
- Comparison: button presses to goal for LLM and RL on the same segments, and what the comparison does not show.

## Acceptance criteria
- [ ] Every E7 cell that ran has attempts, successes, an exact binomial 95% interval, median button presses and dollars per success. Planned cells that did not run are listed as not run.
- [ ] A reviewer recomputes two intervals with `scipy.stats.binomtest(k, n).proportion_ci(method="exact")` and gets the printed bounds to two decimals.
- [ ] Total dollars equals the sum over the per-step token logs. The query and its output are pasted in the pull request.
- [ ] The file names the RAM predicate that grades success for each segment.
- [ ] E8 has a three-seed result with run ids, or one sentence saying it was not run and why.
- [ ] The comparison part states at least three limits. Candidates: 10 attempts per cell, segments that stop well before Brock, dollars and training steps as different units.

## Notes
Contract: `docs/harness-spec.md`, MCP tool surface, and `docs/technical-plan.md`, LLM arm.

10 of 10 has a lower bound of 0.69, so do not rank cells whose intervals overlap.

A cell with zero successes shows dollars per success as "none", with total dollars beside it.

Open the pull request by Wed Nov 25 (our choice of date) so DOC-01 can assemble. Out of scope: new attempts, new models, prompt changes.

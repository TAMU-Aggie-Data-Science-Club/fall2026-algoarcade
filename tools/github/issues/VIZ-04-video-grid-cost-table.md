---
id: VIZ-04
title: Agent video grid and the LLM-vs-RL cost table
team: agent
owner: Agent Engineer
due: 2026-11-22
estimate: 5h
depends_on: AGT-04, OPS-05, OPS-09
labels: viz
---
## Context
We say RL policies and a language model can be compared on identical save states. This item shows it: one side-by-side video, and one table of what each success cost. VIZ-06 assembles both, and DOC-04 builds its comparison on the table.

## Deliverable
- A cell type for the OPS-05 `--grid` composer that replays an LLM attempt from its logged button presses.
- One grid mp4 under `data/videos/grid/` for one of seg_01 to seg_03: a cell per RL agent with a checkpoint for that segment, and one for the LLM at L2.
- `src/algoarcade/viz/cost_table.py`, one row per (agent, segment). RL rows: training steps and GPU-hours to the first checkpoint whose evaluation succeeds, and button presses to goal. LLM rows, from the AGT-04 results: success rate with its exact binomial 95% interval, median button presses, dollars per success.
- An agents page in `src/algoarcade/viz/dashboard/`.

## Acceptance criteria
- [ ] `uv run pytest tests/test_agent_grid.py tests/test_cost_table.py` passes in CI with no ROM and asserts two table cells against known values.
- [ ] A test asserts frame 0 of every cell is the same pixel array before overlays.
- [ ] Replaying one successful LLM attempt ends with the segment's RAM predicate true. The result is pasted in the pull request.
- [ ] The grid mp4 plays in the rendered page with Wi-Fi off, at a size divisible by 16.
- [ ] Every table cell is computed from Parquet. An agent with no success shows "none" and the attempts or steps tried.
- [ ] The caption defines first success and names the hardware. The table is pasted in the pull request.

## Notes
Contract: docs/technical-plan.md, LLM arm and Visualization. docs/harness-spec.md, Start states and segments.

Gotchas. Align cells on button presses, not wall time. If the attempt's reset added no-op frames, the replay needs the same count. GPU-hours means wall-clock hours on the training box, and the caption says so. PokeAgent Challenge numbers are for Emerald and stay out of the table.

Fallback by Sunday: single-agent clips from OPS-05 next to each other on the page.

Out of scope: new LLM attempts, new models, E8.

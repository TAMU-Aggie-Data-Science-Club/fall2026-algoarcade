---
id: VIZ-05
title: Run registry table, second-game panel, batch video rendering
team: environment
owner: Emulation Engineer
due: 2026-11-22
estimate: 5h
depends_on: OPS-05, OPS-09, ENV-12
labels: viz
---
## Context
The run registry takes a reader from a figure to the config that produced it. The second-game panel is our evidence that the framework transfers (E9). Batch rendering gives every arm a clip. VIZ-06 assembles the pages.

## Deliverable
- `src/algoarcade/viz/registry.py`: one DuckDB query joining each run's config to its results. One row per run: run id, experiment, arm, seed, git commit, the factors that vary, steps, status, final score, furthest milestone, wall-clock hours.
- A runs page in `src/algoarcade/viz/dashboard/` with the table, sortable by any column.
- A second-game panel: IQM of `level_progress` with a 95% bootstrap band for Super Mario Land, drawn with the VIZ-02 curve function.
- `src/algoarcade/viz/render_all.py`: calls the OPS-05 renderer on the final checkpoint of every registry row that has one. It skips existing clips and ends with one line of counts: rendered, skipped, failed.

## Acceptance criteria
- [ ] `uv run pytest tests/test_registry.py` passes in CI on fake-logger data.
- [ ] The registry's row count equals the number of `run_id=` directories under `data/runs/`. Both numbers are pasted in the pull request.
- [ ] With Wi-Fi off, clicking a column header on the rendered page reorders the rows.
- [ ] The second-game caption prints the seed count and names the ENV-12 test that proves the PPO config is untouched.
- [ ] `render_all` prints counts where rendered + skipped + failed equals the registry rows with a checkpoint. The line is pasted in the pull request, with every failure named.
- [ ] A second `render_all` run renders 0 clips.

## Notes
Contract: docs/harness-spec.md, Logging schema. docs/technical-plan.md, Experiments and Visualization.

Gotchas. Never start a render by hand on the training box while final runs are going. Use the run queue, or a laptop with copied checkpoints. Check that Plotly's table sorts on click before building on it. Any other package is a new dependency and needs a PM's yes.

If E9 has under five seeds, the panel is labelled exploratory. If it did not run, the panel says so.

Fallback by Sunday: the W&B runs table, exported as an image.

Out of scope: new runs, new overlays, publishing.

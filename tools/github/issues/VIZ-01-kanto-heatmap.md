---
id: VIZ-01
title: Kanto exploration heatmap, animated across training
team: environment
owner: Memory Engineer
due: 2026-11-22
estimate: 5h
depends_on: ENV-13, OPS-09
labels: viz
---
## Context
The heatmap opens the dashboard: where the agent went, and how that changed as it trained. It joins the per-step logs to the ENV-09 coordinate table and the ENV-13 schematic map. VIZ-06 assembles it and DOC-05 publishes it.

## Deliverable
- `src/algoarcade/viz/heatmap.py`: one DuckDB query over the per-step Parquet gives visit counts per (run, checkpoint window, map_group, map_num, x, y).
- A Plotly figure over the schematic Kanto map: log colour scale, viridis or cividis, one frame per checkpoint window, a slider.
- Inset panels for warp-only maps: at least Viridian Forest (1,0) and Pewter Gym (6,2).
- A timeline of the first environment step at which each ENV-11 milestone was reached, one row per seed.
- A heatmap page in `src/algoarcade/viz/dashboard/`.

## Acceptance criteria
- [ ] `uv run pytest tests/test_heatmap.py` passes in CI with no ROM. A fake-logger run with a known walk gives exact counts for three tiles.
- [ ] For one real baseline run, the counts sum to the number of per-step rows. Both numbers are pasted in the pull request.
- [ ] The query prints rows with no ENV-09 entry, grouped by map. The count is 0 for the seven maps from Pallet (3,0) to Pewter Gym (6,2).
- [ ] `uv run poe dashboard` exits 0. The page shows the baseline arm, five seeds summed, and prints "n = 5 seeds".
- [ ] Screenshots in the pull request show two slider frames, both insets and the timeline, with the page's HTML size.
- [ ] The pull request adds no image, Parquet or map.bin file. The page uses the schematic render.

## Notes
Contract: docs/harness-spec.md, Logging schema. docs/technical-plan.md, Visualization.

Place counts with the ENV-13 pixel function at render time, so a layout bug never gets baked into data.

Plotly embeds its data in the page. Stay under the OPS-09 frame cap by merging windows.

Fallback if the global layout is not ready by Sunday: a grid of per-map heatmaps, then the W&B exploration chart exported as an image.

Out of scope: tile art, a live map stream.

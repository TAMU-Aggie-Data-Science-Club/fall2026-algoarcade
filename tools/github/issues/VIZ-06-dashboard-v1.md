---
id: VIZ-06
title: Dashboard v1 assembled and exported on real data
team: pm
owner: Co-PM
due: 2026-11-22
estimate: 4h
depends_on: OPS-09
labels: viz
---
## Context
This item puts the five week 6 panels in one dashboard on real runs. It also proves the static export works with no network, because the presentation room may have none. DOC-05 publishes what this produces.

## Deliverable
- Dashboard v1 in `src/algoarcade/viz/dashboard/` with five pages: heatmap (VIZ-01), comparisons (VIZ-02), rewards and hack catalogue (VIZ-03), agents (VIZ-04), runs and second game (VIZ-05).
- `uv run poe dashboard` renders the static site from Parquet under `data/runs/` and clips under `data/videos/`.
- A footer on every page with the git commit, the render date and the number of runs read.
- A walkthrough by Sahil (PM) and the Co-PM, each on their own laptop with Wi-Fi off.

## Acceptance criteria
- [ ] `uv run poe dashboard` exits 0 on a machine holding the real Parquet. Its last 20 lines are pasted in the pull request.
- [ ] With Wi-Fi off, the site opens from disk. Every figure responds to hover, every video plays, and the browser console shows no failed request.
- [ ] The pull request lists the run count per experiment (E1 to E9) and the output folder's size from `du -sh`.
- [ ] Both PMs comment on this issue with one line per page: pass, or the defect. Each defect has its own issue in the W7 milestone.
- [ ] A panel not merged by Sunday is replaced by a static image of the matching W&B chart, labelled "W&B fallback". This issue lists them.
- [ ] No page reads fake-logger data: the footer's run count equals the row count on the runs page.

## Notes
Contract: docs/technical-plan.md, Visualization. docs/development-plan.md, Week 6.

Gotchas. A W&B iframe needs the network, so a fallback must be an exported image. Plotly can load its JavaScript from a CDN, and the console check catches that. Render from a copy of the data, not on the training box.

OPS-10 freezes results the same day. If the tag results-v1 lands after this renders, re-render with the same command. Until then the footer marks the numbers as provisional.

Out of scope: publishing (DOC-05), visual polish, new panels.

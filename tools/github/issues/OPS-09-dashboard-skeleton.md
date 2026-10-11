---
id: OPS-09
title: Dashboard skeleton and static export spike
team: pm
owner: Co-PM
due: 2026-11-15
estimate: 3h
depends_on: OPS-03
labels: viz
---
## Context
In week 6 seven people add panels to one dashboard. If the page does not already build, that week goes to Quarto setup. This spike proves Parquet to static HTML on fake data. VIZ-01 to VIZ-06 and DOC-05 start from it.

## Deliverable
- A Quarto dashboard project under src/algoarcade/viz/dashboard/ (`_quarto.yml`, `index.qmd`, a README).
- `uv run poe dashboard` renders it to static HTML in a git-ignored folder.
- Two Plotly figures from fake-logger Parquet, queried with DuckDB at render time.
- One mp4 from the fake backend, embedded with the Quarto video shortcode.
- A size table for a Plotly heatmap with one frame per checkpoint.
- The publish target, recorded in docs/decisions.md.

## Acceptance criteria
- [ ] On a fresh clone with only fake-logger data, `uv run poe dashboard` exits 0 and writes `index.html`.
- [ ] Opened from disk with Wi-Fi off, both figures respond to hover and the mp4 plays.
- [ ] Every figure cell runs a DuckDB query over a Parquet glob. None reads a CSV or a hard-coded array.
- [ ] The pull request gives HTML size in MB for the heatmap at 10, 50 and 100 frames, and a frame cap for VIZ-01.
- [ ] docs/decisions.md names the publish target and states whether the repository is public.
- [ ] A reviewer who did not write the skeleton adds one panel by following the README, and the render still exits 0.

## Notes
Contract: docs/technical-plan.md, section Visualization, and docs/harness-spec.md, section Logging schema.

Each Plotly figure embeds its own copy of its data. Size the test grid like the ENV-09 Kanto map. A 20 MB page limit is our guess.

The repository is public, so GitHub Pages is available. We do not run `quarto publish gh-pages` here.

`quarto-cli` downloads the Quarto binary at install. List every dependency this adds in the pull request.

The video shortcode is untested inside a dashboard card. If it fails, use a plain page and say so.

Out of scope: real data, real panels, publishing (DOC-05).

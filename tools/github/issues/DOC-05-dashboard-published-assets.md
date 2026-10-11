---
id: DOC-05
title: Dashboard published and showcase assets
team: pm
owner: Co-PM
due: 2026-11-29
estimate: 4h
depends_on: VIZ-06
labels: docs
---
## Context
VIZ-06 exported dashboard v1 on real data. This item publishes it at its final address and produces what we present from: a slide deck and a two-minute demo video. It also fills in the README results section. The v1.0 tag on Mon Nov 30 (DOC-06) is the only thing after it.

## Deliverable
- The static dashboard, re-rendered at or after tag results-v1 and published with `quarto publish gh-pages`. Its address goes in `README.md`.
- A slide deck and a demo video (mp4, about 2 minutes), linked from `README.md` at addresses that open without a login.
- `README.md` results section: headline numbers with interval and seed count, the goals we reached, links to the dashboard and `docs/writeup.md`.

## Acceptance criteria
- [ ] The dashboard address in `README.md` opens in a private browser window, and every page, figure and clip loads.
- [ ] `git merge-base --is-ancestor results-v1 <commit>` exits 0 for the commit in the published footer.
- [ ] No published page contains tile-art renders. The heatmap uses the schematic Kanto map.
- [ ] The video runs between 1:45 and 2:15 (the tolerance is our choice) and plays in a browser. The pull request lists the run id behind each clip.
- [ ] Every number in the README results section equals its value in `docs/results-v1/headline.json`, with interval and seed count.
- [ ] The deck follows the event's slide and time limits, confirmed with ADSC and recorded in the pull request.

## Notes
Contract: `docs/technical-plan.md`, Visualization.

Gotchas:
- Each Plotly figure embeds its own copy of its data. The animated heatmap page can get large, so time a cold load on a phone.
- `data/videos/` is git-ignored. The clips reach the site through the render, and nothing under `data/` is committed.
- VIZ-06 proved the site works with the network off. Bring that rendered folder on a laptop in case the venue Wi-Fi fails.

The event date, talk length and slide format are not in our plan. Confirm them with ADSC before building the deck.

Out of scope: new panels, new figures, new overlays.

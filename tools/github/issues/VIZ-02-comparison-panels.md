---
id: VIZ-02
title: Comparison panels with bootstrap bands
team: training
owner: RL Engineer
due: 2026-11-22
estimate: 5h
depends_on: OPS-06, OPS-09
labels: viz
---
## Context
E1 to E4 only mean something if the reader can see the uncertainty. These panels draw the four comparisons with the OPS-06 statistics module, so every interval is computed the same way. VIZ-06 assembles the page, VIZ-05 reuses the curve function, and DOC-03 quotes the numbers.

## Deliverable
- `src/algoarcade/viz/comparison.py`, called once for each of E1 to E4. Arms and seeds come from the run data.
- Four figures per experiment:
  - IQM learning curve per arm with a 95% stratified bootstrap band, against environment steps.
  - The same metric against wall-clock hours on the training box (Ryzen 7 7800X3D), named on the axis.
  - Performance profile: the fraction of runs above each score threshold.
  - Probability of improvement of each arm over the shared baseline arm.
- The seed count per arm on every figure ("n = 5 seeds"). An arm under five seeds is labelled exploratory.
- A comparisons page in `src/algoarcade/viz/dashboard/`.

## Acceptance criteria
- [ ] `uv run pytest tests/test_comparison.py` passes in CI on fake-logger data. One case puts arm A above arm B in every seed and asserts probability of improvement is 1.0.
- [ ] `grep -rnE "trim_mean|mannwhitneyu" src/algoarcade/viz/` prints nothing: the statistics come from `src/algoarcade/training/stats.py`.
- [ ] A test renders twice from the same Parquet and asserts identical band values.
- [ ] All 16 figures render from real E1 to E4 runs, each with a seed count. Screenshots are in the pull request.
- [ ] The pull request has a pasted table of final IQM, 95% interval and n per arm. It matches the TRN-09 and TRN-10 tables, or says why not.

## Notes
Contract: docs/technical-plan.md, Experiments and Visualization. Method: Agarwal et al. 2021.

Gotchas. Bootstrap bands run narrow at small seed counts, so n is always printed. A retried run restarts from step 0 (OPS-04): check which attempt's clock is logged. Plotly embeds its data in the page, so resample long curves before plotting.

Fallback by Sunday: the W&B line chart of the same metric grouped by arm, exported as an image.

Out of scope: new statistics, new runs, E5 (VIZ-03), the second game (VIZ-05).

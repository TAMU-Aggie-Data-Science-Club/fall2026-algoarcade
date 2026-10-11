---
id: OPS-06
title: Statistics module: IQM, bootstrap intervals, profiles
team: pm
owner: Co-PM
due: 2026-11-08
estimate: 3h
---
## Context
Every comparison we publish (E1 to E5, E9) reports the same numbers, computed the same way. rliable is archived, so we write the functions ourselves over scipy. TRN-07 needs them for the E1 report this week. TRN-09 and VIZ-02 import them later.

## Deliverable
`src/algoarcade/training/stats.py` and `tests/test_stats.py`. The module docstring cites Agarwal et al. 2021 (arXiv 2108.13264).
- IQM: `scipy.stats.trim_mean(scores, 0.25)`.
- Percentile bootstrap interval over seeds, 95% by default, with a seed argument. Pooled tasks are resampled independently per task (stratified).
- Probability of improvement: Mann-Whitney U divided by n times m.
- Performance profile: the fraction of runs above each threshold.
- Every estimate prints its seed count, for example `IQM 0.62 [0.48, 0.71] (n=5)`.
- A warning below four seeds, where IQM equals the plain mean.

## Acceptance criteria
- [ ] `uv run pytest tests/test_stats.py` passes in CI.
- [ ] IQM of `[0, 1, 2, 3, 4, 5, 6, 100]` is 3.5, the mean of 2, 3, 4, 5.
- [ ] Probability of improvement of `[3, 4, 5]` over `[1, 2, 6]` is 6/9. For `[1, 2]` over `[1, 0]` it is 3.5/4: a tie counts half.
- [ ] The interval of `[0.4] * 5` is exactly `(0.4, 0.4)`, and the same seed gives the same interval twice. A two-task test shows resamples never mix tasks.
- [ ] The profile of `[0.1, 0.4, 0.6, 0.9]` at thresholds `[0.0, 0.5, 1.0]` is `[1.0, 0.5, 0.0]`.
- [ ] A 3-seed IQM call warns with "equals the mean" (`pytest.warns`). Every printed estimate contains `n=`.
- [ ] The `experiment` skill states the reporting rule: IQM, 95% interval, n, and five seeds for a headline.

## Notes
Contract: docs/technical-plan.md, sections Training and Experiments.

Gotchas: `trim_mean` cuts `int(0.25 * n)` values per side, which is zero below four seeds. `mannwhitneyu(x, y).statistic` is U for the first argument, so the hand case catches a swapped order. Three-seed intervals come out too narrow (Agarwal et al.), so n is always printed.

Out of scope: plots (VIZ-02), the binomial interval for the LLM arm (AGT-04), any new dependency.

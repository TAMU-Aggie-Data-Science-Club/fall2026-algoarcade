---
id: TRN-09
title: E1, E2 and E4 analysed; Brock runs from S1 launched (E6)
team: training
owner: RL Engineer
due: 2026-11-15
estimate: 4h
depends_on: TRN-07, ENV-10, ENV-11, OPS-06
labels: experiment, stretch
---
## Context
E1, E2 and E4 share one baseline arm on the S1-to-Pewter task. Their results choose the config for the Brock attempt (E6). The S1 Brock runs start this week so they finish before OPS-10 freezes results on Nov 22. VIZ-02 and DOC-03 take their numbers from this analysis.

## Deliverable
- An analysis script that reads Parquet under data/runs/ and prints one table for E1, E2 and E4.
- Columns: IQM, 95% bootstrap interval, probability of improvement over the baseline, seed count.
- The chosen config and the reason, in docs/decisions.md.
- An E6 experiment file: Brock from S1, 3 seeds, the chosen config, a step budget from measured throughput.

## Acceptance criteria
- [ ] The analysis command reproduces the table from Parquet, with the output pasted in the pull request.
- [ ] Every arm with fewer than 5 seeds is labelled exploratory in the table.
- [ ] The final score of every seed is listed beside the aggregates.
- [ ] The decisions entry states algorithm, observation mode and archive setting. It cites the numbers behind each choice.
- [ ] The queue listing shows 3 E6 seeds from S1 running or queued with that config.
- [ ] The pull request shows the budget arithmetic: measured steps per second, box-days available, steps per seed, expected finish date.
- [ ] E6 success is graded by FLAG_BADGE01_GET (0x820), evaluated from S1 with the archive off.

## Notes
Contract: docs/technical-plan.md, section Experiments.

With 5 seeds the IQM averages the middle three runs. Intervals on one task will be wide. Do not call a difference real when they overlap heavily.

If seeds are unfinished on Nov 15, analyse what finished and state the count.

The research estimate from S1, a guess, is a first Brock win at 15M to 50M decisions. Three seeds at 50M is 3.5 box-days at 500 steps/s. Redo the sum with the measured rate.

The Brock launch is the stretch part and slips first.

Out of scope: E3 and E5 (TRN-10), the S0 runs (OPS-08), figures (VIZ-02).

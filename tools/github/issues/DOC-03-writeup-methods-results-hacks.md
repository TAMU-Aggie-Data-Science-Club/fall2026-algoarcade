---
id: DOC-03
title: Writeup: methods, results and the hack catalogue
team: training
owner: RL Engineer, Reward Engineer
due: 2026-11-29
estimate: 4h
depends_on: OPS-10
labels: docs
---
## Context
Results froze at tag results-v1 in OPS-10. This section writes up methods and results for E1 to E6 and E9, the trainer parity evidence and the final hack catalogue. DOC-01 merges it into `docs/writeup.md`, so its numbers have to stand without edits.

## Deliverable
- `docs/writeup/rl.md`, in three parts.
- Methods: observations, actions, the 24-frame decision, reward components with weights, PQN, RND, archive resets, and the PPO config as run.
- Results, per experiment: the question, arms, seed count, IQM with a 95% bootstrap interval, probability of improvement, and run ids.
- Trainer parity: the TRN-05 figure and the Nov 1 entry in `docs/decisions.md`.
- `docs/hack-catalogue.md`, final, updated from the TRN-10 draft.

The RL Engineer writes E1, E2, E4, E6, E9 and parity. The Reward Engineer writes E3, E5 and the catalogue.

## Acceptance criteria
- [ ] `docs/writeup/rl.md` has a subsection for each of E1, E2, E3, E4, E5, E6 and E9, with seed count and run ids. Every id is in `docs/results-v1/manifest.json`.
- [ ] Each experiment has one command that rebuilds its table from Parquet. The E1 output is pasted in the pull request and matches the printed table.
- [ ] Arms that lost or tied sit in the same table as the winner, with the same statistics.
- [ ] E5 and E6 are labelled exploratory and report the mean, not IQM.
- [ ] The parity part covers CartPole, Super Mario Land and seg_02, and names the trainer that produced E1 to E6.
- [ ] E6 gives the furthest milestone per seed from S1 and from S0, including seeds that never reached Brock.
- [ ] Every catalogue entry is marked observed (run id, clip) or predicted. Each fix names its test, or says "not fixed".

## Notes
Contract: `docs/technical-plan.md`, sections Experiments, Training and Reward design.

scipy's `trim_mean` rounds the trim count down, so IQM equals the mean below 4 seeds. That is why E5 and E6 report the mean.

The Emulation Engineer ran E2 and E9. Ask for those run ids on Monday.

Open the pull request by Wed Nov 25 (our choice of date) so DOC-01 can assemble. Out of scope: new runs, re-tuning, the LLM arm (DOC-04).

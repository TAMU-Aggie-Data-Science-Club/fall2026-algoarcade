---
id: TRN-05
title: Owned PPO trainer and the parity gate
team: training
owner: RL Engineer
due: 2026-11-01
estimate: 6h
depends_on: TRN-03
labels: critical-path
---
## Context
SB3's PPO has one value head and episodic returns, and SB3 has no PQN. PQN (TRN-07) and RND (TRN-08) need a trainer we own and can explain line by line. ENV-10 and ENV-12 run on it too. We switch before the multi-seed runs so no box-days are spent twice.

## Deliverable
- `src/algoarcade/training/ppo.py`: one file derived from CleanRL's `ppo.py`, with a header naming CleanRL, the source file and its license.
- Gymnasium 1.x `AsyncVectorEnv` with `context="spawn"` and `autoreset_mode=SAME_STEP`. Truncated steps bootstrap from `info["final_obs"]`.
- An optional second value head behind a config flag, off until TRN-08.
- The same checkpoint and logging path as the TRN-01 runner, and the TRN-03 config values.
- The parity gate: owned PPO against SB3 PPO on CartPole, Super Mario Land and seg_02, 5 seeds each, identical hyperparameters. That is 30 runs.
- A docs/decisions.md entry by Nov 1, whichever way it goes.

## Acceptance criteria
- [ ] `test_truncation_bootstrap` passes: with constant reward and a fixed value function, the return at a truncated step equals r + gamma * V(final_obs).
- [ ] `test_no_cross_episode_transition` passes on the fake backend: the observation stored after a truncated step is the reset observation.
- [ ] A test gets two value outputs with the second head on and one with it off.
- [ ] Rows from the owned trainer pass the OPS-03 schema validation, and the TRN-03 evaluation path loads its checkpoint.
- [ ] The parity figure is pasted in the pull request: IQM with 95% bootstrap bands, both trainers, one panel per task. On every task the bands intersect at the last point and at 8 or more of 10 evenly spaced points.
- [ ] docs/decisions.md has an entry dated Nov 1 or earlier: owned trainer or stay on SB3, with the figure.

## Notes
Contract: docs/technical-plan.md, Training. CleanRL is source we copy with attribution, never a dependency.

Gotchas: Gymnasium 1.x defaults to next-step autoreset, which puts an invalid transition in the buffer after every episode. CleanRL's file merges termination and truncation, anneals the learning rate and uses gamma 0.99. SB3 defaults to 10 epochs and batch 64. Set every hyperparameter explicitly on both sides. OPS-06 lands a week later, so compute IQM here with `scipy.stats.trim_mean(x, 0.25)` and a percentile bootstrap over seeds.

The 8 of 10 rule is our choice. Thirty runs need box time before OPS-04 exists, so book it with Sahil (PM) on Monday. If the gate fails we stay on SB3, and the PMs decide what TRN-07 and TRN-08 do.

Out of scope: RND, PQN, recurrent policies.

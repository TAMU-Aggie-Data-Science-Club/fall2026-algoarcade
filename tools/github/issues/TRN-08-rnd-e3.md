---
id: TRN-08
title: RND and E3
team: training
owner: Reward Engineer
due: 2026-11-08
estimate: 6h
depends_on: TRN-05, OPS-04
labels: experiment
---
## Context
Count-based exploration is the proven default on Pokemon, and Pleines et al. list RND as untested there. E3 asks whether RND beats counts. Each RND detail below fails silently when wrong, so each gets a unit test. TRN-10 finishes E3 next week.

## Deliverable
RND in the owned PPO trainer behind `int_coef` (0 reproduces plain PPO):
- Separate extrinsic and intrinsic value heads.
- Intrinsic returns computed without done masking, gamma 0.99. Extrinsic gamma stays 0.997.
- Input whitened by running mean and std, clipped to plus or minus 5.
- Intrinsic reward divided by the running std of intrinsic returns.
- Input is a curated RAM slice: map_group, map_num, x, y, badge bits, milestone bits, party level sum. Never counters, play time or RNG.

The E3 experiment file: none, count, RND, 5 seeds each. The count arm is the shared baseline, so 10 runs are new.

## Acceptance criteria
- [ ] Test: the network returns two values, and with `int_coef=0` the TRN-05 parity test still passes.
- [ ] Test: on a hand-built 4-step rollout with a done at step 2, intrinsic returns equal the unmasked hand value.
- [ ] Tests: whitened input stays in [-5, 5], and a constant column gives 0, not NaN. The reward scale matches a hand case.
- [ ] Test: the input field list equals the seven fields above.
- [ ] The queue status output, pasted in the pull request, shows 5 none and 5 RND runs with the baseline's seeds.
- [ ] The pull request says how an agent could exploit the intrinsic reward.
- [ ] The `reward-component` skill describes RND as built.

## Notes
Contract: docs/technical-plan.md, sections Reward design and Training. Reference: CleanRL's `ppo_rnd_envpool.py`, attributed in the file header.

Gotchas: the target network is frozen, so an input that never repeats (a counter, a clock) gives novelty that never decays. Start the running statistics from random-policy steps. CleanRL's update proportion of 0.25 is for 128 envs; use 1.0 at 32. Write `int_coef` in the experiment file before any run. Its value and the input slice are our guesses, not published results. Milestone bits come from ENV-11, due the same day.

Out of scope: ICM, RND on pixels, a full-vector input ablation, analysing E3 (TRN-10).

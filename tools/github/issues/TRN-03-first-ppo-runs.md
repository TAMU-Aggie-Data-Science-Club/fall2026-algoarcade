---
id: TRN-03
title: First PPO runs end to end on Super Mario Land and FireRed
team: training
owner: RL Engineer
due: 2026-10-25
estimate: 5h
depends_on: TRN-01, ENV-04, ENV-05, OPS-03
labels: experiment
---
## Context
This is the first time the whole stack runs together: backend, reader, rewards, env, trainer, logs. The week 2 gate asks for a first PPO curve on FireRed. OPS-04, OPS-05, TRN-05 and TRN-06 start from the checkpoints, logs and config this produces.

## Deliverable
SB3 2.9 PPO through `AlgoArcadeEnv` with SubprocVecEnv (spawn), launched by the TRN-01 runner:
- Super Mario Land, 3 seeds.
- FireRed seg_01 (leave the house) and seg_02 (Pallet to Route 1), 3 seeds each.
- Config: gamma 0.997, GAE 0.95, n_steps 2048, 3 epochs, lr 3e-4 constant, entropy 0.01, clip 0.2. Observation normalisation on, reward normalisation off.
- A checkpoint every 500,000 steps, with the normalisation statistics beside it.
- Logging through the OPS-03 writer to `data/runs/run_id=ID/`, and to W&B.

Run length is your call. 1M to 2M steps is a guess.

## Acceptance criteria
- [ ] A test asserts the experiment config has gamma 0.997 and reward normalisation off.
- [ ] All 9 runs have Parquet files under `data/runs/` that pass the OPS-03 schema validation. Output pasted in the pull request.
- [ ] Super Mario Land: in each seed, mean `level_progress` over the last 10% of steps beats the first 10%. Numbers posted here.
- [ ] FireRed seg_01: in at least one seed the goal predicate turns True in some episode. Post the run id and step.
- [ ] Each run has a checkpoint per 500,000 steps, and one loads and plays an episode.
- [ ] The curves, W&B links and a five-line reading of them are posted here. Say what did not learn.
- [ ] The `experiment` skill gives the launch command used here.

## Notes
Contract: docs/technical-plan.md, section Training. docs/harness-spec.md, section Logging schema.

Gotchas: SB3 defaults gamma to 0.99. Guard the entry point with `if __name__ == "__main__":` or the spawned workers fail to start.

ENV-05 and OPS-03 land this week too. Start on the FakeBackend env with a stub logger.

Three seeds is exploratory. Label every figure that way.

Out of scope: the owned trainer (TRN-05), the run queue (OPS-04), reward tuning (TRN-06).

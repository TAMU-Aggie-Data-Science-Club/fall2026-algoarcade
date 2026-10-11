---
id: TRN-01
title: Training runner v0 on Stable-Baselines3
team: training
owner: RL Engineer
due: 2026-10-18
estimate: 4h
---
## Context
Every experiment in this project goes through one runner. TRN-03 uses it for the first PPO runs on Super Mario Land and FireRed, and TRN-05 measures our own trainer against it. A run we cannot trace to a config and a commit is a run we cannot report.

## Deliverable
- A frozen dataclass config with a tyro command line, under `src/algoarcade/training/`.
- One command that trains Stable-Baselines3 PPO on any registered Gymnasium env id. Put the exact command in the pull request.
- A directory per run, under `data/runs/` by default. It holds the resolved config, the git commit, checkpoints at a fixed step interval and an evaluation result.
- `gamma` as an explicit config field passed to PPO. The library default never applies by omission.
- Results for `CartPole-v1` and `Acrobot-v1`, 5 seeds each.

## Acceptance criteria
- [ ] The command on `CartPole-v1`, seed 0, creates one run directory. It holds the resolved config, the commit hash with a dirty-tree flag, at least two checkpoints and an evaluation file. A directory listing is pasted in the pull request.
- [ ] A test builds the model from a config and asserts `model.gamma` equals the config value. A second test reloads a saved config and gets an equal object.
- [ ] A CI smoke test trains CartPole for at most 2,000 steps into a temporary directory and finds all four artifacts. It needs no ROM.
- [ ] `CartPole-v1`: final mean evaluation return of at least 475 on at least 4 of 5 seeds. `Acrobot-v1`: at least -100 on at least 4 of 5 seeds. Both numbers are the env's own `reward_threshold`.
- [ ] The pull request has a table of the 10 runs (env, seed, steps, evaluation return, wall time) and one learning-curve figure per env.
- [ ] The `experiment` skill shows the real command and the run directory layout.

## Notes
Background: docs/technical-plan.md (Training, Experiments).

Gotchas:
- SB3's PPO defaults are gamma 0.99, 10 epochs, batch 64 and entropy 0. Ours are gamma 0.997, GAE 0.95, n_steps 2048, 3 epochs, lr 3e-4, entropy 0.01 and clip 0.2. Pass every one from the config.
- `SubprocVecEnv` needs an `if __name__ == "__main__":` guard. Set `start_method="spawn"` so every OS behaves the same.

We set no step budget for the two control tasks. Pick one, state it, and treat it as a guess. The 4-of-5 bar is also a guess. Classic control needs no extra system packages. Tracking is an off-by-default flag here, because OPS-01 may not have landed.

Out of scope: Parquet logging (OPS-03), the FireRed env (ENV-05), our own trainer (TRN-05) and the run queue (OPS-04).

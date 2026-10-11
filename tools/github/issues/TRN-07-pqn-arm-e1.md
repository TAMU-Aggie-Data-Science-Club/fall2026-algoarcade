---
id: TRN-07
title: PQN arm and E1
team: training
owner: RL Engineer
due: 2026-11-08
estimate: 6h
depends_on: TRN-05, OPS-04
labels: experiment
---
## Context
E1 asks whether a value-based learner matches PPO when both consume the same vectorised rollouts. PQN is built for that: Q-learning with no replay buffer and no target network. E1 is the one experiment the Nov 8 gate needs finished. TRN-09 analyses it next week.

## Deliverable
- `src/algoarcade/training/pqn.py`, one file, derived from CleanRL's `pqn.py`. The header gives the source URL, commit and license notice.
- LayerNorm Q-network, Q(lambda) returns, epsilon annealing. Start from CleanRL's defaults: lambda 0.65, epsilon 1.0 to 0.05 over the first half of training.
- Vector env, logging and checkpoint code imported from the owned PPO file, not copied.
- E1: PPO vs PQN, 5 seeds each, S1-to-Pewter, same env count and step budget. The PPO arm is the shared baseline from OPS-07.

## Acceptance criteria
- [ ] PQN on CartPole-v1 reaches mean episodic return 400 within 500k steps on 3 seeds. Curves pasted in the pull request. The threshold is a guess.
- [ ] Unit test: Q(lambda) returns on a hand-computed 3-step rollout match to 1e-6. One case terminates, one truncates and bootstraps.
- [ ] `grep -c "VectorEnv(" src/algoarcade/training/pqn.py` prints 0. The file has no replay buffer and no target network.
- [ ] 10 E1 runs finished: 5 PPO, 5 PQN, same seeds. Run ids in the pull request.
- [ ] The pull request has the OPS-06 table: IQM, 95% bootstrap interval and n per arm, plus probability of improvement. All ten seed curves are attached.
- [ ] The report says which arm won or that the intervals overlap. If PQN lost, it says so with the numbers.

## Notes
Contract: docs/technical-plan.md, sections Training and Experiments.

Gotchas: CleanRL's file treats truncation as termination. Ours bootstraps from `info["final_obs"]` under SAME_STEP autoreset. CleanRL fixed a done-masking bug in the return in Feb 2025 (PR 494), so copy from a later commit.

At the 500 steps/s planning figure, 5 PQN runs at 15M steps take about 1.7 box-days. Submit the arm by Wed Nov 4. Name the E1 metric in the experiment file before any run.

We found no PQN result at 16 to 64 envs on a long sparse-reward task. A PQN that loses is a result, so do not retune after seeing curves.

Out of scope: QR-DQN, PQN on pixels, sweeps.

# Arcadia — Advanced

*ADSC Catalyst Project · Fall 2026*

## Overview

Arcadia trains reinforcement-learning agents to play games through trial and error, compares different RL algorithms head-to-head, and visualizes how strategies improve over time. The final artifact is a set of trained agents plus learning-curve comparisons and playable recordings.

## Objective

Ship a comparative study of at least two RL algorithms on 2–3 environments, with rigorous training logs, reproducible seeds, and a demo that shows the trained agents actually playing.

## Suggested tech stack

- **Environments:** Gymnasium, PettingZoo (multi-agent, if you want to go there)
- **Algorithms:** Stable-Baselines3 (DQN, PPO, A2C)
- **Modeling framework:** PyTorch
- **Visualization:** TensorBoard for training curves, Matplotlib for cross-run comparisons, Pygame for playback
- **Data sources:** Environments themselves (synthetic — no external dataset)

See [`DATA.md`](DATA.md) for how RL "data" works in this project.

## What team members will gain

- Modern RL algorithms as used in real-world applications
- Sequential decision-making through interactive environments
- Rigorous experiment tracking — the difference between "we tried a thing" and "we have a defensible comparison"

## Suggested scope (v1)

Pick **2–3 environments** at different difficulty levels — e.g., CartPole (sanity check), LunarLander (moderate), and one Atari game (stretch). Compare **DQN vs. PPO**.

Build:

1. Training scripts with clean seed management, config-driven hyperparameters, and TensorBoard logging,
2. Reproducible training runs (multiple seeds per algorithm × environment),
3. Cross-run comparison plots: learning curves with confidence bands, final-return distributions,
4. Video recordings of trained agents playing,
5. Streamlit or notebook writeup with the comparison + gameplay clips.

**Out of scope for v1:** distributed training across machines, novel algorithm invention, model-based RL, complex reward shaping, multi-agent competitive setups.

**Compute reality.** Atari agents may need 10M+ frames. Budget wisely — you can make solid contributions on CartPole + LunarLander alone. Atari is a stretch.

See [`DELIVERABLES.md`](DELIVERABLES.md) for the suggested deliverable breakdown and rough timeline.

## Repository map

| File / folder | Purpose |
|---|---|
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | **Start here.** How the team runs the project on GitHub — PM vs. member roles, the issue → PR → `main` flow, branching, worktrees, reviews. |
| [`DELIVERABLES.md`](DELIVERABLES.md) | Suggested deliverables and rough timeline. A living plan, not a contract. |
| [`DATA.md`](DATA.md) | Notes on RL "data" (environments + logs), and how to reproduce runs. |
| [`data/`](data/) | Local working folder for training logs and checkpoints. **Git-ignored** — nothing here is committed. |
| [`AGENTS.md`](AGENTS.md) | Machine-facing workflow rules for AI coding agents. |

## Notes for PMs

This README, [`DELIVERABLES.md`](DELIVERABLES.md), and [`DATA.md`](DATA.md) are **suggestions**, not commitments. Rewrite them as the team scopes the real project.

## Notes for members

Read [`CONTRIBUTING.md`](CONTRIBUTING.md) before touching code. Then pick up an issue from the board.

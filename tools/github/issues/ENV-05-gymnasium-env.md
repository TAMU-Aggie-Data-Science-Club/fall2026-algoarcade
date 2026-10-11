---
id: ENV-05
title: AlgoArcadeEnv: the Gymnasium environment
team: environment
owner: Emulation Engineer
due: 2026-10-25
estimate: 5h
depends_on: ENV-01, TRN-02
labels: critical-path
---
## Context
RL trainers reach every game through this one class. TRN-03 cannot produce the week 2 PPO curve without it, and ENV-08 builds archive resets on its reset path.

## Deliverable
`AlgoArcadeEnv` in `src/algoarcade/envs/`, built from a backend, a StateReader, reward components, a start state and an observation mode.
- One step is 24 frames: hold 8, release 16.
- `Discrete(6)` by default: up, down, left, right, A, B. Start and a no-op are config options.
- Truncation only, at the step budget.
- `reset(seed=s)` loads the start state, then runs 0 to 7 seeded no-op frames. The range is a guess.
- `info` carries each reward component by name, the `(map_group, map_num, x, y)` tuple and the milestone bits.
- Observation v1 (`symbolic`): the scaled state vector plus a player-centred crop of visited tiles.

## Acceptance criteria
- [ ] `uv run pytest -k env_checker` passes in CI: `gymnasium.utils.env_checker.check_env` raises nothing on FakeBackend.
- [ ] `uv run pytest -k golden_trace` passes in CI: seed 0 and 500 fixed actions reproduce the stored FakeBackend trace.
- [ ] On PyBoyBackend (Super Mario Land) and MgbaBackend (FireRed), two processes with the same seed and actions give identical traces. Output pasted in the pull request.
- [ ] A test asserts `truncated` is True only on the budget's last step and `terminated` never is.
- [ ] A test asserts one step advances the backend 24 frames, button down for the first 8.
- [ ] A test asserts the components in `info` sum to the reward, and ten reset seeds give at least two no-op counts.
- [ ] docs/harness-spec.md, section AlgoArcadeEnv, states the spaces, `info` keys and crop size the code uses.

## Notes
Contract: docs/harness-spec.md, section AlgoArcadeEnv.

Gotchas: without reset noise, every worker replays the same episode. SubprocVecEnv uses spawn, so create the backend inside the env factory. Super Mario Land has no map ids. Agree its location tuple with the ENV-04 reader.

Do not wait for ENV-07: any ENV-03 save state works here.

Out of scope: the walkability channel and `pixels` mode (ENV-10), archive resets (ENV-08).

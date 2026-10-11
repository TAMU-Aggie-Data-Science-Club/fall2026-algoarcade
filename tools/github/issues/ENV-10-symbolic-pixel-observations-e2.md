---
id: ENV-10
title: Symbolic and pixel observations, and E2
team: environment
owner: Emulation Engineer
due: 2026-11-08
estimate: 5h
depends_on: ENV-09, TRN-05
labels: experiment
---
## Context
ENV-09 gives us walkability per tile, which the symbolic observation has lacked since ENV-05. The published Pokemon Red agents trained on pixels, so E2 asks whether our cheaper symbolic observation matches them. TRN-09 analyses E2 on Nov 15, so the pixel arm must be queued this week.

## Deliverable
- `symbolic`: the player-centred grid crop gets a walkability channel (from ENV-09) next to the visited channel.
- `pixels`: 72x80 greyscale, 3 stacked frames, plus the same state vector. `both` is the union.
- Rendering cost: steps per second in each mode on one machine, same env count, random policy.
- The E2 experiment file: the shared baseline config with one factor, the observation mode, at 5 seeds. The symbolic arm is the OPS-07 baseline, so only 5 pixel runs are new.

## Acceptance criteria
- [ ] Test: the `symbolic` grid has 2 channels. On a fixture map a wall tile reads not walkable, and the tile the player just left reads visited.
- [ ] Test: the `pixels` frame stack is 3 x 72 x 80, uint8. Its state vector equals the `symbolic` one for the same emulator state.
- [ ] `gymnasium.utils.env_checker.check_env` passes in all three modes on the fake backend.
- [ ] The pull request has the measurement: steps per second per mode, machine, env count, command. There is no threshold.
- [ ] The queue status output shows 5 pixel runs with the baseline's seeds and step budget. A printed config diff shows only observation mode and policy encoder differ.
- [ ] The OPS-03 schema test passes unchanged, and docs/harness-spec.md (AlgoArcadeEnv) lists the final shapes.

## Notes
Contract: docs/harness-spec.md, AlgoArcadeEnv, and docs/technical-plan.md, Experiments.

Gotchas: the GBA frame is 240x160, so 72x80 (half a Game Boy frame) is an uneven resize: 3x across, about 2.2x down. Pick one method and write it in the spec. Pixels need a CNN encoder, a difference E2 cannot remove, so record both parameter counts. Agree with the RL Engineer on who adds the encoder.

Out of scope: tuning either arm, colour, other stack sizes, analysing E2 (TRN-09).

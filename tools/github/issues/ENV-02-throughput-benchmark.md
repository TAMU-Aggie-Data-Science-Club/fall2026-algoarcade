---
id: ENV-02
title: Throughput benchmark on the training box and the M4
team: environment
owner: Sahil (PM)
due: 2026-10-18
estimate: 3h
depends_on: ENV-01
---
## Context
Every compute plan we have rests on a guess: 500 agent steps per second on the 7800X3D, about 43M steps a day. We found no published number for headless mGBA driven from Python on a GBA game. The measured figure sets frameskip and env count for ENV-05 and the run budget for TRN-03 and OPS-04. Sahil owns this because both machines are his.

## Deliverable
- `scripts/benchmark.py`, run with FireRed on `MgbaBackend`. It measures:
  - Emulator frames per second on one core, in 4 cells: render on or off, with or without a state read.
  - Agent steps per second under a random policy, in 16 cells: frameskip 8, 16, 24, 48 by 4, 8, 12, 16 envs.
- docs/benchmarks.md with both tables for the 7800X3D and for the M4 Pro.
- A note per frameskip on whether menu inputs still register.
- The compute budget in docs/technical-plan.md (Experiments), recomputed from the measured number.

## Acceptance criteria
- [ ] docs/benchmarks.md opens with the exact command that reproduces each table, plus the commit, OS and date of each run.
- [ ] For each machine the file holds 4 frames-per-second cells and 16 steps-per-second cells, none empty.
- [ ] Each cell runs for at least 30 seconds and reports the median of 3 runs.
- [ ] For each frameskip, the file gives the hold and release split used and how many of 20 scripted menu presses moved the cursor.
- [ ] docs/technical-plan.md (Experiments) replaces the 500 steps per second guess with the measured figure at 24 frames. It shows the arithmetic for steps per day and box-days for E1 to E4.
- [ ] Raw script output for both machines is pasted in the pull request.

## Notes
Background: docs/technical-plan.md (Simulation layer, Experiments). The box needs OPS-01 done first.

"State read" means one pass over EWRAM and IWRAM through `read()`. Use StateReader v0 if ENV-03 has merged, and say which you used. Run one emulator per process with the spawn start method, so every OS behaves the same.

The default decision is 24 frames (hold 8, release 16). The other three splits are yours to choose and record. The menu check needs a hand-made save state with a menu open, kept under `data/states/`. The 30 seconds and the 20 presses are guesses.

If the 7800X3D gives under 250 steps per second at 24 frames, tell the Co-PM the same day. E1 to E4 would need re-scoping.

Out of scope: policy inference cost and PyBoy numbers.

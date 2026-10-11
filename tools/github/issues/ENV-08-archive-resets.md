---
id: ENV-08
title: Archive resets: return to the frontier
team: environment
owner: Emulation Engineer
due: 2026-11-01
estimate: 4h
depends_on: ENV-05, ENV-07
---
## Context
From a cold start the agent replays the intro and the parcel quest every episode before it sees anything new. pokemonred_puffer reports that sharing save states between envs ended months of stalled training. OPS-07 schedules E4 and the first cold-start run on this, and AGT-05 reuses the reset path.

## Deliverable
- Env side: the first time an episode reaches a cell, `info` carries the save state and the episode's visited set.
- Trainer side: one archive in the main process, keyed by (map_group, map_num, x//4, y//4, badge bits, milestone count). A cell keeps the state bytes, the visited set and a selection count.
- Reset: with probability p (config, default 0.5) load a cell sampled with weight 1/sqrt(1 + selections). Otherwise load the fixed start state.
- Evaluation always runs with the archive off.
- Training logs the share of archive resets every rollout.
- It runs under the SB3 runner now and the TRN-05 trainer later, with no new dependency.

## Acceptance criteria
- [ ] Test on the fake backend: with p = 1 and one archived cell, reset lands on that cell's location with its visited set.
- [ ] Test: after an archive reset, the reset step and a step onto an already visited tile pay zero on every reward component.
- [ ] Test: with p = 0, and in evaluation mode at p = 1, 200 resets all load the fixed start state.
- [ ] Test: cells with selection counts 0, 3 and 8 are drawn within 0.02 of 0.545, 0.273 and 0.182 over 20,000 seeded draws.
- [ ] Test: with p = 0.5 and a non-empty archive, the logged share over 1,000 seeded resets is between 0.45 and 0.55.
- [ ] A 200k-step PPO run on seg_02 with the archive on finishes on the box. Archive size, bytes per cell and reset share are pasted in the pull request.

## Notes
Contract: docs/harness-spec.md, AlgoArcadeEnv, and Start states and segments.

Gotchas: vector envs reset inside the worker, so the trainer cannot pass options at reset. Hand each worker its next start state ahead of time (`env_method` on SB3, `call` on Gymnasium's AsyncVectorEnv). The "new maximum" reward terms must start from the loaded state's values, or a loaded badge pays again.

p = 0.5 and the 4-tile cell are starting guesses. Use the reward v1 milestone count until ENV-11 lands its list.

Out of scope: running E4 (OPS-07), LLM start states (AGT-05), keeping the archive between runs.

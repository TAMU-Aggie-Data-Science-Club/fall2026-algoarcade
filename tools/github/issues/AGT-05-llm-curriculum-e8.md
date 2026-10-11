---
id: AGT-05
title: LLM trajectories as an RL start-state curriculum (E8)
team: agent
owner: Agent Engineer
due: 2026-11-15
estimate: 5h
depends_on: AGT-04, ENV-08
labels: experiment, stretch
---
## Context
A successful LLM run passes through states PPO could start from. E8 asks whether PPO learns Viridian Forest faster from those states, latest first. DOC-04 reports the result. This stretch item slips first if the week is short.

## Deliverable
- State capture in the LLM loop: a save state every k actions, kept only if the run succeeds, with a manifest.
- A reset wrapper: PPO episodes start from the latest state, then earlier ones as success rises.
- An E8 experiment file: curriculum against none on seg_05 (Viridian Forest), 3 seeds.
- One long LLM attempt from S0 toward Viridian City under a hard dollar cap.

## Acceptance criteria
- [ ] A successful seg_05 attempt writes ordered states and a manifest under data/states/. The manifest gives each state's action index and (map_group, map_num, x, y).
- [ ] A named FakeBackend test shows the wrapper starts at the last state, then steps one state earlier once success crosses the threshold.
- [ ] A named test shows every reward component pays zero on the first step after a curriculum reset.
- [ ] The queue listing shows 3 seeds per E8 arm. Evaluation starts from the fixed seg_05 state with the curriculum off.
- [ ] E8 results state the seed count and are labelled exploratory.
- [ ] The long attempt's log shows dollars spent at or under the cap, the action count and the farthest milestone.

## Notes
Contract: docs/harness-spec.md, sections Start states and segments, and AlgoArcadeEnv.

k and the threshold are config values, guessed at k = 10 and 80% success over 100 episodes.

Reuse the ENV-08 reset path, including its rule for the visited set in a saved state.

Sahil (PM) writes the dollar cap here before the long attempt. Emerald first-gym runs took 649 to 1,608 actions (a proxy), so the segment action cap is too low.

If AGT-04 has no successful seg_05 attempt, say so here first. A human-recorded run changes the claim and is a PM call.

Out of scope: LLM reward search, online subgoals, new MCP tools.

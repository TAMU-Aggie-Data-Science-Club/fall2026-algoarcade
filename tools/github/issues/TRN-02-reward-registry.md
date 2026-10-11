---
id: TRN-02
title: Reward registry with isolation tests
team: training
owner: Reward Engineer
due: 2026-10-18
estimate: 4h
---
## Context
Every reward term in AlgoArcade is a named component with a weight in config and its own log column. ENV-05 calls the registry from the Gymnasium env next week, and TRN-04 builds reward v1 and the exploit tests on top of it. Components are written against the GameState protocol and tested on the fake game, so all of this runs in CI with no ROM.

## Deliverable
- A registry under `src/algoarcade/rewards/` that builds components from a config of name to weight.
- One step call that returns the weighted sum, plus each component's raw (unweighted) value under `info`.
- Five components: `explore`, `events`, `level`, `badge` and `milestone`. Each is a positive-only "new maximum" term.
- Tests on FakeBackend, including the isolation tests below.

## Acceptance criteria
- [ ] Building a registry from a config with an unknown component name raises and lists the valid names.
- [ ] Over a 200-step random rollout on the fake game, the returned reward equals the sum of weight times raw value (tolerance 1e-9). `info` carries one raw value per configured component.
- [ ] One parametrised test covers all five components and asserts exactly 0.0 on the reset step and on a no-op step.
- [ ] Over 1,000 random steps no component returns a negative value. Revisiting a tile pays 0 from `explore`. A level sum that drops and returns to its old maximum pays 0 from `level`.
- [ ] A test shows per-episode state cleared by reset: `explore` pays again for a tile visited in the previous episode.
- [ ] The pull request says, for each component, how an agent could exploit it.
- [ ] The `reward-component` skill matches what was built: how to add a component and which tests it must pass.

## Notes
Contract: docs/harness-spec.md (Reward registry, Fake backend and fake logger). The protocol is in `src/algoarcade/rewards/base.py`.

Gotchas:
- The starting tile counts as visited at reset. Otherwise the reset step pays.
- A no-op step means the state did not change. A button press that changes nothing must also pay 0.

The fake game has a position, a door and one flag, and no badges or levels. Build those GameStates by hand in the tests. The level cap and the weights are guesses until TRN-04.

Out of scope: the five off-by-default components (heal, blackout, anti_loop, anti_spam, time) and the FireRed flag whitelist (ENV-06). Also out: wiring into the env (ENV-05), scripted exploit policies (TRN-04) and reward normalisation.

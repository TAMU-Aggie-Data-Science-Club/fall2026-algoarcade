---
id: ENV-12
title: Second game complete: Super Mario Land with the untouched config (E9)
team: environment
owner: Emulation Engineer
due: 2026-11-15
estimate: 4h
depends_on: ENV-04, TRN-05
labels: experiment
---
## Context
We claim a new game costs a reader and a reward config, with the trainer untouched. E9 tests that on Super Mario Land with the PPO config we use on FireRed. VIZ-05 draws the second-game panel from these runs. DOC-02 finishes the adding-a-game guide from the port diary.

## Deliverable
- An E9 experiment file: Super Mario Land on the PyBoy backend, 8 to 10 seeds, PPO config identical to the FireRed baseline.
- Finished runs under data/runs/ with Parquet logs and checkpoints.
- docs/port-diary-super-mario-land.md: every file touched to add the game, with lines changed.
- docs/adding-a-game.md, drafted from the diary as numbered steps.

## Acceptance criteria
- [ ] A named test asserts the E9 PPO config equals the FireRed baseline PPO config field by field.
- [ ] At least 8 seeds have finished and pass the schema validation from OPS-03, with the output pasted.
- [ ] The pull request reports IQM of final `level_progress` with a 95% bootstrap interval and the seed count, from the OPS-06 stats module.
- [ ] The diary totals files and lines from `git log --numstat`. It lists every file changed outside src/algoarcade/games/ and src/algoarcade/backends/pyboy.py, each with a reason.
- [ ] Each step in docs/adding-a-game.md names the file to create and the command that checks it.
- [ ] The pull request gives measured steps per second and hours per seed.

## Notes
Contract: docs/harness-spec.md, sections GameBackend and Conformance tests.

We found no published PPO step count for clearing level 1-1 on PyBoy. Measure it in the first session, then choose 8 or 10 seeds. Eight is enough in a short week.

PyBoy's wrapper reads score and coins from on-screen tiles. Only lives, time, world and `level_progress` are RAM-backed. Use those as the oracle.

If the TRN-05 parity gate failed, the untouched config is SB3's. Say which trainer ran.

Do not tune gamma or entropy for Mario. A weak result with the untouched config is the finding.

Out of scope: the dashboard panel (VIZ-05), the final guide (DOC-02), Metroid Zero Mission.

# Deliverables & Timeline

> **How to read this file.** This is the PMs' current plan for what AlgoArcade ships and when. It is a living plan, not a contract. The authoritative picture lives in **GitHub Issues and the Project board**. The week-by-week assignment is in [`docs/development-plan.md`](docs/development-plan.md).

Kickoff was October 11 2026. A deliverable is due every Sunday through November 29, and v1.0 is tagged on November 30.

## Milestones

| # | Deliverable | Description | Owner (role) | Target | Issues |
|---|-------------|-------------|--------------|--------|--------|
| 1 | Team onboarded, repo live | Everyone set up, ROMs verified, CartPole curve posted. Training box reachable, `main` protected, issues loaded. | PMs, everyone | Oct 18 | ALL-01, OPS-01, OPS-02 |
| 2 | Three backends, one interface | mGBA (FireRed) and PyBoy (Super Mario Land) pass the same conformance suite as the fake backend. | Emulation Engineer, Co-PM | Oct 18 | ENV-01, ENV-04 |
| 3 | Throughput benchmark | Measured steps per second on both machines. Every compute budget is recomputed from it. | Sahil (PM) | Oct 18 | ENV-02 |
| 4 | FireRed StateReader | Position, party and badges first, then the full GameState, then battle state and milestones. Staged so week 1 is not blocked on the hard fields. | Memory Engineer | Oct 18, Oct 25, Nov 8 | ENV-03, ENV-06, ENV-11 |
| 5 | Training runner | One command trains PPO and writes a reproducible run directory. | RL Engineer | Oct 18 | TRN-01 |
| 6 | Reward registry and exploit tests | Named, separately logged components. Each known hack is a scripted test. | Reward Engineer | Oct 25 | TRN-02, TRN-04 |
| 7 | Gymnasium environment and start states | AlgoArcadeEnv on all three backends. Start states S0 and S1, five segments. | Emulation Engineer, Co-PM | Oct 25 | ENV-05, ENV-07 |
| 8 | Logging pipeline and schema freeze | Parquet writer, fake logger, schema frozen. Runs logged before this are thrown away. | Sahil (PM) | Oct 25 | OPS-03 |
| 9 | First learning curves | PPO on Super Mario Land and two FireRed segments. | RL Engineer | Oct 25 | TRN-03 |
| 10 | MCP server and LLM loop | The same harness exposed to a language model, with hard cost caps. | Agent Engineer | Oct 25 | AGT-01, AGT-02 |
| 11 | Run queue | The training box runs experiments unattended. The matrix does not fit without it. | Sahil (PM) | Nov 1 | OPS-04 |
| 12 | Baseline reproduced, trainer decided | Early segments cleared over five seeds. Our PPO trainer passes or fails its parity gate. | Training pair | Nov 1 | TRN-05, TRN-06 |
| 13 | Map data and archive resets | World coordinates and walkability from the game's own data. Return-to-frontier resets. | Environment pair | Nov 1 | ENV-08, ENV-09 |
| 14 | Evaluation tooling | Checkpoint to video, and the statistics module. | Co-PM | Nov 1, Nov 8 | OPS-05, OPS-06 |
| 15 | LLM tool ladder (E7) | Three tool levels, ten attempts per configuration, cost per success. | Agent Engineer | Nov 8 | AGT-03, AGT-04 |
| 16 | Method experiments (E1 to E5) | PPO against PQN, symbolic against pixels, count against RND, archive resets, penalties. Five seeds each for E1 to E4. | Training pair, Emulation Engineer, Sahil (PM) | Nov 15 | TRN-07, TRN-08, TRN-09, TRN-10, ENV-10, OPS-07 |
| 17 | Second game (E9) | Super Mario Land trained with the untouched PPO config, and a diary of what the port touched. | Emulation Engineer | Nov 15 | ENV-12 |
| 18 | Feature freeze | Every experiment done or queued. Only fixes and visuals merge afterwards. | Sahil (PM) | Nov 15 | OPS-08 |
| 19 | Brock runs (E6), stretch | Best config from the post-parcel state, then from a cold start. Reported as it lands. | RL Engineer, Sahil (PM) | Nov 22 | TRN-09, OPS-08, OPS-10 |
| 20 | LLM-to-RL curriculum (E8), stretch | LLM trajectories as start states for PPO. First to slip. | Agent Engineer | Nov 15 | AGT-05 |
| 21 | Dashboard | Kanto heatmap, comparison panels, reward decomposition, agent video grid, run registry, in one static site. Built in week 6 by everyone (PM decision: no visualization work before then). | Everyone | Nov 22 | OPS-09, ENV-13, VIZ-01 to VIZ-06 |
| 22 | Results freeze | Final runs finished or cut off, numbers recomputed from Parquet. | Sahil (PM) | Nov 22 | OPS-10 |
| 23 | Writeup and showcase | Methods, results, the hack catalogue, deck and demo video. | Everyone | Nov 29 | DOC-01 to DOC-05 |
| 24 | Reproducibility check, v1.0 | A fresh clone reproduces one result. Tag and retro. | Emulation Engineer, PMs | Nov 30 | DOC-06 |

## Timeline

```
Week ending:   Oct18  Oct25  Nov1   Nov8   Nov15  Nov22  Nov29
               |------|------|------|------|------|------|
Setup, boot    ██████
Backends       ██████
StateReader    ██████ ██████        ██████
Env, rewards          ██████
Schema freeze         ▲
Run queue                    ██████
Baseline                     ██████
Experiments                         ██████ ██████
LLM arm        ██████ ██████ ██████ ██████ ██████
Second game    ██████ ██████               ██████
Feature freeze                             ▲
Brock runs                                 ██████ ██████
Dashboard                                         ██████
Results freeze                                    ▲
Writeup                                                  ██████
```

## Working agreements

- **Each deliverable maps to one or more GitHub Issues.** The board is the source of truth; this file is the summary.
- **Four dates do not move:** schema freeze (Oct 25), run queue (Nov 1), feature freeze (Nov 15), results freeze (Nov 22). Everything else is an estimate.
- **"Done" is defined per issue** via acceptance criteria, not by a date passing.
- **Reprioritize openly.** If a deliverable is cut or moved, a PM writes why in the issue and in [`docs/decisions.md`](docs/decisions.md).

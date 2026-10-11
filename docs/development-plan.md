# Development plan: October 11 to November 30

Seven weeks, seven Sunday deliverables. Each person owns one issue a week, sized at about five hours. The issue ids below match GitHub; each issue carries its own description and acceptance criteria.

What we are building and why is in [technical-plan.md](technical-plan.md). This file is who does what, by when.

## The team

| Who | Role | Lane | What they own across the project |
|---|---|---|---|
| Sahil | Sahil (PM) | PM | Training machines, logging schema, run queue, video review, the four freeze dates |
| Co-PM (name to come) | Co-PM | PM | GitHub and reviews, PyBoy backend, start states, video renderer, statistics, dashboard |
| Member 1 | Emulation Engineer | Environment | Backends, the Gymnasium env, archive resets, observations, the second game |
| Member 2 | Memory Engineer | Environment | Addresses, StateReader, map data, battle state, the Kanto map |
| Member 3 | RL Engineer | Training | Training runner, our PPO trainer, PQN, the main experiments, Brock runs |
| Member 4 | Reward Engineer | Training | Reward components, exploit tests, the baseline, RND, the hack catalogue |
| Member 5 | Agent Engineer | Agent | MCP server, tools, the LLM loop, LLM evaluation, the bridge experiment |

Issues are assigned by role. Names replace the placeholders here and in [`CODEOWNERS`](../CODEOWNERS) once the lanes are filled.

## How a week works

- Sunday: sync. Everyone demos what they shipped. The deliverable is due before the sync, merged or in review.
- Monday: pick up next week's issue. Read it, ask questions the same day.
- Thursday: post two sentences in the channel: what you did and what blocks you. Anything not in review by Thursday gets a PM pairing session.
- Every week one PM watches five minutes of agent footage and writes what they saw in `docs/video-review.md`.

A deliverable counts when its acceptance criteria are checked and the evidence is in the pull request. Nothing counts because a date passed.

## Week 1, due October 18: everything boots

By Sunday the emulator, memory reads, the training runner and the MCP skeleton all run on every member's machine. Nothing learns yet. The point is to find the setup problems now.

| Who | Issue | Deliverable |
|---|---|---|
| Everyone | ALL-01 | Repo set up, ROMs verified by hash, a CartPole reward curve posted |
| Sahil (PM) | OPS-01 | Training box reachable by SSH, experiment tracking account approved |
| Sahil (PM) | ENV-02 | Throughput table for the 7800X3D and the M4 Pro; compute budget recomputed |
| Co-PM | OPS-02 | Issues loaded, `main` protected, every member on an AI coding tool |
| Co-PM | ENV-04 | PyBoy backend and a Super Mario Land reader |
| Emulation Engineer | ENV-01 | mGBA backend passing the conformance suite on macOS, Windows and Linux |
| Memory Engineer | ENV-03 | FireRed address table and a StateReader that reads position, party and badges |
| RL Engineer | TRN-01 | One command trains PPO and writes a reproducible run directory |
| Reward Engineer | TRN-02 | Reward registry with five components and isolation tests |
| Agent Engineer | AGT-01 | MCP server on the fake backend, callable from Claude Code |

Why this works in parallel: the repo ships a backend contract, a ROM-free fake backend and a conformance suite. Training, rewards and the MCP server build against the fake backend while the Environment pair gets the real emulators working.

Watch for: the mGBA binding on Windows. It is the one piece nobody has run. If it is not working by Thursday, a PM pairs on it and the fallback (libretro.py) gets a one-hour spike.

## Week 2, due October 25: schema freeze

By Sunday an agent trains on the real environment, and the logging schema is frozen.

| Who | Issue | Deliverable |
|---|---|---|
| Everyone | ALL-02 | One RAM field found by save-state diffing, written up in one row |
| Sahil (PM) | OPS-03 | Schema module, Parquet writer, fake logger, sign-off from each lane, tag `schema-v1` |
| Co-PM | ENV-07 | Start states S0 and S1, five segments, the gym states, a hashed manifest |
| Emulation Engineer | ENV-05 | AlgoArcadeEnv passing Gymnasium's checker on all three backends |
| Memory Engineer | ENV-06 | The full FireRed GameState, one validation test per field |
| RL Engineer | TRN-03 | First PPO runs on Super Mario Land and two FireRed segments, curves posted |
| Reward Engineer | TRN-04 | Reward v1 and a scripted-exploit test for each known hack |
| Agent Engineer | AGT-02 | MCP server on FireRed, the LLM loop with hard caps, a measured cost per action |

This is the heaviest week. ENV-05 and OPS-03 both have to land before TRN-03 can produce a curve, so the Emulation Engineer and Sahil aim for Wednesday, not Sunday.

Watch for: freezing a schema nobody has tested. If the StateReader is not validated on real memory by October 25, the freeze moves to November 1. That costs a week of usable runs and is still the right call.

## Week 3, due November 1: reproduce and automate

By Sunday the baseline clears the early segments on five seeds, the queue runs the training box, and we know which trainer we are on.

| Who | Issue | Deliverable |
|---|---|---|
| Sahil (PM) | OPS-04 | The run queue: crash-tolerant, tagged, notifying, nightly |
| Co-PM | OPS-05 | Checkpoint to mp4 with overlays; the first video review entry |
| Emulation Engineer | ENV-08 | Archive resets, with evaluation always from the fixed state |
| Memory Engineer | ENV-09 | World coordinates and walkability grids from the game's own map data |
| RL Engineer | TRN-05 | Our PPO trainer, and the parity result against Stable-Baselines3 |
| Reward Engineer | TRN-06 | seg_01 to seg_03 cleared at 80% or better over five seeds; baseline config named |
| Agent Engineer | AGT-03 | `navigate_to`, `advance_dialogue`, and the three tool levels |

The rule this week is no new ideas. TRN-06 reproduces what the Red literature already shows, on our harness. It will feel slow. Every experiment after this varies one factor from that baseline.

Watch for: the parity gate. If our trainer does not match Stable-Baselines3 by Sunday, we stay on Stable-Baselines3 and record that in `docs/decisions.md`. We do not spend week 4 chasing it.

## Week 4, due November 8: first results

By Sunday E1 is reported, E2 to E4 are running, the LLM has been evaluated across the tool ladder, and the first cold-start run is in the queue.

| Who | Issue | Deliverable |
|---|---|---|
| Sahil (PM) | OPS-07 | E1 to E4 scheduled, budget rebuilt from measured throughput, first S0 run launched |
| Co-PM | OPS-06 | Statistics module: IQM, bootstrap intervals, probability of improvement |
| Emulation Engineer | ENV-10 | Symbolic and pixel observations; E2 queued |
| Memory Engineer | ENV-11 | Battle state in GameState; the ordered milestone list from Pallet to Brock |
| RL Engineer | TRN-07 | PQN, and E1 reported with intervals |
| Reward Engineer | TRN-08 | RND with its unit tests; E3 queued |
| Agent Engineer | AGT-04 | E7: ten attempts per model, tool level and segment, with cost per success |

From here the box should never be idle. The shared baseline and the archive arm run first, because their code is ready first.

Watch for: reward hacks showing up in the first long runs. The video review is how we catch them, and a hack found this week is cheap. One found in week 6 is not.

## Week 5, due November 15: feature freeze

By Sunday every experiment is done or queued, the Brock runs are queued, and the second game is trained. After Sunday no new features merge.

| Who | Issue | Deliverable |
|---|---|---|
| Sahil (PM) | OPS-08 | Freeze checklist passed; cold-start Brock runs queued |
| Co-PM | OPS-09 | Dashboard skeleton that builds to static HTML from fake-logger data |
| Emulation Engineer | ENV-12 | Super Mario Land trained with the untouched config; the port diary |
| Memory Engineer | ENV-13 | Kanto renderer: schematic for the public, tile art for local use |
| RL Engineer | TRN-09 | E1, E2, E4 analysed; best config chosen; Brock runs from S1 launched |
| Reward Engineer | TRN-10 | E3 analysed; penalties ablation run; hack catalogue drafted |
| Agent Engineer | AGT-05 | LLM trajectories as an RL curriculum (E8) |

Two of these aim at the stretch tier: the Brock runs in TRN-09 and AGT-05. If the week is short, stretch work slips in this order: AGT-05 first, then the cold-start runs, then the S1 Brock runs. ENV-12 does not slip, because the second game is cheap and it is the framework claim.

## Week 6, due November 22: dashboard on real data

Everyone is on visualization. Each panel is built on fake-logger data first, then pointed at real runs. Final runs finish in the background.

| Who | Issue | Deliverable |
|---|---|---|
| Sahil (PM) | OPS-10 | Final runs finished or cut off; results frozen under tag `results-v1` |
| Co-PM | VIZ-06 | Dashboard v1 assembled and exported, opened offline |
| Emulation Engineer | VIZ-05 | Run registry, second-game panel, batch video rendering |
| Memory Engineer | VIZ-01 | Kanto exploration heatmap, animated across training |
| RL Engineer | VIZ-02 | Comparison panels with bootstrap bands, against steps and wall-clock |
| Reward Engineer | VIZ-03 | Reward decomposition chart; hack catalogue page with clips |
| Agent Engineer | VIZ-04 | Agent video grid; LLM against RL cost table |

If a panel is not ready by Sunday, the matching Weights & Biases chart goes in its place and the issue says so.

Whatever the Brock runs have reached by November 22 is the result we report. If they are still climbing, they keep running and the writeup says where they stood on the freeze date.

## Week 7, due November 29: ship

Thanksgiving is Thursday the 26th. This week is writing and polish. No training, no features.

| Who | Issue | Deliverable |
|---|---|---|
| Sahil (PM) | DOC-01 | The technical writeup, assembled from the lane sections |
| Co-PM | DOC-05 | Dashboard published; slide deck and a two-minute demo video |
| Emulation Engineer | DOC-06 | A fresh clone reproduces one result; docs fixed where it stumbled |
| Memory Engineer | DOC-02 | Reverse engineering and harness section; the adding-a-game guide |
| RL Engineer, Reward Engineer | DOC-03 | Methods, results and the final hack catalogue |
| Agent Engineer | DOC-04 | The LLM arm and what the comparison shows |

Monday November 30: tag v1.0 and hold a short retro.

## Dates that cannot move

| Date | What | Why |
|---|---|---|
| Oct 25 | Schema freeze | Every run logged before it is thrown away |
| Nov 1 | Run queue live; trainer parity decided | The experiment matrix does not fit without the queue |
| Nov 15 | Feature freeze | Final runs need a week of machine time behind them |
| Nov 22 | Results freeze | Week 7 has Thanksgiving in it and is for writing |

## How PMs float

Each PM owns one decoupled issue a week through week 5. None of them sits on another lane's critical path for more than a week, except OPS-03 and OPS-04, which are Sahil's and have nothing else scheduled against them.

The rest of PM time goes where the Thursday updates point. The order of priority is fixed: an issue marked critical-path first, then anything blocking another lane, then stretch work.

Sahil also owns the two training machines. The Windows desktop (7800X3D, RTX 4070) takes E1, E3, E4 and the S1 Brock runs. The M4 Pro MacBook takes E2, E5, E9 and the cold-start runs.

## If we fall behind

Cut in this order, and write each cut in `docs/decisions.md`:

1. E8, the LLM-to-RL bridge.
2. Cold-start Brock runs from S0. They continue after November 30.
3. E5, the penalties ablation.
4. E2, pixels against symbolic.
5. Shorten ablation runs from 15M steps before reducing seed counts. Five seeds stays.

Do not cut: the conformance suite, the schema freeze, the run queue, the baseline reproduction in week 3, or the second game.

If a member leaves, their lane partner takes the critical-path issues and a PM takes the rest. If the Agent Engineer leaves, the Co-PM keeps E7 running and E8 is dropped.

## After November 30

Unfinished stretch work continues on the same queue: cold-start Brock runs, a Metroid: Zero Mission port on the mGBA backend, and an ICM arm for E3.

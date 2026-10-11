---
id: OPS-07
title: Queue operations: E1 to E4 scheduled and the first cold-start run
team: pm
owner: Sahil (PM)
due: 2026-11-08
estimate: 3h
depends_on: OPS-04, ENV-08
labels: experiment
---
## Context
The box runs one full-throughput job at a time, so run order decides what we can report on Nov 8 and Nov 15. E1 to E4 share one baseline arm, which turns 45 runs into 30. TRN-07, TRN-08 and ENV-10 submit their arms into this queue. TRN-09 and OPS-08 read what comes out.

## Deliverable
- The shared baseline arm (PPO, symbolic, count, archive off), 5 seeds, queued once and tagged E1 to E4.
- The E4 archive-on arm, 5 seeds, then the PQN, pixels, none and RND arms as their owners submit them.
- The compute budget table in docs/technical-plan.md (Experiments), rebuilt from measured steps per second.
- One cold-start run: start state S0, archive resets on, target Viridian City, map (3, 1).
- Video review number two, kept where review one is.

## Acceptance criteria
- [ ] The queue status output, pasted in the pull request, shows 30 runs for E1 to E4: 6 arms, 5 seeds each. All use the S1-to-Pewter task and one step budget.
- [ ] The budget table names the run its steps per second came from, with box-days and a finish date per experiment.
- [ ] If any arm finishes after Nov 15, the table says what gets cut.
- [ ] The cold-start config shows S0, archive on and target map (3, 1). Evaluation starts from S0 with the archive off. The run id is in the pull request.
- [ ] Video review two lists, for each run finished this week: run id, checkpoint watched, what the agent does, any suspected exploit.

## Notes
Contract: docs/development-plan.md, Week 4, and docs/technical-plan.md, Experiments.

Arithmetic on the 500 steps/s planning figure, not a measurement: 30 runs at 15M steps take about 10.4 box-days. E1 is due Nov 8, so the baseline and PQN arms go first. Write the cold-start run's priority against those 30 in its queue entry.

Gotcha from RL-emerald: agents restarted from archive states re-collected explore reward until the saved state carried the visited set. Check ENV-08 does that.

Nothing we read shows PPO reaching Viridian from a FireRed cold start. A stall is a result: record where.

Out of scope: analysing E1 to E4 (TRN-09), the Brock runs (OPS-08).

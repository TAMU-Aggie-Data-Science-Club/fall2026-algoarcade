---
id: OPS-04
title: Run queue for the training box
team: pm
owner: Sahil (PM)
due: 2026-11-01
estimate: 5h
depends_on: TRN-03
labels: critical-path
---
## Context
The box runs one full-throughput job at a time. E1 to E4 are 30 runs of about 15M steps, about 10 box-days at the planning figure (arithmetic, unmeasured). Nobody can launch those by hand on four hours a week. OPS-07, TRN-07 and TRN-08 wait on this, so it must not slip.

## Deliverable
In `src/algoarcade/runqueue/`, run as `uv run python -m algoarcade.runqueue <command>`:
- `submit <file>` takes an experiment: a Python file naming a base config and the factors to vary. It queues one run per factor value and seed. `--dry-run` prints the runs and starts nothing.
- `run` executes queued runs in submit order, each in its own subprocess. A crashed run is retried once, then marked failed, and the next run starts.
- `status` prints queued, running, done and failed runs with their experiment id.
- Every run carries its experiment id in the Parquet log and in W&B.
- A failed run posts to the team channel through a webhook. The URL is an environment variable.
- A nightly schedule on the box (Windows Task Scheduler) starts `run`.

## Acceptance criteria
- [ ] `submit --dry-run` on an experiment with 2 factor values and 5 seeds prints exactly 10 runs and starts no process.
- [ ] `test_crash_does_not_stop_queue` passes on the fake backend. Of three runs the second always raises: runs 1 and 3 finish, run 2 is attempted exactly twice and ends failed.
- [ ] A DuckDB query over a two-run experiment's Parquet files finds one experiment id on every row. Query and output are pasted in the pull request.
- [ ] A forced failure on the box posts one message with the experiment id, run name and last traceback lines. A screenshot is in the pull request, and `git grep` finds no webhook URL.
- [ ] `status` output from the box is pasted in the pull request, taken the morning after an unattended nightly start.
- [ ] docs/setup.md (Training box) and the `experiment` skill describe the commands as built.

## Notes
Contract: docs/technical-plan.md, Experiments. docs/harness-spec.md, Logging schema.

Gotchas: keep queue state in a file under `data/runs/` so a reboot loses nothing. A retry restarts from step 0, which costs hours on a 15M-step run.

Command names are proposals. Out of scope: resume from checkpoint, parallel runs, a second machine, a web page.

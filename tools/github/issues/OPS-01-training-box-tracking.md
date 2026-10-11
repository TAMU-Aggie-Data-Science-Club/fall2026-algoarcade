---
id: OPS-01
title: Training box and experiment tracking ready
team: pm
owner: Sahil (PM)
due: 2026-10-18
estimate: 3h
labels: critical-path
---
## Context
Multi-seed runs happen on two machines: a Windows desktop with a Ryzen 7 7800X3D and an RTX 4070 (the box), and an M4 Pro MacBook. ENV-02 benchmarks on both this week, TRN-03 trains on them next week and OPS-04 puts a queue on the box in week 3. Weights and Biases is our live view of runs. Its free tier stops at 5 seats and we are 7.

## Deliverable
- The box on Windows with git, uv and a clone of the repo. Windows needs no system package for the mGBA binding.
- The M4 with uv, a clone and `brew install mgba`, set not to sleep during a run.
- Remote access to the box for all seven people. Tailscale plus the OpenSSH server that ships with Windows is the suggested route.
- A decision on GPU torch. PyPI's Windows wheel is CPU-only. The only planned run with a CNN is the pixel arm (E2), which is scheduled on the M4.
- docs/setup.md (Training box): how to connect, where runs go (`data/runs/`), and the rule that nobody debugs on the box. It runs committed code only.
- A Weights and Biases Academic plan application sent from tamu.edu addresses. Trackio is the fallback, with a written switch date.

## Acceptance criteria
- [ ] On the box, `uv run poe check` passes. Output pasted in the pull request.
- [ ] On the box, the output of `uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available())"` is pasted, and docs/decisions.md records whether we add the CUDA index and why.
- [ ] On the M4, `uv run poe check` passes and `uv run python -c "import torch; print(torch.backends.mps.is_available())"` prints `True`. Output pasted.
- [ ] Each of the other six people comments here with the output of `hostname`, run on the box over the remote connection.
- [ ] docs/setup.md (Training box) contains the connection steps and the no-debugging rule.
- [ ] docs/decisions.md records the date the Academic application was sent, Trackio as the fallback, and the switch date. We propose Wed Oct 21, because TRN-03 needs tracking by Oct 25.

## Notes
Background: docs/technical-plan.md (Training, Working practices).

We do not know how long Academic approval takes, or whether a club project counts as academic research. That is why the switch date is written down now. Trackio accepts `wandb.init`, `wandb.log` and `wandb.finish`, so code that sticks to those three calls switches by changing one import.

If we want CUDA torch on the box, it is an index entry in pyproject.toml limited to Windows. That is a dependency change and it makes every Windows laptop download the larger build, so both PMs decide it. Emulation is CPU-bound, so the default answer is no.

Windows starts worker processes with spawn. Every training entry point needs an `if __name__ == "__main__":` guard, or the vector env forks into a loop. API keys never go in the repo.

Out of scope: the run queue (OPS-04) and the benchmark (ENV-02).

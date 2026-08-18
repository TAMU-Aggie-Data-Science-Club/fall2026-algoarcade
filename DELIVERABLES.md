# Deliverables & Timeline

> **How to read this file.** This is the PMs' best current estimate of what AlgoArcade needs to ship and roughly when. It is a **living plan, not a contract**. The authoritative picture lives in **GitHub Issues and the Project board**.

## Milestones (suggested)

| # | Deliverable | Description | Owner (role) | Target |
|---|-------------|-------------|--------------|--------|
| 1 | Project scoping | Pick 2â€“3 environments + at least 2 algorithms. Define the comparison metric (mean return, sample efficiency). Decide seed count per config. | PM | Week 1 |
| 2 | Training framework | Config-driven training script with seed logging, TensorBoard, checkpoint saving. | Members | Weeks 1â€“2 |
| 3 | CartPole sanity runs | Both algorithms solve CartPole reproducibly across seeds. Serves as the smoke test. | Members | Week 2 |
| 4 | LunarLander runs | Multi-seed runs of each algorithm. Learning curves with confidence bands. | Members | Weeks 3â€“4 |
| 5 | Atari (stretch) | One Atari game (e.g., Pong or Breakout). Budget-aware â€” abort if not converging within compute budget. | Members | Weeks 5â€“6 |
| 6 | Cross-run comparison | Aggregation script + plots comparing algorithms across environments. Sample-efficiency + final-return summary tables. | Members | Weeks 6â€“7 |
| 7 | Gameplay recordings | `RecordVideo`-wrapped rollouts for each trained agent. Compiled into short clips. | Members | Weeks 6â€“7 |
| 8 | Writeup + demo | Notebook or Streamlit writeup with the comparison, clips, and takeaways. | Members + PM | Week 7 |
| 9 | Handoff & retro | Reproducibility check (fresh clone â†’ results within noise), lessons learned. | PM | Week 8 |

## Timeline (rough)

```
Week:   1     2     3     4     5     6     7     8
        |-----|-----|-----|-----|-----|-----|-----|
Scope   â–ˆâ–ˆ
Framework     â–ˆâ–ˆâ–ˆâ–ˆ
CartPole            â–ˆâ–ˆ
LunarLander               â–ˆâ–ˆâ–ˆâ–ˆ
Atari                           â–ˆâ–ˆâ–ˆâ–ˆ
Compare                             â–ˆâ–ˆâ–ˆâ–ˆ
Videos                              â–ˆâ–ˆâ–ˆâ–ˆ
Writeup                                    â–ˆâ–ˆ
Retro                                              â–ˆâ–ˆ
```

## Working agreements

- **Each deliverable maps to one or more GitHub Issues.** The board is the source of truth; this file is the summary.
- **Dates are estimates.** When reality diverges, update the issue and this file if the shift is material.
- **"Done" is defined per issue** via acceptance criteria â€” not by a date passing.
- **Reprioritize openly.** If a deliverable changes, a PM notes why in the issue so the decision is auditable.

---
id: TRN-06
title: Baseline clears the early segments across five seeds
team: training
owner: Reward Engineer
due: 2026-11-01
estimate: 5h
depends_on: TRN-03, TRN-04
labels: experiment
---
## Context
We reproduce before we innovate. E1 to E5 each change one factor of a named baseline, so the baseline has to clear the easy segments first. If it cannot leave the house, later comparisons measure noise. OPS-07 queues E1 to E4 from the config saved here.

## Deliverable
- 15 training runs on the box: PPO with reward v1 and the count bonus. Five seeds on each of seg_01 (house), seg_02 (Pallet to Route 1) and seg_03 (rival battle).
- They run on SB3, the trainer of record until TRN-05 decides.
- Evaluation: 20 episodes per seed from the segment's fixed start state, archive off. Success is the ENV-07 goal predicate inside the step budget.
- Target: 80 or more successes out of 100 on each segment.
- The config that clears all three, saved under one name (proposed: `baseline_v1`) that experiment files import.
- A GitHub issue with a clip for anything that blocks the target, such as a reward exploit or a wrong RAM read.

## Acceptance criteria
- [ ] A table in the pull request shows successes out of 20 per seed and segment. Every segment totals 80 of 100 or better.
- [ ] The DuckDB query that builds the table from the Parquet logs is in the pull request.
- [ ] The baseline config imports by name. A test pins every field, so a later edit fails CI until the test changes too.
- [ ] One clip per segment of a successful evaluation episode is in `data/videos/` on the box, with a line in docs/video-review.md.
- [ ] Each blocker is an issue with a clip and a run id, linked from the pull request. If there were none, the pull request says so.
- [ ] The `experiment` skill names the baseline and the one-factor rule.

## Notes
Contract: docs/technical-plan.md, Reward design and Experiments. docs/harness-spec.md, Start states and segments.

Gotchas: Pleines et al. report no milestones with zero navigation reward and rare Brock wins at 10 times the weight. The count bonus weight is the first knob. Tune weights, not the component set.

The only published scale reference is PokeRL on Pokemon Red with 4 envs. It reports 65% house exits at 150k steps and about 50% rival wins at 500k. Twenty evaluation episodes per seed is our choice.

If a segment misses 80, report the number and what was tried. Do not lower the bar to close the issue.

Out of scope: seg_04, seg_05, archive resets, RND.

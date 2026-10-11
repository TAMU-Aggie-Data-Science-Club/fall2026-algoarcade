---
id: TRN-10
title: E3 done, penalties ablation (E5), hack catalogue draft
team: training
owner: Reward Engineer
due: 2026-11-15
estimate: 5h
depends_on: TRN-08, OPS-05
labels: experiment
---
## Context
E3 asks whether RND beats tile counts. E5 asks whether penalties help or hurt on FireRed, after prior Pokemon work reported them backfiring. Both finish here, with the first draft of the hack catalogue. VIZ-03 builds its page from the draft and DOC-03 writes it up.

## Deliverable
- E3 (none, count, RND; 5 seeds) complete and analysed with the OPS-06 stats functions.
- An E5 experiment file: positive-only against positive plus the components that are off by default, 3 seeds.
- docs/hack-catalogue.md. Each entry has a name, what the agent did, the component that paid for it, a clip and the fix.

## Acceptance criteria
- [ ] The pull request has the E3 table: IQM, 95% bootstrap interval and seed count per arm.
- [ ] The table gives probability of improvement for count over none and RND over count.
- [ ] The E5 file lists the components on in each arm. The queue listing shows 3 seeds per arm, and every E5 number is labelled exploratory.
- [ ] The catalogue has an entry for each scripted exploit: oscillation, menu spam, faint loop, reset farming, grass camping. Each is marked observed or predicted, not observed.
- [ ] Every observed entry gives its clip as run id, checkpoint and step range, and the OPS-05 renderer reproduces it under data/videos/. `git ls-files '*.mp4'` prints nothing.
- [ ] Every fix that changed code names its regression test, and `uv run pytest -k exploit` passes.
- [ ] The `reward-component` skill lists every exploit named in the catalogue.

## Notes
Contract: docs/harness-spec.md, section Reward registry.

Do not change a default component while E1 to E4 share the baseline. Land a fix as a config option, and say which runs predate it.

RND reward that never decays is usually an input bug. Check the RAM slice for counters, play time and RNG state.

Do not invent an exploit to fill the catalogue. New components stop at the freeze. Fixes do not.

Out of scope: the catalogue page (VIZ-03), the writeup (DOC-03).

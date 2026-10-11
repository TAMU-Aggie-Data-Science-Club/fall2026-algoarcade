---
id: VIZ-03
title: Reward decomposition chart and hack catalogue page
team: training
owner: Reward Engineer
due: 2026-11-22
estimate: 5h
depends_on: TRN-10, OPS-09
labels: viz
---
## Context
A return curve hides which reward term the agent is chasing. This chart shows what each component contributed across training, for the baseline and for the penalties ablation (E5). The catalogue drafted in TRN-10 becomes a dashboard page with a clip per exploit. VIZ-06 assembles both, and DOC-03 writes them up.

## Deliverable
- `src/algoarcade/viz/decomposition.py`: a stacked area chart of mean reward per episode by component, per checkpoint window, averaged over seeds. One chart for the baseline arm and one per E5 arm.
- A hack catalogue page in `src/algoarcade/viz/dashboard/`, built from docs/hack-catalogue.md. Each entry shows what the agent did, the component that paid for it, the fix, the run id and one clip.
- Clips from the OPS-05 renderer in `data/videos/hacks/`, embedded with the Quarto video shortcode.

## Acceptance criteria
- [ ] `uv run pytest tests/test_decomposition.py` passes in CI on fake-logger data.
- [ ] For every window of one real baseline run, the components sum to the logged total reward within 1e-6. The largest difference is pasted in the pull request.
- [ ] A test asserts positive components stack above zero and penalties below.
- [ ] The E5 charts print "n = 3 seeds, exploratory".
- [ ] All five scripted exploits from docs/hack-catalogue.md are on the page. Each is marked "observed" (run id, clip) or "not observed" (test name, no clip).
- [ ] Every clip plays in the rendered page with Wi-Fi off.
- [ ] `git ls-files '*.mp4'` prints nothing.

## Notes
Contract: docs/harness-spec.md, Reward registry and Logging schema. docs/technical-plan.md, Reward design.

Gotchas. A percentage-stacked chart breaks with mixed signs, so plot raw values. If the sum check fails, the bug is upstream and gets its own issue. Read the OPS-09 result on whether the video shortcode works inside a dashboard card. Keep clips under 30 seconds (a guess).

Do not stage an exploit to fill the page. One that no trained agent showed is listed as not observed.

Fallback by Sunday: the W&B per-component reward charts, exported as images.

Out of scope: new reward components, new runs, fixing exploits.

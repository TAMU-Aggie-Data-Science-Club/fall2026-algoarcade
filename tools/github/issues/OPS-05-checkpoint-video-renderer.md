---
id: OPS-05
title: Checkpoint evaluation and video renderer
team: pm
owner: Co-PM
due: 2026-11-01
estimate: 4h
depends_on: TRN-03
---
## Context
A reward exploit is easier to spot in footage than in a curve. The weekly video review is how we catch one before it costs a multi-day run. TRN-06 needs clips as evidence this week, and TRN-10, VIZ-04 and VIZ-05 build on this script.

## Deliverable
- One script: `uv run python -m algoarcade.viz.render --checkpoint <path> --seed 0 --out data/videos/<name>.mp4`.
- It loads a checkpoint and plays one seeded episode from the fixed start state with rendering on.
- It writes mp4 with imageio-ffmpeg (libx264, yuv420p, explicit fps). Frames get a nearest-neighbour integer upscale from 240x160 (GBA) or 160x144 (Game Boy).
- Overlays: one bar per reward component, the step count, and map_group, map_num, x, y and badges.
- `--grid` composes several episodes side by side in numpy.
- docs/video-review.md with the first weekly entry.

## Acceptance criteria
- [ ] The command on a TRN-03 FireRed checkpoint writes an mp4. Read back with imageio, it has the episode's frame count and a width and height divisible by 16.
- [ ] The same command runs on a TRN-03 Super Mario Land checkpoint with no code change.
- [ ] Two runs with the same checkpoint and seed print the same episode return and final (map_group, map_num, x, y).
- [ ] A test on the fake backend renders 10 frames and asserts one bar per enabled reward component.
- [ ] `--grid` with four seeds writes one mp4 with four panels per frame. One frame is pasted in the pull request.
- [ ] docs/video-review.md has an entry for the week of Nov 1: run ids, at least five minutes watched, and what we saw. Each of the five exploit signatures is marked seen or not seen.

## Notes
Contract: docs/harness-spec.md, Reward registry and Logging schema. The five exploit signatures: oscillation, menu spam, faint loop, reset farming, grass camping.

Gotchas: imageio rescales any frame whose width or height is not divisible by 16, and defaults to 10 fps. PyBoy updates its frame buffer in place, so copy every frame. A checkpoint needs the normalisation statistics TRN-03 saves beside it. Text overlays need Pillow. If it is not in `uv.lock`, ask a PM before adding it.

The module path is a proposal. Clips stay in `data/videos/`, which is git-ignored. Out of scope: batch rendering (VIZ-05), dashboard embedding.

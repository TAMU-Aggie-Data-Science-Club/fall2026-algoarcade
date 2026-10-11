---
id: DOC-02
title: Writeup: reverse engineering and the harness; adding-a-game guide
team: environment
owner: Memory Engineer
due: 2026-11-29
estimate: 4h
depends_on: ENV-12
labels: docs
---
## Context
The framework is the deliverable, so the writeup has to say how we read game state and why a reader can trust it. DOC-01 merges this section into `docs/writeup.md`. ENV-12 drafted `docs/adding-a-game.md` from the Super Mario Land port diary, and this item finishes it.

## Deliverable
- `docs/writeup/harness.md` with four headed parts:
  - Where addresses come from: the pret/pokefirered `symbols` branch pinned to commit 3b401eaf14f193946899eb7c056d5ac02a470126, tables keyed by ROM SHA-1, nothing from wikis.
  - How each field is validated: the per-field tests (ENV-06) and save-state diffing (ALL-02).
  - The pointer relocation trap: gSaveBlock1Ptr and gSaveBlock2Ptr move on every warp and every return from battle or menu.
  - What the conformance suite proves, and what it does not, for the three backends.
- `docs/adding-a-game.md`, final: the files a new game needs, in order, with the command that checks each step.

## Acceptance criteria
- [ ] `docs/writeup/harness.md` has the four parts above as headings.
- [ ] The validation part counts GameState fields and fields with a passing validation test. The `uv run pytest` output behind both counts is pasted in the pull request.
- [ ] The pointer part shows gSaveBlock1Ptr read before and after one warp, with the save state named. Both values are in the pull request.
- [ ] The conformance part lists every test with one line on what it proves. Names match `uv run pytest tests/conformance --collect-only -q`.
- [ ] Every repo path in `docs/adding-a-game.md` exists at HEAD. Every file listed in `docs/port-diary-super-mario-land.md` appears in the guide.
- [ ] The `ram-field` skill agrees with the guide. The pull request names the file checked.

## Notes
Contract: `docs/harness-spec.md`, sections FireRed memory map, StateReader and GameState, Conformance tests.

File-local statics in .sym files carry a numeric suffix that differs between builds (sGengarScroll.182, .185). Say we parse on the base name.

The guide says where the Super Mario Land addresses came from, including any taken from PyBoy's wrapper source.

pret/pokefirered has no license. Quote addresses from our committed table and paste no decomp source.

Open the pull request by Wed Nov 25 so DOC-01 can assemble. Out of scope: the Metroid port, new fields, new tests.

---
id: ENV-04
title: PyBoy backend and Super Mario Land reader
team: environment
owner: Co-PM
due: 2026-10-18
estimate: 4h
---
## Context
Super Mario Land on PyBoy is our pipeline test game from week 1 and the second game for E9. It needs no mGBA, so TRN-03 can train on it even if ENV-01 slips, and ENV-12 finishes the port in week 5. A second backend also shows the GameBackend protocol is not shaped around one emulator. The Co-PM owns this item.

## Deliverable
- `src/algoarcade/backends/pyboy.py`: `PyBoyBackend` on PyBoy 2.8.x, added to the conformance registry.
- A Super Mario Land StateReader under `src/algoarcade/games/` that reads lives, time, world and level progress from RAM.
- A test asserting those four fields equal PyBoy's own game wrapper over 1,000 random steps.
- The SHA-1 of the team's standard dump in `rom.py` and DATA.md.

## Acceptance criteria
- [ ] The suite in `tests/conformance/` passes for `PyBoyBackend` on the owner's machine and on one other OS. CI has no ROM, so both pytest summaries are pasted in the pull request.
- [ ] Over 1,000 seeded random steps, the reader's four fields equal the wrapper's `lives_left`, `time_left`, `world` and `level_progress` at every step. Zero mismatches. Output pasted.
- [ ] The reader has no score field and no coins field.
- [ ] `rom.py` and DATA.md carry one Super Mario Land SHA-1. This issue links two ALL-01 comments showing that same hash.
- [ ] `uv run python -m algoarcade.rom <dump>` names the standard dump as Super Mario Land. A test shows `PyBoyBackend` refusing a file with any other hash.
- [ ] Each address in the reader has a comment naming its source file and version.

## Notes
Contract: docs/harness-spec.md (GameBackend, ROM pinning, StateReader and GameState, Conformance tests). ROM tests carry the `rom` marker and skip when the file is absent.

PyBoy's wrapper reads score and coins from screen tiles, not RAM, so they cannot be an oracle. Gotchas from the wrapper source:
- Lives are stored as BCD.
- Level progress is computed from three values: a level block, Mario's x and the scroll register.
- Save states use file-like objects. Call `seek(0)` before loading from a buffer.

Addresses come from PyBoy's wrapper source or the kaspermeerts/supermarioland disassembly, which is partial. If it lacks a label, cite the PyBoy file and note the exception in docs/decisions.md.

One known dump, World Rev A, has SHA-1 `418203621b887caa090215d97e3f509b79affd3e`. We standardise on whatever two members actually hold.

Out of scope: Mario rewards, training (TRN-03) and E9 (ENV-12).

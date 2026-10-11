---
id: ENV-03
title: FireRed address table and StateReader v0
team: environment
owner: Memory Engineer
due: 2026-10-18
estimate: 5h
depends_on: ENV-01
labels: critical-path
---
## Context
Everything that looks at FireRed reads it through the StateReader: rewards, observations, the LLM's state JSON and the logs. ALL-02, ENV-06, ENV-07, AGT-02 and OPS-03 all wait on this first version. No address in our memory map has been tested against a running ROM yet.

## Deliverable
- `scripts/fetch_symbols.py`: fetches `pokefirered.sym` and `pokefirered_rev1.sym` from pret/pokefirered at commit `3b401eaf14f193946899eb7c056d5ac02a470126` into `data/pokefirered/`.
- A small hand-curated address table in the FireRed folder under `src/algoarcade/games/`, keyed by ROM SHA-1, with a provenance comment.
- StateReader v0: `map_group`, `map_num`, `x`, `y`, party count, and per-Pokemon level, HP, max HP and status.
- `scripts/state_diff.py`: prints the EWRAM bytes that differ between two save states. ALL-02 uses it.

## Acceptance criteria
- [ ] After `uv run python scripts/fetch_symbols.py`, both files exist under `data/pokefirered/` and `git status` shows no new files.
- [ ] A test compares every address in the table with the fetched `.sym` files, matching on the base symbol name. It skips when the files are absent.
- [ ] A ROM-free test on synthetic memory moves the save block pointer between two reads and gets correct values both times.
- [ ] A ROM-free test shows a null or out-of-range pointer (outside base to base+0x7C) reported as not ready, never as field values.
- [ ] Three hand-captured states pass, with every v0 field equal to the value written down from the game screen. The tests carry the `rom` marker. Pytest output is pasted in the pull request.
- [ ] `uv run python scripts/state_diff.py A B` on two states one step apart lists a change at the x or y bytes. Output pasted.
- [ ] The `ram-field` skill matches what was built: the field names, and how to add and validate a field.

## Notes
Contract: docs/harness-spec.md (StateReader and GameState, FireRed memory map).

Gotchas:
- `gSaveBlock1Ptr` moves on every warp and every return from a battle or menu. Dereference it on every read. Never cache it.
- File-local symbols carry a numeric suffix that differs between builds (`sGengarScroll.182` against `.185`).
- Read the live party from `gPlayerParty`. The copy inside SaveBlock1 is stale between saves.

Addresses come from the `.sym` files only, never from wikis. The `.sym` files and save states stay under `data/` and are never committed. Capture the three states on different maps, one after choosing a starter. If a value disagrees with the screen, trust the screen and report it.

Out of scope: species and moves (ENV-06), flags, badges, money and battle state.

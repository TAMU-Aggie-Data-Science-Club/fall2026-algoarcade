---
id: ENV-06
title: Full FireRed GameState with a validation test per field
team: environment
owner: Memory Engineer
due: 2026-10-25
estimate: 5h
depends_on: ENV-03
labels: critical-path
---
## Context
Rewards, the LLM's state JSON and the log schema need the rest, each proven against real memory. OPS-03 freezes the schema on Oct 25 only if this reader is validated. ENV-09 and ENV-11 extend it.

## Deliverable
New GameState fields in the FireRed reader under `src/algoarcade/games/`:
- Badge byte (SaveBlock1+0xFE4), trainer-flag popcount (ids 0x500 to 0x7FF), world-map flag popcount (0x890 to 0x8C2).
- A story-flag whitelist for Pallet to Pewter, ids from the decomp's `flags.h`.
- Money: SaveBlock1+0x290 XOR the key at SaveBlock2+0xF20.
- Pokedex owned and seen counts (SaveBlock2+0x28 and +0x5C).
- `in_battle` (bit 1 of 0x03003529), text box (0x0203709C), script status (0x03000EA8), control lock (0x03000F9C).
- An options check: text speed fast (SaveBlock2+0x14, bits 0 to 2, value 2), battle scene off (SaveBlock2+0x15, bit 2).
- Species and moves per slot: XOR 12 words at 0x20 with `personality ^ otId`, order by `personality % 24`, validate the checksum at 0x1C.

## Acceptance criteria
- [ ] One named test per field reads a captured state and matches a value read off the game screen. `uv run pytest -k firered_fields` output pasted in the pull request (CI skips them: no ROM).
- [ ] A test replays a trace crossing one warp and one battle. Map ids and money stay correct, and no progress count decreases.
- [ ] A test corrupts one byte of a party slot's encrypted block and asserts the reader rejects that slot.
- [ ] A test asserts the options check fails on a state with default options.
- [ ] A test asserts no progress count reads a flag id below 0x230. This excludes temp and hide/show flags.
- [ ] The `ram-field` skill and docs/harness-spec.md (FireRed memory map) list every new field with its symbol.

## Notes
Contract: docs/harness-spec.md, sections StateReader and GameState, FireRed memory map.

Gotchas: read both save-block pointers on every access. The money key changes each time the blocks move, so read money and key in the same frame. The option bit positions are derived from declaration order and nobody has run them.

Out of scope: battle state (ENV-11), map geometry (ENV-09).

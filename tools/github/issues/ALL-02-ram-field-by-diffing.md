---
id: ALL-02
title: Find one RAM field by save-state diffing
team: everyone
owner: Everyone
due: 2026-10-25
estimate: 1h
depends_on: ENV-03
---
## Context
Every reward we pay comes from a byte somebody located in FireRed's memory. Each of us finds one field by hand this week, so everyone knows where the numbers come from. Nothing is blocked on this. The rows give ENV-06 a second set of eyes, and TRN-04 pays rewards on the same fields.

## Deliverable
Your row in `docs/re-notes.md`: field, address, how found, symbol that confirms it.

1. Claim a field in a comment here. Easy picks: player x, player y, lead HP, party count, text box open, in battle.
2. Save state A. Make exactly one change. Save state B.
3. Diff A and B with `scripts/state_diff.py`.
4. Repeat with a fresh pair. Keep only addresses that change every time. This drops timers and RNG.
5. Write a new value to the surviving address and watch the game change.
6. Look the address up in the pinned `pokefirered.sym` under `data/pokefirered/`.

## Acceptance criteria
- [ ] `docs/re-notes.md` has your row with all four columns filled. No other row names the same field.
- [ ] The address is written as symbol plus offset, for example `gPlayerParty + 0x56`. `grep -w <symbol>` on the pinned `.sym` file returns a line.
- [ ] The pull request shows the diff output from two A/B pairs and names the address that survived both.
- [ ] The pull request shows the write check: the value you wrote and what changed on screen.
- [ ] The pull request changes `docs/re-notes.md` and nothing else.

## Notes
Contract: docs/harness-spec.md, section FireRed memory map.

Gotchas: the block behind `gSaveBlock1Ptr` (0x03005008) moves by 0 to 124 bytes on every warp and every return from a battle or full-screen menu. If your change crosses one, the whole block shows as changed. Stay on one map, or subtract the pointer value and record the offset. Skip money: it is XORed with a key that changes on each move.

Seven people edit one table. Append your row, and keep both rows on a merge conflict.

Out of scope: adding the field to the StateReader (ENV-06).

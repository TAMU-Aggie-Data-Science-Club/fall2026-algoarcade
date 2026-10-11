---
id: ENV-11
title: Battle state and the Pallet-to-Brock milestone list
team: environment
owner: Memory Engineer
due: 2026-11-08
estimate: 4h
depends_on: ENV-06
---
## Context
GameState knows a battle is on but not who is winning. The Brock runs in TRN-09 need both sides' HP, level, moves and PP. The archive key, the milestone reward and the log timeline all need one ordered milestone list, defined once here.

## Deliverable
- Battle fields on GameState from gBattleMons: own and enemy HP, max HP, level, moves and PP. Null outside battle.
- Nine ordered milestones in the FireRed folder under `src/algoarcade/games/`, each a named predicate over GameState. In order: starter chosen, rival beaten, parcel delivered, Pokedex received, Viridian Forest exited, Pewter reached, gym entered, FLAG_DEFEATED_BROCK (0x4B0), FLAG_BADGE01_GET (0x820).
- The archive key (ENV-08), the milestone reward and the log timeline read this list. No schema column is added or renamed.

## Acceptance criteria
- [ ] One validation test per battle field, as in ENV-06: its value in the seg_03 rival battle state equals the one read off the screen. Every field is null in an overworld state.
- [ ] Each predicate has a unit test on a hand-built GameState: False before, True after.
- [ ] Test on real states: all nine are False on S0. On S1 the first three are True and the last five are False.
- [ ] Test: Pewter reached stays True after the player walks out of Pewter.
- [ ] Every flag or var id is in the address table with its decomp file and symbol name.
- [ ] The OPS-03 schema test passes unchanged. The `ram-field` skill lists the battle fields and the milestones.

## Notes
Contract: docs/harness-spec.md, sections StateReader and GameState, FireRed memory map, Logging schema.

Leads from the research notes, not yet run against a ROM: gBattleMons at 0x02023BE4, 0x58 plaintext bytes per battler, VAR_STARTER_MON 0x4031, FLAG_SYS_POKEDEX_GET 0x829. Take field offsets from `struct BattlePokemon` in the decomp. We have no symbol for the rival battle or the parcel. Find them in the decomp's Oak's Lab scripts, never a wiki.

Gotchas: nothing we read says gBattleMons is cleared after a battle, so gate every read on gMain.inBattle. Check which battler index is ours. Map-based milestones go False when the player leaves, so latch them per episode.

Out of scope: double battles, status bits, reward weights, anything past Brock.

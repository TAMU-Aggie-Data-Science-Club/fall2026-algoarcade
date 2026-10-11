# games

One folder per game: its StateReader, address table, start-state manifest and reward config. `base.py` holds the two protocols every game implements. `fake.py` reads the toy game.

- `firered/` arrives with ENV-03 (Memory Engineer).
- `super_mario_land/` arrives with ENV-04 (Co-PM).

Contract: `docs/harness-spec.md`, StateReader and GameState, and FireRed memory map. No address enters this package without a symbol name and the commit it came from.

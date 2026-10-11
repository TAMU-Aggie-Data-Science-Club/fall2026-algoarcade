---
id: ENV-09
title: Map data pipeline: world coordinates and walkability
team: environment
owner: Memory Engineer
due: 2026-11-01
estimate: 6h
depends_on: ENV-06
---
## Context
RAM holds only the current map plus a 7-tile border, so a whole-Kanto grid has to be built offline from the decomp's map files. ENV-10 needs the walkability grid for the symbolic observation. ENV-13 draws the map from it, and VIZ-01 uses the coordinate table.

## Deliverable
- A fetch script that pulls the `map.json`, `layouts.json`, `map.bin` and `metatile_attributes.bin` files from pret/pokefirered master into `data/pokefirered/`. The commit SHA is pinned in the script. Our research read 037335f4c725d7c9aecdac87066f2002b4bd7e14.
- Placement: a breadth-first walk over `connections` from Pallet Town (3,0) puts the connected overworld maps on one global grid, Pallet at (0,0).
- Walkability per tile from collision bits 10 and 11 of each `map.bin` entry. 0x03FF counts as blocked. Metatile behaviour then marks ledges and water.
- A table from (map_group, map_num) to a global offset: global = local + offset.
- Warp-only maps (Viridian Forest, gyms, gatehouses) kept as separate panels.

## Acceptance criteria
- [ ] The fetch command fills `data/pokefirered/` on a clean clone. A second run downloads nothing, and `git ls-files data/` prints nothing.
- [ ] A test asserts these origins relative to Pallet: Route 1 (0,-40), Viridian City (-12,-80), Route 2 (0,-160), Pewter City (-12,-200).
- [ ] A test asserts no two placed maps share a global tile. The pull request gives the number placed (research counted 63) and lists any connected map the walk missed.
- [ ] A test asserts grid sizes: Pallet Town 24x20, Route 1 24x40, Viridian Forest 54x69.
- [ ] A test checks one ledge tile and one water tile the owner found in the game.
- [ ] For every ENV-07 start state, the offline collision grid matches the live map buffer on at least 99% of the current map's tiles. Mismatches are listed in the pull request.
- [ ] `DATA.md` lists the pinned commit and the file types fetched.

## Notes
Contract: docs/harness-spec.md, FireRed memory map.

Gotchas: a connection's offset shifts the neighbour along the shared edge, x for up and down, y for left and right. The four origins were derived from offsets and never rendered, so if that test fails, check both sides. The live buffer is VMap, which points at gBackupMapData. Take both from the pinned .sym.

Not source-checked: metatile ids below 640 use the primary tileset, and behaviour is bits 0 to 8 of each 32-bit entry. Ledges are 0x38 to 0x3B. Confirm in `src/fieldmap.c`. The 99% threshold is a guess.

Out of scope: drawing (ENV-13), elevation, NPC blockers. Nothing fetched is committed.

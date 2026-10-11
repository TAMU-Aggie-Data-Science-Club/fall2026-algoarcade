---
id: ENV-13
title: Kanto map renderer: schematic for the public, tile art for local
team: environment
owner: Memory Engineer
due: 2026-11-15
estimate: 5h
depends_on: ENV-09
---
## Context
The exploration heatmap needs a base map of Kanto that we may publish. pret/pokefirered has no license and its tiles are Nintendo art, so the public map is a schematic drawn from collision data. VIZ-01 draws visit counts over it in week 6.

## Deliverable
- src/algoarcade/viz/kanto_map.py, reading the decomp checkout under data/pokefirered/.
- `--mode schematic`: one flat colour per behaviour class (walkable, wall, grass, water, ledge).
- `--mode tiles`: composed from tiles.png, metatiles.bin and the palettes. Written only under data/.
- The 63 connected overworld maps placed with ENV-09 world coordinates, plus insets for warp-only maps.
- A function from (map_group, map_num, x, y) to a pixel.

## Acceptance criteria
- [ ] `uv run python -m algoarcade.viz.kanto_map --mode schematic --out <path>` exits 0 and prints 63 placed overworld maps.
- [ ] The schematic has inset panels for at least Viridian Forest (1,0) and Pewter Gym (6,2).
- [ ] A CI test on a synthetic map.bin decodes cell 0x1401 to metatile 1, collision 1, elevation 1.
- [ ] Test: every pixel colour in a schematic render is in the legend palette.
- [ ] Test: `--mode tiles` raises when the output path is outside data/.
- [ ] Test: the pixel function agrees with ENV-09 for Pallet Town (3,0) and Route 1 (3,19).
- [ ] The owner and one reviewer each state in the pull request that they compared the tile render with porymap's export.

## Notes
Contract: docs/technical-plan.md, sections Reverse engineering and Visualization.

Each map.bin cell is 16 bits: bits 0 to 9 metatile, 10 to 11 collision, 12 to 15 elevation. We have not read the metatiles.bin entry layout or the behaviour mask in the 32-bit attributes. Read src/fieldmap.c in the decomp first.

Reuse the ENV-09 coordinate table. A second placement walk would drift from the heatmap.

Porymap's export is File > Export Map Stitch Image, GUI only. Never upload it or a tile render. Tests that need the decomp skip when it is absent.

Out of scope: the heatmap overlay (VIZ-01), animated tiles, sprites.

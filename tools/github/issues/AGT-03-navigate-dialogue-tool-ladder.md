---
id: AGT-03
title: navigate_to, advance_dialogue and the tool ladder
team: agent
owner: Agent Engineer
due: 2026-11-01
estimate: 5h
depends_on: AGT-02
---
## Context
Public Pokemon harnesses credit pathfinding and a dialogue macro with most of their gains. The PokeAgent paper reports raw models near 0% on the Emerald speedrun without a harness. The ladder L0, L1, L2 is what E7 measures, so AGT-04 waits on this.

## Deliverable
- `navigate_to(x, y)`: A* over the current map's collision grid, read live from RAM, with NPC positions from gObjectEvents as blocked tiles. It stops on arrival, battle, dialogue, warp or no path, and returns the reason with the post-action state. One map only.
- `advance_dialogue`: presses A until the text box closes or a choice appears, and returns the text.
- Tool level set by config. L0 is press plus screenshot. L1 adds the state JSON. L2 adds the two tools above.
- Attempts on seg_01, seg_02 and seg_03 written in the frozen logging schema, so they join the RL runs. Presses made inside `navigate_to` are counted.

## Acceptance criteria
- [ ] Test on the fake backend: `navigate_to` around a wall presses exactly as many buttons as a breadth-first oracle's shortest path.
- [ ] Scripted tests return each stop reason: arrived, battle, dialogue, warp, no_path.
- [ ] From the seg_02 start state on FireRed, `navigate_to` a tile at least 10 tiles away ends with the reader's (x, y) equal to the target.
- [ ] From a state with an open text box, `advance_dialogue` returns non-empty text and stays under the press cap. It ends with the box closed or a choice shown.
- [ ] An MCP client lists two tools at L0 and L1, and four at L2. At L0 no tool result contains state JSON.
- [ ] One attempt per level on each segment (9 attempts) is logged. A DuckDB query joining them to a TRN-03 run by segment is pasted in the pull request, with dollars spent.

## Notes
Contract: docs/harness-spec.md, MCP tool surface and Logging schema.

Gotchas: object coordinates in gObjectEvents carry a +7 offset from map-local tiles, and the live map buffer has a 7-tile border. Live collision bits do not show ledges, so a path can fail. Plan again a bounded number of times, then stop with a reason.

Our research has no symbol for the dialogue text or an open choice menu. Find them in the pinned .sym, add them to the address table, and write a validation test. Press caps are guesses. Use claude-haiku-5-5 for the nine attempts.

Out of scope: routes across maps (the model plans those), a battle macro, the E7 evaluation (AGT-04).

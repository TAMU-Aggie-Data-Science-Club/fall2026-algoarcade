---
id: AGT-02
title: MCP server on FireRed and the first LLM run
team: agent
owner: Agent Engineer
due: 2026-10-25
estimate: 5h
depends_on: AGT-01, ENV-03
---
## Context
This puts the AGT-01 server on FireRed and has a model press real buttons. Our cost estimate rests on token counts nobody has measured, and the pilot here replaces it before AGT-04 runs the evaluation. AGT-03 adds tools to this server.

## Deliverable
In `src/algoarcade/agent/`:
- The server on MgbaBackend with two tools: `get_state` (compact JSON, optional PNG upscaled 2x to 480x320) and `press` (returns the state after the press).
- A manual Messages API loop over the MCP stdio client, with append-only history and prompt caching.
- A per-step log: input, output, cache-write and cache-read tokens from `response.usage`, dollars, and the button pressed.
- Hard per-attempt caps on actions and dollars. The model id and prices are config values.
- A 20-action pilot on seg_01, then one full attempt at seg_01 (leave the house).

## Acceptance criteria
- [ ] A test (skipped without the ROM) asserts the `get_state` location equals the StateReader's, and the PNG is 480x320.
- [ ] A test starts the server as a subprocess on FakeBackend and makes 10 tool calls through the stdio client with no protocol error.
- [ ] A test with a stubbed model asserts the loop stops at each cap and never changes an earlier message.
- [ ] The pilot report is posted here: mean input, output and cache-read tokens per action, and dollars per action.
- [ ] docs/technical-plan.md (LLM arm) carries the measured cost per 300-action attempt in place of the estimate.
- [ ] The seg_01 attempt is posted with its outcome (graded by the ENV-07 goal predicate), button presses and dollars. A failed attempt still counts.

## Notes
Contract: docs/harness-spec.md, section MCP tool surface. docs/technical-plan.md, section LLM arm.

Gotchas: anything on stdout corrupts the stdio wire. Whether mGBA prints at load is unchecked, so test Windows early. Changing tool definitions mid-attempt invalidates the cache.

Ask Sahil (PM) for the API key and both caps first. The key stays out of git.

Out of scope: `navigate_to`, `advance_dialogue` and the tool ladder (AGT-03), the 10-attempt evaluation (AGT-04).

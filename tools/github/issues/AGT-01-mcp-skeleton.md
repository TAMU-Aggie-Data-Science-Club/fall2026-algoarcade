---
id: AGT-01
title: MCP server skeleton on the fake backend
team: agent
owner: Agent Engineer
due: 2026-10-18
estimate: 4h
---
## Context
The language model plays through an MCP server that owns the emulator. Building it on FakeBackend this week keeps the agent work off the mGBA critical path. AGT-02 swaps in FireRed once ENV-03 lands, and AGT-03 adds navigate_to and advance_dialogue.

## Deliverable
- An `MCPServer` (official `mcp` SDK v2) under `src/algoarcade/agent/`, on stdio. Its lifespan creates one FakeBackend, and the tools use that instance.
- Two tools, `get_state` and `press`. Each returns the state after the call.
- `.mcp.json` at the repo root that launches the server through `uv`.
- A test that starts the server as a subprocess and proves only protocol frames reach stdout.
- The "MCP tool surface" section of docs/harness-spec.md, updated to match what was built.

## Acceptance criteria
- [ ] A test starts the server as a subprocess through the SDK's stdio client and lists exactly two tools, `get_state` and `press`.
- [ ] In that test, the state returned by `press` equals the next `get_state`, and equals a direct FakeBackend run of the same inputs.
- [ ] A test reads the subprocess's raw stdout across startup, one `get_state` and one `press`. Every line parses as JSON with `"jsonrpc": "2.0"`. A deliberate log call inside a tool shows up on stderr.
- [ ] Two server processes started side by side hold independent state: a `press` in one leaves the other's `get_state` unchanged.
- [ ] `.mcp.json` has one entry under `mcpServers` that uses only `command` and `args`. A pasted tool list or screenshot shows Claude Code or VS Code listing both tools after a fresh clone and `uv sync`.
- [ ] docs/harness-spec.md (MCP tool surface) gives each tool's arguments and return shape, and they match the schemas the server reports.
- [ ] The tests above run in CI with no ROM, and `uv run poe check` passes.

## Notes
Background: docs/technical-plan.md (LLM arm).

Gotchas:
- In SDK v2 the class is `MCPServer`, imported from `mcp.server.mcpserver`. The v1 path `mcp.server.fastmcp` is gone. The PokeAgent reference server still uses it, so do not copy its imports.
- On stdio, anything printed to stdout corrupts the wire. Log through `logging` to stderr.
- State belongs to the process, never to an MCP session. The 2026-07-28 protocol revision has no sessions.

Tools read the backend from `ctx.request_context.lifespan_context`. Keep `.mcp.json` free of `${...}` interpolation.

Out of scope: screenshots, navigate_to, advance_dialogue, the model loop and FireRed (AGT-02 and AGT-03).

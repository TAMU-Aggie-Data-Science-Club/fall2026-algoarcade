---
id: ENV-01
title: mGBA backend passes the conformance suite on all three OSes
team: environment
owner: Emulation Engineer
due: 2026-10-18
estimate: 5h
labels: critical-path
---
## Context
FireRed cannot run until we have a GBA backend, and nothing on the mGBA path has been run yet. ENV-02 and ENV-03 wait on this item this week. ENV-05 and every FireRed run wait on it after that.

## Deliverable
- `scripts/fetch_mgba.py`: downloads the libmgba-py 0.2.0-2 archive for the host OS and checks it against a SHA-256 stored in the repo.
- `src/algoarcade/backends/mgba.py`: `MgbaBackend`, implementing the GameBackend protocol and added to the conformance registry. `read()` slices zero-copy views of EWRAM and IWRAM. States are raw bytes. Rendering can be switched off.
- A mirror of the three release zips we use.

## Acceptance criteria
- [ ] On macOS arm64, Windows x64 and Linux x64, `uv run python scripts/fetch_mgba.py` then `uv run python -c "import mgba.core"` exits 0.
- [ ] A test with no network shows the fetch step refusing an archive whose SHA-256 differs from the stored value.
- [ ] The suite in `tests/conformance/` passes for `MgbaBackend` on all three OSes. CI has no ROM, so the pytest summary for each OS is pasted in the pull request.
- [ ] Loading a file whose SHA-1 is not in `rom.py` raises before any frame runs. The test uses a dummy file and needs no ROM.
- [ ] From one saved state, two runs of the same 1,000 scripted frames give the same SHA-256 over EWRAM plus IWRAM. The hash from each OS is pasted, with a note on whether the three agree.
- [ ] The win64, macos-arm64 and ubuntu-lunar zips sit somewhere the team controls. DATA.md records the URL, and each file matches its stored SHA-256.
- [ ] docs/setup.md (Install) lists the system package per OS: `brew install mgba`, `apt install libmgba0.10t64`, nothing on Windows.

## Notes
Contract: docs/harness-spec.md (GameBackend, ROM pinning, Conformance tests). ROM tests carry the `rom` marker and skip when the file is absent.

Gotchas:
- Call `core.reset()` after `load_path`, or the binding's methods raise.
- The Linux archive needs libmgba 0.10. Ubuntu 22.04 ships 0.9 only.
- The views reach into private fields of the binding. Keep that in one place.
- Read pokebot-gen3 to see the calls, but copy nothing. It is GPL-3.0.

The 1,000 frames is a guess. A release asset on our own repository is enough for the mirror. If a machine cannot load the archive, write up the failure and stop. The libretro.py fallback is documented, not built here.

Out of scope: the Gymnasium env (ENV-05), throughput (ENV-02) and game fields (ENV-03).

# AlgoArcade

*ADSC Catalyst Project, Fall 2026*

AlgoArcade is a framework for training and comparing game-playing agents on real video games. We are proving it on Pokémon FireRed: reinforcement learning agents and a language model play through the same harness, from the same save states, and we measure both.

The framework is the deliverable. Pokémon is the demo.

**Status:** kickoff was October 11 2026. The repo holds the backend contract, a ROM-free test backend, the plan and the work items. Nothing is trained yet. Results land here on November 29.

## What we are building

- One backend interface over three emulators: mGBA for FireRed, PyBoy for Super Mario Land, and a fake backend for tests.
- A StateReader that turns live game memory into typed state, with every address taken from the pokefirered decompilation.
- A Gymnasium environment whose reward is built from named parts, each logged on its own.
- PPO as the baseline, compared against PQN, RND and archive resets, five seeds per arm.
- An MCP server that hands the same harness to a language model, evaluated across three levels of tooling.
- A static dashboard, with an exploration heatmap over Kanto as the centerpiece.

We are aiming at the first gym badge. The plan says what we report if we miss.

## Quick start

You need [uv](https://docs.astral.sh/uv/) and git.

```sh
git clone https://github.com/sahil-d-patel/AlgoArcade.git
cd AlgoArcade
uv sync
uv run poe check
```

`uv sync` installs Python 3.12 and every dependency from the lockfile. `uv run poe check` runs the formatter, linter, type checker and tests. If both pass, your setup works.

ROMs are not in this repo and never will be. [`docs/setup.md`](docs/setup.md) covers where yours go, how to verify them, and the emulator install for your OS.

## Where things are

| Path | What it is |
|---|---|
| [`docs/technical-plan.md`](docs/technical-plan.md) | What we are building and why |
| [`docs/development-plan.md`](docs/development-plan.md) | Who does what, week by week, through November 30 |
| [`docs/harness-spec.md`](docs/harness-spec.md) | The interfaces and the logging schema |
| [`docs/decisions.md`](docs/decisions.md) | Design decisions and the reasons behind them |
| [`docs/setup.md`](docs/setup.md) | Onboarding |
| [`DELIVERABLES.md`](DELIVERABLES.md) | The milestone table |
| [`DATA.md`](DATA.md) | Every data source, its license, and what may be committed |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How work moves from an issue to `main`. Start here before touching code. |
| [`AGENTS.md`](AGENTS.md) | Rules for AI coding agents working in this repo |
| [`src/algoarcade/`](src/algoarcade/) | The package. Each subfolder has a README naming its owner and first issue. |
| [`tests/`](tests/) | The conformance suite every backend must pass, and unit tests |
| [`tools/github/`](tools/github/) | The work items as files, and the script that loads them into GitHub Issues |
| [`data/`](data/) | Local ROMs, save states, logs and checkpoints. Git-ignored. Nothing here is committed. |

## How we work

Every change starts as a GitHub issue and reaches `main` through a reviewed pull request. [`CONTRIBUTING.md`](CONTRIBUTING.md) has the flow.

We use AI coding agents heavily. The repo is set up so they follow the same rules we do: [`AGENTS.md`](AGENTS.md) is read by every tool, Claude Code picks up the skills in `.claude/skills/` (including one that cleans a branch before every pull request), and the same checks run in pre-commit and CI whoever wrote the code. The author is responsible for every line an agent writes.

## Team

Two PMs and five members across three lanes: Environment, Training and Agent. Roles are in [`docs/development-plan.md`](docs/development-plan.md). Code owners are in [`CODEOWNERS`](CODEOWNERS).

---
id: OPS-02
title: GitHub project live and every member has an AI tool
team: pm
owner: Co-PM
due: 2026-10-18
estimate: 2h
---
## Context
The first pull requests arrive this week, so the review rules have to exist before them. The loader turns the 52 work item files into the issues everyone picks from. Every week 1 pull request waits on the ruleset and CODEOWNERS, and ALL-01 needs each person on an AI coding tool.

## Deliverable
- The repository set to public, so the ruleset is enforced on the free plan.
- A ruleset on `main`: pull request required, one approval, code owner review, CI check required.
- CODEOWNERS with a real GitHub handle for every role.
- `python3 tools/github/bootstrap.py` run once, so the labels, 7 milestones and 52 issues exist.
- A GitHub project holding all 52 issues.
- A comment on this issue listing each person's AI coding tool and plan.

## Acceptance criteria
- [ ] `python3 tools/github/bootstrap.py --check` prints `52 work items valid across 7 milestones`.
- [ ] `gh issue list --state all --limit 100` shows 52 issues whose titles start with an `[ID]` prefix. The repository has 7 milestones.
- [ ] `gh api repos/{owner}/{repo}/rulesets` returns one ruleset with enforcement `active`.
- [ ] A test pull request touching `src/algoarcade/backends/` requests review from the environment owners. It cannot merge before approval, and the CI check is listed as required. Screenshot in this issue.
- [ ] The project shows 52 items. Link in this issue.
- [ ] The tool comment covers all seven people by role. Each has a matching ALL-01 comment showing the tool read AGENTS.md.
- [ ] The repository page shows Public, and `main` is the default branch.

## Notes
Background: CONTRIBUTING.md and docs/technical-plan.md (Working practices).

Rulesets and branch protection are enforced on public repositories on the free plan. Before the switch to public, check that no ROM, save state or key was ever pushed.

The loader needs an authenticated `gh`. It is safe to re-run because it matches issues on the `[ID]` prefix. Project commands need `gh auth refresh -s project` first. Code owners need write access to the repository.

GitHub Copilot Student is free once GitHub verifies a student. Any tool that reads AGENTS.md works with this repo.

Out of scope: issue types and sub-issues.

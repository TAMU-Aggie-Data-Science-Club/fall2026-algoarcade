@AGENTS.md

## Claude Code

- Skills in `.claude/skills/` load on their own when relevant: `plain-writing`, `deslop`, `pr-cleanup`, `ram-field`, `reward-component`, `experiment`. Two run only when typed: `/start-issue` and `/open-pr`.
- Ask the `rl-reviewer` agent to review any diff that touches rewards, training, the environment, a state reader or the logging schema.
- Two hooks run from `.claude/settings.json`. One blocks a push to `main`, a force push, `--no-verify`, and `git add` of game data. The other formats and lints each Python file you edit and returns what it could not fix. Fix those findings; do not work around the hook.

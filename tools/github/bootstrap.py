#!/usr/bin/env python3
"""Load the work items in tools/github/issues/ into GitHub Issues.

    python tools/github/bootstrap.py --check     validate the files, touch nothing
    python tools/github/bootstrap.py --dry-run   print what would be created
    python tools/github/bootstrap.py             create labels, milestones and issues

The last form needs the GitHub CLI (`gh`), authenticated, run from inside the repo.
Re-running is safe: anything that already exists is skipped. Issues are matched on
the "[ID]" prefix of their title, so editing a title's wording will not duplicate it.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

ISSUES_DIR = Path(__file__).parent / "issues"

# One milestone per weekly deliverable. Every work item is due on one of these Sundays.
MILESTONES: list[tuple[str, str, str]] = [
    (
        "2026-10-18",
        "W1 Oct 18: Everything boots",
        "Emulator, RAM reads, training runner and MCP skeleton run on every machine.",
    ),
    (
        "2026-10-25",
        "W2 Oct 25: Schema freeze",
        "Full GameState, the Gymnasium env, reward v1, and the first PPO curve on FireRed. Logging schema frozen.",
    ),
    (
        "2026-11-01",
        "W3 Nov 1: Reproduce and automate",
        "Baseline clears the early segments across seeds. Run queue takes over the training box.",
    ),
    (
        "2026-11-08",
        "W4 Nov 8: First results",
        "E1 done; E2, E3 and E4 running. LLM arm evaluated. First cold-start run launched.",
    ),
    (
        "2026-11-15",
        "W5 Nov 15: Feature freeze",
        "Every experiment done or queued. Brock runs queued. Second game trained. No new features after today.",
    ),
    (
        "2026-11-22",
        "W6 Nov 22: Dashboard on real data",
        "Everyone on visualization. Final runs finish. Results frozen.",
    ),
    (
        "2026-11-29",
        "W7 Nov 29: Ship",
        "Static dashboard, writeup, reproducibility check, showcase assets. Tag v1.0 on Nov 30.",
    ),
]

TEAMS: dict[str, tuple[str, str]] = {
    "environment": ("1d76db", "Emulation, RAM reading, save states, the Gymnasium env"),
    "training": ("0e8a16", "Algorithms, rewards, exploration, experiments"),
    "agent": ("8250df", "MCP server and the LLM comparison arm"),
    "pm": ("bf8700", "Infrastructure, run queue, freezes, reviews"),
    "everyone": ("57606a", "Assigned to the whole team"),
}

EXTRA_LABELS: dict[str, tuple[str, str]] = {
    "critical-path": ("b60205", "Other work is blocked until this lands"),
    "stretch": ("d4a72c", "Aimed at a stretch goal; first to slip if the week is short"),
    "viz": ("0969da", "Visualization and showcase work in weeks 6 and 7"),
    "experiment": ("1a7f37", "Produces runs that feed the results"),
    "docs": ("6e7781", "Writing, not code"),
}

REQUIRED_KEYS = ("id", "title", "team", "owner", "due", "estimate")
REQUIRED_SECTIONS = ("## Context", "## Deliverable", "## Acceptance criteria")
ID_PATTERN = re.compile(r"^[A-Z]{2,4}-\d{2}$")
MIN_CRITERIA = 4


@dataclass
class WorkItem:
    path: Path
    id: str
    title: str
    team: str
    owner: str
    due: str
    estimate: str
    depends_on: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    body: str = ""

    @property
    def issue_title(self) -> str:
        return f"[{self.id}] {self.title}"

    @property
    def milestone(self) -> str:
        return next(title for date, title, _ in MILESTONES if date == self.due)

    @property
    def all_labels(self) -> list[str]:
        return [f"team:{self.team}", *self.labels]


def _split_list(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def parse_item(path: Path) -> WorkItem:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"{path.name}: missing front matter block")
    meta: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        key, sep, value = line.partition(":")
        if not sep:
            raise ValueError(f"{path.name}: bad front matter line {line!r}")
        meta[key.strip()] = value.strip()
    missing = [key for key in REQUIRED_KEYS if not meta.get(key)]
    if missing:
        raise ValueError(f"{path.name}: missing {', '.join(missing)}")
    return WorkItem(
        path=path,
        id=meta["id"],
        title=meta["title"],
        team=meta["team"],
        owner=meta["owner"],
        due=meta["due"],
        estimate=meta["estimate"],
        depends_on=_split_list(meta.get("depends_on", "")),
        labels=_split_list(meta.get("labels", "")),
        body=match.group(2).strip(),
    )


def load_items(directory: Path = ISSUES_DIR) -> list[WorkItem]:
    return [parse_item(path) for path in sorted(directory.glob("*.md"))]


def _item_problems(item: WorkItem) -> list[str]:
    where = item.path.name
    problems = []
    if not ID_PATTERN.match(item.id):
        problems.append(f"{where}: id {item.id!r} does not look like ENV-01")
    if item.team not in TEAMS:
        problems.append(f"{where}: unknown team {item.team!r}")
    if item.due not in {date for date, _, _ in MILESTONES}:
        problems.append(f"{where}: due {item.due} is not one of the weekly Sundays")
    problems += [
        f"{where}: unknown label {label!r}" for label in item.labels if label not in EXTRA_LABELS
    ]
    problems += [
        f"{where}: missing section {section!r}"
        for section in REQUIRED_SECTIONS
        if section not in item.body
    ]
    criteria = re.findall(
        r"^- \[ \] .+", _section(item.body, "## Acceptance criteria"), re.MULTILINE
    )
    if len(criteria) < MIN_CRITERIA:
        problems.append(
            f"{where}: needs at least {MIN_CRITERIA} acceptance criteria, found {len(criteria)}"
        )
    return problems


def _dependency_problems(items: list[WorkItem], by_id: dict[str, WorkItem]) -> list[str]:
    problems = []
    for item in items:
        for dep in item.depends_on:
            if dep not in by_id:
                problems.append(f"{item.path.name}: depends on unknown id {dep}")
            elif by_id[dep].due > item.due:
                problems.append(
                    f"{item.path.name}: due {item.due} but depends on {dep}, due {by_id[dep].due}"
                )
    return problems


def validate(items: list[WorkItem]) -> list[str]:
    """Return every problem found. An empty list means the set is loadable."""
    problems: list[str] = []
    by_id: dict[str, WorkItem] = {}
    for item in items:
        if item.id in by_id:
            problems.append(
                f"{item.path.name}: duplicate id {item.id} (also in {by_id[item.id].path.name})"
            )
        by_id[item.id] = item
        problems += _item_problems(item)
    problems += _dependency_problems(items, by_id)

    # Every week needs a concrete deliverable from every team.
    problems += [
        f"no {team} deliverable in {title!r}"
        for date, title, _ in MILESTONES
        for team in TEAMS
        if team != "everyone" and not any(item.due == date and item.team == team for item in items)
    ]

    if not problems:
        try:
            ordered(items)
        except ValueError as error:
            problems.append(str(error))
    return problems


def _section(body: str, heading: str) -> str:
    match = re.search(rf"{re.escape(heading)}\n(.*?)(?=\n## |\Z)", body, re.DOTALL)
    return match.group(1) if match else ""


def ordered(items: list[WorkItem]) -> list[WorkItem]:
    """Dependencies first, so each issue can link the issues it depends on by number."""
    by_id = {item.id: item for item in items}
    done: list[WorkItem] = []
    seen: set[str] = set()
    visiting: set[str] = set()

    def visit(item: WorkItem) -> None:
        if item.id in seen:
            return
        if item.id in visiting:
            raise ValueError(f"dependency cycle through {item.id}")
        visiting.add(item.id)
        for dep in item.depends_on:
            visit(by_id[dep])
        visiting.discard(item.id)
        seen.add(item.id)
        done.append(item)

    for item in sorted(items, key=lambda i: (i.due, i.id)):
        visit(item)
    return done


def render_body(item: WorkItem, numbers: dict[str, int]) -> str:
    day = dt.date.fromisoformat(item.due)
    due = f"{day:%a %b} {day.day}"
    deps = (
        ", ".join(f"#{numbers[dep]}" if dep in numbers else dep for dep in item.depends_on)
        or "none"
    )
    header = (
        "| Owner | Team | Due | Estimate | Depends on |\n"
        "|---|---|---|---|---|\n"
        f"| {item.owner} | {item.team} | {due} | {item.estimate} | {deps} |\n"
    )
    return f"{header}\n{item.body}\n"


def gh(*args: str, stdin: str | None = None) -> str:
    result = subprocess.run(["gh", *args], input=stdin, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args[:3])} failed: {result.stderr.strip()}")
    return result.stdout


def create_labels(dry_run: bool) -> None:
    labels = {f"team:{name}": spec for name, spec in TEAMS.items()} | EXTRA_LABELS
    for name, (color, description) in labels.items():
        print(f"label      {name}")
        if not dry_run:
            gh("label", "create", name, "--color", color, "--description", description, "--force")


def create_milestones(dry_run: bool) -> None:
    existing: set[str] = set()
    if not dry_run:
        listed = json.loads(gh("api", "repos/{owner}/{repo}/milestones?state=all&per_page=100"))
        existing = {milestone["title"] for milestone in listed}
    for date, title, description in MILESTONES:
        if title in existing:
            print(f"milestone  {title} (exists)")
            continue
        print(f"milestone  {title}")
        if not dry_run:
            gh(
                "api", "repos/{owner}/{repo}/milestones",
                "-f", f"title={title}",
                "-f", f"description={description}",
                # Late in the UTC day so GitHub shows the Sunday in every US timezone.
                "-f", f"due_on={date}T23:59:59Z",
            )  # fmt: skip


def existing_issue_numbers() -> dict[str, int]:
    listed = json.loads(
        gh("issue", "list", "--state", "all", "--limit", "1000", "--json", "number,title")
    )
    numbers = {}
    for issue in listed:
        match = re.match(r"^\[([A-Z]{2,4}-\d{2})\]", issue["title"])
        if match:
            numbers[match.group(1)] = issue["number"]
    return numbers


def create_issues(items: list[WorkItem], dry_run: bool) -> None:
    numbers = {} if dry_run else existing_issue_numbers()
    for item in ordered(items):
        if item.id in numbers:
            print(f"issue      {item.issue_title} (exists as #{numbers[item.id]})")
            continue
        print(f"issue      {item.issue_title}  [{item.milestone}]")
        if dry_run:
            continue
        args = ["issue", "create", "--title", item.issue_title, "--body-file", "-"]
        args += ["--milestone", item.milestone]
        for label in item.all_labels:
            args += ["--label", label]
        url = gh(*args, stdin=render_body(item, numbers)).strip()
        numbers[item.id] = int(url.rsplit("/", 1)[-1])


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="validate the work item files and exit")
    mode.add_argument(
        "--dry-run", action="store_true", help="print what would be created without calling gh"
    )
    args = parser.parse_args(argv)

    try:
        items = load_items()
    except ValueError as error:
        print(error, file=sys.stderr)
        return 1
    problems = validate(items)
    if problems:
        print("\n".join(problems), file=sys.stderr)
        return 1
    if args.check:
        print(f"{len(items)} work items valid across {len(MILESTONES)} milestones")
        return 0
    create_labels(args.dry_run)
    create_milestones(args.dry_run)
    create_issues(items, args.dry_run)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

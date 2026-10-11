from pathlib import Path

import pytest

import bootstrap

CORE_TEAMS = ("environment", "training", "agent", "pm")
PREFIX = {"environment": "ENV", "training": "TRN", "agent": "AGT", "pm": "OPS"}
BODY = """\
## Context
Why this exists.

## Deliverable
What exists when it is done.

## Acceptance criteria
- [ ] First check
- [ ] Second check
- [ ] Third check
- [ ] Fourth check
"""


def write_item(directory: Path, item_id: str, team: str, due: str, body: str = BODY, **extra: str):
    meta = {
        "id": item_id,
        "title": f"Title of {item_id}",
        "team": team,
        "owner": "Someone",
        "due": due,
        "estimate": "2h",
        **extra,
    }
    front = "\n".join(f"{key}: {value}" for key, value in meta.items())
    (directory / f"{item_id}-slug.md").write_text(f"---\n{front}\n---\n{body}", encoding="utf-8")


@pytest.fixture
def issues(tmp_path: Path) -> Path:
    """The smallest valid set: one item per core team per milestone, numbered by week."""
    for week, (due, _, _) in enumerate(bootstrap.MILESTONES, start=1):
        for team in CORE_TEAMS:
            write_item(tmp_path, f"{PREFIX[team]}-{week:02d}", team, due)
    return tmp_path


def problems(directory: Path) -> list[str]:
    return bootstrap.validate(bootstrap.load_items(directory))


def test_parse_reads_front_matter_lists_and_body(tmp_path: Path) -> None:
    write_item(
        tmp_path,
        "ENV-05",
        "environment",
        "2026-10-25",
        depends_on="ENV-01, TRN-02",
        labels="critical-path",
    )
    item = bootstrap.parse_item(tmp_path / "ENV-05-slug.md")
    assert item.id == "ENV-05"
    assert item.depends_on == ["ENV-01", "TRN-02"]
    assert item.labels == ["critical-path"]
    assert item.all_labels == ["team:environment", "critical-path"]
    assert item.issue_title == "[ENV-05] Title of ENV-05"
    assert item.milestone == "W2 Oct 25: Schema freeze"
    assert item.body.startswith("## Context")


def test_parse_rejects_a_file_without_front_matter(tmp_path: Path) -> None:
    path = tmp_path / "ENV-01-slug.md"
    path.write_text(BODY, encoding="utf-8")
    with pytest.raises(ValueError, match="missing front matter"):
        bootstrap.parse_item(path)


def test_parse_rejects_a_missing_required_key(tmp_path: Path) -> None:
    write_item(tmp_path, "ENV-01", "environment", "2026-10-18", owner="")
    with pytest.raises(ValueError, match="missing owner"):
        bootstrap.parse_item(tmp_path / "ENV-01-slug.md")


def test_minimal_set_is_valid(issues: Path) -> None:
    assert problems(issues) == []


def test_missing_section_is_reported(issues: Path) -> None:
    body = BODY.replace("## Deliverable\nWhat exists when it is done.\n\n", "")
    write_item(issues, "ENV-01", "environment", "2026-10-18", body=body)
    assert problems(issues) == ["ENV-01-slug.md: missing section '## Deliverable'"]


def test_too_few_acceptance_criteria_is_reported(issues: Path) -> None:
    write_item(
        issues, "ENV-01", "environment", "2026-10-18", body=BODY.replace("- [ ] Fourth check\n", "")
    )
    assert problems(issues) == ["ENV-01-slug.md: needs at least 4 acceptance criteria, found 3"]


def test_unknown_dependency_is_reported(issues: Path) -> None:
    write_item(issues, "ENV-02", "environment", "2026-10-25", depends_on="ENV-99")
    assert problems(issues) == ["ENV-02-slug.md: depends on unknown id ENV-99"]


def test_dependency_due_later_than_dependent_is_reported(issues: Path) -> None:
    write_item(issues, "ENV-01", "environment", "2026-10-18", depends_on="TRN-02")
    assert problems(issues) == [
        "ENV-01-slug.md: due 2026-10-18 but depends on TRN-02, due 2026-10-25"
    ]


def test_cycle_is_reported(issues: Path) -> None:
    write_item(issues, "ENV-01", "environment", "2026-10-18", depends_on="TRN-01")
    write_item(issues, "TRN-01", "training", "2026-10-18", depends_on="ENV-01")
    assert problems(issues) == ["dependency cycle through ENV-01"]


def test_a_week_with_no_deliverable_for_a_team_is_reported(issues: Path) -> None:
    (issues / "AGT-03-slug.md").unlink()
    assert problems(issues) == ["no agent deliverable in 'W3 Nov 1: Reproduce and automate'"]


def test_ordered_puts_dependencies_first_then_sorts_by_due_and_id(issues: Path) -> None:
    write_item(issues, "AGT-01", "agent", "2026-10-18", depends_on="TRN-01")
    write_item(issues, "ENV-02", "environment", "2026-10-25", depends_on="OPS-02")
    ids = [item.id for item in bootstrap.ordered(bootstrap.load_items(issues))]
    assert ids[:8] == [
        "TRN-01",
        "AGT-01",
        "ENV-01",
        "OPS-01",
        "AGT-02",
        "OPS-02",
        "ENV-02",
        "TRN-02",
    ]
    assert len(ids) == len(set(ids)) == 28

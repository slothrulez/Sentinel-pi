#!/usr/bin/env python3
"""Idempotently sync unchecked PiSentinel checklist items into Jira Tasks.

- Reads checklists/*.md
- Only [ ] items are synced
- [x]/[X] completed and [!] blocked items are ignored
- Non-week headings such as "## Current status" are ignored
- Uses a stable SHA-256 label for duplicate prevention
- Existing synced issues are skipped; missing ones are created
"""

from __future__ import annotations

import base64
import hashlib
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import requests


# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

BASE_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
EMAIL = os.environ["JIRA_EMAIL"]
TOKEN = os.environ["JIRA_API_TOKEN"]
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KAN")
CHECKLIST_DIR = Path(os.getenv("CHECKLIST_DIR", "checklists"))

ASSIGNEES = {
    "A": os.environ["JIRA_ASSIGNEE_A"],
    "B": os.environ["JIRA_ASSIGNEE_B"],
    "C": os.environ["JIRA_ASSIGNEE_C"],
    "D": os.environ["JIRA_ASSIGNEE_D"],
}

MONTHS = {
    "jan": 1,
    "feb": 2,
    "mar": 3,
    "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dec": 12,
}


# ---------------------------------------------------------------------------
# Week heading parser
# ---------------------------------------------------------------------------
#
# Supports:
#
#   ## 21–27 Sep — Edge Foundation
#   ## 28 Sep–11 Oct — FastAPI Skeleton
#   ## 12–25 Oct — Database Layer
#   ## 26 Oct–8 Nov — Mock / Demo Data
#   ## 21 Dec–10 Jan — Reports
#   ## 22–28 Feb — Final
#
# The previous parser could not correctly parse headings where the
# month appeared between the start and end day.
#
WEEK_RE = re.compile(
    r"^##\s+"
    r"(?P<start>\d{1,2})"
    r"(?:\s*(?:–|-|—)\s*(?P<end>\d{1,2}))?"
    r"\s+(?P<month>[A-Za-z]{3,9})"
    r"(?:\s*(?:–|-|—)\s*(?P<end_month_day>\d{1,2})\s+"
    r"(?P<end_month>[A-Za-z]{3,9}))?"
    r"\s+—\s+"
    r"(?P<title>.+?)"
    r"\s*$"
)


TASK_RE = re.compile(
    r"^- \[(?P<state>[ xX!])\]\s+(?P<task>.+?)\s*$"
)


ROLE_RE = re.compile(
    r"^#\s+PiSentinel\s+—\s+.+?\s+"
    r"\((?P<member>[ABCD])\)\s+Checklist"
)


@dataclass(frozen=True)
class Task:
    member: str
    source_file: str
    week: str
    week_title: str
    text: str
    due_date: date


# ---------------------------------------------------------------------------
# Checklist parsing
# ---------------------------------------------------------------------------

def due_date_for(heading: str) -> date | None:
    """Return the week-ending date for a valid week heading.

    Supports both same-month and cross-month headings.

    Examples:
        21–27 Sep       -> 2026-09-27
        28 Sep–11 Oct   -> 2026-10-11
        26 Oct–8 Nov    -> 2026-11-08
        21 Dec–10 Jan   -> 2027-01-10

    Non-week headings return None.
    """

    match = WEEK_RE.match(heading)

    if not match:
        return None

    start_month = MONTHS[
        match.group("month")[:3].lower()
    ]

    end_month = MONTHS[
        (
            match.group("end_month")
            or match.group("month")
        )[:3].lower()
    ]

    end_day = int(
        match.group("end_month_day")
        or match.group("end")
        or match.group("start")
    )

    # Project starts in September 2026
    # and ends in February 2027.
    start_year = 2026 if start_month >= 9 else 2027

    end_year = (
        start_year
        if end_month >= start_month
        else start_year + 1
    )

    return date(
        end_year,
        end_month,
        end_day,
    )


def parse_checklist(path: Path) -> list[Task]:
    """Parse one member checklist and return only pending week tasks."""

    lines = path.read_text(
        encoding="utf-8"
    ).splitlines()

    member = None

    # Member identity is encoded in the first heading.
    for line in lines[:5]:
        match = ROLE_RE.match(line.strip())

        if match:
            member = match.group("member")
            break

    if member is None:
        raise ValueError(
            f"Cannot determine A/B/C/D from {path}"
        )

    tasks: list[Task] = []

    heading: str | None = None
    heading_title: str | None = None
    due_date: date | None = None

    for line in lines:

        # ---------------------------------------------------------------
        # Week / section heading
        # ---------------------------------------------------------------

        if line.startswith("## "):
            heading = line.strip()

            match = WEEK_RE.match(heading)

            if match:
                heading_title = match.group("title")
                due_date = due_date_for(heading)

            else:
                # Examples:
                # ## Current status
                # ## Notes
                heading_title = heading[3:].strip()
                due_date = None

            continue

        # ---------------------------------------------------------------
        # Checklist item
        # ---------------------------------------------------------------

        match = TASK_RE.match(line)

        if not match:
            continue

        # Tasks outside a valid week section are ignored.
        if heading is None or due_date is None:
            continue

        state = match.group("state")

        # Only unchecked [ ] tasks are created.
        #
        # [x] / [X] = completed
        # [!]     = blocked / dependency
        if state != " ":
            continue

        task_text = match.group("task")

        tasks.append(
            Task(
                member=member,
                source_file=path.name,
                week=heading[3:].strip(),
                week_title=heading_title or "",
                text=task_text,
                due_date=due_date,
            )
        )

    return tasks


# ---------------------------------------------------------------------------
# Stable IDs / Jira helpers
# ---------------------------------------------------------------------------

def stable_id(task: Task) -> str:
    """Generate a deterministic ID that stays the same across sync runs."""

    raw = (
        f"{task.source_file}|"
        f"{task.week}|"
        f"{task.text}"
    ).encode("utf-8")

    return hashlib.sha256(raw).hexdigest()[:12]


def auth_headers() -> dict[str, str]:
    credentials = f"{EMAIL}:{TOKEN}"

    encoded = base64.b64encode(
        credentials.encode("utf-8")
    ).decode("ascii")

    return {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def jira(method: str, path: str, **kwargs):
    response = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers=auth_headers(),
        timeout=30,
        **kwargs,
    )

    if not response.ok:
        raise RuntimeError(
            f"{method} {path}: "
            f"{response.status_code}: "
            f"{response.text}"
        )

    return (
        response.json()
        if response.content
        else {}
    )


def description_adf(task: Task) -> dict:
    paragraphs = [
        f"Member: {task.member}",
        f"Source: checklists/{task.source_file}",
        f"Week: {task.week}",
        f"Week title: {task.week_title}",
        f"Stable task ID: {stable_id(task)}",
        "",
        "Checklist item:",
        task.text,
        "",
        "Definition of done:",
        (
            "Working code/output is built, run, tested, and committed. "
            "Update the Markdown checklist only after the work is actually "
            "complete."
        ),
    ]

    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [
                    {
                        "type": "text",
                        "text": line or " ",
                    }
                ],
            }
            for line in paragraphs
        ],
    }


def existing_issue(task: Task) -> dict | None:
    """Find an already-synced task using its deterministic label."""

    label = f"pisentinel-{stable_id(task)}"

    jql = (
        f'project = "{PROJECT_KEY}" '
        f'AND labels = "{label}"'
    )

    data = jira(
        "GET",
        "/rest/api/3/search/jql",
        params={
            "jql": jql,
            "maxResults": 1,
            "fields": (
                "summary,"
                "status,"
                "assignee,"
                "labels"
            ),
        },
    )

    issues = data.get("issues", [])

    return issues[0] if issues else None


def create_issue(task: Task) -> str:
    """Create one Jira Task."""

    stable = stable_id(task)

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },

            "issuetype": {
                "id": "10003"
            },

            "summary": (
                f"[{task.member}] "
                f"{task.text}"
            ),

            "description": description_adf(task),

            "assignee": {
                "accountId": ASSIGNEES[
                    task.member
                ]
            },

            "labels": [
                "pisentinel-sync",
                f"pisentinel-{stable}",
            ],

            "duedate": (
                task.due_date.isoformat()
            ),
        }
    }

    response = jira(
        "POST",
        "/rest/api/3/issue",
        json=payload,
    )

    return response["key"]


# ---------------------------------------------------------------------------
# Main sync
# ---------------------------------------------------------------------------

def main() -> None:

    if not CHECKLIST_DIR.exists():
        raise SystemExit(
            f"Missing checklist directory: "
            f"{CHECKLIST_DIR}"
        )

    checklist_paths = sorted(
        path
        for path in CHECKLIST_DIR.glob("*.md")
        if path.name.lower() != "readme.md"
    )

    if not checklist_paths:
        raise SystemExit(
            "No checklist Markdown files found "
            f"in {CHECKLIST_DIR}"
        )

    tasks: list[Task] = []

    # ---------------------------------------------------------------
    # Parse all checklists
    # ---------------------------------------------------------------

    for path in checklist_paths:

        print(
            f"Reading checklist: {path}"
        )

        parsed_tasks = parse_checklist(path)

        print(
            f"  Found "
            f"{len(parsed_tasks)} "
            f"pending week tasks"
        )

        tasks.extend(parsed_tasks)

    print()
    print(
        f"Total pending checklist tasks: "
        f"{len(tasks)}"
    )
    print()

    # ---------------------------------------------------------------
    # Sync to Jira
    # ---------------------------------------------------------------

    created = 0
    skipped = 0

    for task in tasks:

        stable = stable_id(task)

        issue = existing_issue(task)

        if issue:

            skipped += 1

            print(
                f"SKIP   {issue['key']}  "
                f"[{task.member}] "
                f"{task.text} "
                f"(id={stable})"
            )

            continue

        key = create_issue(task)

        created += 1

        print(
            f"CREATE {key}  "
            f"[{task.member}] "
            f"{task.text} "
            f"(id={stable})"
        )

    print()
    print("=" * 60)
    print("PiSentinel Jira Sync Complete")
    print("=" * 60)
    print(
        f"Created:         {created}"
    )
    print(
        f"Already present: {skipped}"
    )
    print(
        f"Pending tasks:   {len(tasks)}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()

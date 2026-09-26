#!/usr/bin/env python3
"""Idempotently sync unchecked PiSentinel checklist items into Jira Tasks."""

from __future__ import annotations

import base64
import hashlib
import os
import re
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import requests


# ============================================================
# Configuration
# ============================================================

BASE_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
EMAIL = os.environ["JIRA_EMAIL"]
TOKEN = os.environ["JIRA_API_TOKEN"]

PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KAN")
CHECKLIST_DIR = Path(os.getenv("CHECKLIST_DIR", "checklists"))


# Jira account IDs are configuration values, not secrets.
ASSIGNEES = {
    "A": os.environ["JIRA_ASSIGNEE_A"],
    "B": os.environ["JIRA_ASSIGNEE_B"],
    "C": os.environ["JIRA_ASSIGNEE_C"],
    "D": os.environ["JIRA_ASSIGNEE_D"],
}


# ============================================================
# Parsing configuration
# ============================================================

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


# Matches headings such as:
#
# ## 21–27 Sep — Edge Foundation
# ## 28 Sep–4 Oct — Event Collection Skeleton
# ## 5–11 Oct — Session Builder
#
WEEK_RE = re.compile(
    r"^##\s+"
    r"(?P<start>\d{1,2})"
    r"(?:\s*(?:–|-|—)\s*(?P<end>\d{1,2}))?"
    r"\s+(?P<month>[A-Za-z]{3,9})"
    r"(?:\s*(?:–|-|—)\s*(?P<end_month>[A-Za-z]{3,9}))?"
    r"\s+—\s+"
    r"(?P<title>.+?)"
    r"\s*$"
)


# Matches:
#
# - [ ] Task
# - [x] Completed task
# - [!] Blocked task
#
TASK_RE = re.compile(
    r"^- \[(?P<state>[ xX!])\]\s+(?P<task>.+?)\s*$"
)


# Matches checklist title such as:
#
# # PiSentinel — Edge Computing / Network Telemetry (A) Checklist
#
ROLE_RE = re.compile(
    r"^#\s+PiSentinel\s+—\s+.+?\s+"
    r"\((?P<member>[ABCD])\)\s+Checklist"
)


# ============================================================
# Data model
# ============================================================

@dataclass(frozen=True)
class Task:
    member: str
    source_file: str
    week: str
    week_title: str
    text: str
    due_date: date


# ============================================================
# Date parsing
# ============================================================

def due_date_for(heading: str) -> date | None:
    """
    Return the week-end date for a valid week heading.

    Informational headings such as:

        ## Current status

    return None instead of raising an exception.
    """

    match = WEEK_RE.match(heading)

    if not match:
        return None

    start_month = MONTHS[
        match.group("month")[:3].lower()
    ]

    end_month = MONTHS[
        (match.group("end_month") or match.group("month"))[:3].lower()
    ]

    end_day = int(
        match.group("end") or match.group("start")
    )

    # PiSentinel build period:
    # September 2026 -> February 2027.
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


# ============================================================
# Checklist parser
# ============================================================

def parse_checklist(path: Path) -> list[Task]:
    """
    Parse one member checklist.

    Only unchecked [ ] tasks under valid week headings
    become Jira issues.

    [x] completed tasks are ignored.
    [!] blocked tasks are ignored.

    Informational headings such as "## Current status"
    are ignored for Jira due-date purposes.
    """

    lines = path.read_text(
        encoding="utf-8"
    ).splitlines()

    # --------------------------------------------------------
    # Determine team member
    # --------------------------------------------------------

    member = None

    for line in lines[:5]:
        match = ROLE_RE.match(line.strip())

        if match:
            member = match.group("member")
            break

    if member is None:
        raise ValueError(
            f"Cannot determine A/B/C/D from {path}"
        )

    # --------------------------------------------------------
    # Parse tasks
    # --------------------------------------------------------

    tasks: list[Task] = []

    heading = None
    heading_title = None
    due_date = None

    for line in lines:

        # ----------------------------------------------------
        # Heading
        # ----------------------------------------------------

        if line.startswith("## "):

            heading = line.strip()

            match = WEEK_RE.match(heading)

            if match:
                heading_title = match.group("title")
                due_date = due_date_for(heading)
            else:
                # Informational/non-week heading.
                #
                # Example:
                # ## Current status
                #
                heading_title = heading[3:].strip()
                due_date = None

            continue

        # ----------------------------------------------------
        # Task
        # ----------------------------------------------------

        match = TASK_RE.match(line)

        if not match:
            continue

        # A task must be inside a valid week heading.
        if heading is None or due_date is None:
            continue

        state = match.group("state")

        # Only unchecked [ ] tasks become Jira issues.
        #
        # [x] = completed
        # [!] = blocked
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


# ============================================================
# Stable task ID
# ============================================================

def stable_id(task: Task) -> str:
    """
    Generate a deterministic ID for a checklist task.

    The same checklist item will always produce the same ID,
    preventing duplicate Jira issues on repeated syncs.
    """

    raw = (
        f"{task.source_file}|"
        f"{task.week}|"
        f"{task.text}"
    ).encode()

    return hashlib.sha256(raw).hexdigest()[:12]


# ============================================================
# Jira authentication
# ============================================================

def auth_headers() -> dict[str, str]:
    """
    Build Jira Basic Auth headers using:

        JIRA_EMAIL
        JIRA_API_TOKEN
    """

    credentials = f"{EMAIL}:{TOKEN}"

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    return {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


# ============================================================
# Jira HTTP helper
# ============================================================

def jira(method: str, path: str, **kwargs):
    """
    Make an authenticated Jira REST API request.
    """

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


# ============================================================
# Jira description
# ============================================================

def description_adf(task: Task) -> dict:
    """
    Build a Jira Atlassian Document Format description.
    """

    paragraphs = [
        f"Member: {task.member}",
        f"Source: checklists/{task.source_file}",
        f"Week: {task.week}",
        f"Stable task ID: {stable_id(task)}",
        "",
        "Checklist item:",
        task.text,
        "",
        "Definition of done:",
        (
            "Working code/output is built, run, tested, "
            "and committed. Update the Markdown checklist "
            "only after the work is actually complete."
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


# ============================================================
# Duplicate detection
# ============================================================

def existing_issue(task: Task) -> dict | None:
    """
    Search Jira for an existing issue with this task's
    deterministic label.
    """

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
                "summary,status,assignee,labels"
            ),
        },
    )

    issues = data.get("issues", [])

    return issues[0] if issues else None


# ============================================================
# Jira issue creation
# ============================================================

def create_issue(task: Task) -> str:
    """
    Create a Jira Task for one checklist item.
    """

    stable = stable_id(task)

    payload = {
        "fields": {
            "project": {
                "key": PROJECT_KEY
            },

            # Jira Task issue type.
            "issuetype": {
                "id": "10003"
            },

            "summary": (
                f"[{task.member}] "
                f"{task.text}"
            ),

            "description": description_adf(task),

            "assignee": {
                "accountId": ASSIGNEES[task.member]
            },

            "labels": [
                "pisentinel-sync",
                f"pisentinel-{stable}",
            ],

            "duedate": task.due_date.isoformat(),
        }
    }

    response = jira(
        "POST",
        "/rest/api/3/issue",
        json=payload,
    )

    return response["key"]


# ============================================================
# Main sync
# ============================================================

def main() -> None:

    if not CHECKLIST_DIR.exists():
        raise SystemExit(
            f"Missing checklist directory: "
            f"{CHECKLIST_DIR}"
        )

    # --------------------------------------------------------
    # Parse all member checklists
    # --------------------------------------------------------

    tasks: list[Task] = []

    for path in sorted(
        CHECKLIST_DIR.glob("*.md")
    ):

        # README is documentation, not a checklist.
        if path.name.lower() == "readme.md":
            continue

        print(
            f"Reading checklist: {path}"
        )

        parsed_tasks = parse_checklist(path)

        print(
            f"  Found {len(parsed_tasks)} "
            f"pending week tasks"
        )

        tasks.extend(parsed_tasks)

    # --------------------------------------------------------
    # Sync tasks to Jira
    # --------------------------------------------------------

    created = 0
    skipped = 0

    for task in tasks:

        issue = existing_issue(task)

        if issue:

            skipped += 1

            print(
                f"SKIP   {issue['key']}  "
                f"{task.text}"
            )

            continue

        key = create_issue(task)

        created += 1

        print(
            f"CREATE {key}  "
            f"{task.text}"
        )

    # --------------------------------------------------------
    # Summary
    # --------------------------------------------------------

    print()
    print("=" * 60)
    print("PiSentinel Jira Sync Complete")
    print("=" * 60)
    print(f"Created:         {created}")
    print(f"Already present: {skipped}")
    print(f"Pending tasks:   {len(tasks)}")
    print("=" * 60)


# ============================================================
# Entry point
# ============================================================

if __name__ == "__main__":
    main()

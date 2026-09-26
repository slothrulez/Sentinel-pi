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

BASE_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
EMAIL = os.environ["JIRA_EMAIL"]
TOKEN = os.environ["JIRA_API_TOKEN"]
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KAN")
CHECKLIST_DIR = Path(os.getenv("CHECKLIST_DIR", "checklists"))

# Jira account IDs are configuration, not secrets. Keep them out of source control.
ASSIGNEES = {
    "A": os.environ["JIRA_ASSIGNEE_A"],
    "B": os.environ["JIRA_ASSIGNEE_B"],
    "C": os.environ["JIRA_ASSIGNEE_C"],
    "D": os.environ["JIRA_ASSIGNEE_D"],
}

MONTHS = {
    "jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6,
    "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12,
}
WEEK_RE = re.compile(
    r"^##\s+(?P<start>\d{1,2})(?:\s*(?:–|-|—)\s*(?P<end>\d{1,2}))?"
    r"\s+(?P<month>[A-Za-z]{3,9})"
    r"(?:\s*(?:–|-|—)\s*(?P<end_month>[A-Za-z]{3,9}))?"
    r"\s+—\s+(?P<title>.+?)\s*$"
)
TASK_RE = re.compile(r"^- \[(?P<state>[ xX!])\]\s+(?P<task>.+?)\s*$")
ROLE_RE = re.compile(r"^#\s+PiSentinel\s+—\s+.+?\s+\((?P<member>[ABCD])\)\s+Checklist")


@dataclass(frozen=True)
class Task:
    member: str
    source_file: str
    week: str
    week_title: str
    text: str
    due_date: date


def due_date_for(heading: str) -> date:
    m = WEEK_RE.match(heading)
    if not m:
        raise ValueError(f"Unsupported week heading: {heading!r}")

    start_month = MONTHS[m.group("month")[:3].lower()]
    end_month = MONTHS[(m.group("end_month") or m.group("month"))[:3].lower()]
    end_day = int(m.group("end") or m.group("start"))

    # PiSentinel runs Sep 2026 -> Feb 2027.
    start_year = 2026 if start_month >= 9 else 2027
    end_year = start_year if end_month >= start_month else start_year + 1
    return date(end_year, end_month, end_day)


def parse_checklist(path: Path) -> list[Task]:
    lines = path.read_text(encoding="utf-8").splitlines()

    member = None
    for line in lines[:5]:
        m = ROLE_RE.match(line.strip())
        if m:
            member = m.group("member")
            break
    if member is None:
        raise ValueError(f"Cannot determine A/B/C/D from {path}")

    tasks: list[Task] = []
    heading = None
    heading_title = None

    for line in lines:
        if line.startswith("## "):
            heading = line.strip()
            m = WEEK_RE.match(heading)
            heading_title = m.group("title") if m else heading[3:].strip()
            continue

        m = TASK_RE.match(line)
        if not m or heading is None:
            continue

        # Only unchecked tasks become Jira issues.
        if m.group("state").lower() != " ":
            continue

        tasks.append(
            Task(
                member=member,
                source_file=path.name,
                week=heading[3:].strip(),
                week_title=heading_title or "",
                text=m.group("task"),
                due_date=due_date_for(heading),
            )
        )

    return tasks


def stable_id(task: Task) -> str:
    raw = f"{task.source_file}|{task.week}|{task.text}".encode()
    return hashlib.sha256(raw).hexdigest()[:12]


def auth_headers() -> dict[str, str]:
    encoded = base64.b64encode(f"{EMAIL}:{TOKEN}".encode()).decode()
    return {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def jira(method: str, path: str, **kwargs):
    r = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers=auth_headers(),
        timeout=30,
        **kwargs,
    )
    if not r.ok:
        raise RuntimeError(f"{method} {path}: {r.status_code}: {r.text}")
    return r.json() if r.content else {}


def description_adf(task: Task) -> dict:
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
        "Working code/output is built, run, tested, and committed. "
        "Update the Markdown checklist only after the work is actually complete.",
    ]
    return {
        "type": "doc",
        "version": 1,
        "content": [
            {
                "type": "paragraph",
                "content": [{"type": "text", "text": line or " "}],
            }
            for line in paragraphs
        ],
    }


def existing_issue(task: Task) -> dict | None:
    label = f"pisentinel-{stable_id(task)}"
    jql = f'project = "{PROJECT_KEY}" AND labels = "{label}"'
    data = jira(
        "GET",
        "/rest/api/3/search/jql",
        params={
            "jql": jql,
            "maxResults": 1,
            "fields": "summary,status,assignee,labels",
        },
    )
    issues = data.get("issues", [])
    return issues[0] if issues else None


def create_issue(task: Task) -> str:
    stable = stable_id(task)
    payload = {
        "fields": {
            "project": {"key": PROJECT_KEY},
            "issuetype": {"id": "10003"},  # Jira Task
            "summary": f"[{task.member}] {task.text}",
            "description": description_adf(task),
            "assignee": {"accountId": ASSIGNEES[task.member]},
            "labels": ["pisentinel-sync", f"pisentinel-{stable}"],
            "duedate": task.due_date.isoformat(),
        }
    }
    return jira("POST", "/rest/api/3/issue", json=payload)["key"]


def main() -> None:
    if not CHECKLIST_DIR.exists():
        raise SystemExit(f"Missing checklist directory: {CHECKLIST_DIR}")

    tasks: list[Task] = []
    for path in sorted(CHECKLIST_DIR.glob("*.md")):
        if path.name.lower() != "readme.md":
            tasks.extend(parse_checklist(path))

    created = skipped = 0
    for task in tasks:
        issue = existing_issue(task)
        if issue:
            skipped += 1
            print(f"SKIP   {issue['key']}  {task.text}")
            continue

        key = create_issue(task)
        created += 1
        print(f"CREATE {key}  {task.text}")

    print(
        f"Done. created={created}, already_present={skipped}, "
        f"pending={len(tasks)}"
    )


if __name__ == "__main__":
    main()

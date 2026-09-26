#!/usr/bin/env python3

import base64
import os
import requests


BASE_URL = os.environ["JIRA_BASE_URL"].rstrip("/")
EMAIL = os.environ["JIRA_EMAIL"]
TOKEN = os.environ["JIRA_API_TOKEN"]
PROJECT_KEY = os.getenv("JIRA_PROJECT_KEY", "KAN")


def headers():
    credentials = f"{EMAIL}:{TOKEN}"

    encoded = base64.b64encode(
        credentials.encode()
    ).decode()

    return {
        "Authorization": f"Basic {encoded}",
        "Accept": "application/json",
        "Content-Type": "application/json",
    }


def jira(method, path, **kwargs):
    response = requests.request(
        method,
        f"{BASE_URL}{path}",
        headers=headers(),
        timeout=30,
        **kwargs,
    )

    if not response.ok:
        raise RuntimeError(
            f"{method} {path} failed: "
            f"{response.status_code}\n"
            f"{response.text}"
        )

    return response.json() if response.content else {}


def get_all_task_ids():
    issues = []
    next_page_token = None

    while True:
        params = {
            "jql": (
                f'project = "{PROJECT_KEY}" '
                f'AND issuetype = Task'
            ),
            "maxResults": 100,
            "fields": "summary",
        }

        if next_page_token:
            params["nextPageToken"] = next_page_token

        data = jira(
            "GET",
            "/rest/api/3/search/jql",
            params=params,
        )

        issues.extend(data.get("issues", []))

        next_page_token = data.get(
            "nextPageToken"
        )

        if not next_page_token:
            break

    return issues


def delete_issue(issue):
    key = issue["key"]
    summary = issue["fields"]["summary"]

    print(
        f"DELETE {key}: {summary}"
    )

    jira(
        "DELETE",
        f"/rest/api/3/issue/{key}",
        params={
            "deleteSubtasks": "true"
        },
    )


def main():

    print("=" * 60)
    print("PiSentinel Jira RESET")
    print("=" * 60)

    issues = get_all_task_ids()

    print(
        f"\nFound {len(issues)} Jira Tasks "
        f"in project {PROJECT_KEY}."
    )

    if not issues:
        print("Nothing to delete.")
        return

    print()
    print(
        "This will permanently delete "
        f"{len(issues)} Jira Task issues."
    )
    print()

    confirmation = input(
        "Type DELETE PISENTINEL to continue: "
    ).strip()

    if confirmation != "DELETE PISENTINEL":
        print("Cancelled.")
        return

    print()

    deleted = 0

    for issue in issues:
        delete_issue(issue)
        deleted += 1

    print()
    print("=" * 60)
    print("RESET COMPLETE")
    print("=" * 60)
    print(
        f"Deleted: {deleted}"
    )
    print("=" * 60)


if __name__ == "__main__":
    main()

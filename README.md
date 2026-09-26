# PiSentinel

Adaptive cyber deception, explainable behavioural intelligence, and digital
forensics platform built around a Raspberry Pi 4 (2 GB).

## Team

- A — Anirudh: Edge Computing / Network Telemetry / Session & Feature Engineering
- B — Anshika: Machine Learning / SHAP / Behavioural Intelligence
- C — Amala: Backend / Dashboard / System Integration
- D — Britto: Cybersecurity Intelligence / Adaptive Defense / Digital Forensics

## Jira automation

`checklists/*.md` is the source of truth. GitHub Actions runs
`scripts/sync_jira.py` every Monday and whenever a checklist changes.

The sync:
1. Parses weekly headings and unchecked tasks.
2. Creates Jira **Task** issues in project `KAN`.
3. Assigns each issue to A/B/C/D.
4. Sets the weekly end date as the Jira due date.
5. Adds a stable ID label to prevent duplicates.
6. Leaves completed/blocked checklist items untouched.

## Required GitHub Actions secrets

- `JIRA_BASE_URL`
- `JIRA_EMAIL`
- `JIRA_API_TOKEN`
- `JIRA_ASSIGNEE_A`
- `JIRA_ASSIGNEE_B`
- `JIRA_ASSIGNEE_C`
- `JIRA_ASSIGNEE_D`

Never commit the Jira API token.

## Working agreement

**Understand → Build → Run → Test → Commit → Done**

# PiSentinel checklist sync

These four Markdown files are the source of truth for team work:
- `anirudh.md` — A
- `anshika.md` — B
- `amala.md` — C
- `britto.md` — D

The sync creates Jira **Task** issues only for unchecked `- [ ]` items under
weekly `##` headings.

- `[x]` completed items are ignored.
- `[!]` blocked items are ignored.
- Each item gets a stable SHA-256-derived label, so reruns are idempotent.
- The Jira due date is the end date in the weekly heading.
- Tasks are assigned using the four Jira account-ID secrets.

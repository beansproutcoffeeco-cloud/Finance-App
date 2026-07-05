# TASKS — coordinating parallel work

This app is essentially **one big file** (`index.html` holds all markup, styles, and
logic). That's great for shipping a self-contained offline PWA, but it means two
uncoordinated edits — especially from separate Claude Code sessions — almost always
land in the same file and collide. This document is how we avoid that: **claim your
area here first, work on a branch, open one PR.**

## Active projects / ownership

Add a row **before** you start work so others can see the area is taken.

| Project | Owner | Branch | Status | Area of code |
|---|---|---|---|---|
| _example:_ Faster CSV import for big files | @you | `import-perf` | Planned | Import / CSV parsing |
| _example:_ Dark-mode polish on Overview | @someone | `overview-dark-mode` | In progress | Overview / dashboard styles |

Areas are roughly: **Import/CSV**, **Overview/dashboard**, **Activity/transactions**,
**Categorization & rules**, **Budgets**, **Savings/investments**, **Recurring**,
**Settings/backup**, **Service worker (`sw.js`)**, **Manifest/icons**.

## Branching model

- Branch off the default branch: **`main`**.
- One project = one short-lived branch = one PR. Don't batch unrelated changes.
- Name branches descriptively (`import-flip-signs-fix`, not `patch-1`).
- `git fetch` and **rebase onto the default branch** before pushing.
- **Never force-push the default branch.**
- Delete your branch after it merges.

## Before you start / PR checklist

- [ ] Claimed a row in the table above (area + branch).
- [ ] Checked open PRs and existing branches for overlap in your area.
- [ ] Branch is rebased on the latest default branch.
- [ ] Change is scoped to your area — no drive-by edits elsewhere in `index.html`.
- [ ] CI is green: the Pages deploy runs on the default branch, and the smoke-test
      workflow on your PR must pass before merge — don't merge on red.
- [ ] PR description explains **what** changed and **why**.

## Running multiple Claude Code sessions at once

- Give each session a **disjoint area** — e.g. one on Import, one on the Overview
  dashboard, one on Settings. Overlap here is where conflicts come from.
- Each session claims its row in the table above **first**, then checks existing
  branches/PRs before creating new work.
- Keep changes **additive** — add new functions / sections rather than rewriting
  shared helpers. A smaller conflict surface means cleaner rebases.
- Note: separate web sessions are **isolated** — each gets a fresh clone and can't
  see the others' uncommitted work. That isolation is exactly why this shared,
  committed coordination doc exists.

## Planned improvement

The real fix is to **split `index.html` into modules** (import, dashboard, settings,
etc.) with a small build step that bundles them back into the single deployable file.
Then different areas live in different files and most of this coordination pain goes
away. Until then, this doc is the guardrail.

# Task Board

Live state of the project. Claude Code: update this file whenever a task changes state.
One task = one work session, ideally. Big tasks get split before starting.

**Current phase:** Phase 0 — Foundation (see `ROADMAP.md`)

## Now (this session / next session)

- [ ] Work through `docs/SETUP-CHECKLIST.md` — create all service accounts
- [ ] Scaffold repo from starter template (see `specs/tech.md`)
- [ ] App boots locally; commit "hello world" + push
- [ ] Set up CI: lint + typecheck + tests run on every push

## Next (this phase, not started)

- [ ] Spec: auth + tenant model (`specs/features/0-auth-and-tenancy.md`)
- [ ] Implement: sign up / log in / log out (Supabase Auth)
- [ ] Implement: `tenants` + `memberships` tables, RLS policies, tenant-scoping helper
- [ ] Implement: app shell — nav sidebar with placeholder pages per module
- [ ] Smoke test: sign up → land on dashboard → data isolated between two test accounts

## Later (parked — do NOT start these until their phase)

- [ ] Phase 1: Contacts & CRM (spec first)
- [ ] Phase 2: Quotes → Invoices → Stripe payments
- [ ] Phase 3: Scheduling & booking page
- [ ] Phase 4: Contracts & e-signature
- [ ] Phase 5: Workflow automation engine
- [ ] Phase 6: Bookkeeping, SMS, polish

## Done

<!-- Move finished tasks here with the date, newest first. -->

## Decisions log

<!-- One line per decision so future sessions don't re-litigate.
Format: YYYY-MM-DD — decision — why. -->

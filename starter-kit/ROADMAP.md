# Roadmap — Business Manager

Build order for the whole app. Each phase produces something you can actually use in
your business before the next phase starts. Do not start a phase until the previous
one is **shipped and verified** (deployed, tested, and used at least once for real).

The rule for every feature inside a phase: **spec → plan → implement → verify → commit.**

---

## Phase 0 — Foundation (the boring part that makes everything else safe)

**Goal:** an empty-but-real app: you can sign up, log in, and see a dashboard shell.
Two different accounts can never see each other's data.

- Repo scaffolded from starter template (Next.js + Supabase + Stripe + Resend)
- Deployed to hosting from day one (every push to `main` auto-deploys)
- Auth: sign up / log in / password reset (Supabase Auth)
- Tenancy: `tenants`, `users`, `memberships` tables; RLS policies; server-side
  tenant-scoping helper used by ALL queries
- App shell: sidebar nav with a placeholder page per module
- CI: lint + typecheck + tests on every push; a smoke test that signs up and loads the dashboard

**Exit test:** create two accounts; verify account B cannot read account A's rows even
with hand-crafted API calls.

## Phase 1 — Contacts & CRM

**Goal:** replace your address book / spreadsheet. First real daily-use value.

- Contacts CRUD: name, email, phone, company, notes, tags
- Lead pipeline: stages (Inquiry → Quoted → Booked → Done), drag between stages
- Activity notes on a contact (calls, emails, meetings — manual entry for now)
- Lead capture form: public page that creates a contact (this is Workflow trigger #1 later)

**Exit test:** all your real clients imported; new inquiry via the public form shows up
in the pipeline.

## Phase 2 — The money path: Quotes → Invoices → Payments  ← MVP line

**Goal:** send a real quote, client accepts, invoice goes out, they pay by card. When
this phase ships, the app is genuinely useful — this is the MVP.

- Services/price list (name, description, unit price, tax rate)
- Quotes: line items from the price list, totals, expiry; client-facing public quote
  page (tokenized link); accept button
- Invoices: created from an accepted quote or from scratch; statuses
  (draft → sent → paid → overdue); client-facing payment page
- Stripe: Checkout for invoice payment; webhook marks invoice paid (signature-verified,
  idempotent); receipts emailed via Resend
- Email sending: quote-sent, invoice-sent, payment-received templates

**Exit test:** full loop with a real client (or yourself with a test card): quote →
accept → invoice → pay → invoice shows paid → receipt email received.

## Phase 3 — Scheduling & booking

**Goal:** clients book time with you online (Workflow trigger #2 later).

- Appointment types (duration, price, buffer time)
- Availability rules (weekly hours, blocked dates)
- Public booking page: pick type → pick slot → enter details → booked
- Booking creates/links a contact; optional payment at booking (reuse Phase 2 Stripe)
- Email confirmations + reminder emails (e.g. 24h before)
- Calendar view of upcoming appointments

**Exit test:** book yourself via the public page; confirmation + reminder arrive;
double-booking is impossible.

## Phase 4 — Contracts & e-signature

**Goal:** send a contract, client signs online, you have an audit trail.

- Contract templates with merge fields ({{client_name}}, {{total}}, {{date}})
- Create a contract from a template for a contact/project
- Client-facing signing page via a managed e-sign provider or embedded signing flow
  (evaluate current options and pricing when you get here — see report's open questions;
  candidates: Documenso, SignWell, Dropbox Sign)
- Signed-PDF storage + audit trail (who, when, IP)
- Status: draft → sent → signed (Workflow trigger #3 later)

**Exit test:** send yourself a contract, sign on a phone, verify stored PDF + audit log.

## Phase 5 — Workflow automation (the "17hats magic")

**Goal:** the app starts doing the follow-up for you. Only possible now because the
earlier phases created the events and the actions.

- Event system: emit events for `lead.created`, `quote.accepted`, `invoice.paid`,
  `booking.created`, `contract.signed`
- Workflow builder: pick a trigger event → ordered list of actions
- Actions: send email template, create to-do, apply tag, send quote/contract/questionnaire,
  wait N days (scheduled step)
- Workflow run log: what fired, when, for whom, success/failure
- To-dos module (simple task list per contact/project) to receive workflow actions

**Exit test:** "when lead form submitted → send welcome email + create 'call them' to-do"
fires end-to-end for a real form submission.

## Phase 6 — Bookkeeping, SMS, polish

**Goal:** round out the suite.

- Bookkeeping: payments from Phase 2 auto-recorded as income; manual expense entry;
  categories; simple profit & loss view per month/quarter
- Recurring invoices (card on file via Stripe)
- SMS notifications/reminders (e.g. Twilio) — optional, has real per-message cost
- Questionnaires/forms builder (send to clients, answers saved to contact)
- Reports dashboard: pipeline value, bookings this month, revenue

---

## What is deliberately NOT in scope (v1)

Say no to these until the above is shipped and in daily use:

- Multi-user teams / staff permissions (the tables support it via `memberships`;
  the UI can wait)
- Native mobile apps (the web app should be responsive; that's enough)
- Third-party calendar two-way sync, Zapier-style integrations, public API
- Multi-currency, multi-language
- Building your own email-sending infrastructure, auth, or payment handling — always managed services

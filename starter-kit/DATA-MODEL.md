# Starter data model

The core entities for all modules, in build order. This is a starting sketch — each
feature spec refines its own tables before building. Conventions:

- Every tenant-owned table: `id uuid primary key default gen_random_uuid()`,
  `tenant_id uuid not null references tenants(id)`, `created_at timestamptz default now()`.
- **Every tenant-owned table gets an RLS policy** (pattern at the bottom). Enable RLS
  the moment the table is created — same migration, no exceptions.
- Statuses are Postgres enums or checked text — never free text.
- Money is stored in **cents as integers** (`total_cents int`), never floats.

## Phase 0 — Tenancy & auth

```
tenants        id, name, created_at
users          (managed by Supabase Auth — auth.users)
memberships    id, tenant_id, user_id, role ('owner'|'staff'), created_at
               unique (tenant_id, user_id)
```

Sign-up flow creates: auth user → tenant → membership(owner).

## Phase 1 — Contacts & CRM

```
contacts       id, tenant_id, first_name, last_name, email, phone, company,
               stage ('inquiry'|'quoted'|'booked'|'done'|'archived'),
               source (e.g. 'lead_form'|'manual'), created_at
tags           id, tenant_id, name unique per tenant
contact_tags   contact_id, tag_id
notes          id, tenant_id, contact_id, body, created_at
lead_forms     id, tenant_id, slug, fields jsonb, is_active
```

## Phase 2 — Money path

```
services       id, tenant_id, name, description, unit_price_cents, tax_rate_pct
quotes         id, tenant_id, contact_id, number, status ('draft'|'sent'|'accepted'|'declined'|'expired'),
               public_token unique, expires_at, accepted_at, total_cents
quote_items    id, quote_id, service_id nullable, description, qty, unit_price_cents
invoices       id, tenant_id, contact_id, quote_id nullable, number,
               status ('draft'|'sent'|'paid'|'overdue'|'void'),
               public_token unique, due_date, total_cents, paid_at
invoice_items  id, invoice_id, description, qty, unit_price_cents
payments       id, tenant_id, invoice_id, stripe_payment_intent_id unique,
               amount_cents, status, paid_at
stripe_events  id, stripe_event_id unique, type, processed_at   -- webhook dedup table
```

Quotes, contracts, and invoices are **separate linked records** (quote → invoice via
`quote_id`), not one mega-document. Separate tables keep statuses, numbering, and
client pages simple, and let each be used standalone.

## Phase 3 — Scheduling

```
appointment_types  id, tenant_id, name, duration_min, price_cents nullable, buffer_min, slug
availability_rules id, tenant_id, weekday (0-6), start_time, end_time
blocked_dates      id, tenant_id, date, reason
bookings           id, tenant_id, contact_id, appointment_type_id,
                   starts_at, ends_at, status ('confirmed'|'cancelled'|'completed'),
                   public_token unique
```

Prevent double-booking with an exclusion constraint or a serialized slot-check
transaction — decide in the Phase 3 spec.

## Phase 4 — Contracts

```
contract_templates id, tenant_id, name, body (with {{merge_fields}})
contracts          id, tenant_id, contact_id, template_id, status ('draft'|'sent'|'signed'|'void'),
                   public_token unique, sent_at, signed_at,
                   signed_pdf_path (Supabase Storage), audit jsonb (who/when/IP)
```

## Phase 5 — Workflows

```
events         id, tenant_id, type ('lead.created'|'quote.accepted'|'invoice.paid'|
               'booking.created'|'contract.signed'), subject_id, payload jsonb, created_at
workflows      id, tenant_id, name, trigger_type (event type), is_active
workflow_steps id, workflow_id, position, action ('send_email'|'create_todo'|'apply_tag'|
               'send_document'|'wait_days'), config jsonb
workflow_runs  id, tenant_id, workflow_id, event_id, status ('running'|'done'|'failed'),
               current_step, log jsonb, run_at
todos          id, tenant_id, contact_id nullable, title, due_date, done_at
email_templates id, tenant_id, name, subject, body
```

Modules write to `events` from Phase 1 onward (cheap insert); the engine that consumes
them arrives in Phase 5. `wait_days` steps need a scheduled runner (cron/scheduled
function) that advances due `workflow_runs`.

## Phase 6 — Bookkeeping

```
txn_categories id, tenant_id, name, kind ('income'|'expense')
transactions   id, tenant_id, kind ('income'|'expense'), category_id,
               amount_cents, date, description,
               payment_id nullable  -- income rows auto-created from Stripe payments
```

## The RLS pattern (used on every tenant-owned table)

Standard SaaS "pool" model: shared tables + `tenant_id` column, isolation enforced by
Postgres Row Level Security — the database applies the tenant filter automatically, so
a forgotten WHERE clause in app code cannot leak data across customers.

```sql
alter table contacts enable row level security;

create policy tenant_isolation on contacts
  for all
  using (
    tenant_id in (
      select tenant_id from memberships where user_id = auth.uid()
    )
  )
  with check (
    tenant_id in (
      select tenant_id from memberships where user_id = auth.uid()
    )
  );
```

Notes:
- `auth.uid()` is Supabase's current-user function; this is the Supabase-native version
  of the classic `current_setting('app.current_tenant')` pattern from the AWS SaaS guides.
- Public client pages (`/pay/[token]` etc.) don't have a logged-in user: fetch those rows
  server-side with the service-role key, looked up **only** by the unguessable
  `public_token` — never expose service-role access to the browser.
- The service-role key bypasses RLS by design; it must only ever exist in server env vars.
- Add an index on `tenant_id` for every large table.

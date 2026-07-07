# Steering doc: Product

<!-- This file rarely changes. It's the "what are we building" anchor every session reads. -->

## Vision

An all-in-one business manager for a solo/small service business (in the spirit of
17hats): one place for leads, quotes, contracts, invoices, payments, bookings, and the
automated follow-up between them. Single-owner accounts first; built multi-tenant from
day one so it can serve other business owners later.

## Who it's for

- **The owner** (primary user): runs the business day-to-day from a phone or laptop.
  Not a developer. Needs everything obvious and forgiving.
- **Their clients** (secondary, public pages only): receive links to view/accept quotes,
  pay invoices, book time, sign contracts. Never log in — tokenized links.

## Module map

The product is these modules, connected. Build order lives in `ROADMAP.md`.

| Module | One-line job | Key objects |
|---|---|---|
| Contacts & CRM | Every person/lead in one place, with a pipeline | contact, tag, pipeline stage, note |
| Quotes | Price a job, client accepts online | quote, line item, service |
| Invoices & Payments | Bill and get paid by card | invoice, payment (Stripe) |
| Scheduling | Clients book time online | appointment type, availability, booking |
| Contracts & e-sign | Send agreements, signed online, audit trail | contract template, contract, signature |
| Workflows | Event-triggered automation: things happen without you | workflow, trigger, action, run log |
| Bookkeeping | Income (automatic) + expenses (manual), simple P&L | transaction, category |
| To-dos & notes | The glue: tasks per contact/project | todo, note |

## The connecting idea (what makes it "all-in-one")

Modules emit **events** (`lead.created`, `quote.accepted`, `invoice.paid`,
`booking.created`, `contract.signed`). Workflows listen to events and run **actions**
(send email template, create to-do, apply tag, send document, wait N days). This is the
product's core differentiator — every module must emit its events from the start, even
though the workflow engine ships in Phase 5.

## Product principles

1. **The money path is sacred.** Quote → invoice → payment must always work; everything
   else can break politely.
2. **Client-facing pages are the storefront.** Fast, mobile-first, zero login friction.
3. **Never lose data, never leak data.** Tenant isolation is enforced by the database,
   not by remembering to filter.
4. **Boring and proven beats clever.** Managed services, standard patterns.

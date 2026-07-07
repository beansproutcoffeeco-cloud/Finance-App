# Build Blueprint: A 17hats Competitor Done Right

Synthesis of docs 01–12. This is the "so what" — what to build, how to structure it, and where to beat 17hats (and HoneyBook/Dubsado, since users comparison-shop all three).

## 1. The core insight: one spine, many views

Everything 17hats does well comes from one architectural decision: **a single client lifecycle spine** — Contact → Project → Documents (quote/contract/invoice) → Payments → Bookkeeping — where every module reads and writes the same records. Scheduling creates projects; forms create contacts; invoice payments become bookkeeping income; workflows orchestrate all of it. Competitors that bolt together point solutions can't match the "everything is already connected" feel.

Everything 17hats does badly comes from age and closure: a UI unchanged since 2014, day-level linear automation, single-entry bookkeeping with no rules, a read-only client portal, a triage-only mobile app, no API, and hostage-grade data export.

**Thesis for our app:** keep the spine, modernize every surface of it, and open the box (API-first, export-everything). Per doc 12, no incumbent holds more than two of: modern UX · deep-but-easy automation · real financial reporting · full-featured mobile · honest pricing · data freedom. Holding four or five of these wins switchers.

## 2. Unified data model

Consolidated from the per-doc schema sketches (docs 02–10). Names are suggestions; relationships are the point.

```
Account (tenant)
├─ Brand (1..n — branding, sending identity, timezone, currency)
├─ User (roles: owner/admin/member; per-member permissions)
└─ Settings, ApiKey, Webhook, Integration

Contact
├─ type: lead | prospect | client | other  → replace with: stage on Pipeline (customizable)
├─ emails[], phones[], addresses[], company, custom_fields (typed, tokenizable)
├─ tags[] (shared tag registry; tags drive automation + views)
├─ portal: capability_url, pin/passkey, visibility_settings
└─ referred_by → Contact, lead_source → LeadSource

Project  ("folder" — the work unit; 17hats got this right)
├─ contact (primary), related_contacts[] (role: cc | co_signer | participant)
├─ title, base_dates[] (NAMED anchor dates — improvement over 17hats' single base date)
├─ stage → PipelineStage (ONE stage system, kanban-visualized — not three overlapping ones)
├─ tags[], custom_fields, calendar, archived_at
└─ children: Document[], EmailThread[], Note[], File[], Task[], Event[],
             TimeLog[], PhoneLog[], WorkflowInstance[], ActivityEvent[]

Document  (unified abstraction — doc 04's key finding)
├─ kind: quote | contract | invoice | questionnaire | bundle
├─ status: draft → sent → viewed → in_progress → completed | expired | voided
├─ template_ref, token_context, expiration, reminder_rules[]
├─ Quote: line_items[] (standard | choose_one | choose_any, qty rules, images),
│         discounts, tax_rates[], selections sync → attached Invoice
├─ Contract: rich_text + form_fields (initials/checkbox/text), signers[] (ordered),
│            signature_events[], audit_certificate (BUILD THIS — 17hats lacks it)
├─ Invoice: number (immutable), line_items[], PaymentSchedule (installments[]:
│           amount, due_rule {absolute | on_receipt | relative_to base_date},
│           auto_charge_optin), payments[], refunds[], receipts[]
├─ Questionnaire: questions[] (typed, if/then branching), answer_mapping → fields
└─ Bundle: ordered children [quote, contract, invoice] with forward-locking gates

Payment / Refund / PayoutEvent  (Stripe-backed; fee rows auto-post to ledger)

Scheduling
├─ Service (duration, buffers, location{zoom|physical|phone}, price/deposit,
│           booking_questions[], confirmation mode, workflow_trigger)
├─ AvailabilitySchedule (rules[], overrides[], min_notice, max_horizon, caps,
│                        calendar cross-check refs, team_members[])
├─ Booking (→ auto: Contact + Project + Event + Invoice? + WorkflowInstance)
└─ CalendarAccount (google | microsoft | ical_feed; two-way sync state)

Automation  (docs 07's engine sketch, upgraded)
├─ WorkflowTemplate (versioned; steps[]; publishable to template gallery)
├─ Step: kind {task | action | wait | gate | branch}
│   ├─ action: send_email/document, apply_tag, change_stage, start_workflow,
│   │          create_task, webhook_out, archive
│   ├─ timing: offset ± N {days|hours} from {activation | named_base_date | prev_step}
│   ├─ execution: automatic | require_approval        ← copy 17hats exactly
│   ├─ gate: until {quote_accepted | contract_signed | invoice_paid ...}   ← copy
│   └─ branch: on tag / questionnaire answer / document outcome  ← beat 17hats
├─ WorkflowInstance (copied steps + LIVE template re-sync option — fixes their #1 pain)
└─ Trigger registry: form_submitted, booking_confirmed, tag_added/removed,
   document_event, payment_event, stage_changed, date_reached, manual, api
   → every trigger doubles as an outbound webhook/Zapier event (doc 10)

Finance  (docs 05/06 + the user's existing Finance-App strengths)
├─ LedgerAccount (bank/cc; feed via aggregator or CSV import)
├─ Transaction (imported | manual; category, splits[], receipt_files[],
│               project_ref, verified flag ← copy the verify gate)
├─ CategoryRule (user-visible, learning — port from Finance-App)
├─ TransferMatch (opposite-amount cross-account detection — port from Finance-App)
├─ InvoicePayment → auto-post categorized income + processor-fee expense  ← copy
├─ DepositMatch (payout → bank transaction reconciliation — 17hats can't; we can)
└─ Reports: P&L, sales tax, receivables, quarterly tax estimate (they lack it),
            category/budget views (port from Finance-App)

Comms
├─ EmailAccount (OAuth Gmail/Microsoft; per-tenant DKIM sending domain)
├─ EmailMessage/Thread (webhook-based real-time filing onto contact+project —
│                       beats their 20–45 min poll that drops unknown senders)
├─ Template (kind-scoped; folders; shared token language)
└─ TokenLanguage: [% entity.path | filters %] — one grammar across email,
   documents, SMS, reminders (17hats proved this; copy it)
```

## 3. Architecture recommendations

- **Event bus at the core.** Every state change (document viewed, payment succeeded, tag added) emits a typed event. Workflows, webhooks, Zapier, notifications, and the activity log are all consumers. 17hats clearly lacks this (no webhooks, weak Zapier, batched emails); building it first makes automation, integrations, and audit trails nearly free.
- **Scheduler as a first-class service** for workflow timing (named-base-date offsets, re-flow on date edit), document reminders, and installment auto-charges (their 10 a.m. batch model is fine; add hour-level precision).
- **API-first:** the public REST API is the frontend's API. Publish docs + webhooks from day one — the single clearest structural gap in the whole category (doc 10).
- **PDF/audit service:** server-side PDF rendering with signature audit certificates (IP, timestamp, event chain). 17hats' print-to-PDF workaround is indefensible in 2026 (doc 04).
- **PWA-first mobile.** Every incumbent's mobile app is their worst-reviewed surface (~3.3★, can't create documents — doc 11). A responsive PWA with full create-capability beats three codebases; the user has already shipped an offline-capable PWA (Finance-App), so this plays to existing strength.
- **Multi-brand from day one** (cheap if modeled early, painful to retrofit — doc 11), but skip multi-currency-per-brand, payroll, and inventory at launch.

## 4. MVP cut

Phase 1 — the money loop (this alone is a sellable product):
1. Contacts + projects + tags + custom fields
2. The **3-in-1 bundle**: quote (choose-one/choose-any items) → contract (e-sign + audit cert) → invoice (payment schedule, Stripe card/ACH/wallets, auto-charge opt-in, reminders)
3. Templates + token language
4. Client-facing document pages (no-login capability URLs) + real PDF export

Phase 2 — the automation moat:
5. Lead capture forms (answer mapping, tag-driven routing)
6. Workflow engine (linear + gates + approval mode first; branching next)
7. Email OAuth send + real-time thread filing; scheduling (service + availability + booking fan-out)

Phase 3 — the finance wedge (our unfair advantage):
8. Port Finance-App's import/categorization/rules/transfer-detection; add invoice-payment auto-income, deposit matching, P&L + quarterly tax estimates, budgets
9. Public API + webhooks + Zapier (rich event surface), QBO/Xero sync, full-account export

Skip (deliberately, per docs 01/12): SMS infrastructure at launch, native mobile apps, 100-industry marketing surface, lifecycles-style duplicate stage systems, marketplace-inbox email parsing, payroll/inventory.

## 5. Differentiation strategy (evidence → move)

| 17hats weakness (evidence) | Our move |
|---|---|
| UI "stuck in 2015", broken doc editor (docs 11, 12) | Modern, fast UI; block-based document editor with clean Word/Google-Docs paste |
| 3-step workflow ceiling, no branching, day-only timing (07) | Gates + approval mode at parity, then branching, named anchor dates, template re-sync |
| Shallow bookkeeping: no rules, splits, deposit matching, tax estimates (06) | The Finance-App engine as the accounting layer — "the one that gets your books right" |
| "Little to nothing on reporting" (12) | Dashboard with a money snapshot + drill-down reports from day one |
| Mobile app ~3.3★, can't create documents (11) | Full-capability PWA |
| No API/webhooks, contacts-only Zapier, export hostage (10) | API-first, webhooks, one-click full-account export (even post-cancellation) |
| Add-on pricing creep: $60 base ≈ $85 real (12) | One honest price, everything included; publish the comparison |
| 7-day trial vs heavy setup (01) | 30-day trial + guided setup checklist + starter template gallery per industry |
| Read-only client portal, no uploads/messaging (03) | Two-way portal: uploads, comments, task visibility, magic-link auth |
| Google-only calendar sync (08) | Google + Microsoft two-way at parity |

Positioning to steal: 17hats' own best ideas — the lifecycle spine, the 3-in-1 bundle, approval-mode automation, invoice→bookkeeping auto-income, the template marketplace, tag-driven everything, 30-day soft-delete — are documented per-doc under "Build recommendations: copy."

## 6. Open questions to resolve before building

1. **Vertical focus:** 17hats won photographers first, then broadened. Pick the beachhead segment (photographers are switch-willing but crowded; adjacent: coaches, planners, home services).
2. **Pricing:** flat all-inclusive (~$40–50/mo undercuts everyone post-hikes) vs free-tier-plus-payments-revenue (HoneyBook model). Doc 01 §7 has the trade-offs.
3. **Local-first stance:** Finance-App's privacy story (data never leaves the device) can't fully survive a multi-user client-facing SaaS — decide where the line is (e.g. bookkeeping stays local-capable, client-facing spine is cloud).
4. Re-verify all pricing/plan/Zapier facts against live pages (research environment couldn't fetch 17hats directly — see 00-README caveats).

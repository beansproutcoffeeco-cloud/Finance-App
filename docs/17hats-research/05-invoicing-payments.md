# 17hats: Invoicing & Payments

> Research area 5 of 12 — how 17hats handles invoice creation, payment schedules, recurring billing, payment processing, reminders, refunds, and the client payment experience.
>
> **Method note:** Direct fetching of 17hats.com / help.17hats.com was blocked by the network proxy in this environment, so this document is compiled from extensive web-search extractions of 17hats Help Center articles, 17hats feature/pricing pages, 17hats University, release notes, and third-party reviews (Capterra, G2, blogs). All fee figures are **as of mid-2026 search results** and should be re-verified before launch. Items marked *(inferred)* or *(unverified)* were not directly confirmed.

---

## 1. Summary

- Invoicing is one of 17hats' core "Money Matters" pillars, tightly coupled with Quotes, Contracts, Bookkeeping, and Workflows. Invoices live inside Projects and Contacts, are branded automatically (logo/fonts/colors), and can be sent standalone or as part of a **3-in-1 Quote → Contract → Invoice** document where the client selects options, signs, and pays in one flow.
- The invoice model supports line items pulled from a saved **Products & Services** catalog, multiple named **tax rates** (applied per line item via a "taxable" flag), invoice-level **discounts** (fixed $ or %), tips, PO numbers, notes, and auto-incrementing invoice numbers.
- Deposits/retainers are handled through **Payment Schedules**: an invoice's total is split into up to **12 installments** ("Equal" auto-split or fully "Custom" amounts/dates), with due dates that can be absolute, upon receipt, or **relative to a project date** (e.g., "50% due 2 months prior to event").
- **Recurring Invoices** are a separate concept from payment schedules: a duplicate invoice is auto-generated and sent weekly/monthly/yearly for N occurrences, with optional client-opt-in **automatic charging** of a saved card (charged ~10 a.m. on the due date).
- Payment processing has consolidated onto **17hats Payments** (Stripe-powered) for new accounts; legacy **Stripe** and **Square** connections persist for older accounts, and **PayPal / Authorize.net** are legacy/retired. Cards (Visa/MC/Discover/Amex), **ACH (US only)**, and **Apple Pay / Google Pay** digital wallets are supported. Card fee ≈ **2.9% + $0.30**; ACH ≈ **0.8% + $1.50 capped at $6.50**.
- Automation is a differentiator: auto payment reminders (before due + recurring past-due), auto receipts, auto-created invoices from lead capture forms, workflows, and online scheduling ("Pay Upon Booking" with full or partial payment).
- Notable gaps users complain about: **no native late fees**, one processor + one currency at a time (global, not per-client), weak bookkeeping reports, no fee pass-through/surcharge feature, and payment-method settings being account-wide.

---

## 2. Invoice model

### 2.1 Where invoices live

- Invoices are documents attached to a **Contact + Project**; they also appear in the account-wide **Documents** tab, in the client's **Client Portal**, and in "Recent Client Activity."
- The dashboard surfaces "overdue invoices" and money owed at a glance; Bookkeeping provides receivables reports (see §5.5/§6).
- Invoices can be created: manually from a contact/project, from an **Invoice Template**, by conversion from an accepted **Quote**, automatically by a **Workflow** or **Lead Capture Form** submission, by **Online Scheduling** booking, or by a **Recurring Invoice** schedule.

### 2.2 Invoice Options (header-level fields)

Set at the top of each invoice ("Invoice Options"):

| Field | Notes |
|---|---|
| Internal title | For the member's own reference |
| Display title | What the client sees |
| Invoice number | Auto-generated, sequential (use "10" → next is "11"); editable **before first save only**; numbers are unique and never reused, even after deletion |
| Due date | Drives reminders/overdue status; reminders require a due date |
| PO number | Optional purchase-order reference |
| Notes | Free text shown on invoice |
| Tax rate | Select from pre-configured tax rates; applies to line items flagged taxable |
| Discount | Fixed dollar amount **or** percentage of invoice total (invoice-level) |
| Tipping on/off | Per-invoice toggle (see §5.4) |
| Online payments on/off | Whether client can pay online |
| Payment schedule | Checkbox to split total into installments (see §3) |
| Recurring settings | Frequency/occurrences (see §4) |
| Save card / automatic payments | Opt-in options offered to client (see §4/§7) |

*(inferred)* Additional global defaults (default due terms, default merchant, currency) come from **Account Settings → Money Matters → Invoice Options**.

### 2.3 Line items

- Three sources when composing: **packages**, **à la carte items**, and **standard items**, plus free-typed one-off items.
- Line item fields: **name, description, price, quantity, category** (income category for bookkeeping), **taxable flag + tax rate**. Packages can list included sub-items, hours included, and headcount ("how many people the item includes").
- **Products & Services catalog** (Account Settings → Money Matters → Products & Services): saved reusable items; view/edit/duplicate/delete; typing an item name in a line item autocompletes from the catalog. Items support separate **internal name vs. display name**.
- **Images** can be added to invoice and quote line items (help article "Adding Images to Invoices and Quotes").
- Quote-specific line-item types that flow into the generated invoice: **Standard item** (must purchase), **"Choose One"** (pick one option), **"Choose Any"** (pick any from a list, e.g. add-ons/upsells). "Choose Any" items can allow the **client to edit quantity** (e.g., tickets) or lock it. Client selections on a quote automatically update the linked invoice.
- **No per-line discount field**: to discount a single item you manually lower its price or add a **negative line item**. Invoice-level discount applies to the total.

### 2.4 Taxes

- Multiple named **tax rates** are configured in Account Settings → Money Matters → **Tax Settings**.
- On an invoice, you pick the applicable rate in Invoice Options; it applies to every line item marked **Taxable**, and taxability/rate can be overridden per line item.
- Catalog items carry a default "Taxable" checkbox that prompts selection from the pre-set rate list.
- A **Sales Tax Report** aggregates tax collected for remittance (exportable; see §6/§5.5).
- *(unverified)* No evidence of compound taxes, tax-inclusive pricing, or automatic jurisdiction lookup — appears to be simple named flat rates only.

### 2.5 Statuses & lifecycle

Statuses observed in documentation (17hats does not publish a single canonical status list — partially *(inferred)*):

- **Draft** — created but not sent; drafts do not sync to QuickBooks and *(inferred)* don't trigger reminders.
- **Sent / Unpaid (Open)** — emailed to client (or "marked as sent"); payable online.
- **Partially paid** — payments recorded but balance > 0 *(inferred from partial-payment/payment-schedule behavior; exact label unverified)*.
- **Paid** — "Once the balance is zero, the invoice will be stamped as 'Paid'."
- **Overdue / Past due** — past due date with balance; drives dashboard alerts and past-due reminder emails.
- **Void** — via Edit → Void Invoice. Voiding stops the invoice from showing as due. **Payments already on a voided invoice are NOT deleted or reversed** — they still count toward income categories in Bookkeeping, and payments cannot be removed after voiding.
- **Refunded** *(inferred as a state or annotation after refund actions; see §6.3)*.
- Reminder emails only run for documents in **Active Projects** — archiving/completing a project effectively silences automation.

### 2.6 Templates & branding

- **Invoice Templates** live under Account Settings → Documents & Emails; templates prefill line items/options and are the primary speed tool ("quickly make adjustments before sending").
- Branding (logo, fonts, colors) from **Brand Preferences** is applied automatically to every invoice; the logo renders at the top of the document.
- Multiple **brands** are supported as a paid add-on; each linked brand can have **its own currency and its own merchant account** (this is also the only path to multi-currency; see §2.7).

### 2.7 Currency

- One currency per account/brand, default **USD**, changeable in Account Settings → Invoice Options to an international currency. 17hats supports many currencies but you invoice in **one currency at a time**.
- Multi-currency requires adding a **linked brand** (add-on cost); each brand still has exactly one currency + one merchant connection.
- ACH is **US-members-only**; card acceptance via 17hats Payments is available to international members.

### 2.8 Combined 3-in-1 documents

- Quote + Contract + Invoice can be sent as one package (or 2-part Quote/Contract, Quote/Invoice, or standalone).
- Client flow: view quote → accept (selecting Choose One/Choose Any options) → contract tab unlocks for signature → invoice generated/updated with chosen options → pay. Acceptance date is stamped on the quote footer.
- This "select, sign, pay in one document" flow is 17hats' flagship booking experience and a key thing to replicate.

---

## 3. Payment schedules & deposits

- **Purpose:** split ONE invoice's total into multiple dated installments — 17hats' mechanism for deposits/retainers ("$2,000 due upon receipt, 50% due 2 months prior, balance due 1 week prior" on a $10,000 invoice).
- **Prerequisite:** at least one line item must exist; then a **Payment Schedule checkbox** in the invoice enables the split.
- **Limit:** up to **12 payments** per invoice schedule.
- **Two modes:**
  - **Equal Payments** — choose first payment date, number of payments, and repeat interval; 17hats does the math and splits evenly.
  - **Custom Payments** — define each installment's amount (fixed $ or % — the marketing examples use both) and its own due date; amounts need not be equal.
- **Due-date anchors:** specific date, "upon receipt," and **relative to a project/event date** (e.g., "2 months prior," "1 week prior") — important for wedding/event verticals.
- **Reminders/receipts per installment:** invoice reminders key off the next installment due date; confirmation emails send per payment *(inferred from reminder + auto-payment docs)*.
- **Automatic Payments for Payment Schedules:** when enabled, the client paying installment #1 online is offered two checkboxes — (1) save card, (2) auto-charge saved card — and if both are checked, **all future installments on that invoice are charged automatically** (~10 a.m. on each due date). Client receives a confirmation email on each auto-charge. Requires Stripe/Square/17hats Payments.
- **Plan gating (legacy tiers):** Payment Schedules were **Standard (Level 2) and Premier (Level 3) only** — not in the entry Essentials tier. (In 2025 17hats moved to a single all-inclusive plan ~$60/mo / $600/yr, so gating may be moot now; see §9.)
- **Deposit vs. retainer terminology:** 17hats doesn't have a distinct "deposit object" — the first scheduled payment *is* the retainer. Online Scheduling separately supports partial "pay upon booking" (see §7.3).
- **Distinct from Recurring Invoices:** a payment schedule = one invoice, one total, many due dates. A recurring invoice = many separate invoices over time. 17hats maintains a dedicated help article ("Recurring Invoices Vs. Payment Schedules") because users confuse them — a UX lesson.

---

## 4. Recurring invoices

- **Model:** auto-generate and auto-send a **duplicate** of an invoice on a schedule — **weekly, monthly, or yearly** — ending after a set number of **occurrences**. (Marketing also says "weekly, monthly, or custom.")
- **Setup:** enable Recurring Billing in Account Settings → Money Matters → Invoice Options (turn on Online Payments, Recurring Invoice, and "Enable Automatic Charging"), then set recurrence on the individual invoice/template.
- **Auto-charge (subscription-like behavior):** with automatic charging enabled, the client paying the first invoice sees two opt-ins — save card + auto-charge. If both accepted, each future recurring invoice is charged to the saved card **around 10 a.m. on its due date**, and the client gets a confirmation email per charge.
- **Card storage:** card data is stored **with the processor (Stripe/Square), not 17hats**. Consequence documented by 17hats: **switching processors breaks all saved-card auto-charges** — clients must re-enter card data. 17hats explicitly warns not to switch providers after enabling recurring billing.
- **Processor requirement:** recurring/auto-charge only works with Stripe and Square (now 17hats Payments); it never worked with PayPal/Authorize.net.
- **Failed charge handling:** *(unverified)* no public documentation found on retry logic or dunning for failed auto-charges; assume minimal (notification only) and verify.
- **No true subscription engine:** no proration, plan upgrades/downgrades, usage billing, or open-ended "until cancelled" documentation found (occurrence count appears required — *(unverified)* whether an "indefinite" option exists).

---

## 5. Payment processing

### 5.1 Processors (history and current state)

| Processor | Status (as of 2025–2026) | Notes |
|---|---|---|
| **17hats Payments** | Current default; **only option for new accounts** | White-labeled solution **powered by Stripe** (Stripe Connect under the hood). KYC survey required by Stripe at signup; business review typically 24–48 h. |
| **Stripe (direct)** | Legacy — existing connections keep working | Help article "Stripe Payments" + "[legacy] Using Stripe for Online Payments." Members may keep legacy connection until they enable 17hats Payments. |
| **Square** | Legacy — existing connections keep working | Supported tipping, save-card, recurring. |
| **PayPal** | Legacy/retired | Only reachable via Zapier-type automation now; old accounts historically could connect it. Could not be active simultaneously with Stripe. |
| **Authorize.net** | Legacy/retired | Historical option. |

- **One merchant account active at a time** per brand — a recurring user complaint (no per-client or per-invoice processor choice).

### 5.2 Fees (cross-checked; re-verify before building comparisons)

| Method | Fee | Source/as-of |
|---|---|---|
| Credit/debit cards (Visa, MC, Discover, Amex) | **2.9% + $0.30** per transaction | 17hats Help ("Credit Card and ACH Processing Fees in 17hats Bookkeeping with Stripe", 2026 search) — described as Stripe's standard fees passing through |
| ACH / eCheck (US only) | **0.8% + $1.50**, **capped at $6.50** (any payment ≥ ~$625 pays $6.50); no monthly or verification fees | 17hats Help "Accept ACH payments through 17hats" (2026 search). Note: this is Stripe's 0.8%/$5-cap ACH fee **plus a $1.50 markup** → 17hats/Stripe-via-17hats effective cap $6.50 |
| Apple Pay / Google Pay | *(inferred)* processed as card transactions at card rates | Help articles confirm availability, not pricing |
| Square (legacy) | Square's own rates (2.6% + 15¢ in person; ~2.9–3.3% + 30¢ online depending on Square plan, post Oct-2025 Square pricing) | Square public pricing, not 17hats-specific |
| 17hats subscription | Single all-inclusive plan ≈ **$60/mo, $600/yr, $800/2yr** (2025 repricing); legacy tiers were Essentials $13 / Standard $25 / Premier $50 per month (annual) | 17hats pricing page + third-party pricing guides |

- **No surcharge/fee-pass-through feature**: 17hats has no built-in way to add the processing fee to the client's total; members who want this add a manual line item. (Users work around ACH-vs-card costs by toggling methods account-wide — another complaint.)
- **Fees in bookkeeping:** a 2025-era help article covers how Stripe processing fees are represented in 17hats Bookkeeping (fees recorded so income nets correctly) — build takeaway: record gross payment + fee expense automatically.

### 5.3 Payment methods summary

- **Cards:** Visa, Mastercard, Discover, American Express (all members on 17hats Payments).
- **ACH/eCheck:** US members only; multi-day clearing — the payment-confirmation email to the client is held until the ACH clears; funds transfer historically ~7 business days via Stripe ACH.
- **Digital wallets:** **Apple Pay** and **Google Pay**, enabled by a single checkbox — Account Settings → Invoice Options → "Accept digital wallets (Apple Pay and Google Pay)". One-click pay using wallet-stored cards. Requires 17hats Payments.
- **Saved cards:** "Save Card Data" invoice option (Stripe or Square); card stored at processor, reusable on future invoices; member can also **charge a saved card on the client's behalf** ("Pay Invoices on Behalf of Your Clients").
- **Manual/offline:** cash, check, or anything else via **Record Payment** (amount, date, method, reference/check #, deposit account, optional emailed receipt).
- **Not found / unverified:** Klarna/Affirm/BNPL, Link by Stripe, wire, Venmo, in-person card readers/terminal, Stripe Radar controls, multi-party splits — no documentation surfaced; assume unsupported.

### 5.4 Tipping / gratuity

- "Tip Amount" can be enabled on **Quotes, Invoices, and Online Payments** — aimed at verticals like hair care and massage.
- Requires **17hats Payments** (feature shipped for Stripe and Square per release notes; current docs say 17hats Payments connection needed).
- Toggle per invoice via Invoice Options; **auto-enabled on all new Quotes** (must be manually enabled on pre-existing templates); can be on for some invoices, off for others.
- Constraint: **tip cannot exceed the total value of the associated invoice**.
- *(unverified)* Preset tip percentages vs. free-form amount on the payment page.

### 5.5 Payouts & payment reporting

- **Payout timing:** card funds deposit in **1–2 business days** (Stripe standard); first-ever payout delayed 7–14 days; ACH slower (~7 business days historically). *(No evidence of 17hats-specific instant payout or next-day guarantee.)*
- **Bank reconciliation:** processor deposits appearing in the connected bank feed should be categorized as **"Transfer between accounts"** to avoid double-counting income (income was already recognized when the payment hit the invoice).
- **Reports** (Bookkeeping tab dropdown; all print/CSV-exportable): **Profit & Loss** (income auto-populates as invoices are paid; PDF export), **Sales Tax Report**, **Upcoming Receivables**, **Aged Receivables**, **Client Sales**, **Product Sales**. Dashboard shows past-due money owed.
- **QuickBooks Online sync** (US/CA/UK): sent (non-draft) invoices sync automatically, payments applied sync too; requires "Custom Transaction Numbers" enabled in QBO so invoice numbers match; expenses do NOT sync.
- Payment management UI: "How do I manage my payments?" — invoice-level payment list with per-payment actions (refund, receipt); transactions searchable in Bookkeeping by account, category, type, date range, amount, keyword.

---

## 6. Reminders, late fees, receipts, refunds

### 6.1 Automatic payment reminders

- Configured in **Account Settings → Email Settings → Email Reminders** (per document type: Quote, Contract, Invoice, Questionnaire).
- Defaults: reminder **1 day before due date**, and **monthly** for past-due invoices.
- Configurable knobs: days-before for upcoming reminder; days-after for first past-due reminder; past-due cadence **daily, weekly, or monthly**; custom **subject line and message body with tokens** (document-related merge fields).
- Reminders **auto-stop** when the invoice is brought into good standing / paid in full; email includes a **direct link to pay online**.
- Conditions: document must have a **due date**, and must belong to an **Active Project**.
- Recurring/auto-payment confirmations are separate automatic emails (global toggle per document type under "Automatic Confirmation Emails").

### 6.2 Late fees

- **No native late-fee feature.** No help article exists; a 17hats user-group thread asks whether it's been added. Members improvise (manual line item for the fee, or wording in contract + reminder cadence). This is a clear build opportunity.

### 6.3 Receipts

- **Online payments:** receipt email is sent to the client **automatically** on successful payment; for **ACH**, the confirmation email is withheld **until the payment clears**.
- **Auto-charges:** confirmation email per automatic payment (recurring or scheduled installment).
- **Manual payments:** optional "send receipt" checkbox when recording a payment; there's also a standalone "How do I send an invoice receipt?" flow to (re)send a receipt on demand.

### 6.4 Refunds & voiding

- **In-app refunds** (newer capability, help article "Processing Refunds inside 17hats", article ID suggests 2025+):
  - **Refund button** at top of invoice → refunds the **full amount** (across multiple payments).
  - Per-payment **"refund" link** at the bottom of the invoice → partial refund / refund a single payment.
  - During refund you may optionally **void the invoice** and/or **send a customizable refund email** to the client.
- **Legacy/manual approach** ("How do I issue a refund to my client?"): refund at the processor, then Record Payment with a **negative amount** to zero the books.
- **Voiding** (Edit → Void Invoice): stops invoice from showing due (e.g., cancelled service, returned deposit). Caveats: payments on a voided invoice remain in Bookkeeping income; payments can't be removed post-void.
- **Deleting:** invoices can be deleted; their numbers are never reused. *(inferred from numbering doc)*
- **Chargebacks/disputes:** no 17hats-specific handling documented; handled at Stripe level (funds + dispute fee pulled; standard Stripe evidence flow). *(unverified whether 17hats surfaces disputes in-app.)*

---

## 7. Client-side payment UX

### 7.1 Paying an invoice

1. Client receives invoice email (or reminder) with a **secure link** — no client login required *(inferred; consistent with 17hats document links)*; invoices are also accessible in the optional **Client Portal** (portal shows Quotes, Contracts, Invoices, Questionnaires; customizable welcome message with text/links/images).
2. Online payment page shows the branded invoice; client picks method: **card**, **ACH (US)**, or **one-click Apple Pay / Google Pay** if enabled.
3. Optional checkboxes at payment: **"Save my card"** and **"Charge automatically"** (only shown when member enabled those invoice options). Both must be checked for auto-pay of future installments/recurrences.
4. **Tip prompt** shown when tipping enabled (capped at invoice total).
5. Payment applies instantly; invoice stamps **Paid** at zero balance; client gets an automatic receipt (ACH receipt deferred until cleared).
- With a **payment schedule**, the client pays only the installment(s) currently due; *(unverified)* whether the client may voluntarily prepay future installments or overpay/partial-pay an installment — no doc found; partial payments otherwise happen via member-recorded payments or schedules.
- Members can also take payment **on the client's behalf** against a saved card (phone orders etc.).

### 7.2 3-in-1 booking flow (see §2.8)

Quote (select options/quantities) → accept → contract unlock + e-sign → invoice auto-updated with selections → pay (optionally just the first scheduled payment = retainer). This single-link "book me" flow is the conversion centerpiece.

### 7.3 Pay Upon Booking (Online Scheduling)

- When a client books a service through 17hats Online Scheduling, they enter contact + payment info in the booking flow.
- Member configures **full payment** or **partial payment** (fixed $ or % upfront), remainder later/day-of.
- An **invoice is auto-created** and appears in the contact's Project, Client Portal, Documents tab, and activity feed. Processing via Stripe/17hats Payments. Reduces no-shows.

---

## 8. Inferred data model (schema sketch)

Reverse-engineered from observed behavior — a plausible schema for a competing build:

```
Brand
  id, name, logo, fonts, colors, currency (ISO code, one per brand),
  merchant_account_id (one active per brand)

MerchantAccount
  id, brand_id, provider (seventeenhats_payments|stripe_legacy|square_legacy),
  provider_account_ref, kyc_status, capabilities {cards, ach, wallets}

TaxRate
  id, account_id, name, rate_percent

ProductService (catalog item)
  id, internal_name, display_name, description, price, default_quantity,
  income_category_id, taxable (bool), default_tax_rate_id, image_url,
  type (standard|package), package_contents[], hours, headcount

Invoice
  id, brand_id, contact_id, project_id, template_id?, quote_id? (source),
  number (unique, auto-increment, immutable after save),
  internal_title, display_title, po_number, notes,
  issue_date, due_date, currency,
  status (draft|sent|partially_paid|paid|overdue*|void)   [*overdue = derived]
  discount {type: fixed|percent, value}          // invoice-level only
  tax_rate_id (default for taxable lines),
  tipping_enabled, online_payments_enabled,
  save_card_enabled, auto_charge_enabled,
  recurring_schedule_id?, payment_schedule_id?,
  totals {subtotal, discount_amt, tax_amt, tip_amt, total, balance}

InvoiceLineItem
  id, invoice_id, position, name, description, image_url,
  quantity, unit_price, taxable, tax_rate_id, income_category_id,
  source_item_type (standard|choose_one|choose_any),
  client_editable_quantity (bool), amount   // negative allowed (ad-hoc discounts)

PaymentSchedule
  id, invoice_id, mode (equal|custom), max 12 installments
  Installment: {position, amount | percent, due_rule
                (on_date d | upon_receipt | relative {n, unit, before|after, anchor=project_date}),
                status (pending|due|paid|overdue), paid_payment_id?}

RecurringSchedule
  id, invoice_template_ref, frequency (weekly|monthly|yearly),
  occurrences_total, occurrences_sent, next_run_at (send ~due date, charge ~10:00 local),
  auto_charge (bool)

Payment
  id, invoice_id, installment_id?, amount (negative = manual refund entry),
  method (card|ach|apple_pay|google_pay|cash|check|other),
  date, reference, deposit_account_id, processor_charge_ref,
  status (pending_clearing|cleared|failed|refunded|partially_refunded),
  tip_amount, fee_amount (processor fee for bookkeeping),
  receipt_sent (bool)

Refund
  id, payment_id?|invoice_id (full), amount, processor_refund_ref,
  void_invoice (bool), notify_email_sent (bool), created_at

SavedPaymentMethod                    // stored AT the processor, token only
  id, contact_id, merchant_account_id, processor_customer_ref,
  processor_pm_ref, auto_charge_consent (bool, per invoice/recurrence)

ReminderPolicy (per document type)
  days_before_due, first_past_due_offset_days,
  past_due_cadence (daily|weekly|monthly),
  subject_template, body_template (token merge),
  active_condition: project.active && due_date != null

Reports: P&L, SalesTax, UpcomingReceivables, AgedReceivables,
         ClientSales, ProductSales  (all CSV/PDF export)
```

Key invariants worth copying:
- Invoice numbers: unique forever, sequential, immutable after save.
- Card tokens live at the processor → switching processors invalidates saved cards (design your vault to avoid this: use your own PSP-agnostic vault or accept the constraint knowingly).
- Void ≠ refund: voiding freezes the document but leaves recognized income intact.
- Reminder engine keys off (due_date, balance>0, project active) and self-terminates on payment.
- ACH receipts/confirmations are deferred until settlement.

---

## 9. Strengths / weaknesses

### Strengths (worth emulating)

1. **3-in-1 quote/contract/invoice** — select, sign, pay in one link; client choices auto-update the invoice. Consistently praised as the "book me faster" killer feature.
2. **Payment schedules with project-date-relative due dates** ("50% two months before the wedding") — perfectly tuned to event-based solopreneurs; up to 12 installments, equal or custom.
3. **Auto-charge opt-in UX** — two clear client checkboxes (save card / charge automatically) covering both recurring invoices and scheduled installments.
4. **Set-and-forget reminders** — sensible defaults (1 day before; monthly past-due), token-customizable, auto-stop on payment, pay-link embedded.
5. **Deep automation hooks** — invoices auto-created/sent from lead capture forms, workflows, and online scheduling with pay-upon-booking (full/partial).
6. **Frictionless client payment** — no portal login required to pay, digital wallets one-click, receipts automatic.
7. **Tight bookkeeping loop** — payments auto-categorized; fee accounting; sales tax + receivables reports; QBO sync.
8. **Single all-inclusive plan** (2025+) removed feature-gating confusion (previously payment schedules etc. were mid-tier+ only).

### Weaknesses / user complaints (opportunities)

1. **Processor lock-in & rigidity:** one merchant account at a time, account-wide (not per client/invoice); can't run Stripe + PayPal together; new accounts forced onto 17hats Payments. Switching processors silently breaks saved-card auto-charges (clients must re-enter cards) — documented footgun.
2. **No native late fees** — users have asked; still absent.
3. **No fee pass-through / surcharging / convenience-fee option**; ACH-vs-card toggles are site-wide, so members who want to steer clients to cheap ACH must disable cards for everyone.
4. **Bookkeeping/reporting depth is weak:** e.g., no full-year P&L with monthly breakdown in one view (must run month-by-month); "better than nothing" sentiment; scaling businesses outgrow it.
5. **Recurring billing is shallow:** fixed duplicate invoices only — no proration, plan changes, indefinite subscriptions documentation, or dunning/smart-retry story found.
6. **Single currency per brand;** multi-currency requires paying for linked brands.
7. **Void semantics confuse users** (payments survive voiding and can't be detached).
8. **Discounting is invoice-level only** — per-line discounts require hacks (negative line items).
9. Historic tier-gating and add-on nickel-and-diming (extra users, brands, bank connections) generated pricing complaints pre-2025.
10. ACH markup (cap $6.50 vs Stripe's raw $5 cap) — mild, but a competitor can undercut or be transparent about it.

---

## 10. Build recommendations

### Copy (table stakes / proven)

- 3-in-1 proposal → e-sign → invoice → pay flow with client-selectable options that re-price the invoice live.
- Payment schedules: ≤N installments, equal-split helper + custom amounts (% or $), due dates absolute/on-receipt/**relative to an event date**; per-installment reminders and auto-charge.
- Recurring invoices with client opt-in save-card + auto-charge; charge at a predictable local time; confirmation email per charge.
- Reminder engine with 17hats' exact defaults (1 day before due; configurable past-due cadence daily/weekly/monthly; token-based templates; auto-stop; embedded pay link).
- Auto receipts (defer ACH confirmations until cleared), manual Record Payment (cash/check/other with reference + deposit account + optional receipt).
- Products & Services catalog with internal vs display names, packages, images, income categories, per-item taxable flags; named tax rates + sales tax report.
- Immutable sequential invoice numbers; branded documents; invoice templates.
- In-app refunds: full-invoice button + per-payment partial refunds, optional void + notify email.
- Digital wallets (Apple/Google Pay) behind a single toggle; tipping toggle per invoice with tip ≤ invoice total; pay-upon-booking (full/partial) for scheduling.
- Receivables reports (upcoming + aged), client/product sales, QBO sync (respect the custom-transaction-numbers trick).

### Improve (differentiators against 17hats)

- **Native late fees**: % or flat, grace period, auto-apply + notify — direct answer to an unmet ask.
- **Fee steering / pass-through**: per-invoice payment-method control, optional surcharge/convenience fee (with state-law guardrails), "ACH discount" framing.
- **Processor-agnostic card vault** (or network tokens) so changing PSPs never strands saved cards — fixes 17hats' documented migration footgun.
- **Real subscription engine**: indefinite recurrences, pause/skip, proration, dunning with smart retries and failed-payment emails — 17hats has none of this.
- **Per-line discounts** and both tax-inclusive/exclusive pricing; compound/multiple taxes per line for CA/EU markets.
- **Multi-currency without paywalled brands**; at minimum per-client currency.
- **Clearer void/refund semantics** (void reverses receivable; refunds create explicit contra-entries; immutable audit trail).
- **Full-range financial reports** (any date range, monthly columns in one P&L) — loudly requested by 17hats users.
- Client-side **partial prepayment** ("pay ahead" on schedules) and pay-what's-due clarity.
- Surface **disputes/chargebacks** in-app instead of punting to the Stripe dashboard.

### Skip / deprioritize

- Supporting 4+ external processors (17hats retreated from PayPal/Authorize.net to a single Stripe-powered offering for good reasons: consistent features, wallets, tipping). One PSP + great UX beats processor breadth; consider Square only if in-person is a target.
- Building a full bookkeeping suite at launch — 17hats' own is its weakest pillar; ship invoicing/payments + QBO/Xero sync first.
- Complex approval chains, multi-entity AR, inventory — out of scope for the solopreneur ICP.

---

## 11. Sources

17hats Help Center (content obtained via search extraction; fetch was proxy-blocked):

- https://help.17hats.com/en/articles/849340-17hats-invoicing-bookkeeping
- https://help.17hats.com/en/articles/924380-money-matters-invoice-options
- https://help.17hats.com/en/articles/3116849-invoice-settings
- https://help.17hats.com/en/articles/950108-invoice-templates
- https://help.17hats.com/en/articles/3116928-quote-invoice-line-item-settings
- https://help.17hats.com/en/articles/849333-money-matters-products-services-page
- https://help.17hats.com/en/articles/4120797-products-and-services-internal-and-display-names
- https://help.17hats.com/en/articles/6192166-adding-images-to-invoices-and-quotes
- https://help.17hats.com/en/articles/2673313-money-matters-tax-settings-page
- https://help.17hats.com/en/articles/924623-sales-tax-report
- https://help.17hats.com/en/articles/2548662-scheduled-payments
- https://help.17hats.com/en/articles/1072575-recurring-invoices-vs-payment-schedules
- https://help.17hats.com/en/articles/5052370-automatic-payments-for-payment-schedules
- https://help.17hats.com/en/articles/2508194-how-to-setting-up-recurring-invoices
- https://help.17hats.com/en/articles/4260937-invoice-options-recurring-billing-automatic-payments
- https://help.17hats.com/en/articles/4530767-invoice-options-save-card-data
- https://help.17hats.com/en/articles/1331543-pay-invoices-on-behalf-of-your-clients
- https://help.17hats.com/en/articles/6418020-stripe-payments
- https://help.17hats.com/en/articles/3162740-legacy-using-stripe-for-online-payments
- https://help.17hats.com/en/articles/843846-accept-ach-payments-through-17hats
- https://help.17hats.com/en/articles/11498904-credit-card-and-ach-processing-fees-in-17hats-bookkeeping-with-stripe
- https://help.17hats.com/en/articles/6759842-enable-apple-pay-using-17hats-payments
- https://help.17hats.com/en/articles/6759877-enable-google-pay-using-17hats-payments
- https://help.17hats.com/en/articles/3591193-tipping
- https://help.17hats.com/en/articles/879792-how-do-i-set-automatic-invoice-reminders
- https://help.17hats.com/en/articles/2280471-email-settings-document-email-reminders
- https://help.17hats.com/en/articles/1967185-automatic-confirmation-emails-that-send-from-17hats
- https://help.17hats.com/en/articles/928591-how-do-i-send-an-invoice-receipt
- https://help.17hats.com/en/articles/897500-how-do-i-issue-a-refund-to-my-client
- https://help.17hats.com/en/articles/12649453-processing-refunds-inside-17hats
- https://help.17hats.com/en/articles/3967282-how-to-void-a-document
- https://help.17hats.com/en/articles/924616-how-do-i-record-a-payment-manually
- https://help.17hats.com/en/articles/924368-how-do-i-manage-my-payments
- https://help.17hats.com/en/articles/924622-how-do-i-categorize-payments-deposited-into-my-bank
- https://help.17hats.com/en/articles/924358-combined-documents
- https://help.17hats.com/en/articles/2198457-send-automated-invoices-using-lead-capture-forms-and-workflows
- https://help.17hats.com/en/articles/3980157-online-scheduling-payments
- https://help.17hats.com/en/articles/927251-what-currencies-does-17hats-support
- https://help.17hats.com/en/articles/3112838-bookkeeping-overview
- https://help.17hats.com/en/articles/924603-what-is-the-profit-and-loss-report-in-17hats
- https://help.17hats.com/en/articles/859661-17hats-quickbooks-online-integration
- https://help.17hats.com/en/collections/550596-online-payment-options
- https://help.17hats.com/en/collections/550672-invoices

17hats marketing / other first-party:

- https://www.17hats.com/features/invoices
- https://www.17hats.com/features/online-payments
- https://www.17hats.com/features/payment-schedule
- https://www.17hats.com/features/recurring-billing • /features/recurring-invoices
- https://www.17hats.com/features/quote-contract-invoice
- https://www.17hats.com/features/tipping
- https://www.17hats.com/features/document-reminders
- https://www.17hats.com/features/sales-tax-reporting • /features/profit-loss-report
- https://www.17hats.com/features/online-scheduling-payments
- https://www.17hats.com/integration/17hats-payments • /integration/stripe • /integration/quickbooks
- https://www.17hats.com/pricing
- https://blog.17hats.com/tipping/ • https://blog.17hats.com/online-schedule-payments/ • https://blog.17hats.com/simplify-invoicing-with-17hats-invoice-email-reminders/
- https://17hats.releasenotes.io/release/qdYrP-tipping-is-now-available-on-square-and-stripe
- https://www.17hatsuniversity.com/17hats-quick-tips/recurring-invoices-with-automatic-payments-in-17hats
- https://www.17hatsuniversity.com/17hats-quick-tips/the-bookkeeping-tab-in-17hats

Third-party (fees, pricing history, complaints):

- https://www.capterra.com/p/144328/17hats/reviews/ (and page 2)
- https://www.g2.com/products/17hats/reviews
- https://sprucerd.com/blog/17hats/ (processor/global-settings complaints)
- https://onesuite.io/blog/17hats-pricing/ • https://taskip.net/17hats-pricing/ • https://getzendo.io/blog/17hats-pricing/ • https://www.agencyhandy.com/17hats-pricing/ (2025 single-plan repricing; legacy tiers)
- https://squareup.com/help/us/en/article/6171-17hats-and-square • https://squareup.com/us/en/payments/our-fees (Square rates)
- https://www.letnicolehelp.com/post/automated-invoice-reminders-17hats
- https://www.facebook.com/groups/17HatsUserQA/ (late-fee ask; QBO accuracy thread)

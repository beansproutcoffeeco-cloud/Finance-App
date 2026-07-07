# 17hats: Bookkeeping & Financial Reporting

Research date: 2026-07-07. Sources: help.17hats.com articles (via search extraction — the 17hats domains were not directly fetchable from this environment, so article contents were captured through search-engine snippets/summaries; exact UI wording may vary slightly), 17hats.com feature/integration pages, 17hats blog, 17hats University tutorials, Capterra/G2/Software Advice reviews, and third-party comparisons (Fondo, agencyhandy, taskip, apps4rent). Uncertainty is flagged inline.

---

## 1. Summary

- 17hats bookkeeping is a **single-entry, cash-basis, business-only ledger** bolted onto an invoicing/CRM product — not real accounting software, and 17hats' own docs and reviewers consistently describe it as "basic bookkeeping."
- Core loop: connect bank/credit-card accounts (paid **$5/mo add-on**, ~22,000 institutions, reads transactions only) → transactions land in a **Bookkeeping tab** → user assigns a **category** (with learning auto-suggestions) → user clicks **Verify** → only verified transactions appear on reports.
- Income is largely **automatic**: when a client pays a 17hats invoice (online or manually recorded), a bookkeeping income transaction is auto-created, auto-categorized (from the invoice line item's assigned Income Category), and auto-verified — plus a separate sales-tax transaction and (with Stripe/17hats Payments) a merchant-fee expense transaction.
- Bank-feed **deposits of those same payments are deliberately NOT auto-matched**; the documented practice is to manually categorize deposits as "Transfer between accounts" to avoid double-counting. A manual "Apply to an invoice" flow exists only for exact-amount, not-yet-recorded payments.
- Reports: **Profit & Loss (cash basis), Sales Tax, Upcoming Receivables, Aged Receivables, Client Sales, Product Sales, Lead Source, Time Tracking** — all printable/CSV-exportable. No balance sheet, no cash-flow statement, no reconciliation, no quarterly tax estimation, no Schedule C mapping.
- **No** double-entry ledger, chart of accounts (flat category list only), transaction splits, bank reconciliation, receipt OCR, mileage tracking, recurring expense automation, or multi-currency accounting.
- QuickBooks Online integration is **one-way and sales-side only**: invoices + payments push to QBO (payments to Undeposited Funds); **expenses/bookkeeping do not sync** — users who need real accounting run QBO in parallel. A QuickBooks Desktop path exists via transaction export (gear icon → Export Transactions).
- The aggregator behind bank sync is **not publicly named** (docs say only "our bank sync partners"; the 22,000-institution claim suggests Yodlee/Finicity-scale coverage rather than Plaid, but this is unconfirmed).
- Biggest user complaints: fragile bank connections that require manual refresh/re-auth, losing all categorized history if an account is disconnected, no receipt-photo capture on mobile at least historically, no recurring-expense automation, and reports too shallow for a tax preparer — many users "outgrow" it and move to QBO/Xero/Wave.

---

## 2. Bank connections & transaction sync

### Module & pricing
- Bank Connections is a **paid add-on: $5.00/month** on top of the base subscription (base plan was tiered — bookkeeping in Standard/Premier only — and is now a single all-inclusive plan ~$60/mo, $600/yr, with add-ons still billed separately). ([help: Money Matters – Connecting Your Bank Account], [17hats.com/pricing], [agencyhandy/taskip pricing reviews])
- Marketing claims integrations with **~22,000 financial institutions**; named examples: Bank of America, Citibank, Wells Fargo, Capital One, Chase, Key Bank (Key Bank has its own dedicated connect article). ([17hats.com/integration/banks])

### Aggregator
- **Not publicly disclosed.** Help articles refer only to "our bank sync partners" (plural) who file tickets with banks when connections break. No official mention of Plaid, Yodlee/Envestnet, MX, or Finicity was found in help docs, privacy pages surfaced by search, or reviews. The 22,000-institution figure is larger than Plaid's usual (~12k) marketing number and closer to Yodlee-class screen-scraping coverage — but treat the vendor as **unknown/unconfirmed**.

### Connection flow
1. Account Settings → **Bookkeeping Options** → "Connect Account" button.
2. Redirect to a search page to find your institution among the supported list; enter online-banking credentials in the aggregator widget.
3. On success, **the past 90 days of transactions import** automatically; new transactions flow in on an ongoing basis and appear on the main Bookkeeping page.
- Supports **bank accounts and credit card accounts**. Multiple accounts can be connected (each is filterable in the transaction list).
- Connection is **read-only** ("restricted connection… we can only read transaction history"); 17hats states it never stores or views account numbers or passwords.

### Sync behavior & reliability
- Sync is automatic but **frequency is not documented** (no "updates every X hours" statement found). There is a **"REFRESH ACCOUNT" (manual refresh)** button; users may be re-prompted for credentials on refresh. Help notes "all banks now require occasional manual refreshes as a security measure."
- **MFA-heavy banks never auto-update**: accounts requiring a texted code "cannot be automated" — only manual refresh pulls recent transactions.
- When a bank changes its interface, the documented remedy is to email support@17hats.com so 17hats' "bank sync partners" repair the connection — i.e., no self-serve fix.
- **Critical data-loss footgun (documented)**: "What Happens If I Disconnect My Synced Bank Account?" — disconnecting **removes ALL transactions for that account, including categorized/verified ones**. Help explicitly warns against the common "disconnect and reconnect" troubleshooting move because it destroys past work.

### Manual/file import
- **Importing Older Bank Transactions**: Bookkeeping page → small **cog/gear icon → "Import Transactions"** → choose target account → choose file. Used both for history older than the 90-day initial pull and as the fallback when a feed is broken.
- Documented formats: bank-exported **QBO or OFX** files (the help article tells users to export older transactions from their bank "to a QBO or OFX format file"). CSV import support is **uncertain** — search snippets did not conclusively show CSV accepted by 17hats' importer (unlike Wave/QBO). Assume OFX/QBO/QFX-family; verify before relying on CSV parity claims.
- Manual single-entry: **"New Expense"** button on the Bookkeeping page — fields: **Description, Amount, Date, Account, Category, Project** → OK. (Note the Project link — expenses can be tied to a client project, feeding the project's Financials view.)

---

## 3. Categorization (taxonomy, rules, splits, review flow)

### Taxonomy / "Chart of Accounts"
- There is **no chart of accounts** in the accounting sense — no account types (asset/liability/equity), no account numbers, no hierarchy documented. It is a **flat list of transaction categories** split by direction:
  - **Income categories** (assignable to invoice line items / Products & Services).
  - **Expense categories**.
  - Built-in/special semantics observed in docs: **"Transfer between accounts"** (excluded from P&L; used for deposits already counted as invoice payments and for credit-card payments), **"Merchant Fee"** (auto-used for processing fees, reported under **Cost of Goods Sold** on the P&L — the only COGS-ish behavior found), and **Sales Tax** (auto-created transaction rows when taxable invoices are paid).
- Accounts come **pre-populated with "basic categories"** which are editable; the exact default list is not published anywhere findable (it's only visible in-app at Account Settings → Bookkeeping Options). *Uncertain: full default category list.*
- **Custom categories**: Account Settings → Bookkeeping Options → **"Add Category"**; used e.g. to create a custom income category for itemized discounts.

### Auto-suggestions (the "rules engine")
- "How Do Category Auto-Suggestions Work?": when transactions arrive from a bank feed or import, 17hats **suggests a category per transaction**.
  - **Initial suggestions come from the bank's own transaction data** ("initial suggestions depend on your bank institutions" — i.e., aggregator-provided category/merchant metadata).
  - **The system learns from your manual categorizations** and improves suggestions over time (per-user learned merchant→category mapping).
- **No user-defined rules** (no "if description contains X then category Y" rule builder) were found in docs or reviews — the only automation is the learned suggestions. This is a notable gap vs. QBO/Wave bank rules.

### Splits
- **No split-transaction feature found.** No help article documents dividing one bank transaction across multiple categories; the docs actually steer users *away* from needing splits — batch merchant deposits are handled by categorizing the whole deposit as "Transfer between accounts" (since per-invoice income was already recorded), "eliminating the work of having to split the deposit." Reviewers list absence of splits/robust editing among reasons the module is "basic." *Confidence: high that splits are absent, but based on absence of evidence.*

### Review flow (categorize → verify)
- The Bookkeeping tab lists all transactions with **filters: account, category, type (income vs. outgoing/expense), date range, amount, keyword search**.
- Per row: click **"Select a category"** dropdown → scroll or type-search categories → pick one.
- **Verification is a distinct state**: a transaction only hits the P&L (and other reports) when it **has a category AND has been Verified** (Verify button). Docs suggest a speed workflow: categorize many rows, then click Verify once to confirm all selections (bulk verify).
- Rows have a dropdown arrow (right of Amount) exposing actions: **Apply to an invoice**, **Add receipt**, (and edit/delete for manual entries).
- Transactions created by 17hats itself (invoice payments, merchant fees) arrive **already categorized and verified** — no review needed.

---

## 4. Invoice/payment matching & business income tracking

### Automatic income recording (the core differentiator)
- 17hats is invoice-centric: **income enters bookkeeping via invoices, not via the bank feed.**
- When a payment is received on an invoice — online (17hats Payments/Stripe/Square/PayPal) or recorded manually — 17hats **auto-creates a bookkeeping income transaction, categorized and verified**, dated on the payment date (cash basis: payment date = bookkeeping record date).
- Categorization source: each **invoice line item / Product & Service carries an assigned Income Category** (set in Products & Services, tied to categories in Bookkeeping Options). On partial or full payment, the module creates **a transaction for the sale based on the line item's income category, plus a separate sales-tax transaction when applicable**. This gives per-category income on the P&L without any bank-feed work.
- With Stripe/17hats Payments connected, **credit-card and ACH processing fees appear as their own line items** in Bookkeeping, auto-categorized as **Merchant Fee** under Cost of Goods Sold and auto-deducted from Total Income. (17hats Payments pricing: 2.9% + $0.30 cards; ACH 0.80% + $1.50 capped at $6.50.)
- Refunds: refunding a payment (full/partial, Stripe/Square or manual) flows back into bookkeeping; processor keeps its fee and a **negative expense** shows under the project's Financials. Alternative flows: record a negative payment on the invoice, or void the invoice.

### Bank-deposit handling — matching is manual and limited
- Because income was already recorded at payment time, the **bank-feed deposit of that same money is a duplicate**. 17hats' documented practice: categorize such deposits as **"Transfer between accounts"** so revenue isn't counted twice. This includes **batch merchant deposits** (a single Stripe/Square payout covering several sales minus fees) — the whole payout is marked as a transfer.
- **"Apply to an invoice"** exists for the opposite case — a deposit arrives for a payment that was **never recorded**: only when the **deposit amount exactly equals the invoice payment amount** AND no payment is recorded yet, click the row's arrow → "Apply to an invoice" → popup → "Assign to payment" dropdown → pick the invoice payment. This records the payment and links the transaction.
- There is **no automatic matching engine** (no fuzzy amount/date matching, no suggested matches like QBO's "match" tab, no payout-splitting of batch deposits into constituent payments). Matching correctness rests entirely on user discipline with the "Transfer between accounts" convention — a frequent point of confusion (double-counted income) in user Q&A groups.

### Receivables tracking
- Because invoices live in-app, 17hats can report **Upcoming Receivables** (balances coming due, bucketed 0–30/30–60/60–90/90+ days) and **Aged Receivables** (overdue balances, same bucketing), both under Bookkeeping → Reports.

---

## 5. Expenses, receipts, mileage, sales tax

### Expense tracking
- Two ingestion paths: **bank/credit-card feed** (then categorize + verify) or **manual "New Expense"** (Description, Amount, Date, Account, Category, Project).
- Expenses can be **linked to a Project**, surfacing in the project's Financials alongside income — lightweight job costing.
- **No recurring-expense automation** (a repeated Capterra complaint: "cannot automate recurring monthly/annual expenses").
- **No vendor/payee entity**, no bills/accounts-payable, no purchase orders — none documented anywhere.

### Receipts
- **Receipt attachment exists** (contrary to some older reviews): on any Bookkeeping transaction, dropdown arrow → **"Add receipt"** → upload one or **multiple files, each up to 75 MB**; view later via the built-in Image & PDF viewer, with download/delete. (17hats University: "How To Add a Receipt in 17hats".)
- **No OCR / receipt-scan-to-transaction creation**, no email-in receipt inbox, and reviewers report no mobile receipt-photo capture flow (older reviews explicitly complained about the lack; the "Add receipt" upload appears to be a later addition). *Uncertain: current mobile-app receipt capabilities.*

### Mileage
- **No mileage tracking feature.** Nothing in help docs, feature pages, or reviews. (Contrast: QuickBooks Self-Employed/Solopreneur auto-tracks mileage — a gap 17hats users who need Schedule C mileage must fill elsewhere.)

### Sales tax
- **Tax Settings page** (Account Settings → Tax Settings): create **multiple named tax rates**. On a Quote/Invoice, select the applicable rate(s) in the **document header**, then mark each **line item** as taxable at a specific rate; taxable amounts compute per line. Products & Services items can be saved as taxable so settings auto-fill once a header rate is chosen.
- Docs advise **never editing an existing rate** when rates change — create a new rate so historical invoices/bookkeeping stay intact (rates are referenced, not snapshotted; *inference from that advice*).
- When a taxed invoice is paid, a **sales-tax bookkeeping transaction** is created automatically (separating tax collected from income).
- **Sales Tax Report** (Bookkeeping → Reports → Sales Tax): totals sales and tax collected **per rate**, over a calendar/quick-select timeframe (defaults to "Last Month"; quarterly periods selectable manually). Exportable as CSV. Cash basis.
- No jurisdiction/nexus logic, no filing integration, no tax-agency remittance tracking — it's a collected-tax summary only.

---

## 6. Reports (what exists and what doesn't)

All reports: Bookkeeping tab → **"Reports"** button (top right). Every report can be **printed or exported as CSV**.

### Exists
| Report | Contents / notes |
|---|---|
| **Profit & Loss** | Cash-basis. Income (auto from invoice payments) and verified expenses grouped **by category**; Merchant Fees under Cost of Goods Sold deducted from Total Income; bottom line = net profit/loss. Custom date range (start/end + Apply) and quick-select periods. **"Show Transactions"** toggle expands per-category transaction detail; CSV export includes transactions only if shown. Only categorized+verified transactions appear. |
| **Sales Tax** | Total sales + tax collected per configured rate, per timeframe; CSV export (export feature shipped ~2024 per release notes). |
| **Upcoming Receivables** | Invoice balances coming due, bucketed 0-30/30-60/60-90/90+ days from report date. |
| **Aged Receivables** | Overdue invoice balances, same bucketing. |
| **Client Sales** | Per client for a timeframe: sum of invoices, number of invoices, average sale. |
| **Product Sales** | Same idea per product/service; CSV export. |
| **Lead Source** | Payments on invoices for projects with a Lead Source; bar chart + detail rows (lead name, converted?, income). Marketing ROI, not accounting. |
| **Time Tracking** | Hours per project (billable/non-billable, hourly rates) vs. earnings. |

### Does NOT exist (verified absences / strong inferences)
- **Balance Sheet** — impossible without double-entry; not offered.
- **Cash-flow statement** — not offered.
- **Bank reconciliation** (statement-vs-ledger tick-off) — not offered; "Verify" is the only control.
- **Quarterly estimated-tax calculator / tax-savings set-aside** — nothing found (QuickBooks Solopreneur, Hurdlr, Keeper all do this; 17hats does not).
- **Schedule C category mapping or tax-line tagging** — not offered.
- **1099 tracking / contractor payments** — not offered.
- **Accrual basis option** — cash basis only, by design.
- **Budgets / budget-vs-actual** — not offered.
- **Multi-currency bookkeeping** — not documented; invoicing is effectively single-currency per account.
- **Comparative P&L (vs. prior year/period) built-in** — not documented; users export CSV and compare in Excel. *Uncertain but likely absent.*
- **Year-end**: no closing process. The 17hats blog's "End-of-Year Bookkeeping Checklist" is procedural: confirm all accounts connected & syncing, verify/categorize everything, run P&L + Sales Tax reports, export CSVs for the tax preparer. That is the entire tax-time story.

---

## 7. Accounting integrations (QuickBooks etc.)

### QuickBooks Online (native, one-way, sales-side)
- Setup: Account Settings → Integrations → "Connect to QuickBooks" (OAuth). Available **US, Canada, UK only**.
- **What syncs (17hats → QBO):**
  - **Invoices** — auto-synced once sent/marked-sent (**drafts never sync**); bulk "select all → Sync" for backfilling existing invoices.
  - **Payments** on those invoices — sync automatically; land in **Undeposited Funds** by default (so the user can match batch bank deposits inside QBO for reconciliation).
  - **Contacts and Products/Services** are created in QBO as needed by invoice sync.
- **What does NOT sync:** **expenses / bookkeeping transactions** (explicitly: "banking and bookkeeping should still be handled directly within QuickBooks Online"), credit memos/refund nuance, and nothing flows QBO → 17hats (one-way).
- **Constraints / gotchas (documented):**
  - Must enable **"Custom Transaction Numbers"** in QBO so invoice numbers match.
  - Invoice numbers & payment reference numbers must be **≤ 21 chars** to be stored in full.
  - **Products & Services must have unique Display Names** (duplicates merge into one QBO item).
  - **Contacts must have unique names** for QBO (17hats disambiguates by email; QBO can't).
  - **Tax rates must be identically named** in both systems or QBO sales-tax reports will be wrong.
- **User-reported problems:** sync errors creating **double payment records** (one reviewer left over this); duplicate invoices with no way to change/replace an invoice number; general fragility per Facebook user-group threads.

### QuickBooks Desktop
- No live integration. **Export path**: Bookkeeping page → gear icon → **"Export Transactions"** → pick start/end date → download → import into QBD. Export format not clearly documented — a user-group thread about "converting IIF to CSV" suggests the export may be **IIF**; the general transactions export is CSV. *Uncertain: exact QBD export format.*

### Others
- **Xero, Wave, FreshBooks: no native integrations.** Escape hatch is the generic transactions CSV export (gear → Export Transactions) plus report CSVs. Some users run Xero side-by-side manually.
- **Zapier** exposes 17hats triggers/actions (incl. a 17hats↔QuickBooks Zap template), but bookkeeping-transaction-level Zapier support is not evidenced.
- Payment processors feeding bookkeeping: **17hats Payments (Stripe-powered), Stripe (legacy), Square, PayPal** — payments recorded against invoices generate the auto income entries described in §4.

---

## 8. Inferred data model (schema sketch)

Reverse-engineered from documented behavior — 17hats has no public API docs for bookkeeping. Confidence: moderate.

```text
BankAccount
  id, name, institution_id, type (bank | credit_card)
  aggregator_connection_id (external, read-only scope)
  status (connected | needs_refresh | broken), last_synced_at
  is_manual (accounts that only receive imports/manual entries)
  # ON DISCONNECT: cascade-deletes all Transactions (documented, destructive!)

Category
  id, name, direction (income | expense)
  is_system (Transfer Between Accounts, Merchant Fee, Sales Tax, ...)
  reporting_group (income | cogs | expense | excluded)   # inferred from P&L placement
  # flat list — no parent_id, no account-type, no tax-line mapping

Transaction  (single-entry ledger row)
  id, bank_account_id (nullable for pure manual?), date, description, amount
  direction (money_in | money_out)
  source (bank_feed | file_import | manual | payment_auto | fee_auto | tax_auto)
  category_id (nullable until categorized)
  verified (bool)                      # gate for ALL reporting
  suggested_category_id (from aggregator data + learned merchant map)
  project_id (nullable)                # manual expenses link to Projects
  invoice_payment_id (nullable)        # set by auto-creation or "Apply to an invoice"
  external_txn_id (aggregator id, for dedupe on refresh/import)

Receipt
  id, transaction_id, file_url, size <= 75MB, uploaded_at   # many per transaction

CategorySuggestionRule (learned, per user)   # inferred
  user_id, merchant_fingerprint(description), category_id, confidence, updated_at

TaxRate
  id, name, percent, archived (docs: never edit, create new)

Invoice / InvoiceLineItem (owned by invoicing module)
  line_item: product_id, amount, taxable(bool), tax_rate_ids[]
  product: display_name (unique for QBO), income_category_id   # drives auto-categorization

InvoicePayment
  id, invoice_id, date, amount, method (17hats_payments | stripe | square | paypal | manual)
  # on create: emits Transaction(payment_auto, category=line-item income category, verified=true)
  #            + Transaction(tax_auto) if taxable
  #            + Transaction(fee_auto, category=Merchant Fee/COGS) if processor fee known

QBOSyncLink
  entity_type (invoice | payment | contact | product), 17hats_id, qbo_id, last_synced_at
  # one-way push; payments -> Undeposited Funds
```

Key behavioral invariants worth copying or fixing:
1. `appears_on_reports = (category_id IS NOT NULL) AND verified` — a two-field gate, simple and effective.
2. Income truth lives in `InvoicePayment`, not the bank feed; bank deposits of known payments are neutralized via the `Transfer Between Accounts` category rather than matched. (17hats chose convention over a matching engine.)
3. Cash basis is hard-wired: bookkeeping date = payment date.
4. Deleting a bank connection deletes its transactions — no soft-delete/archive (a design mistake to avoid).

---

## 9. Strengths / weaknesses

### Strengths
- **Zero-effort income books**: because invoicing, payments, and bookkeeping share one system, income + sales tax + merchant fees are recorded, categorized, and verified automatically — solopreneurs literally never categorize income. This is the single best idea in the module.
- **Line-item → income-category mapping** yields a genuinely useful per-service revenue P&L for free.
- **Learning auto-suggestions** on expense categorization (aggregator hints + user-behavior learning).
- **Verify gate** keeps unreviewed noise off reports — a clean, comprehensible mental model for non-accountants.
- Receipts attach directly to transactions (multi-file, 75 MB).
- Receivables reports (aged/upcoming) fall out of invoice data — most personal-finance tools can't do this at all.
- Everything exports to CSV; QBO push covers the sales side for users with real accountants.
- Cheap relative to running a CRM + QuickBooks (though the $5/mo bank add-on on top of ~$60/mo annoys reviewers).

### Weaknesses / gaps (as reported by users + verified absences)
- **Single-entry, cash-basis only**: no double-entry, no balance sheet, no accrual, no audit trail — "lacks the accounting rigor… financially complex businesses require" (Fondo); "quick glimpse at business health rather than in-depth financial analysis."
- **No bank reconciliation** — nothing ties the ledger to statement balances; errors accumulate silently.
- **No transaction splits** — one bank row = one category, period.
- **No user-defined categorization rules** — only the black-box suggestion learner.
- **No auto-matching of deposits to payments** — the "Transfer between accounts" convention confuses users and produces double-counted income when misapplied; batch processor payouts are never decomposed.
- **Fragile bank feeds**: MFA banks never auto-sync; manual refreshes with re-entered credentials are routine; broken connections require emailing support so "bank sync partners" file a ticket; UK users report auto-connect stopped working.
- **Disconnecting an account destroys all its history** including categorized/verified work — documented, and brutal.
- **No recurring expense automation** (top Capterra complaint), no vendors/bills/AP, no purchase orders.
- **No mileage tracking**, no receipt OCR, no email-in receipts, weak mobile app generally ("poorly designed mobile app" per reviews).
- **No tax-time tooling**: no quarterly estimated-tax calc, no Schedule C mapping, no 1099s, no tax-savings envelope; year-end = "export CSVs for your tax preparer."
- **Sales tax is a summary report only** — no jurisdictions, filing, or remittance tracking; rate edits can corrupt history (hence "never edit a rate" doc guidance).
- **QBO integration is sales-only and error-prone**: expenses never sync; users report duplicate payments/invoices; naming/number constraints (21-char, unique display names, identical tax-rate names) are sharp edges.
- **Flat category list** — no hierarchy, no COGS section beyond the hard-coded Merchant Fee behavior, no category archiving documented.
- Net effect repeatedly seen in reviews: businesses **outgrow it** ("basic features inside bookkeeping… didn't exist") and end up paying for QBO/Xero anyway, at which point 17hats bookkeeping becomes dead weight.

---

## 10. Build recommendations

Context: the user's finance app already has **CSV import + learning auto-categorization + budgets**. 17hats' most defensible ideas are the ones that come from owning the *income* side; its expense side is weaker than what the user already built.

### Copy (proven, cheap, high-value)
1. **The two-state review gate** (`categorized` + `verified`) with bulk verify. Simple, legible; only verified rows hit reports. The user's app can add a `verified/reviewed` flag and filter reports on it.
2. **"Transfer between accounts" as a first-class excluded category** — every P&L-style report needs an exclusion mechanism; make it built-in and un-deletable.
3. **Receipt attachments on transactions** (multi-file). Bonus over 17hats: add OCR + auto-create-from-receipt.
4. **Filterable single ledger** (account / category / direction / date / amount / keyword) as the one home screen for money — 17hats' Bookkeeping tab UX is well-liked.
5. **CSV export of every report**, and a raw transactions export with date range (their gear-menu pattern).
6. **Cash-basis P&L with "Show Transactions" drill-down** grouped by category — trivially derivable from data the user already has; it's the report solopreneurs actually hand to tax preparers.
7. **"Never edit a tax rate / rate history" principle** — generalize: snapshot any rate-like reference data onto historical records instead of referencing mutable rows.

### Improve (17hats does it badly or half-way)
1. **Categorization rules**: keep the learning suggester (user already has one — it's ahead of 17hats' black box) and ADD user-visible, editable rules (match on description/amount/account → category), which 17hats lacks entirely.
2. **Splits**: support one-to-many category splits per transaction — a glaring 17hats absence and table stakes in QBO/Wave/Monarch.
3. **Deposit/payment matching**: if the user's app ever grows an income/invoice side, build a real matcher (amount+date fuzzy match, payout decomposition for Stripe-style batch deposits) instead of 17hats' "mark it a transfer" convention. Even without invoices, transfer-detection between the user's own accounts (matching ±amount within N days) beats manual marking.
4. **Bank feed resilience**: if adding an aggregator (Plaid/MX/Finicity/Teller), (a) NEVER delete transactions on disconnect — archive the connection and keep history; (b) show per-connection health + last-sync; (c) keep file import (the user's CSV import) as the permanent fallback, exactly the role it plays for 17hats users with broken feeds.
5. **Recurring transactions**: detect and templatize recurring expenses (17hats users beg for this); the user's app likely already has the data to infer recurrence.
6. **Quarterly tax estimation**: 17hats has nothing here despite targeting US solopreneurs — a P&L-driven estimated-tax widget (income × entity-type effective rate, IRS due-date calendar) is cheap and highly differentiating for a finance tracker.
7. **Sales-tax-collected report**: only if the user's app tracks business income streams; otherwise skip.

### Skip (not worth building / anti-patterns)
1. **Paid bank-connection add-on pricing** — reviewers resent the $5/mo upsell; bundle connectivity or price it honestly.
2. **Destructive disconnect** — explicitly an anti-pattern to avoid.
3. **One-way QBO invoice push** — irrelevant to a personal finance tracker; if accountant hand-off matters, a clean CSV/Schedule-C-tagged export beats a brittle sync (note 17hats' sharp edges: 21-char refs, name-collision rules, identically-named tax rates).
4. **Double-entry ledger / balance sheet** — 17hats proves solopreneurs neither need nor want it; a personal tracker doesn't either. Don't over-build; spend the effort on rules, splits, matching, and tax estimates.
5. **Receivables reports** — only meaningful with an invoicing module; skip unless the user's app adds one.
6. **Time tracking / lead-source reporting** — out of scope for a finance tracker.

### Positioning insight
17hats wins by **making income bookkeeping a side effect of getting paid** and loses on everything an accountant would ask for. A competing finance app should keep 17hats-level simplicity on review flow while beating it decisively on: rules + splits + transfer detection (the user is already partway there), bank-feed trust (no data loss, visible health), recurring detection, and tax-time outputs (quarterly estimates, Schedule-C-ish category mapping, one-click accountant export bundle). None of those require double-entry accounting.

---

## 11. Sources

17hats Help Center (content captured via search extraction; direct fetch blocked from this environment):
- https://help.17hats.com/en/articles/3112838-bookkeeping-overview
- https://help.17hats.com/en/collections/550518-bookkeeping
- https://help.17hats.com/en/articles/849340-17hats-invoicing-bookkeeping
- https://help.17hats.com/en/articles/928589-money-matters-connecting-your-bank-account
- https://help.17hats.com/en/articles/924615-how-do-i-connect-my-bank-account-to-17hats
- https://help.17hats.com/en/articles/879915-why-is-my-bank-not-connecting-or-updating-automatically
- https://help.17hats.com/en/articles/879921-bank-account-manual-refresh
- https://help.17hats.com/en/articles/933992-what-happens-if-i-disconnect-my-synced-bank-account
- https://help.17hats.com/en/articles/879929-importing-older-bank-transactions
- https://help.17hats.com/en/articles/924611-how-do-i-categorize-bookkeeping-transactions
- https://help.17hats.com/en/articles/924612-how-do-i-add-custom-bookkeeping-categories
- https://help.17hats.com/en/articles/927616-how-do-category-auto-suggestions-work
- https://help.17hats.com/en/articles/924622-how-do-i-categorize-payments-deposited-into-my-bank
- https://help.17hats.com/en/articles/924610-how-do-i-apply-a-bookkeeping-transaction-to-an-invoice
- https://help.17hats.com/en/articles/924616-how-do-i-record-a-payment-manually
- https://help.17hats.com/en/articles/879995-how-do-i-manually-record-expenses
- https://help.17hats.com/en/articles/924603-what-is-the-profit-and-loss-report-in-17hats
- https://help.17hats.com/en/articles/9050472-export-your-profit-and-loss-report-as-a-csv-file
- https://help.17hats.com/en/articles/924623-sales-tax-report
- https://help.17hats.com/en/articles/9554242-export-your-sales-tax-report-as-a-csv-file
- https://help.17hats.com/en/articles/2673313-money-matters-tax-settings-page
- https://help.17hats.com/en/articles/924556-aged-receivables-report
- https://help.17hats.com/en/articles/924557-upcoming-receivables-report
- https://help.17hats.com/en/articles/9231084-export-your-client-and-product-sales-reports-as-a-csv-file
- https://help.17hats.com/en/articles/7336856-overview-of-lead-source-reporting-in-17hats
- https://help.17hats.com/en/articles/859661-17hats-quickbooks-online-integration
- https://help.17hats.com/en/articles/861483-invoice-payments-undeposited-funds-quickbooks-online
- https://help.17hats.com/en/articles/879841-how-do-i-export-my-17hats-bookkeeping-to-quickbooks-desktop
- https://help.17hats.com/en/articles/11498904-credit-card-and-ach-processing-fees-in-17hats-bookkeeping-with-stripe
- https://help.17hats.com/en/articles/849333-money-matters-products-services
- https://help.17hats.com/en/articles/1052603-discounts-how-to-customize-discounts-and-view-on-your-profit-loss-report
- https://help.17hats.com/en/articles/897500-how-do-i-issue-a-refund-to-my-client
- https://help.17hats.com/en/articles/12649453-processing-refunds-inside-17hats

17hats marketing / blog / university:
- https://www.17hats.com/integration/banks
- https://www.17hats.com/features/profit-loss-report
- https://www.17hats.com/features/sales-tax-reporting
- https://www.17hats.com/features/client-sales-report
- https://www.17hats.com/integration/quickbooks
- https://www.17hats.com/pricing
- https://blog.17hats.com/end-of-year-bookkeeping-checklist-for-small-business-owners/
- https://blog.17hats.com/reporting-in-17hats-your-businesss-secret-weapon/
- https://www.17hatsuniversity.com/17hats-quick-tips/the-bookkeeping-tab-in-17hats
- https://www.17hatsuniversity.com/17hats-quick-tips/how-to-add-a-receipt-in-17hats
- https://17hats.releasenotes.io/release/0EzY5-export-profit-and-loss-report-as-a-csv-file

Reviews & comparisons:
- https://www.tryfondo.com/blog/17hats-vs-quickbooks
- https://www.capterra.com/p/144328/17hats/reviews/
- https://www.g2.com/products/17hats/reviews
- https://www.softwareadvice.com/compare/393202-QuickBooks-Online/vs/403005-17hats/
- https://www.agencyhandy.com/client-portal/17hats-pricing/
- https://taskip.net/17hats-pricing/
- https://www.apps4rent.com/blog/17hats-quickbooks/
- https://www.staged4more.com/blog/review-17hats
- https://johngress.com/17hats-referral-code-a-quickbooks-alternative-that-transformed-my-photography-business/
- Facebook 17hats User Q&A group threads (QBO sync accuracy, bookkeeping refresh issues, IIF→CSV export) — https://www.facebook.com/groups/17HatsUserQA/

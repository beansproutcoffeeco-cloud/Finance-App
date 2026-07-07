# 17hats: Integrations, API & Data Portability

> Research note: 17hats' own domains (17hats.com, help.17hats.com) and zapier.com app pages were blocked from direct fetching in this research environment. Facts below were assembled from web-search extracts of those exact pages plus third-party sources (TaxDome migration docs, ShootProof help center, review/comparison articles). Items marked *(unverified)* could not be cross-checked against a second source. Two earlier research passes on this area were interrupted by an environment restart; this doc is intentionally tighter than its siblings and leans on cross-references to the other research docs where an integration is covered in depth there.

## 1. Summary

17hats takes a **built-in-house, thin-integrations** strategy: rather than integrating deeply with best-of-breed tools, it re-implements most functions natively (scheduling instead of Calendly, bookkeeping instead of QuickBooks, SMS instead of Twilio-via-Zapier) and offers a short catalog of integrations concentrated on payments, calendars, accounting hand-off, and photographer gallery/sales tools. There is **no public, documented REST API**; the only programmatic surface is a **contacts-only Zapier app** authenticated by an account-level API key. Data export is similarly narrow — contacts and some reports export to CSV, but projects, documents, emails, and bookkeeping detail largely do not — making vendor lock-in high and giving a competing product an easy differentiation lane: **API-first, export-everything**.

## 2. Integration catalog

The officially advertised list (17hats.com/integrations, via search extracts): Stripe, Square (legacy), PayPal (retired), Google Calendar, Apple Calendar, Zoom, QuickBooks Online, Greetabl, Zapier, Fundy, N-Vu, The Knot, WeddingWire, ProSelect, ShootProof, plus "20,000+ banks" via the bookkeeping bank-feed add-on.

| Integration | What it does | Direction | Notes / plan gating |
|---|---|---|---|
| **17hats Payments (Stripe)** | Card/ACH/Apple Pay/Google Pay processing on invoices and bookings | n/a (embedded processor) | Only option for new accounts; Square/Stripe-direct are legacy, PayPal & Authorize.net retired. Full detail in doc 05. |
| **QuickBooks Online** | Pushes invoices + payments into QBO (Undeposited Funds) | One-way, sales-side only | Expenses never sync; naming/length constraints; user-reported duplicate-payment bugs. Full detail in doc 06. |
| **Google Calendar** | Two-way calendar sync (polling) | Two-way | The only true two-way calendar sync. Full detail in doc 08. |
| **Apple Calendar** | iCal feed of 17hats calendars | One-way (out) | Subscribe-only; no inbound sync. Doc 08. |
| **Zoom** | Auto-creates a Zoom meeting for bookings with a "video call" location type | One-way (out) | Attached to Online Scheduling services. Doc 08. |
| **Bank feeds** | Read-only bank/credit-card transaction import for bookkeeping | One-way (in) | $5/mo add-on; aggregator not publicly named; ~22,000 institutions claimed on some pages, "20,000+ banks" on the integrations page. Doc 06. |
| **The Knot / WeddingWire** | Turns marketplace inquiry emails into 17hats leads | One-way (in) | Implemented as **inbox email parsing**, not an API — brittle when the marketplaces change their email formats. Doc 02. |
| **ShootProof** | Gallery creation from 17hats bookings; ShootProof orders flow back into dashboard + bookkeeping with a chosen Income Category & bank account | Two-way (bookings out, orders in) | Connected via OAuth-style "connect account" in Settings → Integrations. |
| **N-Vu** | Gallery/IPS sales orders flow into projects and bookkeeping | One-way (in) | "Order to getting paid" flow for photographers. |
| **Fundy Designer** | Album/wall-art order import into 17hats | One-way (in) | Manual import into projects *(mechanics unverified)*. |
| **ProSelect** | Desktop IPS software; orders imported into a project + bookkeeping | One-way (in), manual | Explicitly **not** a live sync — user manually imports orders per project. |
| **Greetabl** | Client gift sending | One-way (out) | Peripheral; listed on marketing page. |
| **Zapier** | Bridge to ~8,000 apps | Both (but contacts only) | See §3. |
| **Email (Gmail/IMAP), SMS add-on** | Covered as core features rather than integrations | — | Doc 09. |

What's *absent* is as telling as what's present: no native Meta/Google ads lead forms, no Mailchimp/ActiveCampaign email-marketing sync (only via Zapier contacts), no Slack, no cloud storage (Drive/Dropbox), no Calendly-class tools (they want you on native scheduling), no Xero/Wave/FreshBooks (QBO only).

## 3. Zapier surface

From 17hats' own help article ("Zapier Integration"):

- **Setup:** Account Settings → Integrations → Zapier → "Enable" reveals an **API key** that authenticates the Zapier connection. (This key is the closest thing to a public API credential 17hats has.)
- **Scope:** the first iteration is explicitly **limited to Contacts, two-way**:
  - **Triggers (2):** New Contact created · Contact updated
  - **Actions (2):** Create Contact · Update Contact
  - **Search (1):** Find Contact
- 17hats has said more triggers/actions are planned with no published roadmap; as of this research no expansion is documented — reviews and the help center still describe the contacts-only surface. *(Recheck at build time.)*

Implications: none of the high-value events (lead captured, quote accepted, contract signed, invoice paid, booking made) are exposed to Zapier. Users who want "when invoice paid → add to accounting/email list" cannot automate it externally; they rely on 17hats' internal workflows only. Competing products (Dubsado, HoneyBook) expose noticeably richer Zapier surfaces.

## 4. API & webhooks

- **No public REST API.** No developer portal, no API docs anywhere on 17hats.com or help.17hats.com findable via search. The github.com/17hats organization exists (~17 repos) but contains internal libraries (payments, Slack, date/time helpers), not an SDK or API spec.
- Third-party directory listings (apitracker.io, workload.co) show generic "API Reference / Webhooks" boilerplate for 17hats; these appear to be **templated directory pages, not evidence of a real public API** *(assessed, not proven)*.
- **No webhooks.** The only outbound eventing is the Zapier contact triggers (which Zapier implements by polling or by 17hats' private endpoint — mechanism not public).
- The account API key shown in the Zapier setup implies a private HTTP API exists internally, but it is undocumented and unsupported for direct use.

## 5. Data import & migration

- **CSV contact import** is the core mechanism (help: "How do I import a CSV file of Contacts and Projects?"): upload CSV, map columns to standard/custom fields, and optionally **auto-create a Project per contact** during import.
- Onboarding docs ("Moving your Clients to 17hats") walk users through exporting CSVs from competitors: Dubsado (Address Book → Export), HoneyBook (Contacts → Download spreadsheet), Google Contacts, Sprout Studio (dedicated switching guide exists).
- **No automated full-account migration** from any competitor — templates, documents, projects-in-flight, and financial history must be rebuilt by hand (the template Marketplace, doc 11, partially compensates). Third parties sell migration services.
- Inbound project/document import beyond the contact+project CSV does not exist.

## 6. Data export & lock-in assessment

What can leave 17hats:

- **Contacts:** CSV export from Contacts/Leads pages (gear icon → Export Contacts), filterable by type/tag. **Contact fields only** — the help article states project information (documents, project details, emails, time logs) "will need to be saved individually."
- **Reports:** P&L, Client/Product Sales, and transaction lists export to CSV (doc 06).
- **Documents:** no bulk export; per-document browser print-to-PDF (doc 04).
- **Emails, notes, to-dos, workflows, templates:** no export path documented.
- **Cancellation:** account data becomes inaccessible on cancellation (data lockout was flagged in docs 01 and 12 as a churn-time complaint); third-party guides (e.g. Kieri Solutions) exist purely to help users scrape their data out before leaving.

**Lock-in verdict: high.** The practical export is "your contact list and some financial CSVs." Everything that makes the account valuable — projects, signed contracts, email history, automations — stays behind.

## 7. Strengths / weaknesses

**Strengths**
- Photographer vertical is genuinely well served: gallery/IPS order flows (ShootProof, N-Vu, ProSelect, Fundy) land orders directly into bookkeeping with income categories — a niche moat.
- The built-in-house strategy means the integrations that exist feed one shared contact/project record; nothing feels bolted on.
- CSV contact import with auto-project creation makes basic onboarding easy.

**Weaknesses (exploitable)**
- No public API, no webhooks, contacts-only Zapier: the platform is a closed box. Power users and agencies can't extend it.
- One-way, sales-only QBO sync with known bugs (doc 06).
- Lead-source "integrations" (Knot/WeddingWire) are brittle email parsing.
- Export coverage is so thin it functions as retention-by-hostage; users notice and resent it.
- No email-marketing, storage, or team-tool integrations at all.

## 8. Build recommendations

**Table-stakes integrations for a competing app (in priority order):**
1. **Stripe** (cards + ACH + wallets) — embedded payments, day one.
2. **Google Calendar two-way + Microsoft 365/Outlook two-way** (17hats' Google-only sync is a persistent complaint) + iCal feeds.
3. **QuickBooks Online AND Xero**, two-way where safe (payments, expenses, contacts), with an idempotent sync log — directly attacks 17hats' flakiest integration.
4. **Zapier + Make** with a *rich* event surface (lead created, form submitted, quote accepted, contract signed, invoice paid, booking created/cancelled, project stage changed).
5. **Gmail/Microsoft OAuth email** (core feature; see doc 09).
6. Vertical galleries (ShootProof/Pic-Time) only if targeting photographers.

**Strategy: API-first.** Build the public REST API as the same API the frontend uses, add webhooks early (they're cheap if evented from the start), and publish docs. 17hats/HoneyBook/Dubsado all lack a real public API — it is the single clearest structural differentiator available, it earns integrations you don't have to build, and it removes the #1 objection of technical buyers.

**Export-everything as a trust feature.** Full-account export (JSON + CSVs + PDFs of signed documents) — advertised, one click, available even after cancellation for 90 days. It converts 17hats' most resented behavior into a selling point, and the user's existing Finance-App already demonstrates the right instinct (local-first data, one-file JSON backup/restore).

**Skip:** brittle inbox-parsing lead integrations (offer a generic inbound-email-to-lead address and native webhook/Zapier intake instead); desktop-software manual imports (ProSelect-style) unless the vertical demands it.

## 9. Sources

- https://www.17hats.com/integrations — official integration catalog
- https://help.17hats.com/en/collections/1522689-integrations — help center integrations collection
- https://help.17hats.com/en/articles/2761371-zapier-integration — Zapier setup, API key, contacts-only scope
- https://zapier.com/apps/17hats/integrations — Zapier app directory listing (fetch blocked; triggers/actions via search extracts)
- https://help.17hats.com/en/articles/843725-how-do-i-export-my-contact-list — contact CSV export, contact-fields-only caveat
- https://help.17hats.com/en/articles/934801-how-do-i-import-a-csv-file-of-contacts-and-projects — CSV import with auto-project creation
- https://help.17hats.com/en/articles/10450504-onboarding-step-2-moving-your-clients-to-17hats — competitor export walkthroughs
- https://help.17hats.com/en/articles/9363325-switching-from-sprout-studio-to-17hats — Sprout Studio migration guide
- https://help.17hats.com/en/articles/934807-how-do-i-integrate-with-shootproof and https://help.17hats.com/shootproof-integration/how-do-shootproof-orders-work — ShootProof mechanics
- https://help.17hats.com/en/articles/2701035-proselect-integration — ProSelect manual order import
- https://help.17hats.com/en/articles/4252909-n-vu-integration-how-it-works — N-Vu integration
- https://help.shootproof.com/hc/en-us/articles/115010776668-17hats-ShootProof — ShootProof-side documentation
- https://help.taxdome.com/article/242-how-to-import-from-17hats — third-party view of what's exportable
- https://www.kieri.com/17hats-export-or-convert-to-excel-csv-tab-xls/ — third-party export workaround guide
- https://github.com/17hats — GitHub organization (no public SDK/API)
- https://apitracker.io/a/17hats — directory listing (boilerplate, treated as non-evidence)
- https://help.17hats.com/en/articles/9231084-export-your-client-and-product-sales-reports-as-a-csv-file — report CSV export

# 17hats Research — Index

Deep research into how **17hats** (all-in-one business management software for solopreneurs) works inside and out, produced overnight on 2026-07-07 by 12 parallel research agents plus a synthesis pass. Purpose: inform the design and build of our own competing application.

**Start with `13-build-blueprint.md`** — it synthesizes everything into a unified data model, an MVP cut, and a differentiation strategy. The numbered docs are the per-module deep dives.

| Doc | Area | One-line takeaway |
|---|---|---|
| [01](01-platform-overview.md) | Platform, pricing, competitors | Founded 2014; moved to a single ~$60/mo all-inclusive plan in 2025 (plus $5 add-ons); wins on breadth-per-dollar vs HoneyBook/Dubsado/Bonsai. |
| [02](02-crm-leads-contacts.md) | CRM, leads, lead capture | No separate lead object — 4 fixed contact types; lead capture forms auto-create contact + project + workflow; tags are the load-bearing infrastructure. |
| [03](03-projects-client-portal.md) | Projects & client portal | Project = central "manila folder"; three overlapping stage systems (lifecycles/tags/pipelines); per-contact portal via capability URL + PIN, read-mostly. |
| [04](04-documents-quotes-contracts-questionnaires.md) | Quotes, contracts, questionnaires | The 3-in-1 quote→sign→pay bundle with forward-locking tabs is the killer feature; no server-side PDF or audit certificate. |
| [05](05-invoicing-payments.md) | Invoicing & payments | Payment schedules (up to 12 installments, event-relative due dates), auto-charge opt-in, Stripe-powered "17hats Payments"; no late fees or surcharging. |
| [06](06-bookkeeping-finance.md) | Bookkeeping & reporting | Single-entry, flat categories, no rules/splits, no real deposit matching; invoice payments auto-become verified income — the one great idea. |
| [07](07-workflows-automation.md) | Workflows & automation | Linear checklists of To-Do/Action/Pause steps; base-date-relative timing; per-step approval mode; client-action gates; no branching. |
| [08](08-scheduling-calendar.md) | Scheduling & calendar | Service + availability-schedule model; booking fan-out auto-creates contact/project/invoice/workflow; Google-only two-way sync. |
| [09](09-email-templates-communication.md) | Email, templates, SMS | Gmail/IMAP send-as-user; selective 20–45 min inbox sync onto projects; `[% token %]` expression language everywhere; SMS is a paid add-on. |
| [10](10-integrations-api-data.md) | Integrations, API, portability | No public API/webhooks; contacts-only Zapier; contact-only CSV export → high lock-in. Photographer gallery integrations are the niche moat. |
| [11](11-ux-navigation-mobile.md) | UX, navigation, mobile | Contact-centric IA with a strong Project page; dashboard is an action feed; UI dated since 2014; mobile app is a weak triage companion (~3.3★). |
| [12](12-user-feedback-opportunities.md) | User feedback & opportunities | 4.4–4.6★ web product, loyal users; complaints: dated UI, weak mobile, shallow reporting, add-on pricing creep. Category is switch-willing post-HoneyBook price hikes. |
| [13](13-build-blueprint.md) | **Synthesis: build blueprint** | Unified schema, architecture, MVP cut, differentiation plan. |

## Research method & caveats

- Each doc was produced by a dedicated agent running 15–75 web searches over 17hats' marketing site, the help.17hats.com knowledge base, release notes, the template marketplace, Zapier listings, review sites (G2, Capterra, GetApp, app stores), Reddit/Facebook discussions, and competitor comparisons.
- **17hats' own domains (and several review sites) were blocked from direct fetching by this environment's egress proxy.** Content from those pages was recovered via search-engine extracts of the exact articles. Facts are triangulated across sources where possible; unverifiable items are flagged inline as *(unverified)* / *(inferred)*.
- Pricing, plan structure, and the Zapier surface change often — **re-verify against live pages before relying on them for build decisions.**
- Inferred data models are reconstructions from observed behavior and 17hats' template-token grammar (`[% project.client.portal_url %]` etc.), not from any internal documentation.

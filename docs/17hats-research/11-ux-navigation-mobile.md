# 17hats: UX, Navigation & Mobile

> Research area 11 of 12 — overall app information architecture, dashboard/Overview page, global search, onboarding & education, account/brand/user structure, mobile apps, design language, and UX reputation.
>
> **Method note:** 17hats-owned properties (help.17hats.com, 17hats.com, blog.17hats.com) and the app stores block automated page fetches, so this document is compiled from extensive search-engine extraction of those pages plus third-party review sites (Capterra, G2, Trustpilot, GetApp, Software Advice, JustUseApp) and competitor teardown articles. Statements that could not be double-confirmed are flagged **[uncertain]**. Nothing here is invented; where evidence was absent the gap is stated explicitly.

---

## 1. Summary

- 17hats is a **contact-centric, single-page-app style web product** with a **left-hand navigation bar** (Dashboard/Overview, Leads, Contacts, Projects, Calendar, Documents, Bookkeeping, plus Workflows and feature areas) and a **persistent top toolbar** (contact search, time-tracking timer, templates shortcut, help, account settings, brand switcher).
- The **Dashboard ("Overview") is an action feed, not an analytics page**: five sections — 5-day quick-view calendar, local weather, recent client activity, pending documents, and a "Let's Take Care of Business" smart to-do/alert feed driven by workflows and leads. There is **no revenue/money chart widget on the dashboard** (money reporting lives in Bookkeeping) — a notable gap competitors exploit.
- **Global search is contacts-only** (name, last name, company, phone, email). You cannot globally search documents, emails, or transactions from the omnibox — a repeated UX complaint.
- **Onboarding is education-led, not product-led**: a 7-day no-credit-card trial, a numbered "Onboarding Step 1…" help series, live "First 24 Hours" and weekly Getting Started workshops, a full video school ("17hats University"), and a paid/free **template Marketplace** where third-party sellers publish workflows, contracts, emails, lead-capture forms, and scheduling services that auto-install into an account.
- **Account structure:** one master login can own **multiple linked Brands** (separate businesses with their own logo, colors, email, templates, and client-facing identity), switched from a top-right avatar menu. **Multi-user** has three permission levels (Owner / Admin / Team Member) with granular per-feature permissions for Team Members; historically 3 users came with the Premier tier, extra seats ~$5/mo.
- **Mobile apps (iOS + Android) are a companion, not a parity client**: dashboard, contacts/projects create-edit, calendar, to-dos, template-based emails, sending/counter-signing existing documents, and push notifications — but **you cannot build invoices, contracts, or questionnaires in the app**. Store sentiment is mediocre (~3.3/5 cumulative on iOS per JustUseApp analysis) with complaints about stale updates and crashes; the web product scores far better (4.4/5 Capterra, 4.6/5 G2).
- **Design reputation:** functional but dated; no major visual redesign since launch; criticized for cute-but-unclear UX copy ("Let's Take Care of Business"), missing tooltips, clunky multi-click navigation paths, an "ancient" document editor, occasional slowness/glitches, and no kanban/Gantt views. No public accessibility (WCAG) statement was found.

---

## 2. Information architecture (nav map of the whole app)

### 2.1 Top-level layout

- **Left-hand vertical navigation bar** — primary section switcher ("Features Tab menu on the left-hand side" in 17hats' own help language).
- **Top toolbar** — persistent utility strip on every page.
- **Top-right avatar/logo menu** — brand switching, "Create New Brand," account-level items.
- **Main content area** — list pages (tile or list view toggles on Projects) and record pages (Project Overview, Contact page).

### 2.2 Left navigation sections (confirmed items)

Confirmed from help-center and blog language ("left hand navigation bar", "Features Tab menu"):

| Nav item | What it contains |
|---|---|
| **Dashboard / Overview** | The daily action home page (see §3). |
| **Leads** | Contacts typed *Hot Lead* or *Cold Prospect*; archived leads; tag search; sort by Project Date, Lead Date, or Next Due Date; access to Lead Capture Forms (install + edit) from this page. Lead Source Reporting also surfaces here. |
| **Contacts** | Contacts typed *Client* and *Other Contact*. Contact records link to their Projects. |
| **Projects** | All projects; **tile view / list view toggle** (two small icons at top of the page). Clicking a project opens Project Overview. |
| **Calendar** | Full calendar: day/week/month views, unlimited color-coded 17hats calendars, connected Google calendars, team members' calendars (multi-user). |
| **Documents** | Type-filtered lists of all documents — all Invoices, all Contracts, all Quotes, all Questionnaires as lists ("see all of one type of Document in one place"). |
| **Bookkeeping** | Transaction ledger + reports dropdown (Profit & Loss, Sales Tax, Upcoming Receivables, Aged Receivables, Client Sales, Product Sales). |
| **Workflows** | Main Workflow overview page listing active workflow items awaiting completion/approval. **[uncertain whether this is a top-level left-nav item or reached via Projects/Templates — help articles reference a "main Workflow overview page" but not its exact nav position]** |

Other feature areas referenced as pages/tabs whose exact left-nav placement is **[uncertain]**: **Online Scheduling** (its own tab per onboarding article: "visit this tab and toggle your Online Scheduling on"), **SMS Texting dashboard/status page** (added ~2025), **Client Portal** configuration (lives in Account Settings), **Time tracking** (timer lives in the toolbar; time logs appear per-project).

### 2.3 Top toolbar (from "Tour of 17hats" help article)

1. **Contact Search Bar** — gray box, top right, labeled "Search Contacts"; available on **every page**. Searches first/last name, company name, phone number, email address (see §2.6).
2. **Timer** — start a new time-tracking timer, pause/stop an active one, view elapsed time for an active timer.
3. **Documents & Emails** — one-click shortcut to the Documents & Emails **template** page (in Account Settings).
4. **Help & Support** — opens Help Center + Video Tutorial Center in a new tab.
5. **Account Settings** — gear/shortcut into settings.
6. **Brand switcher** — click your logo or initials, top right, to switch between linked Brands or "Create New Brand."
7. **Quick-create ("shortcut") button** — "the shortcut button located at the top right of the current page" creates documents (e.g., quotes) from anywhere. **[uncertain: exact scope of the quick-create menu — confirmed at least for quotes; document creation is also offered contextually via "Create New" inside a Project's Important Documents panel]**

### 2.4 Record-level IA: the Project Overview page

The Project (job) page is the workhorse record and the model to copy:

- **Header / Project Details:** Project Title, Primary Email, Project Date, Phone, Contact Type, assigned Calendar (customizable fields).
- **Important Documents panel:** Quotes, Contracts, Invoices, Questionnaires for this project, with a "Create New" button.
- **Related Contacts:** additional people on a project; can receive documents/emails and be contract signees.
- **Bottom tab strip:** **Notes, Emails, Files, To-do's, Events, Phone Log, Time Log, Activity Log** — each tab lists prior entries and has a "+" to add. Files tab holds uploaded PDFs/JPEGs.
- SMS conversations (2025+) also thread onto the Project Page alongside notes/emails.

### 2.5 Contact vs Project vs Lead (the data model that drives the nav)

- A **Contact** is a person, classified as **Hot Lead, Cold Prospect, Client, or Other Contact**. Type determines whether they appear on the **Leads** page (Hot Lead / Cold Prospect) or the **Contacts** page (Client / Other).
- A **Project** is a job/engagement attached to a Contact; a Contact can have many Projects, and Projects can be moved between Contact records.
- Both Contacts and Projects support **tags** (with automation to auto-tag) and archiving.
- Clicking a Contact leads to their project/record page where contact info and related documents are organized.

### 2.6 Global search — capabilities and limits

- Omnipresent **"Search Contacts"** box; matches on first name, last name, company name, phone number, email address; typing a few letters surfaces matches.
- **It searches contacts only.** No evidence of global search across document contents, email bodies, invoices, or bookkeeping transactions from the omnibox. Document lookup is done by going to Documents and filtering by type; bookkeeping has its own keyword/amount/date filters inside its tab.
- Reviewers cite roundabout navigation as a consequence — e.g., you cannot click from a dashboard to-do straight into its project; "you have to click on 'Project' and then select the specific project" (Zendo teardown).

### 2.7 Client-facing IA (adjacent surfaces)

- **Client Portal** (per-contact secure page): accept quotes, sign contracts, complete questionnaires, pay invoices, view event details; brandable with cover image (recommended 1140×220px), logo, and global welcome message (text/links/images); optional per-portal password + a **universal client portal login link**; clients **cannot upload files**, and internal project Files are **not** shown in the portal.
- **Online Scheduling** public booking pages; **Lead Capture Forms** embedded on the member's website. These are separate public surfaces hanging off the same account.

---

## 3. Dashboard / Overview page (every widget)

17hats calls it "the Dashboard, or overview page — your one location to see the items you'll need to complete or check in on each day." It is explicitly an **action queue for today**, not a reporting dashboard. Five sections:

1. **5-Day Quick View Calendar** — horizontal strip of the next five days; see and **add events directly** from the widget.
2. **Weather Preview** — yes, real feature: local weather forecast displayed with the mini calendar, pitched at outdoor-work businesses (photographers etc.).
3. **Recent Client Activity** — reverse-chron feed of important client events: invoices paid, contracts signed, questionnaires completed, new leads, document views. Designed so you can email contacts / open projects from the feed.
4. **Pending Items (Pending Documents)** — contacts with outstanding/unactioned documents auto-filter here (unsigned contracts, unpaid invoices, unanswered quotes/questionnaires) so you can chase them.
5. **"Let's Take Care of Business"** — the smart daily to-do feed, described as "your go-to section each morning." It aggregates:
   - To-do tasks due (each to-do also lives on its assigned calendar);
   - **Workflow items** needing manual completion or approval (also surfaced on the Workflow overview page and inside the project);
   - **New-lead notifications** (a dashboard notification "automatically appears" in this section when a Lead Capture Form is submitted);
   - Individual alerts or whole alert groups can be **snoozed** to de-clutter.

Also on/around the dashboard: SMS replies are surfaced to the Dashboard for quick reply (post-2025 SMS feature); the toolbar (search, timer, templates, help, settings) rides above it.

**What is NOT on the dashboard:** no money snapshot/revenue chart, no P&L teaser, no pipeline value widget — financial reporting is buried in the Bookkeeping tab, and reviewers on Capterra call the financial side weak. Marketing copy calls the dashboard "the perfect at-a-glance page," but its content is tasks and activity only. Dashboard is also **not customizable** (no evidence of widget rearrangement/hide options beyond snoozing alerts) **[uncertain — absence of evidence]**.

Criticism to learn from (Zendo/Plutio teardowns): the section names are whimsical but opaque ("Let's Take Care of Business" → contains "Pending items"), there are **no tooltips or inline explanations**, and dashboard items don't deep-link into the specific project.

---

## 4. Onboarding & education

### 4.1 Sign-up and trial

- **7-day free trial, no credit card required**; all features unlocked during trial, support included. Trials can be **restarted** after expiry.
- Alternative path at signup: "buy now" with a discount and 30-day money-back guarantee (marketing offer, varies).
- Pre-signup funnel: live group demo sign-up, **self-guided tour** page (17hats.com/self-guided-tour), and a 20-minute personalized 1:1 option.
- No evidence of a pre-populated sample-data/demo account inside the trial; instead 17hats tells you to **add yourself as a test Contact** to simulate the client experience.

### 4.2 In-product / documented setup flow ("Onboarding | Step 1) Set Up Your New 17hats Account")

The canonical numbered onboarding series in the Help Center (article 10447114 and the older "Getting Started with 17hats" collection) covers, in order:

1. **Brand setup** — Brand Preferences (4 tabs: Account, Logo, Colors & Fonts, Images): upload logo, set document/button colors and fonts, internal look.
2. **Email connection** — connect incoming & outgoing email servers (Google/IMAP), set Document Email Reminders, create Email Signatures.
3. **Calendar connection** — create 17hats calendars and/or link Google Calendar(s).
4. **Money setup** — enable online payments (connect Stripe/Square/PayPal), connect bank account for bookkeeping.
5. **Add a test Contact (yourself)** — via "Add First Contact" empty-state button or "Add Contact" → "Basic Contact Form"; used later to test Workflows end-to-end.
6. **Online Scheduling** — visit the tab and toggle it on.
7. **Documents & Emails templates** — view/create templates.
8. **Custom Fields** — personalize tokens/automation.

The same steps are taught live in the **First 24 Hours Workshop**, which walks new members step-by-step to sending their **first invoice**, plus emails, templates, and token automation. **Getting Started Workshops** run weekly (Wednesdays, 1pm PT / 4pm ET) with themed sessions: *Account Setup & Branding*, *Contacts & Projects*, *Online Scheduling*, *Workflow*, etc. (gettingstarted.17hats.com).

### 4.3 Template Marketplace (marketplace.17hats.com)

- A first-party marketplace where **other 17hats members/partners sell or share templates**: Email, Quote, Contract, Invoice, and Questionnaire templates, **Lead Capture Forms, Online Scheduling services, and complete Workflows**.
- Items are organized by industry (photographer, web designer, business coach, etc.) plus general-use collections.
- **Install flow:** purchase/download → items are **auto-loaded into your 17hats account** → seller-provided **Post-Purchase Instructions** guide customization to your brand.
- There is also peer-to-peer **Template Sharing** between accounts (help article "Template Sharing") — members can share templates directly, and one Capterra reviewer noted selling their own templates became "another revenue stream."
- Sellers apply via a Marketplace Sellers program (17hats.com/marketplace-sellers).

### 4.4 17hats University (17hatsuniversity.com)

- Positioned as "your virtual business school" — free education portal, launched via release notes as a first-class retention feature.
- Content types: **Quick Start Course**, **The Business Makeover course**, **webinars** (20-minutes-or-less business insights + 17hats feature webinars, with on-demand replays), **Quick Tips / Tutorials** (short task-level videos, e.g., "How to change the Calendar view", "The Bookkeeping Tab"), **Guides**, and a separate hosted **courses** subdomain (courses.17hatsuniversity.com) with login.
- Topics span both product training and general business education (marketing, process, lead management).
- No certification program found **[uncertain — none surfaced in search]**.
- Supporting cast: Help Center (Intercom-based, help.17hats.com) with video tutorial center; release-notes site (17hats.releasenotes.io); active official Facebook user Q&A group (17HatsUserQA); blog with feature walkthroughs; in-app chat support widely praised ("answer within minutes").

### 4.5 Assessment

Onboarding is heavily **human/education-led** (live workshops, videos, help articles) rather than product-led; the in-app experience itself reportedly lacks contextual tooltips and guided checklists, which is why "steep learning curve" is the consensus complaint across review platforms even while support quality scores are high.

---

## 5. Account structure (brands, users, permissions, settings map)

### 5.1 Account Settings map

Settings pages are organized into **four categories** (help article "Account Settings Overview"):

**Settings**
- **My Account** — brand information + list of linked Brands; membership/subscription management.
- **Brand Preferences** — internal look of 17hats + client-facing document look. Tabs: **Account** (brand name/details), **Logo** (brands client-facing documents, document emails, Client Portal), **Colors & Fonts** (button colors, accent fonts, button fonts on documents/emails), **Images** (image library, e.g., portal cover).
- **Email Settings** — incoming/outgoing email connection, document email reminders, email signatures.
- **Calendars** — create/update 17hats calendars; manage Google Calendar connection.

**Admin**
- **Users** — add users, manage team-member permissions.
- **Change My Login** — email/password.
- **Referrals** — referral link + code (credit/discount on annual+ subscriptions for referrer and referee).

**Account Templates**
- **Documents & Emails** — template library for Emails (Regular type and Document type with auto-appended action button), Quotes, Contracts, Invoices, Questionnaires. (Also reachable from the top toolbar shortcut.)
- **Workflows** — workflow template builder (action items can send any Email/Quote/Contract/Invoice/Questionnaire, create to-dos, etc.).
- Lead Capture Forms and Online Scheduling templates/services are managed from their feature areas **[uncertain: whether they also list under Account Templates]**.

**Money Matters**
- **Invoice Options** — global invoice settings; choose payment merchant (Stripe, Square, PayPal); currency; custom invoice footer; tips, save-card, recurring/automatic payments (Stripe); ACH.
- **Bookkeeping Options** — connect bank/credit-card accounts (feeds P&L, Sales Tax, receivables reports).
- **Products & Services** — reusable line-item catalog for quotes/invoices.

Also configured under settings/feature areas: **Client Portal** global customization (cover image, logo, welcome message, per-portal passwords) and **Online Scheduling**.

### 5.2 Brands (multi-brand under one login)

- Many members run multiple businesses; 17hats supports **Linked Brands managed under a single master login**.
- **Create:** click your logo/initials (top right, any page) → "Create New Brand." **Switch:** same top-right icon.
- Each Brand carries its **own branding** (logo, colors/fonts, images), and effectively its own client-facing identity across documents, document emails, and Client Portal; the My Account page lists all linked brands.
- **Each additional Brand is a paid add-on** (historically roughly the cost of an additional subscription at a discount; exact current pricing varies) **[uncertain on current price]**. Performance reportedly degrades ("takes longer to load") for accounts with multiple businesses (review reports).

### 5.3 Users & permissions (multi-user)

- **Three permission levels: Owner, Admin, Team Member.**
  - **Owner** — full control including business/billing settings.
  - **Admin** — everything except business settings and Owner settings; no granular choices ("there are no permission choices for Admin"); can create/delete Admin accounts and create/change/delete Team Members.
  - **Team Member** — granular, feature-by-feature permissions granted by Owner/Admin (help: "Users - Getting Started and Setting Permissions").
- **Multi-user calendars:** team calendars visible in the main Calendar view; events/projects can be assigned to users.
- **Seat economics (historical 3-tier era):** Essentials and Standard = 1 user only; **Premier included 3 users total** (owner + 2); extra users **$5/month** each. In **2025 17hats moved to a single all-inclusive plan** (third-party pricing teardowns), so seat rules may differ now **[uncertain on current seat count in the single plan]**.
- Workflows support **assignment** of tasks to users (mobile app mentions workflow assignment).

### 5.4 Tier gating that shaped the IA (historical, for reference)

- Essentials: contracts, invoices, basic workflows, 1 lead-capture form, limited reports (client sales, sales tax).
- Standard: + online scheduling, questionnaires, more reports (product sales), more forms.
- Premier: full/advanced workflow automation, up to 20 lead-capture forms, 3 users, all reports.
This matters for a competitor build: 17hats gates *automation depth*, *number of public forms*, and *seats* by tier.

---

## 6. Mobile apps (iOS & Android)

### 6.1 Identity

- **iOS:** App Store id 1069498016 ("17hats"), free. **Android:** Google Play package `com.isomnio.seventeenhats` (developer Isomnio = 17hats' original company name), free. Supports iPhone, iPad, Android.

### 6.2 What the app can do (from 17hats' own mobile-app feature page + help article)

- **Dashboard:** recent client activity, pending documents, upcoming to-dos.
- **Emails:** send from **existing email templates** to respond to leads quickly.
- **Contacts & Projects:** create new; view and **edit** existing; quick access to emails, phone numbers, locations; open contact address / project location **in maps**; edit and delete projects.
- **Calendar:** view and adjust calendar; create/edit/delete events.
- **Documents:** **send** an existing document, **counter-sign a contract**, view completed questionnaires.
- **To-dos:** view, add, edit; add to-do lists.
- **Workflows:** workflow assignment **[uncertain: extent — mentioned in feature summaries, likely limited to assigning/completing items, not building workflows]**.
- **Push notifications:** new Lead Capture Form submission, invoice payment received, questionnaire submitted, new Online Scheduling booking.

### 6.3 What the app cannot do (gaps vs web)

- **Cannot build/create invoices, contracts, or questionnaires** from the phone (competitor teardown, 2026: "the mobile app only allows viewing — you cannot create contracts, questionnaires, or invoices"; iOS reviewer: "can't create, send or receipt invoices" — note the help docs say you can *send* an already-built document, so the hard gap is document *creation/editing*).
- No template building, no workflow building, no bookkeeping/transaction categorization, no reports **[uncertain — inferred from absence in every feature list, consistent with "view-only with severe limitations" review language]**.
- Users report the **mobile web version is more capable than the native app** ("the app is not as up to date as using the mobile version of the website").

### 6.4 Ratings & complaints

- **iOS cumulative rating ~3.3/5** (JustUseApp analysis of 23 App Store reviews). UpdateStar users: 3/5. Exact current official App Store / Play Store star counts could not be scraped (both listings block automated fetch) **[uncertain on exact current figures]**.
- Company (not app) review context: **Trustpilot 3.2/5 "Average"**; **Capterra 4.4/5 (136 reviews)**; **G2 4.6/5 (114 reviews)**; ease-of-use praised on Capterra while mobile drags sentiment down.
- Recurring complaints:
  - **Stale releases** — "no app updates for over a year" (iOS review); "the app version needs to be updated, as the mobile [web] version offers several features the app is not set up to handle."
  - **Crashes** — calendar section "causing the app to close repeatedly."
  - **Sync bugs** — accepting bookings on the app vs laptop produced **duplicate client correspondence** (two identical invoices) multiple times for one reviewer.
  - **Booking workflow gaps** — no way to book a client internally without going out to the public booking page and re-asking for their info; no internal booking override.
- Recurring praise: quick on-the-go checks, sending documents "in minutes," push notifications for payments/leads.

### 6.5 Strategic read

17hats treats mobile as a **notification + triage companion** while all heavy creation stays on desktop web. This is the single most-cited product gap in reviews as of 2026 and an obvious wedge for a competitor (HoneyBook, by contrast, markets a full-featured mobile app).

---

## 7. Design language & UX reputation

- **Brand story:** named for the "17 hats" a solopreneur wears; founded by Donovan Janus (inspired by a 2011 NYT piece, "Maybe It's Time for Plan C"); top-hat 🎩 iconography; friendly, cheeky copywriting throughout the product ("Let's Take Care of Business").
- **Visual style:** clean but **dated**; multiple 2025–2026 teardowns state the interface "has not received a major redesign since the platform launched" (2014). Screens are form- and list-heavy; Projects offer only tile/list views — **no kanban boards, no Gantt charts, no drag-and-drop pipeline** (Plutio's core attack on it). Member-side branding customization (logos/colors) applies to *client-facing* documents, not the internal UI theme.
- **UX copy problem:** playful section names without explanation; reviewers note absence of tooltips/inline help forces trips to the Help Center.
- **Navigation friction:** "the transition is a bit clunky… users often having to take the long route" — e.g., dashboard to-dos not deep-linking to their project; document editor for contracts/questionnaires described as "an ancient interface" with text-selection glitches.
- **Density/scale:** interface "cluttered and overwhelming as client volume grows"; platform pitched at 1–3 person businesses and reviewers agree it strains beyond that.
- **Performance:** recurring reports of slow loads (worse with multiple brands), occasional glitches/"sometimes won't load at all," and some downtime incidents; no public status/performance SLA surfaced.
- **Accessibility:** **no accessibility statement, WCAG conformance claim, or screen-reader documentation found anywhere** on 17hats properties — treat as unaddressed (and as a differentiation opportunity).
- **What users love (keep in a clone):** everything-in-one-place consolidation; the morning-coffee dashboard ritual; automation that "tells you exactly what needs to be done today"; template-driven speed; fast human chat support; easy client-side experience (portal, signing, paying).

---

## 8. Build recommendations (for the competing app)

**IA to copy**
1. Keep the **7±2-item left nav**: Home, Leads, Clients, Projects, Calendar, Documents, Money, Automations, Settings. 17hats' contact→project→documents hierarchy is well-loved; preserve it.
2. Copy the **Project page pattern**: header details + Important Documents panel + Related Contacts + tabbed history (Notes / Emails / Files / To-dos / Events / Calls / Time / Activity). This is 17hats' best screen.
3. Keep an **omnipresent quick-create button** and **persistent search**, but make search **global** (contacts, projects, documents, emails, transactions) — 17hats' contacts-only search is a known weakness.
4. Keep the **brand switcher in the avatar menu** and design multi-brand in from day one (separate branding, templates, email identity per brand; shared login) — but avoid 17hats' per-brand performance degradation.

**Dashboard to copy-and-beat**
5. Rebuild the five widgets — mini week calendar (+weather; it's a beloved quirk for outdoor pros), recent client activity feed, pending documents chase-list, and a smart "today" queue fed by automations with snooze. Then fix its flaws: **deep-link every item to its record**, add plain-language section labels with tooltips, and add the missing **money snapshot** (outstanding invoices total, this-month revenue, overdue count).
6. Make the dashboard **customizable** (reorder/hide widgets) — 17hats offers none of that.

**Onboarding to improve**
7. Mirror the education stack cheaply (short task videos, weekly live onboarding call, help center), but add what 17hats lacks: an **in-app setup checklist** (connect email → branding → payment processor → calendar → first contact → first invoice), contextual tooltips, and optional **sample data** instead of "add yourself as a test contact."
8. Build a **template marketplace/starter-template gallery by industry** early — it is 17hats' stickiest onboarding asset (installed workflows = instant activation) and even a community revenue stream. Auto-install + post-install customization instructions are the pattern to copy.
9. Keep the **7-day no-card trial with restart**; walk users to *first invoice sent* as the activation milestone (17hats' First 24 Hours Workshop targets exactly this).

**Account structure**
10. Ship **Owner/Admin/Member** roles with granular member permissions; price seats cheaply ($5-ish) rather than gating whole tiers; gate on automation depth/forms if tiering is needed.

**Mobile strategy (biggest opening)**
11. Do not ship a view-only companion. Minimum parity bar: **create and send invoices/quotes on mobile**, edit documents, record payments, and full push-notification triage. 17hats' 3.3-star app with year-old builds is its softest flank.
12. Consider a high-quality **responsive PWA** first (17hats users already prefer its mobile web to the native app), then wrap natively.

**Quality bars 17hats misses**
13. Fast page loads at multi-brand/high-volume scale; a modern block-based document editor (their editor is the single most-hated component); WCAG 2.1 AA accessibility with a published statement; a public status page.

---

## 9. Sources

**17hats official (content extracted via search; direct fetch blocked)**
- Help: Tour of 17hats — https://help.17hats.com/en/articles/3110578-tour-of-17hats
- Help: 17hats Dashboard — https://help.17hats.com/en/articles/3110596-17hats-dashboard
- Help: Project Overview — https://help.17hats.com/en/articles/3110647-project-overview
- Help: How do I navigate the Project Overview screen — https://help.17hats.com/en/articles/928568-how-do-i-navigate-the-project-overview-screen
- Help: Projects vs. Contacts — https://help.17hats.com/en/articles/879690-projects-vs-contacts
- Help: Lead Overview — https://help.17hats.com/lead-capture/lead-overview-lead-capture-lead-overview-page
- Help: Account Settings Overview — https://help.17hats.com/en/articles/3156330-account-settings-overview
- Help: My Account Settings — https://help.17hats.com/en/articles/3110667-my-account-settings
- Help: Brand Preference Page Overview — https://help.17hats.com/en/articles/2108661-account-settings-brand-preference-page-overview
- Help: Brand Preferences - Colors & Fonts / Images / Account tabs — https://help.17hats.com/en/articles/3110814-brand-preferences-colors-fonts-tab , https://help.17hats.com/en/articles/3110802-brand-preferences-images-tab , https://help.17hats.com/en/articles/3110791-brand-preferences-account-tab
- Help: How do I add and use Linked Brands — https://help.17hats.com/en/articles/843598-how-do-i-add-and-use-linked-brands
- Help: Users - Getting Started and Setting Permissions — https://help.17hats.com/en/articles/840254-users-getting-started-and-setting-permissions
- Help: Working with Users — https://help.17hats.com/en/articles/2968814-working-with-users-in-17hats
- Help: Onboarding Step 1 (Set Up Your New Account) — https://help.17hats.com/en/articles/10447114-onboarding-step-1-set-up-your-new-17hats-account
- Help: Getting Started collection — https://help.17hats.com/en/collections/1817945-getting-started-with-17hats
- Help: The 17hats Mobile App — https://help.17hats.com/en/articles/3152558-the-17hats-mobile-app
- Help: 17hats Marketplace — https://help.17hats.com/en/articles/840250-17hats-marketplace
- Help: Template Sharing — https://help.17hats.com/en/articles/2551565-template-sharing
- Help: Client Portal Overview / Global Settings / Giving Access — https://help.17hats.com/en/articles/1131267-client-portal-overview , https://help.17hats.com/en/articles/3160018-client-portal-customizing-your-global-settings , https://help.17hats.com/en/articles/3160537-client-portal-giving-contacts-access
- Help: Calendar Overview — https://help.17hats.com/en/articles/894193-calendar-overview
- Help: Bookkeeping Overview — https://help.17hats.com/en/articles/3112838-bookkeeping-overview
- Help: Money Matters (Invoice Options / Bank Account / Products & Services) — https://help.17hats.com/en/articles/924380-money-matters-invoice-options , https://help.17hats.com/en/articles/928589-money-matters-connecting-your-bank-account , https://help.17hats.com/en/articles/849333-money-matters-products-services
- Help: Documents & Emails / templates — https://help.17hats.com/en/articles/3110651-17hats-documents-emails , https://help.17hats.com/en/articles/879803-how-to-create-manage-document-email-templates
- Help: Workflow Overview — https://help.17hats.com/en/articles/1046329-workflow-overview
- Help: All About To-Do Tasks — https://help.17hats.com/en/articles/2841749-all-about-to-do-tasks
- Marketing: Dashboard / Mobile App / Multi Brands / Multi Users / Lead Management / Calendar / Features / Pricing / About — https://www.17hats.com/features/dashboard , https://www.17hats.com/features/mobile-app , https://www.17hats.com/features/multi-brands , https://www.17hats.com/features/multi-users , https://www.17hats.com/features/lead-management , https://www.17hats.com/features/calendar , https://www.17hats.com/features , https://www.17hats.com/pricing , https://www.17hats.com/about
- First 24 Hours Workshop — https://www.17hats.com/first-24-hours ; Getting Started workshops — https://gettingstarted.17hats.com/ ; Self-guided tour — https://www.17hats.com/self-guided-tour ; Demo sign-up — https://www.17hats.com/demo-sign-up
- 17hats University — https://www.17hatsuniversity.com/ (webinars, guides, tutorials, courses.17hatsuniversity.com)
- Marketplace — https://marketplace.17hats.com/ ; seller program — https://www.17hats.com/marketplace-sellers
- Blog: Easy Navigation Within 17hats — https://blog.17hats.com/easy-navigation-within-17hats/ ; Action-Packed Dashboard — https://blog.17hats.com/the-action-packed-17hats-dashboard/ ; Marketplace posts — https://blog.17hats.com/jumpstart-your-journey-with-17hats-marketplace/ , https://blog.17hats.com/a-guide-to-utilizing-newly-installed-17hats-marketplace-items/ ; SMS Texting — https://blog.17hats.com/meet-17hats-sms-texting-instant-organized-client-conversations/
- Release notes — https://17hats.releasenotes.io/ (incl. "Welcome To 17hats University!", "Universal Client Portal Link")

**App stores & app-review aggregators**
- iOS App Store listing — https://apps.apple.com/us/app/17hats/id1069498016
- Google Play listing — https://play.google.com/store/apps/details?id=com.isomnio.seventeenhats&hl=en_US
- JustUseApp iOS review analysis (~3.3/5, 23 reviews) — https://justuseapp.com/en/app/1069498016/17hats/reviews
- InsiderApps — https://insiderapps.com/app/17hats ; UpdateStar — https://17hats.updatestar.com/

**Third-party reviews & teardowns**
- Capterra (4.4/5, 136 reviews) — https://www.capterra.com/p/144328/17hats/reviews/
- G2 (4.6/5, 114 reviews) — https://www.g2.com/products/17hats/reviews
- Trustpilot (3.2/5) — https://www.trustpilot.com/review/www.17hats.com
- Software Advice — https://www.softwareadvice.com/bpm/17hats-profile/reviews/
- GetApp — https://www.getapp.com/collaboration-software/a/17hats/
- Zendo: 17hats vs Tave (UX copy/navigation critique) — https://getzendo.io/blog/17hats-vs-tave/ ; 17hats pricing — https://getzendo.io/blog/17hats-pricing/
- Plutio: "Still Using 17hats? It Has No Kanban or Gantt Charts" — https://www.plutio.com/freelancer-magazine/still-using-17hats ; Dubsado vs 17hats — https://www.plutio.com/compare/dubsado-vs-17hats
- Agiled vs 17hats (mobile view-only claim) — https://agiled.app/compare/agiled-vs-17hats
- HoneyBook comparison/alternatives — https://www.honeybook.com/blog/honeybook-vs-17hats , https://www.honeybook.com/blog/17hats-alternative
- AgencyHandy review & portal overview — https://www.agencyhandy.com/17hats-reviews/ , https://www.agencyhandy.com/client-portal/17hats/
- Pricing teardowns (single-plan shift) — https://onesuite.io/blog/17hats-pricing/ , https://taskip.net/17hats-pricing/
- Improve Photography in-depth review — https://improvephotography.com/52314/how-to-manage-your-photography-business-17hats-in-depth-review/
- Staged4more review — https://www.staged4more.com/blog/review-17hats ; Spruce Rd. review — https://sprucerd.com/blog/17hats/

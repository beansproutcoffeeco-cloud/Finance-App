# 17hats: CRM, Leads & Contact Management

Research date: 2026-07-07. Sources: help.17hats.com knowledge base (via search digests — direct fetch blocked by Cloudflare), 17hats.com feature pages, 17hats blog, third-party tutorials (Deb Mitzel Creative, Jebb Graff, 17hats University), review sites (Capterra, G2, Software Advice, Trustpilot), and competitor comparisons. Where sources conflicted or content could not be verified verbatim, it is flagged as *(uncertain)*.

---

## 1. Summary

17hats' CRM is deliberately simple: it is a **contact-based system** with exactly four hard-coded contact types (Hot Lead, Client, Cold Prospect, Other), color-coded throughout the UI. There is **no separate "lead object"** — a lead *is* a contact whose type is Hot Lead or Cold Prospect. All actual work (emails, documents, notes, tasks, events) hangs off **Projects**, not contacts: every contact needs at least one project before you can send them anything, and one contact can have many projects.

The lead engine is the **Lead Capture Form (LCF)**: a hosted/embeddable form that, on submission, automatically (1) creates or matches a contact by email, (2) always creates a **new project**, (3) applies contact/project tags, (4) records a Lead Source, (5) fires a Dashboard/email/push notification, (6) sends a one-time auto-response email, and (7) kicks off a **Workflow** (optionally chosen dynamically from the answer to a "Choose from a List" question). Leads can also arrive by email-parsing rules (The Knot / WeddingWire / ShowitFast), Online Scheduling bookings, CSV import, Zapier, or manual entry (which reuses an LCF internally).

Lead→client conversion is **automatic and event-driven**: sending an invoice, an accepted quote, or a signed contract flips the contact type to Client. Reporting covers **Lead Sources** (up to 25, bar-chart over time) and **Referral Sources** (from the contact's "Referred By" field). Organization is tag-driven (contact tags vs project tags), with tags also powering the newer **Pipelines** kanban-ish feature. Notable gaps to exploit in a competing build: no contact merging/dedup tooling found, no lead scoring, weak list views (no kanban for leads), LCF count capped by plan tier, single main contact per project, and dated UI.

---

## 2. Contact model

### 2.1 What a Contact is

- "The customers you communicate with in 17hats are defined as Contacts" — any person, company, or vendor. Unlimited contacts on all plans (CRM itself is marketed as "free CRM for life" on paid sign-ups).
- Contacts are **individual-first** with an optional company; a "Show as company" checkbox makes the company name display in lists instead of the person's name (that's the extent of "company records" — there is no separate Company/Account entity).

### 2.2 Contact types (fixed enum, color-coded)

| Type | Color | Meaning | Where it lives |
|---|---|---|---|
| Hot Lead | Orange | Potential customer you are actively converting | **Leads** page |
| Cold Prospect | Blue | Was interested, stopped actively communicating | **Leads** page |
| Client | Green | Accepted a quote, was sent an invoice, or signed a contract | **Contacts** page |
| Other | Grey | Vendors, partners, anyone else | **Contacts** page |

- Colors are **not customizable**; types are **not user-definable** (a frequent limitation vs. bigger CRMs).
- Type is edited via the "Edit Contact" screen (dropdown: Client / Hot Lead / Cold Prospect / Other Contact) from the Leads page row "Edit" button or the contact/project page edit button.
- Hot Leads and Cold Prospects **always** appear on the Leads page; Clients and Others on the Contacts page. The type doubles as the pipeline status.

### 2.3 Standard contact fields

Quick-add ("Basic Contact Form") fields:
- Name (required; may include middle name/suffix), Company (optional, + "Show as company" checkbox), Email (optional but strongly recommended — it drives email sync and dedup matching), Phone (optional), Title (optional), Tags (optional), Contact Type.

"Full Contact Form" / Edit Contact adds:
- Profile image (custom avatar)
- Website
- Birthday
- Address, Address 2, City, State, Zip, Country
- **Referred By** (free-text; feeds Referral Source Reporting; auto-filled by Lead Source when blank)
- Notes
- Social links: Facebook, LinkedIn, Twitter, Instagram, Pinterest
- Custom Contact Fields (see 2.5)

CSV import header vocabulary reveals the fuller underlying field set (import accepts many synonyms):
- Name: first name / firstname / first / given name; last name / lastname / last / family name; middlename; suffix; title
- Company: company / company name / business name / business
- Email: email / e-mail / e-mail address
- Phones (large set): assistant's phone, business fax, business phone, business phone 2, callback, car phone, company main phone, home fax, home phone, home phone 2, mobile phone, fax, other fax, other phone, pager, primary phone. Format expected `888-888-8888`.
- Addresses: street / address 2 / city / state / zip / postal code / country, each prefixable with business / home / other (i.e., multiple address slots per contact)
- Website: web page / website / url
- Notes
- Tags (comma- or semicolon-separated)
- Project columns can be included in the same CSV to bulk-create projects (project name, dates, etc.) *(exact project header list not verified)*

Export: only **Contact Details** export (CSV), filterable by contact type or contact tag. Contact Custom Fields export; **Project Custom Fields do not**. Project data (documents, emails, time logs) cannot be bulk-exported — a well-known lock-in complaint.

### 2.4 Tags

- Two independent tag namespaces: **Contact Tags** (group/search/filter people) and **Project Tags** (label/filter services provided). Rationale: a contact can have many or zero projects, so the two must be filterable independently.
- Tags filter the Contacts, Leads, Projects, and Recent Client Activity pages and enable **bulk actions** (add/remove tags in bulk via a Bulk Actions dropdown; can apply Project Tags, Contact Tags, or both at once).
- **Tag Management** screen (Account Settings): rename a tag (renames across current + archived contacts/projects; caveat — tags applied via a "Choose One" LCF/questionnaire answer must be deleted and re-added on the form for the new name to stick), delete with confirmation, and **merge two tags** (all users of tag A now have tag B). Note: tag merge exists; *contact* merge does not (see 2.8).
- Automatic tagging: LCF submissions and Online Scheduling bookings can auto-apply contact and/or project tags; Advanced Workflows (Premier tier) can **add or remove** tags as workflow steps; Lead Sources can each carry tags to apply.
- Tags are load-bearing infrastructure: they drive Pipelines (a project tag moves a project into/through/out of a pipeline phase), conditional workflow triggering, and even team assignment (the documented way to "assign" a project to a team member is… adding their name as a project tag).

### 2.5 Custom Fields

- Defined in **Account Settings → Custom Fields**, two tabs: Contact Fields and Project Fields. Unlimited count; unlimited per contact/project.
- Field types: **Short Field** (single-line text), **Long Field** (multi-line), **Yes/No**, **Choose from a List** (single select), **Checkboxes** (multi-select), **Date**.
- Guidance: Contact fields = info about the person (parent's phone, industry, preferred communication method); Project fields = info about the engagement (wedding date, meal selection, session notes).
- Custom Contact Fields display in the "Contact Details" section of the contact record (edit via its "edit" button).
- Usable as **tokens** in email templates, contracts/documents, and client-portal welcome messages; usable as **"Maps To" targets** in Lead Capture Forms, Questionnaires, and Online Scheduling questions (Answer Mapping — question type must match field type).
- Gotchas documented: Team Member users cannot create/edit custom fields; editing a custom field requires revisiting every LCF/questionnaire "maps to" selection that referenced it.
- Availability: Custom Fields arrived ~2018–19 (release notes); feature pages market it on paid plans. *(Exact tier gating unverified.)*

### 2.6 Related Contacts

- Each project has exactly **one main contact**, but unlimited **Related Contacts** (spouse, parent, coworker, planner…). Added from the project page via a "+" next to the Related Contacts header (pick existing or create new).
- Related contacts can receive questionnaires, quotes, contracts, invoices, and emails, and can be **contract signees**.
- Clients can add their own related contacts through a questionnaire question type built for it.
- This is 17hats' answer to multi-party engagements (weddings: bride + groom) without a many-to-many contact↔project model.

### 2.7 Activity history on a contact

- History is **project-scoped**, not contact-scoped. The project page has bottom tabs: **Notes, Emails, Files, To-Dos, Events, Phone Log, Time Log, Activity Log** — each with a "+" to add entries; notes are auto-timestamped.
- The **Activity tab** logs timestamped system events: document created/sent/deleted, booking created/rescheduled/canceled, etc.
- **Email sync**: connecting an IMAP/OAuth inbox makes 17hats poll every ~20–45 minutes and file client emails into the matching **project** — only for senders whose email address already exists on a contact *and* who have a project to store the mail in (no project → mail not imported; archived contact → mail not imported). Emails can be manually moved between projects.
- Contact-level view: the contact record shows contact details, its projects list, and related info; but the day-to-day timeline lives per-project. *(No evidence found of a unified cross-project activity timeline on the contact record.)*

### 2.8 Duplicate handling & merging

- **Dedup at capture**: LCF submissions match on **email address**. Existing email → no duplicate contact; a **new project** is attached to the existing contact instead. New email → new contact + project.
- Auto-responses only send to contacts **not already in 17hats** (another dedup-aware behavior).
- **No contact-merge feature found.** Extensive searching surfaced no help article, release note, or tutorial for merging duplicate contacts (tag merge exists; contact merge does not). Practical consequence: duplicates created via CSV import (e.g., same person under two emails) or manual entry must be cleaned up by hand — move projects to the surviving contact (a "Move Projects Between Contacts" capability exists per release notes) and delete the duplicate. *(Absence of the feature is inferred from absence of documentation; flagged as high-confidence but not verbatim-confirmed.)*
- Deletion safety: Account Settings → **Restore** shows contacts and projects deleted in the last **30 days**, restorable; restoring a project restores its contact; a project deleted within 10 minutes of its contact auto-restores with it. Hard delete removes documents and bookkeeping records permanently. 17hats recommends **archiving** instead of deleting (reversible; archived contacts stop importing email).

---

## 3. Lead lifecycle

### 3.1 Entry channels

1. **Lead Capture Form** (hosted/embedded) — the primary channel; auto-creates contact (type Hot Lead) + project.
2. **Lead Capture Email rules** — 17hats watches a connected inbox for lead-notification emails from **The Knot, WeddingWire, ShowitFast** and parses them into new lead + project. Five settings per rule: source site, watched email address, and auto-response toggle among them; one rule per source site. Explicitly *not* an API integration — it is inbox parsing, and breaks when the source changes its email format (there is a dedicated "how to reconnect" help article).
3. **Online Scheduling booking** — confirmed booking auto-creates contact + project + event on the chosen calendar; service booking questions can include a Lead Source question.
4. **Manual entry** — Leads tab "+" button opens a dialog that **reuses one of your Lead Capture Forms** to enter the lead internally; on save the person becomes a Hot Lead with a new project and the form's workflow starts. Options at save time: "Approve before sending" (workflow's automatic sends become approval steps) or "Continue as normal". Internal entries **never** fire the auto-reply email. Alternative: plain Basic Contact Form (but then you create the project yourself).
5. **CSV import** (Contacts tab → gear icon → Import → CSV) and **Zapier** (triggers: New Contact, Contact Updated; actions: Create Contact, Update Contact — contacts only in v1; Zapier gated to current subscription plans).

### 3.2 Statuses and the funnel

- The "pipeline" is the contact-type enum: **Hot Lead → Client**, with **Cold Prospect** as the parking lot and **Archive** as the exit.
- Documented lead-management loop: **Capture** (LCF) → **auto-respond** → **Qualify** (send questionnaire via workflow; vet fit) → **quote/schedule a call** → either start the **Booking Process workflow** or **turn to Cold Prospect + archive the project** (17hats suggests ending lead workflows with a to-do reminding you to do exactly that).
- **Automatic conversion to Client** happens the moment any of these occurs:
  - an **invoice is sent** (some newer articles say "payment made on an invoice" — the canonical FAQ says *sent*; treat as: invoice event converts) *(minor source conflict noted)*,
  - a **quote is accepted**,
  - a **contract is signed**.
- Manual conversion: Leads page → Edit → Edit Contact → change Contact Type. Same mechanism for demoting to Cold Prospect or Other.
- There is **no finer-grained lead status** (no "contacted/qualified/proposal" stages) built into the contact model — users approximate stages with tags, Workflows, and (since ~2024) **Pipelines**:
  - Pipelines: up to **10 pipelines × 5 phases**, each phase bound to a **project tag** ("By Tag" phases); tag added → project appears in that phase; optional **Completed State** tag removes the project from the pipeline. Available on Premier / Founding memberships. It is a visualization over tags, not a new data model.
  - Legacy **Lifecycles** (a 4–7 stage visual ribbon on projects, selectable per LCF) still appear in older docs/settings; newer plan matrices say Lifecycles are not in the current Free CRM/Essentials/Standard/Premier lineup — effectively superseded by Pipelines. *(Transitional/conflicting documentation; both described because both appear in current help content.)*

### 3.3 Notifications

- Every LCF submission surfaces in the Dashboard's **"Let's Take Care of Business"** queue (groupable by Leads / Documents / To-Dos / Emails), deep-linking into the new lead's project; optional **email** notification and **mobile push** ("someone submitted a Lead Capture Form"); at least one source mentions text notification for new leads *(SMS unverified)*.

---

## 4. Lead Capture Forms

### 4.1 Form settings (the "nine settings")

Per-form configuration (Leads tab → Lead Capture Forms; also under Account Settings):

1. **Title** — internal name; recommended to name by placement ("Website Contact — Homepage") since you should build one LCF per placement for source attribution.
2. **Project Name** — the name given to the auto-created project (e.g., "Wedding Photography").
3. **Notification** — Dashboard notification is always on; toggle email notification.
4. **Workflow** — workflow template to auto-start on every submission, **or** dynamic selection: map each answer of a "Choose from a List" question to a different workflow.
5. **Message (post-submit behavior)** — three options: redirect to a URL, show a custom message, or do nothing/refresh.
6. **Contact Tags** — tags auto-applied to the contact record (project tags can also be applied — via lead source tags, question mapping, or form settings).
7. **Auto-Response** — sends a chosen "Lead Auto-Responder" email template immediately, **first submission only / new contacts only** (workaround for repeat inquiries: put the first email inside the triggered workflow instead).
8. **Calendar** — which calendar the project's event lands on.
9. **Lifecycle** — lifecycle to start the project in *(legacy setting; see 3.2)*.

### 4.2 Question builder

- Mandatory on every form: **Name** and **Email Address** fields. Default sample form: name, email, phone, message.
- Unlimited questions allowed; 17hats recommends 4–6. Each question can be required or optional. Drag-to-reorder *(implied by "drag and drop Lead Sources into desired order")*.
- Question types:
  - **Short Answer** (one line)
  - **Long Answer** (paragraph)
  - **Choose from a List** (single select — can drive workflow selection and apply tags per answer)
  - **Checkboxes** (multi select)
  - **Yes/No**
  - **Date** (calendar picker — commonly mapped to project/event date)
  - **File Upload** (< 9.4 MB)
  - **Lead Source** (special type: renders the account's Active Lead Sources as options; answer writes to the project's Lead Source field and to reporting; auto-fills contact "Referred By" if blank)
  - **Text** (static instructions block, non-input)
  - **Heading** (visual section divider, non-input)
- **Answer Mapping ("Maps To")**: any question can map to built-in contact fields (e.g., phone, address, "Person referred by"), built-in project fields (project date, etc.), **custom contact/project fields** (types must match), or **Project Notes** (mappable multiple times; each mapped answer becomes its own note in question order). Pre-existing field data pre-fills mapped questions in later questionnaires; client can overwrite.
- Non-mapped answers land on the project as the submission record *(visible from the lead's project; exact rendering unverified)*.

### 4.3 Styling

- Defaults: black text, white background, button color from Brand Preferences (Account Settings → Brand Preferences → Colors & Fonts controls fonts/button styling globally for client-facing forms).
- Per-form overrides at the bottom of the LCF edit screen: background/accent colors via color picker or hex codes; header image; goal is seamless embed against the host site. Different palettes per placement = duplicate the form ("Edit → Duplicate") and recolor.

### 4.4 Install / embed options ("Install Form" button on the form page)

1. **Link to 17hats Form** — hosted form URL (use anywhere: email, bio links, blog, social; opens in new window).
2. **Link to Dialog Window** — HTML snippet that renders a link opening the form in a pop-up dialog.
3. **Insert Form on Website** — **iframe** snippet, sized to fill its container. Known issues: WordPress.com strips iframes (workarounds: embed widget plugins, hosted link, or self-hosted WP); mobile rendering is the host site's responsibility.
4. **Facebook / social** — hosted link used as a Facebook Page button, in Messenger auto-reply ("Response Assistant"), or on LinkedIn business pages. (No native FB Lead Ads integration found.)
- Forms can be **disabled** (Edit → Disable): visitors with the link see "information has been removed by the Account Owner"; disabled forms are editable and re-enablable, and show a disabled icon in the list.
- No CAPTCHA / spam protection is documented — a gap users notice.

### 4.5 Submission pipeline (what actually happens)

On submit:
1. Contact lookup by **email**; create contact (type **Hot Lead**) or reuse existing.
2. Create a **new Project** (named from the form's Project Name setting) under that contact — *always*, even for repeat submitters.
3. Write mapped answers to contact/project/custom fields and Project Notes; record Lead Source (and copy to "Referred By" if blank); attach submission answers to the project.
4. Apply configured contact/project tags (which may drop the project into a Pipeline phase and/or select the workflow).
5. Create project event on the configured calendar (when a date is captured) *(behavior inferred from Calendar setting + booking parallels)*.
6. Fire notifications (Dashboard "Let's Take Care of Business", optional email, mobile push).
7. Send Auto-Response (first-time contacts only).
8. Start the configured **Workflow** (fixed or answer-selected); workflow steps can send emails/questionnaires/quotes/contracts/invoices, create to-dos, apply/remove tags (Premier), start other workflows, archive the project, or change its calendar. 17hats even documents a pattern for **fully automated selling**: LCF → workflow → auto-send invoice.
9. Post-submit UX per the Message setting (redirect / message / nothing).

### 4.6 Plan gating (current subscription lineup)

- Essentials (~$13/mo annual): **1** LCF, 20 documents/mo, 1 scheduling service.
- Standard (~$25/mo): **3** LCFs, 35 documents/mo.
- Premier (~$50/mo): **20** LCFs, unlimited documents, advanced automations (tag add/remove in workflows, etc.).
- Lead Source Reporting: Standard & Premier. Pipelines: Premier (and legacy Founding members). Zapier: current subscription plans only. *(Older "Level One/Two/Three" membership naming appears in some articles; treat tier names as in flux.)*

---

## 5. Lead sources & reporting

- **Lead Sources** are an account-level managed list, capped at **25**, maintained under **Leads → Reporting**; sorted alphabetically there, but drag-orderable within each LCF question.
- Each Lead Source has a status:
  - **Active** — appears as an option on LCF/Online Scheduling Lead Source questions and on report charts.
  - **Inactive** — hidden from forms, still charted.
  - **Archived** — hidden from both.
- Each Lead Source can carry **contact/project tags** to auto-apply when chosen.
- Capture points: LCF Lead Source question (required or optional), Online Scheduling service questions. Manual entry also counts because internal lead entry reuses LCFs. The chosen source is stamped on the **project** (visible under Project Details).
- **Reporting**: bar chart of leads per source over a selectable timeframe, under Leads → Reporting. Counted by **project creation date** (not booking/event date).
- **Referral Source Reporting** (separate report, same Reporting section): aggregates the contact-level **"Referred By"** field — who refers you, how many referrals, their impact. Populated manually, via Lead Source auto-copy (when blank), or via a Short Answer question mapped to "Person referred by".
- Feature launched mid-2023 (blog: "Boost Your Business with 17hats Lead Source Reporting"); before that users tracked sources with tags.
- Gap: no conversion-rate or revenue-per-source reporting is documented — counts only. *(Confirmed only counts/bar charts in all sources.)*

---

## 6. UX flows (screens & day-to-day)

- **Left-rail navigation**: Dashboard, Leads, Contacts, Projects, Documents, Calendar, Bookkeeping/Finance, etc. (Leads and Contacts are separate top-level pages.)
- **Dashboard**: "Let's Take Care of Business" action queue (filter/group: Leads, Documents, To-Dos, Emails) — the intended morning-routine surface where new leads appear; plus optional email-needs-reply items.
- **Leads page**: list of Hot Leads (orange) + Cold Prospects (blue); "+" to add a lead (via LCF dialog); per-row **Edit** (Edit Contact, etc.); filter by tags; bulk actions via selection. Sub-areas: **Lead Capture Forms** (form list/builder) and **Reporting** (Lead Sources + Referral List). No kanban/board view of leads; Pipelines (projects-by-tag) is the closest visual.
- **Contacts page**: Clients (green) + Others (grey); search; tag filters; gear icon → import (CSV) / export.
- **Contact record**: header with photo/name/company/type color; Contact Details panel (standard + custom fields; edit button); Projects list; Related Contacts; notes. Day-to-day work happens one level down on the project.
- **Project page** ("manila folder" metaphor): project details (incl. Lead Source, project date, tags, lifecycle/pipeline state), main contact + related contacts, documents; bottom tabs Notes / Emails / Files / To-Dos / Events / Phone Log / Time Log / Activity.
- **Recent Client Activity page**: cross-account feed of document events (invoice paid, contract signed…) filterable by contact, project, activity type, tag, date.
- **Typical day-to-day lead flow**: push/dashboard notification → open lead's project from the notification → review LCF answers/notes → workflow already sent the auto-reply/questionnaire → user sends quote → quote accepted → contact silently flips to Client (moves from Leads page to Contacts page) → booking workflow continues.
- **Mobile app** (iOS/Android): full contact info access, push notifications for LCF submissions, questionnaire completions, quote acceptances, contract signatures, invoice payments. Reviews say the app lags the web feature set.

---

## 7. Inferred data model (schema sketch)

```
ACCOUNT
 ├─ users (owner + team members; team cannot edit custom fields)
 ├─ brand_preferences (colors, fonts, button styles → client-facing forms)
 ├─ custom_field_definitions
 │    id, scope ENUM(contact|project), label,
 │    type ENUM(short_text|long_text|yes_no|single_select|multi_select|date),
 │    options[]                       -- for selects/checkboxes
 ├─ tags            (id, name, scope ENUM(contact|project))   -- rename/merge/delete ops
 └─ lead_sources    (id, name, status ENUM(active|inactive|archived),
                     auto_tags[], sort_order)                 -- max 25

CONTACT
  id, account_id
  type ENUM(hot_lead, cold_prospect, client, other)   -- fixed; color derived
  show_as_company BOOL
  first/middle/last name, suffix, title, company
  emails[] (primary drives matching), phones[] (typed: mobile/home/business/fax/…)
  addresses[] (typed: home/business/other → street, addr2, city, state, zip, country)
  website, birthday, profile_image
  social {facebook, linkedin, twitter, instagram, pinterest}
  referred_by TEXT            -- feeds Referral report; auto-filled from lead source
  notes TEXT
  tag_ids[] (contact-scoped)
  custom_field_values[] (contact-scoped defs)
  archived BOOL, deleted_at (30-day restore window)
  -- state transitions: hot_lead/cold_prospect → client ON (invoice sent |
  --                    quote accepted | contract signed); manual override anytime

PROJECT                        -- unit of work; ALL activity attaches here
  id, contact_id (exactly one main contact)
  name, project_date/event_date, calendar_id
  lead_source_id, lifecycle_id/stage (legacy), tag_ids[] (project-scoped)
  custom_field_values[] (project-scoped)
  archived BOOL, deleted_at
  ├─ related_contacts[] (contact_id, role?)  -- can receive/sign documents
  ├─ notes[] (timestamped; some auto-created from mapped answers)
  ├─ emails[] (synced by sender-email match, every 20–45 min)
  ├─ files[], todos[], events[], phone_log[], time_log[]
  ├─ activity_log[] (system events: doc created/sent/deleted, booking changes)
  └─ documents[] (quotes/contracts/invoices/questionnaires → conversion triggers)

LEAD_CAPTURE_FORM
  id, title, project_name_template
  notify_email BOOL, auto_response_template_id (fires once per new contact)
  workflow_binding {mode: fixed | by_answer(question_id, answer→workflow map)}
  post_submit {mode: redirect|message|none, url?, message?}
  auto_contact_tags[], calendar_id, lifecycle_id
  style {bg_color, accent_color, header_image}   -- + brand defaults
  status ENUM(enabled|disabled)
  └─ questions[] (ordered)
       type ENUM(short, long, single_select, checkboxes, yes_no, date,
                 file(<9.4MB), lead_source, static_text, heading)
       required BOOL, options[]
       maps_to → {contact_field | project_field | custom_field(type-matched)
                  | referred_by | project_notes (repeatable)}
       per-answer: tag(s), workflow selection (single_select only)

SUBMISSION (implied)
  form_id, matched_or_created contact_id (match key = email), new project_id
  answers[] → mapping writes; side effects: tags, lead source stamp,
  notification(dashboard/email/push), auto-response?, workflow instance

EMAIL_LEAD_RULE                 -- The Knot / WeddingWire / ShowitFast
  source ENUM, watched_inbox (must be a connected Incoming Email),
  auto_response BOOL, … (5 settings) → parses notification emails → contact+project

PIPELINE (Premier; ≤10 per account)
  name, phases[≤5] {name, trigger_project_tag}, completed_state_tag?
  membership computed from project tags (no dedicated FK)

WORKFLOW (template → instance per project)
  steps: send email/questionnaire/quote/contract/invoice, create to-do,
  pause/wait, add/remove tags (Premier), start workflow, archive project,
  change calendar
```

Key relationship rules: Contact 1—N Projects (≥1 required to do anything); Project N—N Related Contacts; Contact/Project N—N Tags (scoped); LCF submission ⇒ always a new Project; email→project routing via sender address; conversion is an event trigger on document state, not a user action.

---

## 8. Strengths / weaknesses

### Strengths (worth copying)
- **Zero-friction lead intake**: one form submission yields contact + project + tags + source + notification + auto-reply + running workflow. Nothing to triage manually.
- **Email-based dedup at capture** — repeat inquirers get a new project, not a duplicate contact; auto-reply suppression for known contacts is a thoughtful touch.
- **Answer Mapping** into standard *and* custom fields (and repeatable Project Notes) kills re-keying; later questionnaires pre-fill from stored data.
- **Dynamic workflow routing** off a single dropdown answer ("What are you interested in?") — cheap but powerful branching.
- **Automatic lead→client conversion** on invoice/quote/contract events — the CRM status maintains itself.
- **Contact vs Project separation** — clean handling of repeat clients (new project per engagement, history preserved per engagement).
- Internal lead entry reusing the same LCF (with "approve before sending" safety) keeps phone-inquiry data identical to web-inquiry data.
- Lead source + referral reporting simple enough that solopreneurs actually use it; 30-day restore trash; archive-first philosophy.

### Weaknesses / user complaints (found in reviews & comparisons)
- **Fixed 4-type lifecycle**; no custom stages, no lead scoring, no "nurture" concepts. Users fake stages with tags.
- **No kanban/list-view flexibility** for leads; no Gantt/board views (Pipelines is capped at 10×5 and tag-driven only, Premier-only).
- **No contact merge / dedup tooling** for messes created outside LCFs (imports, manual adds).
- **LCF caps by plan** (1/3/20) called out as limiting for multi-channel marketers; no CAPTCHA/spam controls; iframe embed issues on WordPress.com; forms look dated without heavy color work.
- Email lead "integrations" (Knot/WeddingWire) are brittle inbox parsers that break on format changes.
- Email sync latency (20–45 min) and the "no project → email not captured" rule confuse users; emails from not-yet-saved addresses are silently missed.
- **Team scaling is poor**: assignment = project tags; per-reviewer "not good for organizing leads across team members / controlling visibility"; team members can't manage custom fields.
- Exports limited to contact details → data lock-in complaints; interface widely described as dated/clunky; mobile app lags web; support described as slow to act on feature requests (2,700/yr backlog line).
- Lead reporting = counts only; no conversion or revenue attribution per source.

---

## 9. Build recommendations (for a competing product)

**Copy (table stakes proven by 17hats):**
1. Form → (match-or-create contact by email) → new engagement/project → tags → source → notification → auto-reply → workflow, as one atomic pipeline.
2. Answer mapping to standard + custom fields with type checking, repeatable notes mapping, and pre-fill of known values in later forms.
3. Auto-conversion of lead→client on money/commitment events (invoice, accepted quote, signed contract) with manual override.
4. Contact/engagement split with related contacts who can receive and sign documents.
5. Lead source master list with active/inactive/archived states and per-source auto-tags; referral ("referred by") tracking as a first-class field.
6. Soft-delete with 30-day restore; archive-first UX; auto-reply suppression for existing contacts.
7. Internal "log a lead" flow that reuses the public form definition with an approve-before-send mode.

**Improve (clear gaps to differentiate on):**
1. **Custom pipeline stages** per lead type + true kanban lead board with drag-to-stage (17hats' #1 structural gap).
2. **Merge & dedup tooling**: duplicate detection (email/phone/name fuzzy), one-click merge with field-level survivorship, plus merge preview.
3. Lead reporting with **conversion rates and revenue per source/UTM**, not just counts; capture UTM params on embedded forms automatically.
4. **Spam protection** (honeypot + turnstile/reCAPTCHA) and a modern embed (script-based auto-resizing widget, not raw iframe); unlimited forms — don't meter the top of funnel.
5. Real **team features**: lead assignment/round-robin, ownership, per-user visibility — reviewers explicitly leave 17hats when they hire.
6. Contact-level **unified timeline** across all projects (17hats scatters history per project).
7. Instant email ingestion (webhook/push IMAP) and capture of emails from unknown senders into a triage inbox instead of dropping them.
8. Full-fidelity export (contacts + projects + custom fields + activity) — counter their lock-in complaints.
9. Native integrations (FB Lead Ads, webhooks, public API) instead of inbox-parsing hacks.

**Skip / deprioritize:**
1. Legacy Lifecycles-style visual ribbon (17hats itself is superseding it with Pipelines) — build one staging concept, not two.
2. Facebook page-tab installs and Messenger auto-reply links (low-value, platform-fragile).
3. Email-parsing "integrations" for wedding directories unless targeting that vertical (brittle; prefer API/webhook or a generic parse-rule builder).
4. Contact-type color hardcoding — make statuses/colors configurable from day one instead.
5. 25-source cap, 10×5 pipeline cap, per-plan form caps — arbitrary limits users resent; use fair-use limits instead.

---

## 10. Sources

Help center (help.17hats.com) — content obtained via search digests (direct fetch returned HTTP 403):
- https://help.17hats.com/en/articles/924376-17hats-contact-types
- https://help.17hats.com/en/articles/3110603-contact-types
- https://help.17hats.com/en/articles/3110621-adding-contacts-to-17hats
- https://help.17hats.com/en/articles/924374-how-do-i-manually-add-a-contact
- https://help.17hats.com/en/articles/934801-how-do-i-import-a-csv-file-of-contacts-and-projects
- https://help.17hats.com/en/articles/843725-how-do-i-export-my-contact-list
- https://help.17hats.com/en/articles/934803-related-contacts
- https://help.17hats.com/en/articles/924366-how-do-i-allow-my-clients-to-add-related-contacts-through-questionnaires
- https://help.17hats.com/en/articles/2545832-custom-fields
- https://help.17hats.com/en/articles/2545940-answer-mapping-in-questionnaires-lead-capture-forms
- https://help.17hats.com/en/articles/879690-projects-vs-contacts
- https://help.17hats.com/en/articles/3110647-project-overview
- https://help.17hats.com/en/articles/3110631-17hats-projects
- https://help.17hats.com/en/articles/3388289-17hats-vocabulary / 3388927-17hats-terminology
- https://help.17hats.com/en/articles/853251-lead-capture-forms-overview
- https://help.17hats.com/en/articles/3113718-lead-capture-form-details
- https://help.17hats.com/en/articles/3113231-lead-capture-forms-building-your-first-lcf
- https://help.17hats.com/en/articles/10167140-lead-capture-form-question-types
- https://help.17hats.com/en/articles/2795306-installing-your-lead-capture-form
- https://help.17hats.com/en/articles/1788022-installing-your-lead-capture-form-on-your-facebook-linkedin-business-or-other-social-networking-page
- https://help.17hats.com/en/articles/2865468-adding-your-lead-capture-form-to-facebook-messenger
- https://help.17hats.com/en/articles/923888-why-is-my-lead-capture-form-not-appearing-correctly-on-my-website
- https://help.17hats.com/en/articles/839946-how-do-i-edit-the-colors-in-my-lead-capture-form
- https://help.17hats.com/en/articles/6581237-disable-lead-capture-forms
- https://help.17hats.com/en/articles/1131025-lead-capture-auto-replies
- https://help.17hats.com/en/articles/928565-lead-overview-lead-capture-lead-overview-page
- https://help.17hats.com/en/articles/3113059-lead-management-process-overview
- https://help.17hats.com/en/articles/2509970-manually-adding-leads
- https://help.17hats.com/en/articles/977936-when-do-hot-leads-automatically-turn-into-clients
- https://help.17hats.com/en/articles/879529-changing-a-lead-to-a-client
- https://help.17hats.com/en/articles/840255-automated-lead-workflows
- https://help.17hats.com/en/articles/1828264-all-about-workflows-triggering-your-workflow
- https://help.17hats.com/en/articles/2198457-send-automated-invoices-using-lead-capture-forms-and-workflows
- https://help.17hats.com/en/articles/2823021-email-lead-capture-form-details
- https://help.17hats.com/en/articles/3114074-lead-capture-email-setup
- https://help.17hats.com/en/articles/3148501-how-to-reconnect-weddingwire-theknot-com-or-your-showitfast-website-lead-capture-email-form
- https://help.17hats.com/en/articles/7336856-overview-of-lead-source-reporting-in-17hats
- https://help.17hats.com/en/articles/7336622-lead-source-reporting-in-17hats-with-lead-capture-forms
- https://help.17hats.com/en/articles/7336815-lead-source-reporting-in-17hats-with-online-scheduling
- https://help.17hats.com/en/articles/8178404-referral-source-reporting-in-17hats
- https://help.17hats.com/en/articles/1769360-contacts-tags / 1769384-project-tags / 3196308-tag-feature-overview
- https://help.17hats.com/en/articles/6236261-tag-management-in-17hats
- https://help.17hats.com/en/articles/3760729-how-to-add-remove-tags-in-bulk
- https://help.17hats.com/en/articles/5910127-automatically-tag-contacts-and-projects
- https://help.17hats.com/en/articles/2952802-how-to-assign-projects-using-tags
- https://help.17hats.com/en/articles/9764837-17hats-pipelines-overview
- https://help.17hats.com/en/articles/1052884-projects-vs-lifecycle-vs-workflows / 923689-lifecycles / 923760-what-is-the-difference-between-a-workflow-and-a-lifecycle
- https://help.17hats.com/en/articles/879747-how-do-i-archive-a-project-or-contact-in-17hats
- https://help.17hats.com/en/articles/9015398-restore-recently-deleted-contacts-and-projects
- https://help.17hats.com/en/articles/2761371-zapier-integration
- https://help.17hats.com/en/articles/2548572-email-sync-setup-use / 927448-how-does-email-correspondence-work-in-17hats / 3110879-email-communication-faqs
- https://help.17hats.com/en/articles/2679659-recent-client-activity
- https://help.17hats.com/en/articles/3110596-17hats-dashboard
- https://help.17hats.com/en/articles/3152558-the-17hats-mobile-app
- https://help.17hats.com/en/articles/9894024-online-scheduling-services-project-management / 6837367-online-scheduling-service-booking-questions

Feature/marketing pages: 17hats.com/features/{lead-capture-form, lead-management, lead-source-reporting, contact-card, related-contacts, custom-fields, tags, pipelines, dashboard, mobile-app, auto-responder, workflow-trigger}; 17hats.com/pricing; 17hats.com/integration/{the-knot, wedding-wire, email}

Blog & release notes: blog.17hats.com (lead source reporting launch 2023; pipelines; tags posts; LCF posts); 17hats.releasenotes.io (Custom Fields; Answer Mapping; Recent Client Activity; Move Projects Between Contacts; Restore deleted; Referral Source Reporting)

Third-party: debmitzelcreative.com LCF series (2024) & custom fields (2025); jebbgraff.com LCF tutorial (2023); 17hatsuniversity.com quick tips; Zapier app directory (zapier.com/apps/17hats); TaxDome/StudioCloud import-from-17hats docs

Reviews/comparisons: capterra.com/p/144328/17hats; g2.com/products/17hats; softwareadvice.com/bpm/17hats-profile; trustpilot.com/review/www.17hats.com; honeybook.com/blog/honeybook-vs-17hats; hellobonsai.com/blog/honeybook-vs-17hats; plutio.com/compare/17hats-vs-honeybook; manyrequests.com/blog/17hats-vs-honeybook; taskip.net/17hats-pricing

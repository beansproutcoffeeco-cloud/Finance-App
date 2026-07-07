# 17hats: Email, Templates & Communication

Research area 09 of 12 — how 17hats handles email account integration, the email sync/"inbox", templates and merge tokens, composing/scheduling, tracking, owner notifications, SMS, and branding.

**Research note / confidence caveat:** `help.17hats.com`, `www.17hats.com`, `blog.17hats.com`, `17hatsuniversity.com`, and `17hats.releasenotes.io` were all blocked from direct fetching in this environment (egress policy 403). All findings below were assembled from extensive web-search result extracts of those exact pages (article titles + summarized content), which proved detailed and mutually consistent. Facts are attributed to specific help articles in Sources. Items marked **[uncertain]** could not be double-confirmed; nothing below is invented.

---

## 1. Summary

- 17hats connects to the user's real email account (Google OAuth for Gmail/Workspace; IMAP+SMTP credentials for everything else) and markets itself as "the only small business platform that offers two-way email sync."
- **Sending model:** two outgoing options — (a) the user's own SMTP/Gmail account (email truly sends AS the user), or (b) the shared **17hats Mail Server** (`17hatsmail.com`), which is zero-setup and has SPF/DKIM/DMARC configured, but can show "via 17hatsmail.com" and is explicitly documented as spam-prone when the From address is a free mailbox (@gmail.com, @yahoo.com, etc.).
- **Receiving model:** there is no full unified inbox. A background sync polls connected mailboxes every **20–45 minutes**, imports only **new, unread** messages whose From (or CC) address matches an existing **contact with an active project**, and files them onto that contact/project's email log. Optionally, unread client emails surface on the Dashboard ("Let's take care of business").
- **Templates:** a single template library (Account Settings → Documents & Emails) holds email templates keyed by **Email Type** (Regular, quote_send / contract_send / invoice_send / questionnaire_send, Lead Auto Responder, five Online Scheduling types, Client Portal). Type determines which templates are offered in each sending context.
- **Merge tokens** use `[% ... %]` syntax (e.g. `[% contact.first_name %]`), spanning Contact, Project, Account, Invoice, Quote, Contract, Questionnaire, Client Portal, and Online Scheduling (booking.*) namespaces; **custom fields automatically become custom tokens**.
- **Send Later** schedules an email to the minute; workflow-automated emails batch out **starting 10am local time, staggered over ~2 hours**. Document reminders (upcoming/past-due for Quote/Contract/Invoice/Questionnaire) are automated with per-type rules.
- **Tracking:** opt-in pixel-based read receipts ("Unread" / "Read by Client" with first-open timestamp); document-level events (viewed/accepted/paid/signed) generate owner notifications from `@17hatsmail.com` and mobile push (leads, payments, questionnaires, bookings).
- **SMS Texting** is a paid add-on module (one-time $60 A2P registration + plans from ~$10/mo with a dedicated local number and 100 message fragments), US/Canada only, with 2-way texting threaded into projects, text templates, tokens, and automated scheduling/document-reminder texts.
- **Branding:** logo, header images, hex colors, fonts, and backdrop from Brand Preferences apply to document emails and client-facing pages; multiple rich-text/HTML email signatures; a **subdomain** setting personalizes document URLs; **no custom email-sending domain and no CNAME custom portal domain** found in public docs.

---

## 2. Email account integration

### 2.1 Where it lives
Account Settings (gear icon) → **Email Settings**, with distinct sections/tabs:
- **Incoming Email** (connected mailboxes for sync)
- **Outgoing Email** (which server actually sends)
- **Send Email As** (the From identity, sourced from My Profile email)
- **Email Signature** tab
- **Email Reminders** tab (document reminders — see §4.4)
- Read-receipt enablement (see §5.1) and a **BCC-myself** option ("check this option to get blind copied on the emails and documents that you send out ... through 17hats")

### 2.2 Connection methods
- **Google Gmail / Google Workspace:** choose "Google Gmail" from a provider dropdown, enter the *primary* login address (aliases explicitly not allowed for connection), then an OAuth redirect to Google to accept permissions. After OAuth, the **outgoing** server is auto-configured to the same Google account.
- **Other providers:** enter login credentials plus **IMAP server and port** for incoming; outgoing via SMTP settings ("Change Outgoing Server") or fall back to the 17hats server. Major providers get a simplified login flow.
- **Multiple mailboxes:** users can connect several addresses under Incoming Email ("Syncing Multiple Email Addresses into 17hats"); every connected inbox is "combed through" for contact/project-related mail. No documented hard cap on the number of connected accounts **[uncertain]**.
- **Multi-user accounts:** each user has their own email settings; dedicated help docs cover "Multi User Email Settings" and "Multi User Email Settings: Using the 17hats Mail Server," implying per-user From identities on either sending path.

### 2.3 Sending model (outgoing)
Two mutually exclusive outgoing paths:

1. **17hats Mail Server** (default / simplest)
   - Marketed as "optimized for deliverability right out of the box"; SPF, DKIM, DMARC DNS records maintained by 17hats.
   - Recipients "may see emails as coming from an @17hatsmail.com address due to the email software they use" — i.e., classic send-on-behalf / "via 17hatsmail.com" display.
   - Documented warning: sending through the 17hats server **with a free From address** (@gmail.com, @outlook.com, @icloud.com, @yahoo.com) makes mail "much more likely to be classified as spam and rejected" (because DMARC on those consumer domains fails for third-party senders).
2. **User's own outgoing server (SMTP / Gmail API)**
   - Auto-connected for Gmail after the incoming OAuth; switchable via "Change Outgoing Server."
   - Mail genuinely originates from the user's provider, so it lands in their provider's Sent folder and passes their own SPF/DKIM **[inferred from how Gmail SMTP works; not stated verbatim in 17hats docs]**.

Supporting deliverability guidance 17hats publishes: use a custom-domain address, ask your provider/registrar for SPF/DKIM/DMARC help, and test with mail-tester.com ("Recommended Steps for Successful Email Delivery in 17hats"; "How to ensure emails do not end up in spam").

**From-address behavior:** replies sent inside 17hats "always send from your Outgoing Mail Server email." The "Send Email As" display address derives from My Profile; a Gmail-side alias can interfere and make mail show the wrong From ("Emails are not sending as the right address").

### 2.4 Receiving / threading model (the "two-way sync")
This is a **selective CRM sync, not a full inbox mirror**:

- Poll cycle: **every 20–45 minutes**, scanning connected mailboxes.
- Import filter — a message is pulled in only if ALL are true:
  1. It arrived at a **connected** incoming address;
  2. It is **new and unread** in the mailbox;
  3. The **From (or CC) address matches an existing contact record**;
  4. That contact has an **active project**.
- Filed location: the email lands in the matching **contact's project email log** (Project Activity stream, alongside Notes, Files, To-Dos, Bookings).
- **No backfill:** adding a new contact does not import previously received emails — only mail received after the contact exists.
- **Outbound capture too:** if the user replies from their normal email client (outside 17hats) to someone who is a contact with a project, that outgoing message is *also* synced into the project's email log — this is the "two-way" claim.
- **Dashboard surfacing (optional):** a setting shows new unread contact emails "needing a reply" in the Dashboard's "Let's take care of Business" section; users can reply from the Dashboard or the Project (including with the Hattie AI assistant).
- Troubleshooting doc ("Incoming Email Not Syncing") reiterates the three-condition filter — the most common user confusion is mail not appearing because the sender isn't a contact or the project isn't active.

### 2.5 Lead Capture Email (inbox parsing)
A related ingestion feature: a **Lead Capture Email rule** watches a connected inbox for notification emails from **WeddingWire, TheKnot.com, or Showit/ShowItFast**, parses structured fields (NAME, EMAIL, PHONE, etc.) out of the email body by heading keyword matching, and creates a new lead on the next sync cycle (not instant). Rules are listed under "Lead Capture Methods."

### 2.6 What 17hats email is NOT
- **Not bulk/marketing email.** One email → one contact/project at a time. No opt-out/unsubscribe link mechanism. The sanctioned workaround for one-to-many is **Bulk Apply a Workflow** containing a send-email step across multiple projects, with an explicit warning to not use it for marketing (they point users to Mailchimp).
- **No newsletter composer**; users asking about image-rich newsletters get pointed to HTML paste-in (see §6.3).

---

## 3. Templates & merge tokens

### 3.1 Template management
- Location: **Account Settings → Documents & Emails** (one library shared by email templates and document templates: quotes, contracts, invoices, questionnaires).
- Create via "**New Template**" (pick the type first), or from any composed email via "**Save as a template**."
- Organization: templates list **alphabetically/numerically within document type**; a **Filter** button narrows by type. No folders — 17hats' own guidance is a *naming convention* (e.g., "Dog Walking – Fulfillment – Your Dog Report" = service + lifecycle stage + purpose), which signals the library gets large and unwieldy.
- Lifecycle: templates can be **edited, deleted, or archived** (archive removes from active pickers but retains the template).
- Pre-built content: 17hats ships/offers template samples and "adding an existing email template into 17hats" is a documented copy-paste flow (no import format — literally paste your old template text in).

### 3.2 Email Types (the key design idea)
Every email template has a **Type**, and the sending context filters the picker to matching types — "much easier to select the correct template from a few Quote Type templates than the hundreds of email templates in your account." Types identified:

| Email Type | Used when |
|---|---|
| Regular Email | standalone emails; the type used by generic Workflow send-email steps |
| Email (quote_send) | accompanies sending a Quote |
| Email (contract_send) | accompanies sending a Contract |
| Email (invoice_send) | accompanies sending an Invoice |
| Email (questionnaire_send) | accompanies sending a Questionnaire |
| Lead Auto Responder | auto-reply attached to a Lead Capture Form |
| Online Scheduling: confirmation | service booked |
| Online Scheduling: cancellation | booking cancelled |
| Online Scheduling: waiting-for-approval | booking pending approval |
| Online Scheduling: one-day reminder | day-before reminder |
| Online Scheduling: day-of reminder | day-of reminder |
| Client Portal Email | sends portal access/URL |

Each type exposes the token namespaces relevant to it (e.g., Invoice tokens only work in invoice_send-type emails).

### 3.3 Token system
- **Syntax:** `[% token_path %]` — dot-path expressions, e.g. `[% contact.first_name %]`. Docs describe replacement as: 17hats "detects and replaces the [%%] and everything in between with the token data after you click Send and before the email goes out." Tokens also work in email **subject lines** (documented example: `Thank you for booking [% booking.scheduled_service.name %]`) and in Contracts, Questionnaires, and Lead Capture Form contexts, plus SMS text templates.
- **Three documented groups:** General tokens (Contact / Project / Account), Document tokens (Invoice, Quote, Contract, Questionnaire, Client Portal), and Online Scheduling tokens.
- **Data dependency:** a token fills only if the datum exists on the account/contact/project; users must maintain data hygiene. (Behavior when data is missing — blank vs. literal token — not confirmed **[uncertain]**.)

**Token inventory confirmed from the "Complete List of Tokens" article** (the article is longer; this is what could be extracted — the full page could not be fetched, so treat as a verified subset):

*Contact tokens* (data from the contact record):
- `[% contact.first_name %]`, `[% contact.last_name %]`, `[% contact.name %]` (full name)
- `[% contact.company_name %]`
- `[% contact.address.as_string %]`
- `[% contact.primary_email_address %]`, `[% contact.primary_phone_number %]`

*Project tokens:* project name, project location/venue, project date, start time, end time (pulled "from what's saved within the specific project record this email is sending under"). Exact key paths not captured **[uncertain — likely `project.*`]**.

*Account ("my profile") tokens:* the owner's first name, last name, company name, email address, phone number from Account Settings/My Profile.

*Invoice tokens* (invoice_send type only): invoice number, total amount, outstanding/amount due, due date, **public link** (pay-online URL), and next-payment amount/date for automatic payment plans.

*Contract tokens:* contract name, due date, create date.

*Quote tokens* and *Questionnaire tokens:* exist per the docs (usable in their respective email types); the individual field lists were not retrievable **[uncertain]**.

*Client Portal tokens:* Client Portal URL; Client Portal Password (when PIN-protected).

*Online Scheduling tokens:*
- `[% booking.scheduled_service.name %]` (service name)
- `[% booking.scheduled_service.location.name %]`, `[% booking.scheduled_service.location.location %]` (location name / address)
- `[% booking.calendar_event.formatted_token_date('start') %]` (booking date)
- `[% booking.calendar_event.formatted_time('start') %]`, `[% booking.calendar_event.formatted_time('end') %]`
- `[% booking.scheduled_service.duration %]`

*Custom-field tokens:* creating a **Custom Field** (Account Settings → Custom Fields; Contact Fields or Project Fields tabs; types: Short Field, Long Field, Yes/No, Choose-from-List, Checkboxes, Date) **automatically creates a matching token** usable in emails, contracts, questionnaires, and lead capture forms. Custom fields can be populated by lead-capture forms, questionnaires, and scheduling questions — a very strong personalization loop.

### 3.4 Hattie (AI writing assistant)
- OpenAI-powered assistant embedded in the email editor; available on **all plans**, capped at **50 uses/month**.
- Two modes: **generate** an email from a short prompt (click into the template/email body and describe what you want), or **revise/reword** an existing draft or reply.
- Seven tone "voices": professional, funny, concise, conversational, friendly, elaborate, empathetic.
- Works when replying to client emails from the Dashboard or a Project.

---

## 4. Composing & sending UX

### 4.1 Entry points
- **Project page** — primary hub; compose/reply, with full history in Project Activity.
- **Contact page** — emails filed to the contact.
- **Dashboard** — reply to surfaced unread client emails.
- **Document send flows** — sending a Quote/Contract/Invoice/Questionnaire always wraps the document in an email of the matching Email Type; the document is delivered as a **link/button to a hosted web page** (public link), not a raw attachment. Multiple documents can go in one email ("Sending Multiple 17hats Documents in One Email"), and a **3-in-1 Combined Document** (quote→contract→invoice) sends as a single link.
- **Workflows** — send-email / send-document **Action Items** run either fully automatically or "upon your review" (user approves each send); **To-Dos** can be configured so checking them off triggers a prepared email (again: auto-send or review-then-send).
- **Mobile app** — respond to leads and view/send docs on the go.

### 4.2 Recipients
- One contact/project per send; **CC supported**; owner-BCC-myself global option; no true bulk sends (see §2.6). "Related contacts" on a project are how additional people (e.g., a couple) receive documents/emails.

### 4.3 Scheduling
- **Send Later** on any composed email: pick a future date/time (minute-level precision — type an exact time if not on the half-hour). Scheduled emails can be **canceled** before sending; **editing requires re-scheduling**; scheduled emails are visible **only to the user who scheduled them** (noted as a real multi-user annoyance). Feature may be plan-gated **[uncertain which plans]**.
- **Workflow email timing:** automated workflow emails are queued to start at **10:00 AM in the account's Brand Preferences timezone** and are sent "over the course of two hours, with some automated staggering" — i.e., a shared daily batch window rather than exact-time sends.

### 4.4 Automated transactional emails
- **Document Email Reminders** (Email Settings → Email Reminders tab): per document type (Quote, Contract, Invoice, Questionnaire) toggle **Upcoming** reminders (customizable days-before-due, subject, message) and **Past Due** reminders (day after due, then repeating daily/weekly/monthly). Only fire for **Active projects** and only when the document has a **due date**; completed documents suppress reminders.
- **Automatic confirmation emails**: when a client accepts a quote, signs a contract, pays an invoice, or completes a questionnaire, a client-facing confirmation email sends automatically; content is editable and each can be turned off.
- **Online Scheduling emails**: confirmation, cancellation, waiting-for-approval, one-day and day-of reminders (templates per service; see §3.2), plus optional SMS equivalents.
- **Lead Capture auto-replies**: instant auto-response email (Lead Auto Responder type) on form submission.

### 4.5 Editor & attachments
- Rich-text editor: bold/italic/underline/strikethrough, paragraph formats, bulleted/numbered lists, links, horizontal rules, **inline images** (drag-resize), and **file attachments**.
- **HTML source view** via a `<>` toolbar button — users can paste externally designed HTML into emails, signatures, and contracts ("HTML Customization for Emails & Contracts"); "Creating Linked Images" covers hosted-image workarounds for newsletter-ish emails.
- Attachment/message size limit: not officially documented; a ~10 MB total message ceiling is suggested by integration docs **[uncertain]**.

---

## 5. Tracking & notifications

### 5.1 Email read receipts (opens)
- **Opt-in** via Account Settings → Email Settings. Once on, outgoing 17hats emails show **"Unread"** or **"Read by Client"** labels in the email log; hovering (or opening the email) reveals the **timestamp of first open**. First-open only — no open counts, no click tracking found.
- Mechanism: **tracking pixel**. Documented limitations:
  - Only works for email **sent from within 17hats**;
  - Only the **To** recipient is tracked (CC addresses are not);
  - Privacy plug-ins / image-blocking on the recipient side defeat it.

### 5.2 Document-level tracking
Separate from email opens, documents (hosted pages) generate lifecycle events — quote accepted, contract signed, invoice paid, questionnaire completed, booking made — that trigger both client confirmations (§4.4) and owner notifications (§5.3). (Whether "document viewed" is itself surfaced as an event was not confirmed **[uncertain]**.)

### 5.3 Notifications to the business owner
- **System notification emails** are sent from **`@17hatsmail.com`** addresses, with subjects referencing quote / contract / invoice / questionnaire / lead / "A booking has been made". 17hats even documents Gmail filter recipes so owners can organize these ("How do I filter for 17hats system notification emails").
- **New Lead notifications** go to the **main Account Owner's email only**; adding more recipients requires a **Zapier** workaround.
- **Mobile push notifications** (iOS/Android app): Lead Capture Form submissions, Invoice payments, Questionnaire submissions, new Online Scheduling bookings; release notes mention improved push for **multi-brand** accounts.
- **In-app Dashboard**: "Let's take care of business" panel aggregates unread synced client emails + items needing attention (workflow steps awaiting review, etc.).
- **Daily digest / "Today" summary email:** no evidence found of a daily agenda email product; the Dashboard plays that role in-app. **[Searched specifically; appears NOT to exist — verify before assuming.]**

### 5.4 SMS Texting (add-on module)
- **What it does:** 2-way business texting from a **dedicated local 10-digit number** (user picks state/area code), threaded into the **Project page** alongside email; manual texts plus automated texts for: Lead Capture Form auto-responses, Online Scheduling confirmations / approval / 1-day and few-hour reminders / cancellations, and past-due document reminders.
- **Templates & tokens:** text templates live alongside email templates and support tokens (client name, project title, appointment date, custom tokens).
- **Compliance:** built-in **opt-in/opt-out** handling; A2P 10DLC registration (business name, website, EIN, contact info) — approval "can take up to two weeks"; **US & Canada members only**.
- **Pricing:** one-time **$60 registration fee**; three plan tiers starting **$10/month** including the number lease + **100 message fragments** (SMS segments), scaling up; promo pricing seen through Jan 31, 2026.
- Positioning: heavily marketed against HoneyBook as a differentiator ("keeps personal texting separate from business").

---

## 6. Branding & customization

### 6.1 Brand Preferences (Account Settings → Brand Preferences)
Tabs documented: **Account**, **Images**, **Colors & Fonts** (+ overview pages).
- **Logo:** uploaded once; auto-applied to the **top of every document** (Quote, Contract, Invoice, Questionnaire), **document emails**, the **Client Portal**, **Online Scheduling pages**, and **Lead Capture Form auto-response emails**.
- **Header image:** optional banner for Quotes, Contracts, Invoices, Questionnaires, Lead Capture Forms, and Online Scheduling.
- **Colors & fonts:** hex-code control of background/backdrop, accent colors, button colors, accent fonts, and button fonts across documents and emails — "use the same HEX codes from your website."
- **Multiple brands:** an account can run more than one brand (multi-brand push notifications exist), each presumably with its own preferences **[uncertain on exact per-brand scope]**.

### 6.2 Domains & URLs
- **Subdomain setting** ("Domain Setting" article, under Brand Preferences): user-chosen text that appears in **document URLs** (the hosted quote/invoice/portal links). This is a *17hats-owned* URL personalization, not a custom domain.
- **No custom sending domain** for email (you either send via your own mailbox or via `17hatsmail.com`), and **no CNAME/custom-domain support for the Client Portal** appears anywhere in public docs (competitors like HoneyBook and Moxie document this; 17hats does not).

### 6.3 Email signatures
- Email Settings → **Email Signatures** tab; **multiple named signatures**; the **first in the list is the default**. Rich-text editor plus full **HTML paste-in** (via the `<>` view) and inline images with drag-resize. Signature choice at compose time **[uncertain how per-template/per-user selection works in multi-user accounts]**.

### 6.4 Document email look
Document emails render with logo/header/colors and a prominent **call-to-action button** (View Quote / Pay Invoice, etc.) linking to the hosted document page — the email itself stays simple; the branded experience is mostly on the hosted page.

---

## 7. Inferred data model (schema sketch)

Reverse-engineered from observed behavior; naming is illustrative.

```
EmailAccount            # "Incoming Email" connections; N per account (per user)
  id, account_id, user_id
  provider              # google | imap | (office365?)
  auth_type             # oauth | password
  email_address         # must be primary login, not alias
  imap_host, imap_port  # for generic IMAP
  status, last_synced_at
  is_lead_capture_source bool

OutgoingMailConfig      # one per user (multi-user: each user configures)
  id, account_id, user_id
  mode                  # seventeenhats_server | own_smtp | gmail_oauth
  smtp_host, smtp_port, username, secret
  send_as_address       # "Send Email As" (from user profile)
  bcc_self bool

EmailMessage
  id, account_id, project_id, contact_id, user_id
  direction             # inbound_synced | outbound_app | outbound_synced
  provider_message_id, thread_ref
  from, to[], cc[]
  subject, body_html, attachments[]
  status                # draft | scheduled | queued | sent | failed
  scheduled_at          # Send Later
  scheduled_by_user_id  # visibility limited to this user (17hats quirk)
  sent_at
  first_opened_at       # read receipt (pixel), nullable
  email_template_id, email_type
  source                # manual | workflow | reminder | scheduling | confirmation

EmailTemplate
  id, account_id (brand_id?)
  name                  # convention-based naming; no folders
  email_type            # regular | quote_send | contract_send | invoice_send |
                        # questionnaire_send | lead_auto_responder |
                        # os_confirmation | os_cancellation | os_waiting_approval |
                        # os_one_day_reminder | os_day_of_reminder | client_portal
  subject, body_html    # both token-enabled
  archived bool

EmailSignature
  id, account_id, user_id?, name, body_html, position  # position 1 = default

TokenDefinition (mostly static + generated)
  namespace             # contact | project | account | invoice | quote | contract |
                        # questionnaire | client_portal | booking | custom
  path                  # e.g. contact.first_name, booking.scheduled_service.name
  custom_field_id       # for generated custom-field tokens
  allowed_email_types[] # document tokens restricted to their email type

DocumentReminderRule    # Email Settings > Email Reminders
  id, account_id, document_type   # quote|contract|invoice|questionnaire
  kind                  # upcoming | past_due
  enabled, days_before, recurrence  # daily|weekly|monthly for past-due
  subject, body_html

SyncRule (implicit)     # import filter for inbound sync
  requires: connected EmailAccount + unread + From/CC matches Contact
            + Contact has active Project
  poll_interval: 20–45 min

LeadCaptureEmailRule
  id, email_account_id, source   # weddingwire | theknot | showit
  field_mappings        # heading-keyword -> lead field

SmsNumber / SmsMessage / SmsTemplate
  registration (EIN, business info), status, monthly_plan, fragments_included
  sms_message: project_id, direction, body, fragments_used, opt_in_state
  sms_template: type mirrors email automation types; token-enabled

NotificationEvent
  type: lead_created | invoice_paid | questionnaire_completed | booking_created |
        contract_signed | quote_accepted | email_needs_reply | ...
  channels: system_email (@17hatsmail.com) -> owner only
            push (mobile)  |  dashboard_panel

BrandPreference
  logo_url, header_image_url, backdrop, colors{background, accent, button},
  fonts{accent, button}, subdomain, timezone (drives 10am workflow batch)
```

---

## 8. Strengths / weaknesses

### Strengths (worth studying)
1. **Two-way sync onto projects** is genuinely differentiating vs. HoneyBook-style closed messaging: client replies from their normal inbox still land in the project timeline, even when the owner replies from their own mail client.
2. **Email Types** are an elegant UX device — context-filtered template pickers scale far better than one flat list.
3. **Token system depth**: document tokens (invoice public link, next autopay amount/date) + auto-generated custom-field tokens + tokens in subjects + tokens reused across email/SMS/contracts/questionnaires.
4. **Own-SMTP sending option** — email really comes from the user, preserving deliverability and Sent-folder history; most competitors only offer a shared sender.
5. Automated document reminders + confirmations kill a whole category of manual follow-up.
6. SMS module is compliant (10DLC, opt-in/out) and threaded into the same project timeline as email.

### Weaknesses / user complaints
1. **Deliverability on the shared server**: 17hats' own docs concede "via @17hatsmail.com" display and spam risk with free From addresses; anecdotal user complaints about 17hats mail landing in spam recur in community discussions (Facebook user group, reviews). **[Complaint prevalence: moderate confidence — specific threads could not be fetched.]**
2. **Not an inbox**: 20–45-minute polling latency; unread-only import silently drops mail the user already read on their phone; no sync for non-contacts or contacts without an *active* project — a constant support theme ("Incoming Email Not Syncing").
3. **No bulk email at all** (workflow bulk-apply hack with no unsubscribe support is legally risky if misused).
4. **Dated composer**: basic rich text; real design requires hand-pasted HTML; no drag-drop email builder. Reviews repeatedly call the interface dated vs. HoneyBook.
5. **Scheduled-email visibility** limited to the scheduling user; editing a scheduled email silently unschedules it.
6. **Read receipts are minimal**: first open only, To-recipient only, pixel-fragile; no link-click tracking; no per-recipient tracking on CC.
7. **Owner notifications inflexible**: new-lead alerts only to the account owner unless you bolt on Zapier.
8. Template library has **no folders/categories beyond type** — naming conventions are the official workaround.
9. No custom sending domain / dedicated IP options; no portal custom domain.

---

## 9. Build recommendations (for a competing app)

**Copy (table stakes proven by 17hats):**
- OAuth Gmail/Microsoft + generic IMAP/SMTP connection; per-user identities in multi-user accounts.
- Auto-threading of client email onto contact/project timelines, including mail the owner sends from outside the app.
- Email Types → context-filtered template pickers; tokens usable in subject + body; custom fields that instantly become tokens; document tokens carrying live links/amounts.
- Send Later, document upcoming/past-due reminder engine with per-type rules, auto confirmation emails, scheduling reminder emails.
- BCC-myself option, multiple signatures with HTML, brand logo/colors on document emails, AI compose/rewrite with tone presets (cap usage).
- Compliant 2-way SMS as a paid add-on (10DLC registration flow, per-segment metering, opt-in/out) threaded into the same timeline.

**Improve (clear gaps to exploit):**
- **Real-time sync** (Gmail push/watch + Microsoft Graph webhooks instead of 20–45-min IMAP polling) and import regardless of read state; let users retroactively link past threads to a new contact.
- **Deliverability**: send via user OAuth by default; if offering a shared sender, support **custom sending domains with per-tenant DKIM/SPF alignment** and an in-app domain-health checker (17hats just links to mail-tester.com).
- **Tracking**: link clicks, per-recipient opens, repeat opens, and document-view events unified into one activity feed; make tracking privacy-transparent.
- **Scheduled sends** visible/cancelable account-wide; exact-time workflow sends (not a 10am–noon batch) with per-step time offsets.
- Template **folders/tags + search + usage analytics**; shared team library; version history.
- **Notification center**: per-event, per-channel (email/push/SMS/Slack), per-user routing — beat the "owner-only + Zapier" limitation. Consider the daily digest email 17hats lacks.
- Modern composer: lightweight block editor with saved snippets, without becoming a marketing ESP.

**Skip / deprioritize:**
- Full unified-inbox email client ambitions (folder management, labels, non-client mail) — 17hats proves you only need CRM-relevant threading.
- Bulk marketing email — integrate with ESPs instead (17hats' own stance; avoids CAN-SPAM surface).
- Lead parsing of vendor notification emails (WeddingWire/TheKnot heading-scraping) unless targeting the same wedding/photography verticals — brittle and niche; prefer native form/webhook lead capture.
- Pixel-only read receipts as a headline feature — table stakes at best, increasingly defeated by Apple MPP/privacy tooling.

---

## 10. Sources

All content extracted via web-search summaries of these pages (direct fetch was blocked in this environment):

**17hats Help Center (help.17hats.com)**
- Email Sync Setup & Use — https://help.17hats.com/en/articles/2548572-email-sync-setup-use
- How do I connect my Google Gmail/GSuite Email? — https://help.17hats.com/en/articles/2829398-how-do-i-connect-my-google-gmail-gsuite-email
- How does email correspondence work in 17hats? — https://help.17hats.com/en/articles/927448-how-does-email-correspondence-work-in-17hats
- Email Communication Overview — https://help.17hats.com/en/articles/3110832-email-communication-overview
- Email Communication FAQs — https://help.17hats.com/en/articles/3110879-email-communication-faqs
- Incoming Email Not Syncing — https://help.17hats.com/en/articles/948677-incoming-email-not-syncing
- Syncing Multiple Email Addresses into 17hats — https://help.17hats.com/en/articles/847666-syncing-multiple-email-addresses-into-17hats
- Multi User Email Settings — https://help.17hats.com/en/articles/1063723-multi-user-email-settings
- Multi User Email Settings: Using the 17hats Mail Server — https://help.17hats.com/en/articles/1063708-multi-user-email-settings-using-the-17hats-mail-server
- Using the 17hats Mail Server as your Outgoing Server — https://help.17hats.com/en/articles/1063489-using-the-17hats-mail-server-as-your-outgoing-server
- Recommended Steps for Successful Email Delivery — https://help.17hats.com/en/articles/1691196-recommended-steps-for-successful-email-delivery-in-17hats
- How to ensure emails do not end up in spam — https://help.17hats.com/en/articles/865530-how-to-ensure-emails-do-not-end-up-in-spam
- Emails are not sending as the right address — https://help.17hats.com/en/articles/843946-emails-are-not-sending-as-the-right-address
- Complete List of Tokens — https://help.17hats.com/en/articles/1235598-complete-list-of-tokens
- How to Create & Manage Document & Email Templates — https://help.17hats.com/en/articles/879803-how-to-create-manage-document-email-templates
- What are the Different Email Types in 17hats? — https://help.17hats.com/en/articles/2950670-what-are-the-different-email-types-in-17hats
- Adding an existing email template into 17hats — https://help.17hats.com/en/articles/1008149-adding-an-existing-email-template-into-17hats
- How to write emails with 17hats AI Assistant, Hattie Hats — https://help.17hats.com/en/articles/8096380-how-to-write-emails-with-17hats-ai-assistant-hattie-hats
- Schedule an email to go out at a specific date and time — https://help.17hats.com/en/articles/1228704-schedule-an-email-to-go-out-at-a-specific-date-and-time
- What time are automated emails sent from within my workflows? — https://help.17hats.com/en/articles/897486-what-time-are-automated-emails-sent-from-within-my-workflows
- Email Settings – Document Email Reminders — https://help.17hats.com/en/articles/2280471-email-settings-document-email-reminders
- Automatic Confirmation Emails that send from 17hats — https://help.17hats.com/en/articles/1967185-automatic-confirmation-emails-that-send-from-17hats
- Email Read Receipts — https://help.17hats.com/en/articles/2478209-email-read-receipts
- What is BCC email? — https://help.17hats.com/en/articles/927630-what-is-bcc-email
- Can I send one email to multiple clients/leads? — https://help.17hats.com/en/articles/1042105-can-i-send-one-email-to-multiple-clients-leads
- Sending Multiple 17hats Documents in One Email — https://help.17hats.com/en/articles/1052657-sending-multiple-17hats-documents-in-one-email
- How do I mass share a 17hats document? — https://help.17hats.com/en/articles/1817288-how-do-i-mass-share-a-17hats-document
- Email Settings – Email Signature Tab — https://help.17hats.com/en/articles/840404-email-settings-email-signature-tab
- HTML Customization for Emails & Contracts — https://help.17hats.com/en/articles/3210383-html-customization-for-emails-contracts
- 17hats Customization Options for Emails, Contracts, and Email Signatures — https://help.17hats.com/en/articles/839258
- Creating Linked Images within 17hats — https://help.17hats.com/en/articles/3210382-creating-linked-images-within-17hats
- Brand Preference Page Overview / Images / Colors & Fonts / Account tabs — https://help.17hats.com/en/articles/2108661, /3110802, /3110814, /3110791
- Domain Setting — https://help.17hats.com/en/articles/927442-domain-setting
- Custom Fields — https://help.17hats.com/en/articles/2545832-custom-fields
- Lead Capture Email Setup — https://help.17hats.com/en/articles/3114074-lead-capture-email-setup
- Email Lead Capture Form Details — https://help.17hats.com/en/articles/2823021-email-lead-capture-form-details
- How do I filter for 17hats system notification emails in Gmail — https://help.17hats.com/en/articles/1029541
- Sending New Lead Email Notifications to Additional Email Addresses — https://help.17hats.com/en/articles/2978670
- The 17hats Mobile App — https://help.17hats.com/en/articles/3152558-the-17hats-mobile-app
- Workflows: To-Dos, Action Items, Pauses — https://help.17hats.com/en/articles/879587 and /1037910
- Online Scheduling articles (confirmation/cancellation, automatic email reminders, FAQs) — https://help.17hats.com/en/articles/9904227, /4901233, /2921704

**17hats marketing & blog**
- Email feature — https://www.17hats.com/features/email ; Email integration — https://www.17hats.com/integration/email
- Email Templates — https://www.17hats.com/features/email-templates ; Scheduled Emails — https://www.17hats.com/features/scheduled-emails ; Email Read Receipts — https://www.17hats.com/features/email-read-receipts ; Document Reminders — https://www.17hats.com/features/document-reminders ; Custom Fields — https://www.17hats.com/features/custom-fields ; Mobile App — https://www.17hats.com/features/mobile-app ; Client Portal — https://www.17hats.com/features/client-portal
- SMS Texting — https://www.17hats.com/sms-texting
- Blog: Using Tokens in Email Templates — https://blog.17hats.com/feature-spotlight-using-in-tokens-in-17hats-email-templates/ ; Five things about email templates — https://blog.17hats.com/five-things-you-need-to-know-about-17hats-email-templates/ ; 2 Ways Email Types Simplify Sending — https://blog.17hats.com/2-ways-17hats-email-types-simplify-sending-emails/ ; SMS Texting posts (Meet SMS Texting; Pricing & How to Get Started; vs HoneyBook SMS) — https://blog.17hats.com/17hats-sms-texting-pricing-and-how-to-get-started/ ; Branding posts — https://blog.17hats.com/five-ways-to-showcase-your-branding-with-17hats/

**Third-party**
- 17hats Release Notes (Email Read Receipts; Custom Fields; mobile tag) — https://17hats.releasenotes.io/
- 17hats University token tutorials — https://www.17hatsuniversity.com/17hats-quick-tips/use-email-tokens-in-17hats-tutorial
- App Store / Google Play listings (push notification details) — https://apps.apple.com/us/app/17hats/id1069498016 ; https://play.google.com/store/apps/details?id=com.isomnio.seventeenhats
- Comparisons/reviews (dated UI, support complaints): HoneyBook vs 17hats — https://www.honeybook.com/blog/honeybook-vs-17hats ; ManyRequests comparison — https://www.manyrequests.com/blog/17hats-vs-honeybook ; GetApp — https://www.getapp.com/collaboration-software/a/17hats/ ; Capterra — https://www.capterra.com/p/144328/17hats/
- 17hats User Q&A Facebook group threads (email timing, newsletters, invoicing) — https://www.facebook.com/groups/17HatsUserQA/

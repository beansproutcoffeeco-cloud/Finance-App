# 17hats: Scheduling & Calendar

> Research area 8 of 12 — Online Scheduling, internal Calendar, external calendar sync, and how scheduling ties into projects, workflows, and lead capture.
>
> Method note: 17hats' own domains (17hats.com, help.17hats.com, blog.17hats.com) were not directly fetchable from this environment (network policy), so this document is synthesized from extensive search-engine extraction of the official Help Center articles, 17hats feature/marketing pages, 17hats release notes, 17hats University tutorials, and third-party reviews (Capterra, G2, Software Advice, comparison blogs). Every claim below traces to one of the sources listed in §10. Items that could not be confirmed are explicitly flagged **[unverified]**.

---

## 1. Summary

- 17hats Online Scheduling is a **Calendly/Acuity-style booking engine embedded in an all-in-one CRM**. Its two core objects are the **Service** (the bookable offering: duration, buffers, location, payment, emails, questions, workflow) and the **Availability Schedule** (the bookable window: availability rules, booking limitations, calendar cross-checks, team members). One Availability Schedule can expose one or many Services on a single client-facing booking page/link (embeddable via iframe/embed code).
- The differentiator vs. standalone schedulers is **what happens after booking**: every confirmed booking automatically creates/updates a **Contact + Project**, drops an **Event** on a chosen calendar, can **collect full or partial payment** (auto-generating an Invoice that flows into 17hats Bookkeeping), and can **trigger a Workflow** whose base date is the booking date.
- Scheduling emails are template-driven: **confirmation email** (instant, unless approval mode), up to **two reminder emails** (day-before; day-of 1–2 hours prior), and a **cancellation email**, all personalized with `[Scheduling]` tokens (service name, date, start/end time, location/Zoom URL). SMS confirmations/reminders exist as a paid add-on (US/Canada).
- Availability is computed from **Availability Rules** (weekly-repeating or date-specific time blocks, with a "Start Service" slot-alignment setting), minus **Calendar Checks** (busy events on selected 17hats + Google calendars), minus **Booking Limitations** (min notice, max horizon, daily/weekly booking caps), with an **override hierarchy** between Availability Schedules.
- Two-way external sync is **Google Calendar only**. Apple Calendar is one-way via an iCal/webcal subscription feed; Outlook has **no direct integration** (Google as a bridge is the documented workaround). This is a notable weakness to beat.
- Advanced capabilities (historically a paid tier/module, now folded into the single $60/mo plan): **pay-at-booking**, **Zoom auto-meeting creation**, **workflow triggers from bookings**, **Group services** (N bookings per slot), and **Team Member** scheduling (client picks a person or "Any Team Member" — sequential fill, not true round-robin).
- Known user complaints: dated UI, calendar view "never worked quite the way I wanted," scheduling "not super robust" (some users run Calendly alongside), no client notification when the *owner* reschedules, weak reporting, occasional bugginess.

---

## 2. Online Scheduling

### 2.1 Enablement & information architecture

- Online Scheduling must first be **enabled in Account Settings** (per Brand). Once on, three surfaces appear:
  - **Account Settings → Online Scheduling → Services** — the catalog of bookable Services.
  - **Account Settings → Online Scheduling → Availability** — Availability Schedules; each schedule exposes its **shareable link** and an **Embed button** that generates website embed code.
  - **Bookings** section in the app's left rail — a list of upcoming/pending bookings (a bookings inbox/dashboard).
- Bookings also surface on the **Project page → Bookings tab** (sits between "Events" and "Phone Log" tabs), where you can view, confirm, reschedule, and cancel bookings for that project.
- Historic packaging: "Basic Online Scheduling" shipped in Essentials/Standard plans; **"Advanced Online Scheduling"** (payments at booking, Zoom integration, workflow triggers, Group services, team members) was Premier-only or a purchasable module for Standard. In 2025 17hats collapsed to a **single all-inclusive plan (~$60/mo, discounted annual)**, so the Basic/Advanced split mostly matters as legacy gating language in the docs.

### 2.2 The Service object (bookable offering)

A **Service** is "the offering your leads and clients can book" — phone call, Zoom call, consult, mini-session, product pickup, etc. Configuration blocks per Service:

1. **Name / description** — client-facing.
2. **Service Type: Individual or Group** (Group requires the advanced feature set). Group type unlocks "Number of Bookings per time slot" (max capacity per slot; slot disappears once full).
3. **Service Time Frame**:
   - **Duration** (required).
   - **Buffer before** and **buffer after** (optional). Total blocked time = pre-buffer + duration + post-buffer. Example from docs: 30-min appointment + 5-min buffers = 40 minutes blocked on the calendar.
   - The full time frame (buffers included) is what the availability engine must find room for.
4. **Location** — three location *types*:
   - **In Person** — physical address plus free-text instructions (e.g., parking).
   - **Phone Call** — displays the number you'll call from + instructions ("take the call from a quiet location").
   - **Zoom** (advanced) — on booking, 17hats **auto-creates a unique Zoom meeting** in the connected Zoom account; the URL shows on the confirmation page and can be merged into emails via the Location Address token.
   - Saved locations become **reusable Location Templates**; unlimited templates per account.
5. **Online Payments** (per-Service toggle; see §2.5).
6. **Booking Questions** (per-Service; see §2.6).
7. **Approval Settings** (instant-confirm vs. pending; see §3.2).
8. **Confirmation & Cancellation email settings** (see §3.1).
9. **Automatic Email Reminders** (see §3.1).
10. **Project Management settings** (calendar assignment, project naming, update-project-date; see §6.1).
11. **Workflow triggers** (on pending and/or on confirmed; see §6.2).

### 2.3 The Availability Schedule (when/who can be booked)

An **Availability Schedule** "creates the parameters around the dates and times your contacts can book a Service." Sections:

1. **Name & Services** — name the schedule and attach one or more Services. With multiple Services attached, the booking page starts with a **Service picker** step. (Docs: "Online Scheduling Availability – Multiple Services on one Schedule.")
2. **Availability Rules** — one or more time-block rules. Each rule has:
   - **Repeat** setting — e.g., *weekly* with day-of-week multi-select (Mon–Fri rule + separate Sat–Sun rule with different hours), or non-repeating/date-specific rules for one-off availability. **[Exact list of repeat options unverified — weekly + specific-date patterns are confirmed by examples; monthly-pattern repeats like "first Thursday" are handled by creating a separate schedule.]**
   - **Start / stop times** per rule.
   - **"Start Service" (slot alignment)** — controls when appointments may begin: **on the quarter hour, on the half hour, on the hour, or immediately after the previous appointment (buffers included)**. This is effectively the slot-granularity setting; e.g. a 30-min service with 15-min pre/post buffers set to start every half hour means the engine looks for a free 1-hour window beginning at each half-hour mark.
   - Docs warn the rule's window must be at least as long as duration + buffers or no slots appear (top troubleshooting cause).
3. **Booking Limitations**:
   - **"No sooner than"** — minimum notice (blocks last-minute bookings).
   - **"No later than / more than X in the future"** — maximum booking horizon (e.g., not more than 7 days out ⇒ day 8+ never shows).
   - **Max bookings per day** and **max bookings per week** — caps counted across *all* services on that Availability Schedule; once hit, no more slots show for the period.
4. **Calendar Checks (cross-checking)** — pick which calendars (17hats-type and Google-type; plus enabled team members' 17hats calendars) the engine scans for conflicts. Any overlapping **Event** removes the overlapping slots. Notes:
   - Only **Events** are checked — **To-Dos are never cross-checked**.
   - Google events marked "Free" **still block** — 17hats reads the event, not its free/busy transparency. (Documented gotcha.)
   - Recommended practice: cross-check everything except the to-do calendar; personal-calendar items (vacations, appointments) then automatically suppress bookable times.
5. **Override the Following Availability Schedule** — schedule hierarchy: Schedule B (e.g., first-Thursday feedback sessions) can be set to **override** Schedule A (Mon–Fri consults), removing A's availability wherever B applies. Prevents two schedules from double-exposing the same time.
6. **Team Members** (multi-user accounts) — enable which team members are bookable on this schedule:
   - One member enabled ⇒ all bookings go to them.
   - Two+ enabled ⇒ client picks a specific member **or "Any Team Member."** "Any" fills the **account owner first, then others in Account Settings order** (sequential fill — *not* load-balancing round-robin).
   - **"Group as a Team"** option: every enabled member is booked for *every* booking (joint appointments).
   - Reassigning a booking's team member requires **rescheduling** the booking and picking a new member.
7. **Header image / branding** — per-Availability-Schedule custom header image (recommended 2731×527px, ≤5MB) uploaded via Brand Preferences → Images; a "Remove Logo From Online Scheduling" toggle controls whether the brand logo also renders. Brand colors/fonts (HEX-customizable on higher legacy tiers) apply to Online Scheduling pages along with all other client-facing surfaces.
8. **Cancellation limitations** — the Availability Schedule holds cancellation limitation settings (how close to the appointment clients may cancel/reschedule). **[Existence confirmed in docs; the exact configurable values (e.g., hours before) unverified.]**

**When to create additional Availability Schedules** (per dedicated help article): different working hours per service type, different team members, seasonal/date-specific offerings (mini-sessions), or schedules that must override one another.

### 2.4 Client-facing booking page UX

Confirmed flow (from "Booking Appointments," FAQs, and feature pages):

1. Client opens the **schedule link** (shared by email, linked from social bios, or **embedded on a website** via generated embed code).
2. **Pick a Service** (only if the schedule carries multiple Services).
3. **Pick a date, then a time slot** from computed availability (dates/slots render only where all rules pass; e.g. "Oct 16: 10:30, 11:00, 11:30 …").
4. **Answer Booking Questions** (per-Service, up to 10, each required or optional) — asked *after* time selection, *before* contact info.
5. **Enter contact information** (+ **payment details** if the Service requires payment).
6. **Confirmation page** — shows booking details; for Zoom services the unique Zoom URL appears here. Client receives the confirmation email; page/email expose **"reschedule" / "manage booking"** actions.
- Branding: header image, logo, brand colors/fonts.
- **Time zones**: 17hats has a single account/brand **Time Zone setting (Brand Preferences)** with DST handling ("pick the closest DST-observing city"). **[Unverified: whether the public booking page auto-detects or lets the client switch to their own time zone. No help article or review found describing client-side timezone conversion — a real risk that times display in the business's zone only. Treat as a gap to verify in a trial account, and an easy place to beat them (Calendly/Acuity both auto-localize).]**
- **[Unverified]** Whether a single "master" booking page listing *all* Availability Schedules exists; docs only describe per-schedule links/embeds.

### 2.5 Payments at booking (Pay Upon Booking)

- Per-Service toggle ("Online Payment is a per-service option").
- Prerequisite: **Stripe** (credit-card enabled) or **Square** connected under Invoice Options. (Stripe is the primary documented processor; legacy Stripe article exists; ACH is supported by 17hats invoicing generally.)
- Options per Service: **full payment** or **partial payment/deposit** (percentage or set amount) at booking, with **remaining-balance due date** configurable (e.g., balance due day-of-service).
- Flow: client picks slot → enters contact + card info → payment processes → **an Invoice is auto-created** and visible in the Contact's Project, the **Client Portal**, the Documents tab, and Recent Client Activity; **payments post automatically to 17hats Bookkeeping**.
- Marketing positioning: "secure payment before the appointment," reduce no-shows.
- **[Unverified]** Whether a failed payment holds the slot, and whether refunds on cancellation are automated (no doc found; assume manual refund via processor).

### 2.6 Booking Questions

- Up to **10 questions per Service**; each **required or optional**.
- Asked after date/time selection, before contact info.
- Question answers can be **mapped to Contact fields, Project fields (including Project Name), and Custom Fields** — i.e., booking doubles as structured lead capture.
- Answers surface in: the Bookings tab (booking detail), the Project page's booking tab, and wherever mapped.
- On **reschedule**, previously-given answers persist (client does not re-answer).
- **[Unverified]** Full list of question input types (text, choose-from-list, etc.). "Choose From A List" question types exist in Lead Capture Forms and likely mirror here.

### 2.7 Group scheduling (events/classes)

- **Group Service Type** = multiple bookings per time slot (group coaching, workshops, team headshots, classes).
- **Number of Bookings per time slot** = max capacity; slot hides when full.
- Each attendee books individually (own contact record, own payment if enabled, own emails). Booking detail shows **attendees** list plus name/date/time/location/email/phone/payments/answers — an implicit per-slot roster.
- Was a documented "workaround" pattern before becoming a first-class feature (help article: "Online Scheduling Groups: From Workaround to New Feature," ~late 2024).
- Historically gated to Premier/Founding or the Advanced module.
- **[Unverified]** Waitlists, attendee-cap messaging, or bulk-email-the-roster features — nothing found; assume absent.

---

## 3. Reminders, confirmations, cancel/reschedule

### 3.1 Email/SMS communications

All scheduling emails are **email templates of type "Scheduling"** (template type must be "Scheduling" for scheduling tokens to resolve), selected per Service:

- **Confirmation email** — optional but recommended; sends **immediately upon booking** when Approval Settings are off; with approval on, it sends at confirmation time.
- **Reminder emails — exactly two supported slots**:
  1. **One day before** the booking date.
  2. **Day of** the booking, sent **1–2 hours before** start time.
  - Reminders **only send for confirmed bookings** (pending/unapproved bookings get no reminders).
- **Cancellation email** — template sent to the contact **when they cancel**; configurable **per Service** (cancellation *limitations* live on the Availability Schedule; cancellation *email* lives on the Service).
- **Personalization via Scheduling tokens** (exact token syntax from the "Complete List of Tokens" article):
  - `[% booking.scheduled_service.name %]` — service name
  - `[% booking.scheduled_service.location.name %]` — location name
  - `[% booking.scheduled_service.location.location %]` — location address (renders the **Zoom URL** for Zoom services)
  - `[% booking.calendar_event.formatted_token_date('start') %]` — booking date
  - `[% booking.calendar_event.formatted_time('start') %]` / `...('end')` — start/end time
  - `[% booking.scheduled_service.duration %]` — duration
- **SMS (paid add-on, US/Canada; ~$40 setup + from $10/mo incl. dedicated local number + 100 msgs)**: automatic texts when a meeting is **booked, confirmed, coming up tomorrow, starting in a couple hours, and if the client cancels** — mirroring the email cadence. Contacts must opt in (via Lead Capture Forms, Online Scheduling, or Questionnaires).
- **[Unverified]** ICS attachment / "add to calendar" button in confirmation emails — not documented anywhere found. (Third-party Q&A about "Unknown Organizer" in 17hats scheduling emails suggests **some calendar invite/ICS is sent** with the confirmation, but treat as unconfirmed.)

### 3.2 Approval (request-to-book) mode

- Default: bookings are **instantly confirmed**.
- With **Approval Settings** enabled on a Service: booking goes to **Pending** state; slot is claimed but service is unconfirmed until the owner confirms from the Bookings tab or Project page.
- Pending bookings can trigger their own **"requires approval" Workflow** (e.g., send a quote or invoice); a workflow action can **auto-confirm the booking** once prior items complete (e.g., confirm on invoice payment) — a notable pattern: *approval-gated booking that auto-confirms when the client pays*.
- Confirmation email + confirmed-workflow fire at confirmation.
- Recommended practice: route pending bookings to a dedicated calendar.
- **Pending bookings cannot be edited once they're in the past.**
- **[Unverified]** Auto-expiry of unapproved pending bookings, decline-with-message flow.

### 3.3 Cancellation & reschedule

- **Client side**: confirmation page/email includes **"reschedule" and "manage booking"** buttons. On reschedule the client picks a new slot; **question answers carry over**; **rescheduled bookings do NOT need re-approval** even for approval-gated services. Client cancellation triggers the cancellation email (and SMS if enabled), and the **slot reopens**.
- **Owner side**: reschedule/cancel from the **Bookings tab** or **Project page → Bookings tab**. Rescheduling **moves the linked calendar Event automatically**.
- **Notification asymmetry (documented weakness)**: when a booking is rescheduled, the **account owner** gets an email notification, but **no automatic notice goes to the client** — docs literally say to notify the client manually. **[Direction nuance unverified: at minimum owner-initiated changes don't notify the client automatically.]**
- Cancellation limitations (cutoffs) configurable on the Availability Schedule (§2.3.8).
- **[Unverified]** Automatic refund handling on cancellation of a paid booking; cancellation-reason capture; no-show status tracking (nothing found — likely absent).

---

## 4. Internal calendar & event model

### 4.1 Calendar page & views

- Views: **Day / Week / Month** (no documented agenda/list view on desktop; mobile app has a month view per its own help article). You can filter to a single calendar at a time.
- Dashboard includes a **3–5 day "Quick View" calendar strip** (depth depends on screen size) built from the calendars chosen in the User's Calendar Settings.
- Mobile apps (iOS/Android) include calendar viewing/editing.
- Reviews complain the calendar view is inflexible ("never worked quite the way I wanted") — expect a fairly basic grid.

### 4.2 Calendars (containers)

- Users create **multiple named calendars**, each with a **color** and a **Type**: **"17hats" type** (internal-only) or **"Google" type** (bound 1:1 to a calendar in the connected Google account; syncs both ways).
- 17hats-type calendars can be **shared out read-only via a subscription link** (webcal/iCal feed) to Apple Calendar or "other calendar softwares."
- **Recommended setup** (official guidance): separate calendars for **Leads**, **Booked/Paid Clients**, **To-Do & Workflow items**, **Marketing/Social**, and **Personal/Life** — numbered/labeled and color-coded. Lead Capture Forms get assigned to the Leads calendar; workflow templates assign to the To-Do/Workflow calendar; a **Workflows "Change Calendar" action** moves a project's items from the Leads calendar to the Booked calendar when they convert (calendar = pipeline stage, visually).

### 4.3 Items that appear on the calendar

Auto-populated: **Project Dates, Events, Bookings, and To-Dos.** Details:

- **Event** — the core scheduled object. Creation (click a slot on the calendar → popup) captures:
  - **Event Name** (internal-facing "unless you invite your customer outside of 17hats" — i.e., no native client invite from a plain event),
  - **Description**,
  - **Date/Time** (start; end appears after start is set), **all-day** supported **[all-day: strongly implied, not explicitly documented]**,
  - **Location** (address or video link),
  - **Recurrence** ("select when the event should repeat"),
  - **Calendar** assignment (which named calendar, hence color + sync behavior),
  - **Project attachment** (optional) → unlocks two options:
    - **"Project Date"** — use this event as the project's date (shown at top of Project page); otherwise the event lands in the project's **Events tab**.
    - **"Attach Workflow"** — start a workflow in that project keyed off this event.
- **To-Do** — task with due date; shows on calendar but **never syncs to Google** and is **never cross-checked** by Online Scheduling.
- **Booking** — an Online Scheduling result; materialized as an Event on the Service's configured calendar and listed in Bookings/Project→Bookings.
- **Project Date** — each project's date/time/location renders on the calendar automatically.

### 4.4 Timezone model (internal)

- One **brand-level Time Zone** setting (bottom of Brand Preferences), city-based with automatic DST calculation; docs advise picking the nearest DST-observing city if yours is missing.
- Mismatched 17hats-vs-Google timezone settings cause hour-shifted events (dedicated troubleshooting article) — implying events are stored relative to the brand timezone and rendered without per-user timezone override. No per-user or per-event timezone found. **[No evidence of multi-timezone support anywhere in the product.]**

---

## 5. External calendar sync

### 5.1 Google Calendar (the only two-way sync)

- **Direction**: true **two-way** — events created in 17hats on a **Google-type calendar** push to Google; events created/edited in Google on a synced calendar pull into 17hats.
- **Scope rules**:
  - Only **Google-type** 17hats calendars sync; **17hats-type calendars never reach Google**.
  - Only **Events** sync — **To-Dos never sync** (dedicated FAQ article).
  - Calendars must **already exist in Google**; you connect the Google account (OAuth: enter Google username → Google auth → grant calendar permission), then in **Calendar Settings → Google Cal Settings → "Update Calendars to Sync"** check which Google calendars to sync. Unchecked ones show as "Disabled."
  - A newer article ("Calendar: Create & sync new Google Calendar," 2025) covers pulling newly-created Google calendars into the sync set via the same checkbox flow.
- **Connection limits**: **one Google account connection per 17hats User**. Multi-account needs are handled by **Google-side calendar sharing** into the connected account (documented workaround). Multi-user 17hats accounts: each user connects their own Google account.
- **Sync latency**: first sync takes **5–30 minutes** (pulls all events); ongoing sync is periodic (status shows "last synced"; docs suggest waiting 5–10 minutes). **No documented real-time/webhook push — expect polling.**
- **Conflict/busy semantics**: for Online Scheduling cross-checks, **all Google events block, including ones marked "Free"** (17hats ignores transparency). Docs don't describe edit-conflict resolution (last-write-wins assumed) **[unverified]**.
- **Troubleshooting surface**: "Google Calendar Not Syncing" article (check sync is active per-calendar in Calendar Settings); timezone-mismatch article (§4.4).

### 5.2 Apple Calendar / iCal

- **No direct two-way integration** ("Apple does not allow this two-way sync functionality" per 17hats docs).
- Two documented paths:
  1. **Subscription feed**: generate a share link for a **17hats-type calendar** and add it in Apple Calendar as a **calendar subscription** → strictly **one-way, read-only** (17hats → Apple; changes in Apple never reach 17hats). Works for "other calendar softwares" too (generic iCal/webcal feed).
  2. **Google as a bridge**: sync 17hats ↔ Google two-way, then let Apple devices consume the Google calendar.

### 5.3 Outlook / Microsoft 365

- **No native Outlook integration.** The only official article is "Connect a Google Calendar to an Outlook Calendar Online" — i.e., use **Google as the intermediary** (Outlook ↔ Google ↔ 17hats), or subscribe Outlook to a 17hats iCal feed (one-way).

### 5.4 Sync-related takeaways for a competitor build

- 17hats' sync stack is 2010s-era: Google-only two-way, polling-based, no free/busy transparency handling, no CalDAV, no Microsoft Graph. Matching Calendly-class expectations (Google + Outlook/Graph + iCloud CalDAV, near-real-time via push channels/webhooks, respect transparency) is a clear differentiation opportunity.

---

## 6. Integration with projects, workflows, and lead capture

### 6.1 Bookings → Contacts & Projects (CRM spine)

- On a confirmed booking, 17hats **auto-creates a Contact and a Project** (or attaches to an existing one — matching behavior on existing contacts **[matching rule unverified: presumably by email]**), and adds the booking as an **Event** in the Project.
- **Per-Service Project Management settings**:
  - **Calendar assignment**: pick the calendar the booking Event lands on; a newly created Project is placed on that calendar too.
  - **Project naming**: defaults to the **Service name**; if a Booking Question is mapped to "Project Name," the mapped answer becomes the Project Name.
  - **"Update Project Date to Booking Time"** toggle: off ⇒ booking is just an Event under the project's Bookings/Events tabs; on ⇒ booking's **date/time/location replace the Project's date/time/location**.
- Booking artifacts visible across the CRM: Bookings tab (left rail), Project → Bookings tab (view/confirm/reschedule/cancel), Client Portal + Documents (auto-created invoice for paid bookings), Bookkeeping (payments), Recent Client Activity feed.

### 6.2 Bookings → Workflows

- Each Service can attach workflows at two hooks:
  - **When a booking requires approval** (pending) — e.g., send questionnaire/quote/invoice; a workflow step can **auto-confirm** the booking when its prerequisites complete.
  - **When a booking is confirmed** — fires immediately at confirmation.
- The triggered workflow's **Base Date = the booking date** (not the trigger date): book an Aug 1 appointment ⇒ workflow steps schedule relative to Aug 1 (e.g., "send prep guide 3 days before base date"). This base-date model is the glue that makes booking-driven automation work (and, per reviews, also a common source of user confusion).
- Workflows can themselves contain **"Change Calendar"** actions (move project between Leads/Booked calendars), to-dos, emails, questionnaires, contracts, invoices — so a booking can kick off an entire onboarding sequence.

### 6.3 Lead capture & distribution of the scheduler

- Booking pages are distributed as: **direct link** (email signature, social bio, email-template button/link — reviews grumble the link button sits at the bottom of emails), or **website embed** (embed code from the Availability Schedule's edit screen).
- **Lead Capture Forms (LCFs)** are a separate lead intake object (embeddable forms that create Contact+Project, tag, auto-reply, record lead source, and trigger workflows — including branching to different workflows based on a "Choose From A List" answer). The documented **LCF ↔ scheduling pattern** is: LCF submission → auto-reply or workflow email that **contains the Online Scheduling link** → lead self-books → booking confirms → booking workflow takes over. ("Fully Automating Your Booking Process" blog.)
- **[Unverified]** Native embedding of a scheduler *inside* an LCF or a combined form+scheduler step — not found; the two features appear linked only via emails/workflows.
- Online Scheduling itself acts as lead capture: question answers map to contact/project fields; new bookers become Contacts automatically. Marketing also mentions **Meta (Facebook/Instagram) tracking baked in** for lead attribution **[details unverified]**.
- 17hats marketing leans on this loop: LCF (capture) → workflow (respond in minutes) → scheduling link (book consult) → pay-at-booking (commit) → project/workflow (deliver).

---

## 7. Inferred data model (schema sketch)

What 17hats' documented behavior implies. Naming is ours; 17hats' actual schema is internal. Token syntax (`booking.scheduled_service`, `booking.calendar_event`, `scheduled_service.location`) leaks real relationships: **Booking belongsTo ScheduledService, Booking hasOne CalendarEvent, ScheduledService hasOne Location.**

```text
Brand
  id, name, timezone (city-based, DST-aware), logo, colors/fonts,
  online_scheduling_enabled (bool)

User (team member)
  id, brand_id, name, email, order_index          -- order drives "Any Team Member" fill
  google_connection (0..1 per user)

Calendar
  id, brand_id, owner_user_id, name, color,
  type ENUM('17hats','google'),
  google_calendar_ref (nullable),                  -- bound external calendar id
  ical_share_token (nullable),                     -- read-only webcal feed
  sync_status, last_synced_at

Event
  id, calendar_id, name, description,
  start_at, end_at, all_day?,
  location_text, recurrence_rule (nullable),
  project_id (nullable), is_project_date (bool),
  source ENUM('manual','booking','google_sync','workflow'),
  external_event_id (nullable)                     -- google event mapping

ToDo
  id, calendar_id, project_id?, due_date, ...      -- on calendar; never synced,
                                                   -- never conflict-checked

Service ("ScheduledService")
  id, brand_id, name, description,
  service_type ENUM('individual','group'),
  duration_min, buffer_before_min, buffer_after_min,
  group_capacity (nullable; group only),
  location_id -> LocationTemplate,
  payment_enabled (bool), payment_mode ENUM('full','partial'),
  payment_amount_type ENUM('percent','fixed'), payment_amount,
  balance_due_rule (e.g. day-of-service),
  approval_required (bool),
  confirmation_email_template_id?, cancellation_email_template_id?,
  reminder_day_before_template_id?, reminder_day_of_template_id?,
  workflow_on_pending_id?, workflow_on_confirmed_id?,
  target_calendar_id,                              -- where booking events land
  project_name_source ENUM('service_name','mapped_question'),
  update_project_date (bool)

LocationTemplate
  id, brand_id, type ENUM('in_person','phone','zoom'),
  name, address_or_number, instructions

BookingQuestion
  id, service_id, position (<=10), prompt, input_type,
  required (bool),
  maps_to ENUM(null,'contact_field','project_field','project_name',
               'custom_field'), maps_to_field_ref

AvailabilitySchedule
  id, brand_id, name, slug/link_token, embed_enabled,
  header_image, show_logo (bool),
  min_notice, max_horizon,                         -- booking limitations
  max_bookings_per_day, max_bookings_per_week,
  cancellation_cutoff (config unclear),
  overrides_schedule_id (nullable)                 -- hierarchy

AvailabilityScheduleService (join)                 -- schedule exposes N services
  schedule_id, service_id

AvailabilityRule
  id, schedule_id,
  repeat ENUM('weekly','specific_date', ...),
  days_of_week[] | date,
  start_time, end_time,
  slot_alignment ENUM('quarter_hour','half_hour','hour','back_to_back')

CalendarCheck (join)
  schedule_id, calendar_id                         -- calendars cross-checked busy

ScheduleTeamMember (join)
  schedule_id, user_id, group_as_team (bool)

Booking
  id, service_id, schedule_id, contact_id, project_id,
  calendar_event_id,                               -- 1:1 materialized event
  team_member_user_id (nullable),
  status ENUM('pending','confirmed','cancelled')   -- (+past-locked)
  booked_at, start_at, end_at,
  zoom_meeting_id/url (nullable),
  invoice_id (nullable),                           -- pay-at-booking
  slot_capacity_group_key (group services)

BookingAnswer
  booking_id, question_id, value                    -- persists across reschedule

EmailTemplate
  id, type ENUM(...,'scheduling',...), body with [% ... %] tokens
```

### Availability computation (as documented + inferred)

For a requested (schedule, service, date range), per team member (or pooled for "Any"):

1. **Generate candidate slots**: for each AvailabilityRule active on the date, enumerate start times per `slot_alignment` (:00/:15/:30/:45, :00/:30, :00, or back-to-back packing). Candidate window length = `buffer_before + duration + buffer_after`; the whole window must fit inside the rule's start–end times.
2. **Apply override hierarchy**: remove candidates on this schedule wherever an overriding schedule claims the time.
3. **Calendar Checks**: fetch Events (not To-Dos) from every cross-checked calendar (17hats + Google + enabled team members' calendars); drop any candidate whose *full window* overlaps any event — regardless of the event's free/busy flag.
4. **Booking Limitations**: drop candidates earlier than `now + min_notice` or later than `now + max_horizon`; drop whole days/weeks where confirmed+pending bookings on this schedule have hit `max_bookings_per_day/week`.
5. **Group capacity**: for group services, a slot stays visible while `bookings_in_slot < group_capacity` (skips the overlap-check for its own group slot).
6. **Pending bookings** hold their slot (approval-gated bookings still consume availability).
7. Render remaining slots in the brand's timezone **[client-timezone conversion unverified]**.

Latency caveat: because Google sync is polling-based (minutes), the conflict data in step 3 can be stale — 17hats presumably re-checks at booking time against its own DB, but a just-added Google event may not block a booking made within the sync window **[inferred]**.

---

## 8. Strengths / weaknesses

### Strengths (vs. Calendly/Acuity)

1. **Post-booking depth**: booking → Contact + Project + Event + Invoice + Workflow in one motion. Calendly needs Zapier/integrations for any of this; Acuity has payments but no CRM/projects/contracts.
2. **Approval mode + workflow auto-confirm** (confirm-on-payment / confirm-on-quote-acceptance) is genuinely differentiated for high-consideration bookings.
3. **Pay-at-booking creates a real Invoice** that reconciles into bookkeeping — not just a Stripe charge.
4. **Workflow base date = booking date** enables "X days before appointment" automation chains (prep emails, questionnaires, contracts).
5. **Question→field mapping** turns booking into structured CRM data capture.
6. Schedule **override hierarchy** and **booking caps per day/week** are decent availability primitives (Acuity-esque).
7. Group services, Zoom auto-links, per-schedule branding, SMS reminders — feature parity on most solo-operator table stakes.
8. One price, everything included (post-2025 single ~$60/mo plan).

### Weaknesses / complaints (from docs, reviews on Capterra/G2/Software Advice, comparison articles)

1. **Calendar sync is Google-only two-way.** Apple = one-way feed; Outlook = nothing native. Big adoption blocker for Microsoft-centric users.
2. **Polling sync** (minutes of latency; first sync up to 30 min); "Free" events block; timezone mismatches cause hour-shifted events.
3. **No documented client-timezone localization** on the booking page (single brand timezone) — Calendly/Acuity auto-localize.
4. **Reschedule doesn't notify the client automatically** (owner is told to email manually) — a glaring automation hole in an "automation" product.
5. Only **two fixed reminder slots** (day-before, day-of) — Calendly/Acuity allow arbitrary reminder schedules.
6. **"Any Team Member" = sequential fill (owner-first), not round-robin**; no pooled/collective availability beyond "Group as a Team"; reassignment requires a full reschedule.
7. Reviews: **dated, sometimes buggy UI**; "calendar view never worked quite the way I wanted"; "scheduling features weren't super robust — I still use Calendly"; workflow/base-date confusion; scheduling link buried at the bottom of emails; near-zero reporting/analytics (no booking-conversion metrics).
8. No evidence of: waitlists, no-show tracking, automatic refunds, per-event timezones, agenda view, capacity-based classes with rosters/bulk actions, routing forms, browser-extension/embedded popups, or an API/webhooks for scheduling **[absence inferred from silence — verify in trial]**.
9. Historic feature gating (Advanced module) left docs confusing; terminology (Service vs Schedule vs Rule vs Booking) has a learning curve — 17hats even ships a "17hats Terminology" glossary article.

---

## 9. Build recommendations (copy / improve / skip)

### Copy (proven, differentiating)

- **Service + Availability Schedule split** (offering vs. window, many-to-many via one booking page). It cleanly supports multi-service booking pages, and the override hierarchy.
- **Booking → Contact/Project/Event/Invoice/Workflow fan-out.** This is 17hats' entire moat; make the booking object a first-class CRM citizen from day one.
- **Pay-at-booking with full/deposit + balance-due rules, generating a real invoice** tied to the client record and ledger.
- **Approval mode with workflow-driven auto-confirm** (confirm when invoice paid / contract signed).
- **Booking questions with field mapping** (contact/project/custom fields, project-name mapping) + answers persisting across reschedules.
- **Buffers + slot alignment options** (quarter/half/hour/back-to-back) and **booking caps per day/week** and min-notice/max-horizon limits.
- **Workflow base date = appointment date** relative automation.
- **Per-schedule branding** (header image, logo toggle, brand colors).
- **Group service capacity** model (N bookings per slot, slot hides at capacity).
- **Zoom auto-meeting per booking** with the URL merged into confirmation/reminder templates via tokens.

### Improve (beat 17hats here)

- **Calendar sync**: Google **and** Microsoft Graph (Outlook/365) **and** iCloud CalDAV, two-way, webhook/push-based near-real-time, respecting free/busy transparency, with a booking-time conflict re-check. This alone wins switchers.
- **Timezones**: store UTC + IANA zone per event; auto-detect client timezone on the booking page with a visible switcher; per-user timezones for teams.
- **Notifications**: symmetric automatic notifications for *every* state change (booked, approved, declined, rescheduled-by-either-party, cancelled), email + SMS + ICS attachments/updates (METHOD:REQUEST/CANCEL so client calendars self-update).
- **Reminders**: arbitrary N reminders at configurable offsets, per channel.
- **Teams**: true round-robin with weighting/priority, collective availability (all-must-be-free), easy reassignment without rescheduling.
- **Reschedule/cancel policy engine**: cutoffs with clear client messaging, cancellation reasons, no-show marking, automated refund/credit rules for paid bookings.
- **Analytics**: bookings by service/source/period, show rate, conversion from page view → booking, revenue per service.
- **Modern availability UX**: month-grid with slot preview, agenda/list views, "next available" jump — address the #1 UI complaint.
- **Lead capture native integration**: allow embedding the scheduler as a step of a lead form / routing form (answer-based routing to different services), instead of 17hats' email-a-link-from-a-workflow pattern.
- **API + webhooks** for bookings (17hats has none publicly).

### Skip / deprioritize

- 17hats' **calendar-as-pipeline convention** (Leads calendar vs. Booked calendar, workflow "Change Calendar" steps) — it's a workaround for weak pipeline visualization; a real pipeline/kanban plus calendar tags does this better.
- **One-way iCal share links as the Apple story** — do CalDAV properly instead (keep read-only feeds as a cheap extra, though).
- Legacy **module/tier gating** of scheduling features (Basic vs Advanced) — pricing complexity generated years of confused docs and support load.
- Google-as-a-bridge documentation gymnastics — solved by native providers.
- **Two-types-of-calendars** (17hats-type vs Google-type) mental model — hide sync binding behind a per-calendar "connected account" setting rather than a type the user must understand.

---

## 10. Sources

Official Help Center (help.17hats.com):

- Online Scheduling: Start here! — https://help.17hats.com/en/articles/2912511-online-scheduling-start-here
- Online Scheduling collection — https://help.17hats.com/en/collections/1698393-online-scheduling
- Setup Part 1 – Create your Services — https://help.17hats.com/en/articles/2913378-online-scheduling-setup-part-1-create-your-services
- Setup Part 2 – Availability Settings — https://help.17hats.com/en/articles/2913385-online-scheduling-setup-part-2-availability-settings
- Availability Rules — https://help.17hats.com/en/articles/9967692-online-scheduling-availability-rules
- Service Time Frame — https://help.17hats.com/en/articles/9893901-online-scheduling-service-time-frame
- Service Locations — https://help.17hats.com/en/articles/9893949-online-scheduling-service-locations
- Booking Limitations (release note) — https://17hats.releasenotes.io/release/mU91J-online-scheduling-booking-limitations
- Calendar Checks — https://help.17hats.com/en/articles/9904377-online-scheduling-calendar-checks
- Team Members — https://help.17hats.com/en/articles/9904365-online-scheduling-team-members
- Multiple Services on one Schedule — https://help.17hats.com/en/articles/9904320-online-scheduling-availability-multiple-services-on-one-schedule
- When to create additional Availability Schedules — https://help.17hats.com/en/articles/3332262-online-scheduling-when-to-create-additional-availability-schedules
- Booking Appointments — https://help.17hats.com/en/articles/3059282-online-scheduling-booking-appointments
- FAQs — https://help.17hats.com/en/articles/2921704-online-scheduling-faqs
- Troubleshooting — https://help.17hats.com/en/articles/3287818-online-scheduling-troubleshooting
- Service Booking Questions — https://help.17hats.com/en/articles/6837367-online-scheduling-service-booking-questions
- Approval Settings — https://help.17hats.com/en/articles/9894043-online-scheduling-service-approval-settings
- Confirmation & Cancellation Settings — https://help.17hats.com/en/articles/9904227-online-scheduling-services-confirmation-cancellation-settings
- Automatic Email Reminders — https://help.17hats.com/en/articles/4901233-online-scheduling-service-automatic-email-reminders
- Online Scheduling Payments — https://help.17hats.com/en/articles/3980157-online-scheduling-payments
- Project Management (per-service) — https://help.17hats.com/en/articles/9894024-online-scheduling-services-project-management
- Online Scheduling Workflows — https://help.17hats.com/en/articles/2933608-online-scheduling-workflows
- Online Scheduling Groups — https://help.17hats.com/en/articles/9967753-online-scheduling-groups
- Groups: From Workaround to New Feature — https://help.17hats.com/en/articles/9966962-online-scheduling-groups-from-workaround-to-new-feature
- Header Images (per schedule) — https://help.17hats.com/en/articles/6800159 and https://help.17hats.com/en/articles/6798211-online-scheduling-header-images
- Complete List of Tokens — https://help.17hats.com/en/articles/1235598-complete-list-of-tokens
- Calendar Overview — https://help.17hats.com/en/articles/894193-calendar-overview
- Creating a Calendar Event — https://help.17hats.com/en/articles/927438-creating-a-calendar-event
- Recommended Calendar Setup — https://help.17hats.com/en/articles/3112379-recommended-calendar-setup
- Workflows: Change Calendar — https://help.17hats.com/en/articles/2165044-workflows-change-calendar
- How To Connect Your Google Calendar — https://help.17hats.com/en/articles/966461-how-to-connect-your-google-calendar
- Google Calendar Sync Explained — https://help.17hats.com/en/articles/7438269-google-calendar-sync-explained
- Google Calendar Not Syncing — https://help.17hats.com/en/articles/844570-google-calendar-not-syncing
- Create & sync new Google Calendar — https://help.17hats.com/en/articles/11003245-calendar-create-sync-new-google-calendar
- Multiple Google accounts — https://help.17hats.com/en/articles/853432-sync-google-calendars-from-multiple-google-calendar-accounts
- To-Dos & Google sync — https://help.17hats.com/en/articles/927254-are-to-do-items-synced-to-my-google-calendar
- Apple Calendar connection — https://help.17hats.com/en/articles/927439-how-do-i-connect-17hats-events-to-my-apple-calendar
- Share 17hats calendar to other software — https://help.17hats.com/en/articles/3117305-how-to-share-a-17hats-calendar-to-other-calendar-softwares-such-as-apple-cal
- Google↔Outlook bridge — https://help.17hats.com/en/articles/1273006-connect-a-google-calendar-to-an-outlook-calendar-online
- Event time differences (timezones) — https://help.17hats.com/en/articles/934805-why-are-calendar-event-times-different-between-17hats-and-google
- Zoom Integration — https://help.17hats.com/en/articles/4124528-zoom-integration
- Lead Capture Forms Overview / Details — https://help.17hats.com/en/articles/853251 and https://help.17hats.com/en/articles/3113718
- 17hats Terminology — https://help.17hats.com/en/articles/3388927-17hats-terminology

Official marketing / blog / release notes:

- Online Scheduling feature — https://www.17hats.com/features/online-scheduling
- Online Scheduling Payments feature — https://www.17hats.com/features/online-scheduling-payments
- Group Online Scheduling feature — https://www.17hats.com/features/group-online-scheduling
- Zoom Integration feature — https://www.17hats.com/features/online-scheduling-zoom-integration
- Calendar feature — https://www.17hats.com/features/calendar
- Google integration page — https://www.17hats.com/integration/google-com ; Apple — https://www.17hats.com/integration/apple-calendars ; Zoom — https://www.17hats.com/integration/zoom-us
- SMS Texting — https://www.17hats.com/sms-texting
- Lead Capture Form feature — https://www.17hats.com/features/lead-capture-form
- Pricing — https://www.17hats.com/pricing
- Blog: Online Scheduling Groups — https://blog.17hats.com/maximize-efficiency-with-17hats-online-scheduling-groups/
- Blog: Online Scheduling Payments — https://blog.17hats.com/online-schedule-payments/
- Blog: Locations spotlight — https://blog.17hats.com/feature-spotlight-online-scheduling-locations/
- Blog: Zoom integration — https://blog.17hats.com/online-scheduling-zoom-integration-transforming-frustration-to-joy/
- Blog: 5 calendars you need — https://blog.17hats.com/staying-organized-5-calendars-you-need-in-your-17hats-account/
- Blog: Fully Automating Your Booking Process — https://blog.17hats.com/fully-automating-your-booking-process/
- Release notes: Header Images — https://17hats.releasenotes.io/release/4oYZQ-header-images-for-17hats-online-scheduling ; Zoom — https://17hats.releasenotes.io/release/fbnS6-integration-zoom

Third-party reviews & comparisons:

- Capterra 17hats reviews — https://www.capterra.com/p/144328/17hats/reviews/
- G2 17hats reviews — https://www.g2.com/products/17hats/reviews
- Software Advice: 17hats vs Calendly — https://www.softwareadvice.com/appointment-scheduling/17hats-profile/vs/calendly/
- TrustRadius 17hats vs Calendly — https://www.trustradius.com/compare-products/17hats-vs-calendly
- SchedulingKit: Best booking software for photographers — https://schedulingkit.com/hub/scheduling/best-booking-software-for-photographers
- 17hats pricing analyses — https://taskip.net/17hats-pricing/ ; https://onesuite.io/blog/17hats-pricing/ ; https://getzendo.io/blog/17hats-pricing/
- 17hats University tutorials — https://www.17hatsuniversity.com/17hats-qt-categories/online-scheduling

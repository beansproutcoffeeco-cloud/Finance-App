# 17hats: Workflows & Automation Engine

> Research date: 2026-07-07. Sources: help.17hats.com articles (via search excerpts — the help center and 17hats.com blocked direct fetching from this environment, so article content was reconstructed from extensive search-result extracts of those exact articles), 17hats blog/feature pages, 17hats University tutorials, and third-party writeups (Improve Photography, Idalia Photography, Hannah Marie, Worcus, LetNicoleHelp, Deb Mitzel Creative) and comparison posts. Uncertainty is flagged inline as **[unverified]** or **[inferred]**.

---

## 1. Summary

17hats' automation is built around **Workflows**: reusable, linear checklists of steps (To-Dos, Actions, Pauses) that are attached to a **Project** and execute over time relative to a **Base Date** (usually the project/event date). It is deliberately *not* a branching automation graph like Dubsado's node-based "Flows" — it is a linear sequence with three step types, per-step timing rules, per-step "automatic vs. needs my approval" control, and per-step **completion triggers** (e.g., a "Send Invoice" step isn't "done" until the invoice is paid, which gates every subsequent step). Branching is achieved indirectly: lead-capture-form answers, questionnaire answers, product purchases, and scheduling events apply **Project Tags**, and tags can **start or stop entire workflows** (the 2025-era "Start/Stop Workflow Automation" feature). Multiple workflows can run concurrently on one project, and workflows can chain (an action step can start another workflow). Users consistently rank Workflows as 17hats' killer feature because it's approachable: one linear list, human-readable timing ("7 days before the Project Date"), and a built-in "review before it sends" safety valve.

Key architectural facts for a builder:

- Workflow **templates** are copied into projects at activation time (structural edits to the template do NOT propagate to running instances; edits to *referenced* email/document templates DO, because steps hold references, not copies, to those).
- Steps complete either by **date arrival + auto-execution**, by **user check-off/approval**, or by a **client-side event** (quote accepted, contract signed, invoice paid, questionnaire completed).
- The timing engine anchors every step to one of: the workflow **activation date**, the **Base Date**, or **completion of the previous step**.
- Automated workflow emails batch out **starting at 10 a.m. account-local time, staggered over ~2 hours** — a deliberate humanizing detail.

---

## 2. Core concepts

### 2.1 The object hierarchy

- **Contact → Project → Workflow(s)**. Everything in 17hats hangs off a Project (a job: "Smith Wedding," "Q3 Website Redesign"). Workflows never attach to a contact directly; they attach to a project. (A lead capture form submission creates a Lead contact + a project, then attaches the workflow to that project.)
- **Workflow Template**: built under Account Settings → Templates → Workflows (Premier/higher tiers). A named, ordered list of steps, optionally grouped into **Phases**.
- **Running workflow (instance)**: when you add a workflow to a project, 17hats **copies the template's To-Do/Action/Pause items into the project**. Help center ("Updating Workflow Templates," article 879497): *"When adding a workflow to a project, you are, in essence, copying the previously created Workflow Template's to-dos/action/pause items to the project."*
  - Consequence 1: adding/deleting/rearranging steps in the template does **not** update already-attached workflows; you must edit the instance on the project or re-apply.
  - Consequence 2: **email/quote/contract/invoice/questionnaire templates referenced by a step are live references** — editing the email template's copy updates what active workflows will send. But **swapping** which template a step points to only affects the template, not instances (instances keep the old reference).
- **Phases**: purely organizational segments inside a workflow ("Pre-Wedding," "Post-Wedding") to make long workflows (15+ steps is normal) readable. Phases have no execution semantics documented beyond grouping; users exploit them as deletable blocks ("put all follow-up emails in one phase so it can be deleted as a whole on an instance if not needed" — Streamline Followup Emails article). **[No evidence phases gate execution.]**
- **Lifecycle vs. Workflow** (frequent user confusion, 17hats has 3 help articles on it): a **Lifecycle** is a separate, single-per-project, 4–7 stage visual progress bar (Inquiry → Booked → Fulfilled...), a tracking/Kanban-ish device; a **Workflow** is the many-step task/automation list. Lifecycle **stages can themselves auto-advance on triggers** (e.g., "start this stage when a contract is sent / an invoice is paid") and a stage change can change the project's date/calendar (e.g., move project from Lead calendar to Booked calendar). Lifecycles also emit "stagnant stage" dashboard reminders (snoozable 1 day / 1 week / 1 month). Projects: **many workflows, exactly one lifecycle**, and neither requires the other.
- **Plan gating**: Essentials tier = no workflows at all; Standard = **Basic Workflows** (emails + to-dos only — no document sends); Premier = **Advanced Workflows** (documents, tagging actions, everything below). Note: 17hats' newer marketing claims "automation included on the single plan"; the Basic/Advanced split is from help article 7432912 ("Workflows: Advanced vs Basic") and reflects the 3-tier membership structure — verify current packaging before copying it.

### 2.2 Attachment to projects

Ways a workflow gets onto a project:

1. **Manually**: open the project → click "+" next to the **Workflows** header in the right sidebar → pick template → pick/confirm Base Date → Activate.
2. **Automatically** via any trigger in §3.
3. **In bulk**: Projects list view → select projects (e.g., filtered by a Project Tag) → "Bulk Actions" dropdown → "Add a Workflow" → choose workflow → **choose a base date option** → Activate. Used e.g. to blast an announcement/holiday workflow across all active clients.

At activation the user (or the triggering context) establishes the **Base Date** (§5). All date math is resolved per-instance from that anchor.

---

## 3. Triggers (what starts / advances / stops a workflow)

### 3.1 Workflow-start triggers — complete documented list

| # | Trigger | Mechanism / notes |
|---|---------|-------------------|
| 1 | **Manual attach** | "+" on project sidebar; user picks base date. Recommended by 17hats when you want to customize communications before they fire. |
| 2 | **Lead Capture Form submission (form-level)** | Form Details → Edit → select a Workflow. Every submission creates lead+project and activates that workflow. |
| 3 | **Lead Capture Form "Choose From a List" answer (answer-level)** | Each answer choice on a list question maps to a different workflow ("Wedding" → wedding workflow; "Family session" → family workflow). This is 17hats' primary "branching." |
| 4 | **Online Scheduling booking** | Per scheduling service, trigger a workflow **when a booking is confirmed** and/or **when a booking requires approval** (separate workflow slots). Confirmed-booking workflows fire immediately on confirmation (manual or auto). Base Date is auto-set to the **appointment date the client picked**. The approval-path workflow can itself send quote/contract/invoice that must be completed before the booking auto-confirms. |
| 5 | **Product/service purchase ("Workflows for Products")** | Attach a workflow to a product/service in your price list; when an invoice containing it is paid, the workflow triggers. Configurable: fire on **first payment** or on **paid in full**. If the client doesn't buy the add-on, nothing fires. (Setup flow blogged as Planning → Building → Connecting.) |
| 6 | **Project Tag added — "Start tag" (Start/Stop Workflow Automation, help article 13928403 + blog)** | A workflow template can declare one or more **start tags**; whenever that Project Tag lands on a project (from a lead form, a questionnaire "Choose One" answer, online scheduling lead-source, or another workflow's Add-Tag step), the workflow auto-starts. Constraints: only **one live instance per start tag** — re-applying the start tag spawns a new instance **only if the prior instance is Paused or Completed**; if a start automation is already active, a second tag application is ignored. |
| 7 | **Another workflow's action step** | Action item type "Start a new workflow" — explicit workflow chaining (e.g., Lead workflow's last step starts the Booking workflow). |
| 8 | **Quote acceptance → next workflow** | Via quote/invoice completion triggers plus chaining (the "Send Quote" step completes on acceptance/related contract-sign/invoice-pay, then a following "start new workflow" action fires). Also achievable via tags. |
| 9 | **Questionnaire "Choose One" answer** | Indirect: each answer applies a Project Tag → tag is a start tag → workflow starts immediately when the tag is applied. |
| 10 | **Lifecycle stage change** | Lifecycle stages start on triggers (contract sent, invoice paid) and can change project date/calendar. **[Whether a lifecycle stage can directly start a workflow is not clearly documented — treat as unverified; tag-based start is the documented route.]** |

Not supported (documented gaps): starting on email received/opened, on date thresholds without a project, on payment failure, on custom field values. No webhook/Zapier-native workflow trigger inside the Workflows feature itself **[Zapier integration exists for contacts/leads, but not as a workflow step — unverified for current version]**.

### 3.2 Step-advance (completion) triggers

A running workflow is a cursor over an ordered list; each step declares what "complete" means (see §4 and §6). Documented completion events:

- Date/time arrival (auto steps whose scheduled date arrives execute, then complete).
- User checks off a To-Do / Pause, or approves a pending Action.
- **Send Email**: complete "when sent."
- **Send Quote** (article 2165100): complete when **sent**, when **quote accepted** (items selected), or based on **related actions on the contract or invoice attached to the quote** — i.e., when the attached contract is signed and/or the attached invoice is paid. Marketing phrasing: "the Workflow will not move on to the next step until items are selected in the quote, the contract is signed, and the invoice is paid."
- **Send Contract**: complete when sent or **when contract is signed** **[option list inferred from the quote/invoice pattern and marketing copy; exact dropdown wording unverified]**.
- **Send Invoice** (article 2165133): complete **"When sent," "When the first invoice payment is made,"** or **"When invoice is fully paid."**
- **Send Questionnaire**: complete when sent or **when the client completes/submits it** **[strongly implied ("an email being sent or a contract signed" + review-request recipes); exact wording unverified]**.

These are the "Action Completed settings." Third-party trainer LetNicoleHelp: without them, "your workflow may push your project to 'Confirmed' as soon as you send the quote; with them, the workflow waits until you've collected all the documents you need."

### 3.3 Workflow-stop/pause triggers

- **Project Tag added — "Stop tag"**: a workflow template can declare stop tags; when the tag hits the project, the running workflow **pauses** automatically. Canonical recipe: a follow-up nurture workflow has stop tag "Booked"; when the client books via Online Scheduling (which removes one tag and adds "Booked"), the nagging stops. Multiple stop tags allowed per workflow.
- **Archiving the project** stops workflows; on unarchive, workflows must be **manually resumed** (they do not auto-resume).
- **Manual pause / stop / delete** — §7.

---

## 4. Step types — complete inventory

Exactly **three** step primitives ("items"): **To-Do**, **Action**, **Pause** (help article 879587). Everything else is configuration on these.

### 4.1 To-Do

A human task ("Call client," "Order album," "Back up files").

- **Appears on your calendar** and to-do list, on the Dashboard ("Let's Take Care of Business" section), and in the project.
- **Fields**: name/description; **Due Date** = N days **before/on/after** {workflow activation date | Base Date | previous item's completion} (§5); **assignee** — any user on the account (multi-user accounts can delegate steps); **"When Done" action** — optionally auto-fire something when the to-do is checked off, notably **"Send an Email — automatically"** (email goes the instant you check the box) or upon-approval variants. Recipe: use a To-Do as a lightweight *human review gate*: "review project, then check off → follow-up email sends itself."
- **Tag side-effects**: To-Do steps can **add/remove Contact and Project tags** (17hats University: "How to add and remove Tags from Workflow To-Do Step").
- Does not block by date: an overdue To-Do shows as overdue; steps *dependent on it* wait because their anchor is "after previous item completed." **[Exact overdue semantics for base-date-anchored later steps unverified — see §5.3.]**

### 4.2 Action

A thing 17hats itself performs. Documented action subtypes:

1. **Send Email** (pick an Email Template)
2. **Send Quote** (Quote Template; quotes can bundle contract+invoice → "accept quote, sign contract, pay invoice in one flow")
3. **Send Contract** (Contract Template)
4. **Send Invoice** (Invoice Template)
5. **Send Questionnaire** (Questionnaire Template)
6. **Start a new Workflow** (chaining)
7. **Archive the Project**
8. **Change the Calendar the project appears on** (17hats projects live on named calendars, e.g., Leads vs. Booked)
9. **Add/Remove Tags** (contact tags and project tags in one step; multiple tags per step; can create new tags inline by typing + comma/tab/enter) — Premier-tier ("Advanced Workflows") feature, release-noted as "Automate Tagging with Workflows."

Per-action configuration:

- **Template reference** (which email/document to send). Document sends ride on an email (the document link is delivered via an email template).
- **Timing** (§5).
- **Execution mode**: **automatically** vs. **upon your approval** (§6).
- **Completion trigger** ("Action Completed" setting): what event marks the step complete and unblocks successors (§3.2).
- Actions do **not** appear on the calendar; they appear on the Dashboard and the Workflow overview page.

Not available as actions (gaps worth noting for a competitor): SMS send **[17hats has no native SMS in workflows as of research date — unverified for 2026]**, internal-only notification step, webhook/HTTP step, conditional/if-else step, update-custom-field step, wait-until-specific-weekday step.

### 4.3 Pause

A hard gate. "When a Workflow reaches a Pause item, it will **not continue with any step after it until the Pause has been checked off**."

- Configured like a To-Do (relative due date) but **does not appear on your calendar** — it's a workflow-internal barrier with a reminder date.
- Uses: hold at the session/event date; hold for a human go/no-go ("is this lead a good fit?"); hold between booking and month-of-wedding prep; wait for anything 17hats can't detect.
- Checked off manually from the project's workflow view (or the workflow resumes when you check it).
- Note the distinction: a **Pause item** is a step *inside* the flow; **pausing a workflow** (§7) is an instance-level state.

---

## 5. Timing model

### 5.1 Base Date (help article 925561)

Every workflow instance has one **Base Date** — "the date the Workflow uses to determine when each step needs to be triggered or activated."

Resolution at activation:

- Project has a **Project Date** → Base Date defaults to it.
- Started from **Online Scheduling** → Base Date = the appointment date the lead selected.
- Started from a **Lead Capture Form** → Project Date if the form set one, else…
- **No project date** → Base Date = the date the workflow was activated.
- Manual/bulk attach → user explicitly picks the base date option in the activation dialog.
- **Editable after activation**: change the Base Date on a running workflow and **all steps anchored to it automatically re-schedule**. (This is how date changes/reschedules are absorbed.)

### 5.2 Per-step scheduling

Each To-Do/Action/Pause step chooses an **anchor** + **offset**:

1. **N days before / on / N days after the Base Date** (UI wording: "Before the Base Date," "on the Base Date," "After the Base Date").
2. **N days after the workflow is activated** ("Activating this workflow").
3. **Dependent on the previous item in the workflow** — N days after the previous step *completes* (which for document steps means after its completion trigger fires: contract signed, invoice paid…).

Granularity is **days**, not hours/minutes. There is no documented "at HH:MM" per step; instead:

- **Automated emails batch at 10:00 a.m.** in the account's Brand-Preferences time zone, "over the course of two hours, with some automated staggering in between" (help article 897486). Intent: many clients per day without a robotic simultaneous blast. **[Whether non-email actions (tagging, archiving) run at a different tick is undocumented.]**

### 5.3 Sequencing rules

- Steps execute **in list order**; the list is single-track (no parallel branches inside one workflow — parallelism is achieved by running multiple workflows on the project).
- Date-anchored steps can theoretically be scheduled out of visual order **[behavior when a later-listed step's date precedes an earlier incomplete gating step is not clearly documented; observed behavior per user guides is that Pauses and previous-step-dependent chains gate, while independently base-date-anchored steps fire on their dates — treat as partially inferred]**.
- A **Pause** unconditionally gates all subsequent steps regardless of their dates.
- **Action Completed** settings gate: a step whose completion trigger hasn't fired holds the "previous item" chain (and per marketing copy holds the workflow's progression) until the client acts.
- One Base Date per workflow is a real constraint: photographer Hannah Marie's writeup describes abandoning a single mega-workflow ("first contact→booking→engagement→wedding→post") because phases needed *different* anchor dates (booking date vs. engagement-session date vs. wedding date); the community-standard fix is **splitting into multiple chained workflows, each with its own Base Date**.

---

## 6. Approval vs. automatic execution

Every Action step carries a per-step switch: send **automatically** when its time comes, or **upon your approval**.

- **Automatic**: at the scheduled time (see 10 a.m. batching), the email/document goes out with no human involvement; step completes per its completion trigger.
- **Upon approval** ("pending your review"): when the step activates, it does **not** send; it surfaces as an item needing action on the **Dashboard ("Let's Take Care of Business")**, the **Workflow overview page**, and the **project**. The user can open it, tweak the actual email/document for this client, then approve/send. This is 17hats' answer to "automation that doesn't sound like a robot," and reviewers cite it constantly.
- Hybrid pattern via To-Do "When Done": pair a To-Do ("review gallery") with a following automatic action anchored "after previous item," or set the To-Do itself to "Send an Email when done (automatically)" — one checkbox = review + send.
- Manual-first pattern: 17hats' own docs suggest manual workflow attachment when you want to pre-edit communications for that client before activating.
- Online Scheduling has an analogous account-level **booking approval** setting (bookings require approval; the approval-time workflow can collect quote/contract/invoice before confirmation) — same philosophy at the trigger level.

There is no documented multi-user approval routing (e.g., "manager must approve") — approval = "any user checks it off / the assignee acts." **[Assignment of an approval-mode action to a specific user is implied by "assign Workflow items to other users" but per-item approval permissions are undocumented.]**

---

## 7. Managing running workflows

Surfaces: the **Workflows page** (global) with **Active Workflows** and **Paused Workflows** views (Paused view only appears if any exist) **[a Completed view is implied by the start-tag rule "only if the initial workflow is Paused or Completed" — unverified as a named view]**; plus the per-project Workflows panel.

- **Pause / Resume a workflow** (help article 13753480; the article ID suggests this instance-level control shipped relatively recently, ~2025): Project → open active workflow → **Edit → Pause Workflow**; or Workflows tab → Active Workflows → pause. Pausing "stops future steps from triggering while preserving the Workflow and its progress." Resume from the project or the Paused Workflows view → **Resume Workflow**. Auto-pause also happens via **stop tags** and **project archiving** (manual resume required after unarchive).
- **Edit a running instance**: because instances are copies, you edit the instance directly on the project — add/remove/rearrange steps, change dates, change which steps are automatic vs. approval. Template edits don't back-propagate (except referenced-template *content*, §2.1).
- **Change the Base Date** of the instance → anchored steps re-flow (§5.1).
- **Check off / complete steps manually**: To-Dos, Pauses, and pending approvals are all check-off-able; checking off effectively **skips or fulfills** a step and advances the chain. **[A dedicated "skip step" button distinct from mark-complete is not documented.]**
- **Delete a workflow from a project**: supported from the project's workflow panel **[mechanics under-documented; users reference removing/deleting applied workflows when re-applying an updated template]**.
- **Multiple concurrent workflows**: explicitly supported — "Projects can have multiple workflows in place at the same time"; the standard pattern is many small workflows (Lead Follow-Up + Booking + Fulfillment + Review-Request) live simultaneously or chained, vs. one mega-flow. Only one instance per **start tag** may be live at a time (§3.1 #6).
- **Visibility/monitoring**: Dashboard "Let's Take Care of Business" lists today's/overdue workflow to-dos and items awaiting approval; the project shows step states; Lifecycles provide the stage-level overview. There is **no cross-project "step X failed" error console** — failure surface is essentially "email couldn't send" notifications **[unverified]** and overdue items.

---

## 8. Example recipes (published, real)

### 8.1 Portrait Session pipeline (Improve Photography, "Step by Step: Designing a Portrait Session Workflow with 17hats")

Linear master list, base date = session date:

1. Receive client inquiry (lead capture) → 2. **Action:** send session & pricing info email → 3. Schedule session date (to-do/scheduling) → 4. **Action:** send session agreement (contract) → 5. **Action:** send invoice for session retainer → 6. **Action:** send "What to Wear" guide email — scheduled **14 days before Base Date** → 7. **Action:** session reminder email (days before) → 8. **Pause/To-Do:** shoot session (on Base Date) → 9. **Action:** thank-you email — **1 day after Base Date**, automatic → 10. **To-Do:** edit proofs, deliver gallery link → 11. To-Do: place order → 12. To-Do: deliver order → 13. **Action:** ask for review. Steps chosen automatic vs. upon-approval individually.

### 8.2 Wedding photographer, phase-split (Idalia Photography "Workflow Series"; Hannah Marie)

Four phases — **Pre-Wedding** (starts after quote accepted + contract signed + invoice paid; opens with a questionnaire gathering engagement-session scheduling + timeline info; ends with blog prep & vendor social handles), **Post-Wedding** (wedding night → gallery delivery: backup, cull, edit, client/vendor notifications, delivery), **Post-Gallery-Delivery** (review ask / social share, started manually ~2 weeks after delivery so you can choose which clients get it), **Album Design**. Hannah Marie's lesson: don't build it as ONE workflow — different phases need different base dates (booking vs. engagement vs. wedding date), so build **separate workflows per phase**, chained or manually started, each with its own Base Date. Her payoff anecdote: from the pool, one workflow activation sent personalized email + contract + invoice; contract signed and retainer paid before she got home.

### 8.3 Automated lead follow-up with auto-stop (17hats blog, "Start/Stop Workflow Automations")

Lead Capture Form applies start tag → **Lead Follow-Up workflow** starts: Day 0 auto intro email + scheduling link; Day 2 / Day 5 / Day 10 follow-up emails (automatic). Workflow's **stop tag** = "Consult Booked." Online Scheduling confirmation **removes** the "New Lead" tag and **adds** "Consult Booked" → follow-up workflow auto-pauses; the booking confirmation trigger starts the **Consult workflow** with Base Date = appointment date (reminders before, follow-up after). No lead ever gets a "just checking in!" after they already booked.

### 8.4 Product-purchase fulfillment + pick-your-package invoicing (17hats help 2198457 + University tutorial + blog "Workflows for Products")

(a) Lead Capture Form with a "Choose from a List" question — each package answer mapped to its own one-step workflow that **auto-sends the matching invoice** ("Gold Package" → "Gold Package Invoice" via "Gold Package workflow"); submit → lead+project created → invoice emailed instantly. (b) Attach fulfillment workflows to **products**: when the invoice line-item is paid (configurable: first payment vs. paid-in-full), the product's workflow starts and loads all fulfillment to-dos onto the calendar (e.g., album: order proofs → design → client approval → print order → delivery). Add-on not purchased → no workflow noise.

---

## 9. Inferred data model & engine architecture

Nothing below is published by 17hats; this is a build sketch consistent with all observed behavior.

### 9.1 Schema (relational sketch)

```
workflow_templates
  id, account_id, name, plan_tier_required, created_at
  start_tags  m2m -> tags        -- Start/Stop automation
  stop_tags   m2m -> tags

workflow_template_phases
  id, template_id, name, position

workflow_template_steps
  id, template_id, phase_id?, position
  kind                 ENUM(todo, action, pause)
  action_type          ENUM(send_email, send_quote, send_contract, send_invoice,
                            send_questionnaire, start_workflow, archive_project,
                            change_calendar, modify_tags) NULL unless kind=action
  -- timing
  anchor               ENUM(activation, base_date, previous_step)
  offset_days          INT           -- signed: -7 = before, 0 = on, +3 = after
  -- execution
  mode                 ENUM(automatic, approval)          -- actions
  completion_trigger   ENUM(on_execute, quote_accepted, contract_signed,
                            invoice_first_payment, invoice_paid_full,
                            questionnaire_completed, manual_checkoff)
  -- payload references (LIVE references, not copies)
  email_template_id?, document_template_id?, target_workflow_template_id?,
  target_calendar_id?, add_tag_ids[], remove_tag_ids[]
  assignee_user_id?
  when_done_action     JSONB?        -- to-do "send email when checked off"

workflow_instances
  id, project_id, template_id, name_snapshot
  status               ENUM(active, paused, completed, stopped)
  base_date            DATE          -- editable; re-flows schedule
  activated_at, activated_by, trigger_source ENUM(manual, lead_form, form_answer,
                        scheduling, product_purchase, tag, chained, bulk)
  paused_reason        ENUM(user, stop_tag, project_archived)?

workflow_instance_steps          -- COPIED from template at activation
  id, instance_id, position, phase_name_snapshot
  (all template step fields copied)
  status               ENUM(pending, scheduled, awaiting_approval,
                            executed_awaiting_completion,   -- sent, waiting on client event
                            completed, skipped, overdue)
  scheduled_for        DATE NULL     -- resolved when resolvable
  executed_at, completed_at, completed_by?
  sent_document_id?    -- link to the concrete quote/invoice/contract created

triggers (denormalized attach points)
  lead_form.workflow_template_id
  lead_form_question_option.workflow_template_id
  scheduling_service.{on_confirm_workflow_id, on_approval_workflow_id}
  product.{workflow_template_id, fire_on ENUM(first_payment, paid_full)}
```

Copy-on-activate + live template references is the exact 17hats trade-off: cheap instance isolation, predictable running flows, and content fixes that still propagate. If you build this, consider adding an explicit **"re-sync instance from template"** action — 17hats users complain about manually patching every active project after template edits.

### 9.2 Engine

- **Scheduler**: daily (or hourly) tick per account time zone. At tick: for each active instance, resolve step dates → any `pending` step whose anchor is resolvable gets `scheduled_for`; any `scheduled` step whose date ≤ today and whose **gate is open** (no incomplete Pause/previous-dependency ahead of it, instance not paused) transitions:
  - `mode=automatic` → enqueue execution job; email jobs go to the **10:00 send window with jitter over 2h** (a queue with randomized spacing — copy this, it's a great humanizing touch).
  - `mode=approval` → `awaiting_approval`, surface on dashboard.
- **Event bus**: domain events (`quote.accepted`, `contract.signed`, `invoice.payment_recorded`, `invoice.paid_full`, `questionnaire.submitted`, `booking.confirmed`, `project.tag_added/removed`, `project.archived`) fan out to:
  1. step-completion listeners (`executed_awaiting_completion` steps subscribed to their `completion_trigger` + document id),
  2. workflow start/stop tag listeners (with the "one live instance per start tag" guard),
  3. product-purchase workflow starter,
  4. lifecycle stage advancement.
- **State machine per step** (statuses above) + **per instance** (active/paused/completed/stopped). Completing the last step completes the instance.
- **Re-flow**: on `base_date` change or instance edit, recompute `scheduled_for` for all non-terminal anchored steps. On previous-step completion, resolve `previous_step`-anchored successors (`completed_at + offset_days`).
- **Idempotency**: execution jobs keyed by step id; a step never double-sends (17hats' single-track model makes this easy — keep it).

---

## 10. Strengths / weaknesses

### Strengths (why it's praised)

- **Approachability**: one linear list, three step types, plain-language timing. Non-technical solopreneurs actually finish setup; contrast Dubsado's routinely reported "1–2 weeks before workflows do useful work."
- **Per-step human-in-the-loop** (automatic vs. approval, and the To-Do check-off-to-send pattern) — automation with a personal-touch escape hatch, the most-cited differentiator in reviews.
- **Client-event gating** (Action Completed settings): "don't proceed until quote accepted + contract signed + invoice paid" is first-class, not a hack.
- **Base Date re-flow**: reschedule the wedding, every reminder moves.
- **Tag-based start/stop**: composable, understandable cross-object automation (form/questionnaire/scheduling/workflow all speak "tags"), including auto-stopping follow-up when the client acts.
- **Deep object integration**: workflows natively send the platform's own quotes/contracts/invoices/questionnaires and react to their lifecycle — the whole is the moat.
- Multiple concurrent workflows + chaining + bulk apply + product-triggered fulfillment.

### Weaknesses (documented complaints / gaps)

- **No conditional branching inside a workflow** (no if/else, no multi-path). Branching = separate workflows + tags/list-answers. Dubsado's node-based Flows (conditional triggers on form responses/project value/custom fields, multi-branch, status-dependent paths) is strictly more expressive; HoneyBook's automations have broader trigger menus for some events.
- **One Base Date per workflow** → forced workflow-splitting for multi-date processes (wedding + engagement + album).
- **Template→instance divergence**: structural template edits don't propagate; users must hand-edit every active project.
- **Day-level timing only**; email sends locked to the 10 a.m.–noon window (fine default, but no per-step time control documented).
- Plan-gated: document automation requires the top tier (historically Premier).
- No native SMS steps, no webhooks/API steps, weak reporting/analytics on workflow performance; "rigid customization" and scaling-past-2-people complaints recur in Capterra/G2/third-party reviews; occasional support-speed complaints.
- Discoverability quirks: users ask "where are my missing workflow options" (features differ by tier and by where a workflow is edited — template vs. instance).

---

## 11. Build recommendations

**Copy (table stakes — this is the loved core):**

1. Linear list-of-steps model with exactly the three primitives (task / automated action / hard pause) — resist graph UIs for v1.
2. Anchor+offset timing (`activation | base_date | previous_step` ± N days) with a mutable per-instance Base Date that re-flows the schedule.
3. Per-step **automatic vs. approval** mode + a dashboard "needs your approval" queue + "check off to-do → auto-send email."
4. **Action Completed** gating on document steps (sent / accepted / signed / first-payment / paid-in-full / questionnaire-submitted).
5. Tag-based start/stop automation with the one-live-instance-per-start-tag guard; multiple concurrent workflows per project; workflow chaining step.
6. Trigger set: manual, lead-form (form- and answer-level), scheduling confirmation (base date = appointment), product purchase (first-payment vs. paid-full), bulk apply.
7. 10 a.m. jittered send window as a default (make it configurable per account).

**Improve (clear, cheap wins over 17hats):**

1. **Multiple named anchor dates per project** (booking date, event date, delivery date) selectable per step — kills the #1 workaround (workflow splitting) instantly.
2. **Template versioning + opt-in re-sync to running instances** (show a diff; let users apply structure changes to selected active projects).
3. **Lightweight conditions** without going full node-graph: per-step "only if project has/lacks tag X" covers 80% of Dubsado's branching value at 20% of the UI cost.
4. Per-step send-time control (time-of-day, business-days-only, quiet hours) and hour-level offsets.
5. First-class **skip step** (distinct from complete) with audit trail; instance timeline/history view; workflow analytics (conversion per step, time-in-step, email opens).
6. SMS + webhook + internal-notification action types; assignee-scoped approvals for teams.
7. Recipe library / shareable workflow bundles — 17hats users literally sell workflow template bundles to each other (Becca Jean, Significant Moments Photography) and cite template sharing as a revenue stream; make import/export + a public gallery native.

**Skip (low value / avoid):**

- Separate "Lifecycle" object as a distinct concept — it confuses 17hats users (three help articles disambiguating it). Derive a pipeline/stage view *from* workflow phase progress + tags instead of maintaining a parallel manually-advanced object.
- Basic-vs-Advanced workflow plan gating (users resent it; 17hats' own marketing now leads with "automation included, no tier gating").
- Full node-graph builder in v1 — it's Dubsado's power and its notorious onboarding cliff.

---

## 12. Sources

Help center articles (content obtained via search excerpts; the help site blocked direct crawling from this environment):

- https://help.17hats.com/en/articles/1046329-workflow-overview
- https://help.17hats.com/en/articles/879587-workflows-to-dos-action-items-pauses
- https://help.17hats.com/en/articles/1037910-workflows-action-items
- https://help.17hats.com/en/articles/928580-how-to-use-a-to-do-item-in-my-workflow
- https://help.17hats.com/en/articles/928579-how-to-use-a-pause-item-in-my-workflow
- https://help.17hats.com/en/articles/925561-workflow-base-dates
- https://help.17hats.com/en/articles/1828264-all-about-workflows-triggering-your-workflow
- https://help.17hats.com/en/articles/2165100-workflows-send-quote-completion-triggers
- https://help.17hats.com/en/articles/2165133-workflows-send-invoice-completion-triggers
- https://help.17hats.com/en/articles/879497-updating-workflow-templates
- https://help.17hats.com/en/articles/13753480-how-to-pause-and-resume-a-workflow
- https://help.17hats.com/en/articles/13928403-start-stop-workflow-automation
- https://help.17hats.com/en/articles/5910127-automatically-tag-contacts-and-projects
- https://help.17hats.com/en/articles/897542-what-are-workflow-phases
- https://help.17hats.com/en/articles/923760-what-is-the-difference-between-a-workflow-and-a-lifecycle
- https://help.17hats.com/en/articles/1052884-projects-vs-lifecycle-vs-workflows
- https://help.17hats.com/en/articles/923689-lifecycles
- https://help.17hats.com/en/articles/7432912-workflows-advanced-vs-basic
- https://help.17hats.com/en/articles/3760752-how-to-apply-workflows-to-projects-in-bulk
- https://help.17hats.com/en/articles/2933608-online-scheduling-service-workflows
- https://help.17hats.com/en/articles/840255-automated-lead-workflows
- https://help.17hats.com/en/articles/2198457-send-automated-invoices-using-lead-capture-forms-and-workflows
- https://help.17hats.com/en/articles/2882744-streamline-followup-emails
- https://help.17hats.com/en/articles/897486-what-time-are-automated-emails-sent-from-within-my-workflows
- https://help.17hats.com/en/articles/3113033-recommended-processes-overview
- https://help.17hats.com/en/collections/1841979-workflow-triggers-steps ; https://help.17hats.com/en/collections/550642-workflows

17hats marketing / blog / university:

- https://www.17hats.com/features/workflows ; https://www.17hats.com/features/workflow-trigger ; https://www.17hats.com/features/to-do-workflow
- https://blog.17hats.com/new-feature-start-stop-workflow-automations/
- https://blog.17hats.com/elevate-your-automation-game-workflows-for-products/
- https://blog.17hats.com/automate-tagging-for-optimal-business-organization/
- https://blog.17hats.com/17hats-vs-honeybook-features-automation-client-management-compared/ ; https://blog.17hats.com/17hats-vs-dubsado-full-feature-comparison/
- https://www.17hatsuniversity.com/17hats-quick-tips/17hats-tutorial-starting-a-workflow-after-a-service-has-been-purchased
- https://www.17hatsuniversity.com/17hats-quick-tips/how-to-add-and-remove-tags-from-workflow-to-do-step
- https://17hats.releasenotes.io/release/AJhOp-automate-tagging-with-workflows

Third-party (recipes, reviews, comparisons):

- https://improvephotography.com/49290/step-by-step-designing-a-portrait-session-workflow-with-17hats/
- https://www.idaliaphotography.com/17hats-workflows/
- https://hannahmarie.ca/17hats-workflows/
- http://www.worcus.com/under-the-covers-with-17hats-part-3/
- https://www.letnicolehelp.com/post/control-your-17hats-workflows-with-action-completed-settings
- https://debmitzelcreative.com/2024/10/02/17hats-lead-capture-advanced-tips-to-automate-and-personalize-your-process/
- https://prospeo.io/s/17hats-vs-dubsado ; https://swellsystem.com/dubsado-vs-17hats/ ; https://www.plutio.com/compare/dubsado-vs-17hats ; https://www.honeybook.com/blog/honeybook-vs-17hats
- https://www.capterra.com/p/144328/17hats/reviews/ ; https://www.g2.com/products/17hats/reviews
- https://shop.beccajeanphotography.com/products/17hats-lifestyle-family-photography-workflow-bundle ; https://significantmomentsphotography.com/product/17hats-complete-maternity-workflows-and-templates/

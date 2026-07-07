# 17hats: Quotes, Contracts & Questionnaires (Document System + e-Signature)

> Research agent 4 of 12 — documenting 17hats' document system: Quotes, Contracts, Questionnaires,
> e-signature mechanics, the Quote→Contract→Invoice combined document, templates, merge tokens,
> statuses, expiration, reminders, and PDF output.
>
> **Method / source caveat:** 17hats.com, help.17hats.com, blog.17hats.com, and web.archive.org were
> blocked at the network gateway during this session, so this document is compiled from extensive
> web-search extraction of those help-center articles plus third-party reviews/tutorials. Every claim
> is sourced from search-result content of the cited pages; items I could not verify are explicitly
> flagged as **[unverified]** or **[inferred]**. Do not treat unflagged details as gospel without a
> spot-check against the live help center (URLs in §11).

---

## 1. Summary

- 17hats treats **five things as "Documents"**: Quotes, Contracts, Invoices, Questionnaires (plus
  Emails as a sibling template type). All are created from templates on a single "Documents & Emails"
  template page, all are sent from within a Contact's **Project**, all are trackable
  (created/sent/viewed/completed), all can carry **due dates**, all can be **voided**, and all can be
  automated via Workflows.
- The signature/killer feature is the **3-in-1 combined document**: a Quote with an attached Contract
  and Invoice. The client opens one link, **selects packages/options on the quote → accepts → signs
  the contract → pays the invoice**, in enforced sequence, on one page with tabs. Selections made on
  the quote automatically flow onto the invoice line items.
- **Quotes** support three line-item types — Standard (mandatory), "Choose One" (radio-style package
  pick), "Choose Any" (à-la-carte multi-select, optionally with client-editable quantity) — plus
  tax, discount (fixed or %), a "valid until" expiration date, and payment schedules on the attached
  invoice.
- **Contracts** are rich-text documents with **merge tokens** (`[% contact.first_name %]` style) and
  interactive **Forms** (initials, required/optional checkboxes, short/long text inputs). E-signature
  is built-in, legally binding (ESIGN/UETA), free, supports multiple client signers (primary signs
  first, then related contacts) and owner sign-upon-creation or countersign. 17hats does **not** ship
  lawyer-written contract content; users paste their own or buy from the 17hats Marketplace.
- **Questionnaires** are client-facing forms with ~13 question types, **If/Then branch logic**,
  **answer mapping** into contact/project/custom fields (with pre-population of known answers), and
  "save as draft" for clients.
- **Statuses** are per-type activity events rather than one universal enum: quotes
  (created/sent/viewed/edited/accepted), contracts (created/sent/viewed/edited/signed), invoices
  (created/sent/viewed/paid), questionnaires (created/sent/viewed/answered), plus **draft** (unsent),
  **voided**, and quote **expired** (past valid-until date).
- **Automation hooks**: document completion events (quote accepted, contract signed, invoice paid,
  questionnaire completed) gate workflow progression ("Action Completed" settings), auto-convert a
  Lead into a Client, and can trigger the next email/document in sequence. Automatic
  **upcoming/past-due email reminders** exist per document type.
- **PDF generation is notably weak**: no server-side PDF; users print-to-PDF from the browser.
- Biggest complaints: no built-in legal template library, clunky rich-text editor (paste-from-Word
  problems), rigid layout/branding vs. Dubsado/HoneyBook, weak mobile app, and re-acceptance chains
  when a combined document is edited after partial completion.

---

## 2. Quotes

### 2.1 Where quotes live and how they're built

- Quotes are created either **inside a Project** ("Create New" in the project's Important Documents
  area) or as reusable **Quote Templates** on the **Documents & Emails** template page (Account
  Settings → Documents & Emails → New Template → Quote).
- A quote has a **Quote Options** header section plus a list of **line items**.

**Quote Options** (per help article "Quote Options", 3116500 and "Quote Templates", 1698294):

| Option | Behavior |
|---|---|
| Name (internal) | Document name for the user's own reference/search |
| Display title | Title the client sees |
| **Valid until** date | Quote expiration. On templates the date is **relative** (e.g. "7 days from creation") and re-computes every time the template is used |
| Tax | Apply tax to the quote (line-item taxability configurable via line-item settings) |
| Discount | Fixed dollar amount **or** percentage of the total; applied at top of quote/invoice. Line-level discounts are done by manually lowering price or adding a **negative-value line item** |
| **Contract** | Include a contract that can be signed digitally — choose an existing contract template or write from scratch (this is what creates a combined document) |
| **Invoice** | Include an invoice that is auto-revealed after the quote is accepted (and after the contract is signed, if one is attached) |
| **Payment schedule** | Splits the attached invoice total into installment "mini due dates" — equal or customized installments |

### 2.2 Line-item types (the quote builder's core concept)

Three item types ("Quote Templates" 1698294; "Quote & Invoice Line Item Settings" 3116928):

1. **Standard Quote Item** — a product/service the client **must** purchase (base package, deposit,
   session fee). Always included in the total.
2. **"Choose One" Item** — presents a set of options from which the client picks **exactly one**
   (e.g. Bronze/Silver/Gold package tiers). Radio-button semantics on the client side.
3. **"Choose Any" Item** — an à-la-carte list from which the client may pick **zero or more**
   (prints, framing, insurance, extra hours, upsells). Per option, the seller can set the
   **quantity as locked or client-editable** — client-editable quantity is 17hats' answer to
   variable/tiered pricing (preset price tiers as options; client picks a tier then types quantity —
   help article 935049 "How Do I Manage Variable Pricing on Quotes?").

**Line item fields** (3116928): name, description, price, quantity, category. Typing a name
auto-suggests from **Saved Products & Services** (Account Settings → Products & Services); a
"Save this item for use later" checkbox writes the item (with description, pricing, and settings)
back to that catalog. Categories tie into bookkeeping/P&L reporting.

- **[inferred]** Data model implication: an item-group (Choose One/Choose Any) is a container with
  child options, each option being a full line item (name/description/price/qty/category) plus
  `quantity_editable` flag.

### 2.3 Client acceptance flow

- Client receives a **Quote Email** (an email "type" that auto-appends a button link to the
  document; see §6.3) or accesses the quote via the **Client Portal**; a raw shareable URL also
  exists and can be pasted into any email.
- The client sees a branded web page (logo, brand colors, custom fonts, customizable button color —
  default green, changeable under Account Settings → Brand Preferences; client-facing URLs can be
  customized with the business name).
- Client selects the Choose One option, checks any Choose Any items (adjusting quantity where
  allowed) — the total updates — then clicks **Accept**.
- On acceptance:
  - The **acceptance date is stamped on the quote footer**.
  - Seller is notified by email ("A quote has been accepted").
  - If a contract is attached, a **View Contract** button appears (signing was locked until now).
  - If only an invoice is attached, the invoice is generated/revealed for payment.
  - The client's selections are **copied onto the attached invoice** automatically.
  - If the contact was a **Lead**, they are **automatically converted to a Client** (quote
    acceptance, contract signing, and invoice payment all trigger this conversion).
  - Workflow steps gated on "quote accepted" (or deeper completion criteria) fire.

### 2.4 Quote statuses & lifecycle

Assembled from "Viewing Document Activity" (849328), "How to void a document" (3967282), and quote
feature/help pages:

- **Draft** — created but not sent; not visible in the Client Portal.
- **Sent** — emailed / made available.
- **Viewed** — client opened it (tracked event, shown in the document's activity history).
- **Edited** — seller modified after creation/sending (tracked event).
- **Accepted** — client clicked Accept (date stamped; notification sent).
- **Expired** — past the "valid until" date. **[unverified detail]** Search results confirm quotes
  "can be set to expire" but I could not verify the exact client-side behavior at expiry (hidden vs.
  banner vs. accept disabled). Assume accept is disabled; verify.
- **Voided** — seller voids; a voided quote **may no longer be accepted**. Voiding is allowed on
  uncompleted, partially completed, or completed documents.
- Documents on **archived projects** show the client "The information you are looking for is no
  longer available."

### 2.5 Editing after sending

- Sent quotes are editable; if the client already "finalized" (accepted), they must **re-finalize**
  after the edit. In a combined document, editing the attached contract/invoice after quote
  acceptance forces the client to **re-accept the quote and re-sign the contract** (help 924358).
  This cascade is a notable UX pain point (see §9).

---

## 3. Contracts

### 3.1 Creation & templates

- Created inside a Project ("Create New" → Contract) or as a **Contract Template** (Documents &
  Emails → New Template → Contract). Saved templates are reusable per contact and attachable to
  Workflows and quote templates.
- Template fields: internal **title**, client-facing **display title**, **signature options**, and a
  **due date** picker. On a template the due date is **relative** — e.g. set 7 days and every
  contract created from that template is due 7 days after creation. (Due date drives reminder
  emails and, presumably, "past due" state — see §6.4.)
- Body is a **rich-text editor**. There is **no document import** (no Word/PDF upload into the
  editor): official guidance is to paste contract text through a plain-text editor
  (Notepad/TextEdit) or shift-paste to strip Word's hidden formatting, then re-format inside 17hats
  (help 879490 "Adding Contract Templates to 17hats"). Headers/logo and styling come from global
  brand customization (help 839258 "17hats Customization Options for Emails, Contracts, and Email
  Signatures").
- **No built-in legal library**: 17hats does not ship pre-written, lawyer-drafted contract content
  (comparison articles repeatedly call this out vs. Dubsado/HoneyBook). Users bring their own
  contracts (TheLawTog, The Legal Paige, etc. are the ecosystem sources for photographers) or buy
  **industry-specific templates from the 17hats Marketplace** (see §6.5).

### 3.2 Tokens & Forms inside contracts

- **Tokens** auto-fill contact/project/account data (full list in §6.2). In contracts, tokens are
  filled from stored data **when the contract document is generated from the template**; the help
  center stresses that the data must already exist on the contact/project or the token renders
  blank/unfilled. Contract-specific tokens include `[% contract.name %]`,
  `[% contract.formatted_token_date('due_at') %]`, `[% contract.formatted_token_date('created_at') %]`.
- **Forms** are interactive input elements embedded in the contract body for the client to complete
  at signing time (help 2350413):
  - **Initials (required)** — forces the client to initial a specific section (proof they read it)
  - **Checkbox (required)** — explicit opt-in to a term before signing is possible
  - **Checkbox (optional)** — optional add-on/permission (e.g. model release yes/no)
  - **Short text input (optional/required)** and **long text input (optional/required)** — client
    fills in information inline (e.g. address, allergies)
- Required form fields must be completed before the client can sign.

### 3.3 E-signature mechanics

- **Client side:** the primary contact opens the contract (from email button link or Client Portal),
  completes all required Forms fields, and signs. Only after the primary signs can the **secondary
  signer(s)** complete and sign (enforced order: primary first). **[unverified]** The exact signature
  input style (typed name vs. drawn) is not confirmed in retrieved content; period reviews describe a
  typed-signature box. Verify before copying.
- **Multiple client signers** (help 962028): add each extra signer as a **Related Contact** on the
  project (+ button in Related Contacts), then check their names in the **"Contacts" drop-down next
  to the signature line** in the contract builder. Classic use case: bride + groom.
- **Owner/user side** (help 2868505 "User and Account Owner Contract Signature Options"): there are
  **three signature options** for the business side. Two are confirmed: **sign upon creation**
  (auto-applied when the contract is generated) and **countersign** (owner signs after the client).
  The third is **[unverified]** but is almost certainly "no owner signature required." In both
  confirmed modes the applied signature renders the **"full name" from Account Settings**. By
  default the user who created/last edited the contract is the listed signee — if another user
  edits and re-saves, **their** name replaces the original; multi-user accounts route "a different
  user must sign" via workflow steps set to trigger "upon review."
- **Signature block rendering:** after signing, the contract footer shows the client's signature and
  the date signed (and in a combined doc, the "view invoice" button appears there).
- **Notifications & tracking:** contract activity records created / sent / viewed / **signed** /
  edited events with timestamps, visible above the document and in the project Activity Log.
  **[unverified]** Whether 17hats records signer IP address in a formal audit certificate was not
  confirmable from retrieved content; their legality article leans on ESIGN/UETA generally. Do not
  assume a DocuSign-style completion certificate exists.

### 3.4 Legal validity

- Help article 927258 "Are electronic signatures legally binding?" — yes, per **ESIGN Act (2000)**
  and **UETA (1999)**: electronic records/signatures carry the same legal weight as paper, provided
  intent to sign and consent to do business electronically are demonstrable.
- Marketing: "legally binding e-signatures without extra fees," signed contracts stored securely
  in-app for retrieval. No per-envelope pricing (contrast with DocuSign) — unlimited signing is part
  of the subscription.

### 3.5 Contract lifecycle

- **Draft → Sent → Viewed → (fields completed) → Signed (per signer) → [Countersigned]**.
- **Edited** after send: client must re-sign if they had already signed (re-finalize rule, §2.5).
- **Voided**: a voided contract may no longer be signed.
- **Due date**: drives upcoming/past-due reminder emails; a contract past its due date is treated as
  past due for reminder purposes. **[unverified]** whether signing is blocked after the due date —
  likely not blocked (due date ≠ hard expiry), unlike quote valid-until.

---

## 4. Questionnaires

### 4.1 What they are / when used

- Client-facing forms used to collect information without phone calls: lead qualification right
  after inquiry, onboarding/intake, event-detail gathering (wedding day timeline, shot lists),
  product approvals (via images/links), and post-project **testimonial/feedback** requests.
- 17hats' own guidance: keep each questionnaire to **4–6 questions**; there is **no limit** on the
  number of questionnaire templates; multiple questionnaires can be sent to the same client; each
  can have a **due date**.
- Sent like any document (from a project, via Questionnaire Email type, workflow step, or Client
  Portal). A completed questionnaire appears in the client's portal even if it wasn't formally
  "sent."

### 4.2 Question types

- Officially "**13 different types of questions**" (help 897456 "Questionnaire Templates"). The
  retrieved content never enumerates all 13 in one place. Confirmed types (union of questionnaire
  and lead-capture docs — LCFs share the same engine):
  1. **Text / Statement** (display-only instructions, no answer)
  2. **Short Answer** (one line)
  3. **Long Answer** (paragraph)
  4. **Yes/No**
  5. **Choose from a List** (single select)
  6. **Checkboxes** (multi select)
  7. **Date** (calendar picker)
  8. **File Upload** (≤ 9.4 MB per file)
  9. **Heading/section formatting** element
  10. Image/link-bearing content for product approval (may be a property of Text questions rather
      than a distinct type — **[unverified]**)
  - Lead Capture Forms additionally have a **Lead Source** question type (Standard/Premier plans).
  - Remaining types to reach 13 are **[unverified]** — plausibly Email, Phone, Address, Number,
    Time; verify against the live builder.

### 4.3 If/Then (branch) logic

Help 4755373 + feature page "questionnaire-if-then-logic":

- **Base Questions** = questions with enumerable answers: **Yes/No, Choose from a List,
  Checkboxes**. Only these can carry branches.
- **Branch Questions** are attached to a specific answer choice of a Base Question and render only
  when that answer is selected. A branch may itself be another Base Question → **nested branching**
  is supported.
- Builder interaction: "Add Branch Question" on the base question, pick the answer that triggers it,
  pick the branch question's type.

### 4.4 Answer Mapping

Help 2545940 (applies to Questionnaires + Lead Capture Forms):

- Each question has a **"Maps to"** dropdown targeting a **Contact field**, **Project field**, or a
  **Custom Field** (custom fields are user-defined under Account Settings → Custom Fields).
- Type compatibility is enforced: question type must match field type (a Date question cannot map to
  a Short Answer field). 17hats' custom-field mapping is richer than Dubsado's (supports multi-line,
  yes/no, checkboxes, list-choice — Dubsado smart fields only did short answer + date).
- **Pre-population:** if the mapped field already holds data (e.g., email address), the question is
  **pre-filled** for the client.
- **Project Notes** can be a mapping target **from Lead Capture Forms only**; multiple answers can
  map to Project Notes, each becoming its own note in question order.
- LCFs always include Name + Email questions mapped to the Contact name/email (minimum to create a
  contact).
- Mapped answers write back into the CRM on submission → tokens, workflows, and future documents can
  use the data.

### 4.5 Client experience & lifecycle

- Client opens via email button link or portal; can **"Save as Draft"** mid-way and return later
  (help 853136).
- Statuses/events: created / sent / **viewed** / **answered** (+ draft, voided — a voided
  questionnaire can no longer be submitted). Due dates enable upcoming/past-due reminders.
- Completion notifies the account owner in-app (single-recipient notification; users complain you
  can't notify multiple emails).
- Questionnaire answers can drive automation: e.g., a Choose One question whose answers apply
  **Project Tags**, and tags trigger designated **Workflows** (documented pattern).

---

## 5. The Quote → Contract → Invoice bundle (3-in-1 combined document)

**The** marquee feature (feature page `/features/quote-contract-invoice`; help 924358 "Combined
Documents"). "Quote, Contract, and Invoice wrapped up in one professional-looking package. Now leads
can select, sign, and pay with just one document."

### 5.1 How the seller creates it

1. Create a **Quote** (from scratch or template).
2. In Quote Options, tick the **Contract** box → pick a contract template or write one inline.
3. Tick the **Invoice** box → configure invoice settings (due date, payment schedule, online-payment
   on/off, etc.).
4. Send once (one email, one link). Partial combos are supported: **quote+contract**,
   **quote+invoice**, or quote alone. Note the anchor is always the quote — **[inferred]** there is
   no contract+invoice combo without a quote in this mechanism (contract and invoice are attachments
   *of* the quote).
5. Quote **templates** can have contract + invoice templates saved to them, so a workflow "Send
   Quote" step sends the whole bundle automatically.

### 5.2 Client-side sequence (enforced state machine)

One page with **tabs** (Quote | Contract | Invoice):

1. **Quote first.** Client can *peek* at the Contract tab but **cannot sign until the quote is
   accepted**. The Invoice is not available yet (in fact it's generated from quote selections).
2. Client makes selections (Choose One / Choose Any / quantities) → total updates → **Accept**.
   Footer now shows acceptance date + **"View Contract"** button.
3. **Contract second.** Client completes required Forms fields (initials/checkboxes/text), signs;
   secondary signers sign after the primary. Footer now shows signature, date signed, + **"View
   Invoice"** button.
4. **Invoice last.** Generated **from the accepted quote's selections** ("choices the client makes
   are automatically updated on the corresponding Invoice"), shown with payment schedule if set;
   client pays online (Stripe/Square/PayPal depending on account-level processor config).
5. If no contract was attached, the invoice reveals immediately upon quote acceptance.

### 5.3 Consequences & bookkeeping of the flow

- Lead auto-converts to Client at quote acceptance / contract signature / first payment.
- Workflow **"Send Quote" completion triggers** (help 2165100): the step's "completed" definition
  can be any related action of the bundle — e.g., only proceed when *quote accepted AND contract
  signed AND invoice paid*. This is how users build "booking" automations that wait for full
  booking before sending welcome email → planning questionnaire → prep guide.
- **Edit cascade:** editing the contract or invoice after the quote was accepted requires the client
  to re-accept the quote and re-sign the contract (§2.5).
- Voiding rules apply per part (§2.4/§3.5); payments already made can't be removed by voiding.

### 5.4 Why it's the killer feature

- Single link/email = one decision session: select → sign → pay in ~minutes; removes the multi-day
  email ping-pong of separate quote, then contract, then invoice (faster booking, less drop-off).
- Selection→invoice sync eliminates manual re-keying and errors between quote choices and billed
  amounts, and makes upsells (Choose Any add-ons) frictionless at the exact moment of highest
  intent.
- Sequencing enforces business hygiene automatically: no signature before agreement on scope/price;
  no payment before signature.
- Competitors at the time required separate documents or "proposals" (HoneyBook's proposal =
  invoice+contract; Dubsado has proposal→contract→invoice too — 17hats' differentiators are the
  three-item quote engine with locked/editable quantities and the workflow completion triggers over
  the bundle).

---

## 6. Templates & merge tokens

### 6.1 Template system

- Central hub: **Documents & Emails** template page (also reachable via the document icon top-right).
  Template types: **Email, Quote, Contract, Invoice, Questionnaire** (+ Lead Capture Forms and
  Online Scheduling services elsewhere). Filterable by category. No limits on template counts.
- Templates can also be created "in place" from a live document inside a project and saved back as a
  template.
- Templates are the currency of **Workflows**: a workflow action item can "send any Email, Quote,
  Contract, Invoice or Questionnaire" template, either automatically or "upon review" (human
  approves/edits first). Duplicating a workflow can duplicate all associated templates.
- Relative dates on templates: quote **valid-until** and contract/invoice **due dates** are stored
  as offsets ("7 days after creation") and materialize on document creation.
- **Template Sharing** (help 2551565): share single templates or **bundles** account→account via a
  generated **access code**; unlimited redemptions; imported items may carry the sharer's personal
  settings (calendar defaults etc.) that must be adjusted. Used heavily by multi-brand owners and by
  educators distributing setups.

### 6.2 Merge tokens

- Syntax: `[% ... %]` — placeholders replaced with Contact/Project/Account data. In emails they're
  substituted at **send time**; in contracts they fill on **document generation from template**. If
  the underlying field is empty, the token doesn't fill (data must exist on the profile/project
  first). **[unverified]** Whether 17hats warns about unfilled tokens before sending.
- Usable in email templates, contracts, and other document text areas; custom **date** custom-fields
  are explicitly usable as tokens in emails and contracts.
- Categories & confirmed examples (help 1235598 "Complete List of Tokens"):

| Category | Token | Meaning |
|---|---|---|
| Contact | `[% contact.first_name %]` | First name |
| Contact | `[% contact.last_name %]` | Last name |
| Contact | `[% contact.name %]` | Full name |
| Contact | `[% contact.company_name %]` | Company |
| Contact | `[% contact.address.as_string %]` | Address |
| Contact | `[% contact.primary_email_address %]` | Email |
| Contact | `[% contact.primary_phone_number %]` | Phone |
| Project | `[% project.name %]` | Project name |
| Project | `[% project.main_event.location_string %]` | Project location |
| Project | `[% project.main_event.formatted_token_date('start') %]` | Project date |
| Project | `[% project.main_event.formatted_time('start') %]` | Start time |
| Project | `[% project.main_event.formatted_time('end') %]` | End time |
| Project | ShootProof gallery link tokens | Integration-specific |
| Account | account first/last/full name, company name | From Account Settings |
| Contract | `[% contract.name %]` | Contract name |
| Contract | `[% contract.formatted_token_date('due_at') %]` | Due date |
| Contract | `[% contract.formatted_token_date('created_at') %]` | Created date |
| Invoice | `[% invoice.invoice_number %]` | Invoice number |
| Invoice | `[% invoice.formatted_token_currency('total_amount') %]` | Total |
| Invoice | `[% invoice.formatted_token_currency('amount_due') %]` | Outstanding |
| Invoice | `[% invoice.formatted_token_date('due_date') %]` | Due date |
| Invoice | `[% invoice.link %]` | Public link to invoice |
| Invoice | next payment amount / next payment date tokens | For autopay/recurring |
| Service (scheduling) | `[% booking.scheduled_service.name %]` | Service name |
| Service | `[% booking.scheduled_service.location.name %]` / `...location.location %]` | Location name/address |
| Service | `[% booking.calendar_event.formatted_token_date('start') %]` | Booking date |
| Service | `[% booking.calendar_event.formatted_time('start') %]` / `('end')` | Times |
| Service | `[% booking.scheduled_service.duration %]` | Duration |
| Custom fields | token per custom field (incl. date type) | User-defined |

- Design notes worth stealing: tokens are **object.path expressions with formatter methods**
  (`formatted_token_date(...)`, `formatted_token_currency(...)`) — i.e., a real template language
  (looks like Perl Template Toolkit / similar), not flat placeholders. Document-scoped tokens
  (invoice/contract) are only valid in that document type's email context (e.g., invoice tokens in
  Invoice Emails).

### 6.3 Document email types

Help 2950670: every email template has a **Type** that binds it to a document and auto-appends the
access **button link**: Regular, **Quote Email**, **Contract Email**, **Invoice Email**, Client
Portal Email, **Questionnaire Email**, Lead Auto Responder, Scheduling. Each document type also has
a default pre-created email used when sending manually.

### 6.4 Expiration, due dates & reminders

- **Quotes:** "valid until" expiration date (relative on templates).
- **Contracts / Invoices / Questionnaires:** due dates (relative on templates).
- **Document Email Reminders** (help 2280471; feature page /features/document-reminders; release
  note): per-document-type automated reminders configured at Account Settings → Email Settings →
  Email Reminders:
  - **Upcoming reminder:** customize *when* (N days before due date; default 1), subject, body.
  - **Past-due reminder:** customize *when* (N days after due), **recurrence**, subject, body.
  - Constraints: only for documents on **Active projects**, and the document must have a due date.
  - Applies to all four: quote, contract, invoice, questionnaire.

### 6.5 Marketplace (template commerce)

- **marketplace.17hats.com** — public storefront of member-built items: Email/Quote/Contract/
  Invoice/Questionnaire templates, Lead Capture Forms, Online Scheduling services, and Workflows.
  Sellers are approved "Ambassadors"; **revenue split 50/50** with 17hats; purchase = license for one
  brand/account. Purchases **auto-install** into Documents & Emails (scheduling items into Bookings),
  with seller-provided post-purchase customization instructions. This is how 17hats outsources the
  "legal template library" gap — industry contract packs are sold by third parties (also on Etsy).

---

## 7. UX flows

### 7.1 Sender-side flow (typical booking)

1. Lead arrives (Lead Capture Form → contact+project auto-created, answers mapped) or manual entry.
2. Open the contact's **Project** → Important Documents → **Create New** → Quote (or run a Workflow
   whose action item is "Send Quote," optionally "upon review" so the user can tweak first).
3. Pick quote template → items/prices/valid-until materialize; attach contract template + invoice
   settings (payment schedule, online payments) via checkboxes.
4. Save → prompted to **send by email**: pick/customize the Quote-type email template (tokens fill at
   send) → Send. Alternatively copy the document link or rely on the Client Portal.
5. Track: document header shows the activity trail (created/sent/viewed/…); project **Activity Log**
   aggregates all document events; dashboard/email notifications on accept/sign/pay/answer.
6. Automated reminders nudge before/after due dates. Manual re-send and edit possible anytime
   (with re-finalize consequences).
7. On full completion, workflow "Action Completed" gates release the next steps (welcome email,
   questionnaire, etc.). Countersign if configured. Void if the deal changes; print-to-PDF for
   records.

### 7.2 Client-side flow

1. Email with button link (or portal URL + optional password). No client account/login required for
   a plain document link **[inferred from doc-link mechanics; portal can be password-protected]**.
2. Branded document page; combined docs show Quote/Contract/Invoice tabs with forward-locking
   (§5.2).
3. Quote: pick options → Accept. Contract: fill required fields → sign (primary then secondary).
   Invoice: pay online (full, or per payment-schedule installment; save-card + autopay possible when
   the seller enabled recurring/automatic payments).
4. Questionnaires: answer (branch questions appear dynamically), Save as Draft or Submit.
5. **Client Portal** (per-contact, optionally password-protected, per-contact cover image,
   project-filtered): lists sent documents for active projects — the ~**100 most recent sent
   documents** show by default **[source: portal overview snippet; verify exact number]** — client
   can re-open anything: accept quotes, sign contracts, complete questionnaires, pay invoices, see
   event details. Drafts never appear; archived-project docs show an "information no longer
   available" message.

---

## 8. Inferred data model (schema sketch)

Not from 17hats internals — reverse-engineered from observed behavior. `⚠` = speculative.

```
Account
  users[]                    # multi-user accts; user.full_name renders as signature
  brand_preferences          # logo, colors, fonts, button color, custom URL slug
  email_reminder_settings[]  # per doc type: {upcoming_days_before, pastdue_days_after,
                             #   recurrence, subject, body, enabled}
  custom_field_defs[]        # {entity: contact|project, name, type}
  products_services[]        # saved line items {name, desc, price, category, taxable⚠}

Contact --< Project >--< RelatedContact(contact_id, role)
  contact: {first,last,company,address,emails[],phones[], type: lead|client, custom_values{}}
  project: {name, main_event{start,end,location}, stage/tags[], notes[], activity_log[]}

Template (polymorphic: email|quote|contract|invoice|questionnaire)
  {internal_name, display_title, body/config, relative_due_days | relative_valid_days,
   attached_contract_template_id?, attached_invoice_template_id?}   # quote templates only

Document (STI/polymorphic base)                       ⚠ single table w/ type
  {id, project_id, template_id?, type, internal_name, display_title,
   status_derived, due_at | valid_until, public_token/url, voided_at?,
   created_by_user_id}
  DocumentActivity[] {document_id, event: created|sent|viewed|edited|accepted|signed|
                      paid|answered|deleted, actor: user|client, occurred_at}

Quote < Document
  {tax_rate?, discount {kind: fixed|percent, value}, accepted_at, accepted_by_contact_id⚠,
   contract_id?, invoice_id?}          # combined-doc links; contract/invoice belong to quote
  QuoteItemGroup[] {kind: standard|choose_one|choose_any, position}
    QuoteItem[] {name, description, unit_price, quantity, quantity_editable(bool),
                 category, position, selected(bool), selected_quantity}

Contract < Document
  {body_html_with_tokens_resolved, owner_signature_mode: on_creation|countersign|none⚠,
   owner_signed_at, owner_signer_user_id}
  ContractField[] {kind: initials_req|checkbox_req|checkbox_opt|text_short|text_long,
                   required, value, completed_at}
  ContractSigner[] {contact_id, role: primary|secondary, order, signed_at,
                    signature_text⚠, ip_address⚠}

Invoice < Document
  {invoice_number, line_items[] (copied from accepted quote selections),
   tax, discount, total, amount_due, online_payments_enabled,
   payment_schedule[] {due_at, amount}, recurring_config?, payments[]}

Questionnaire < Document
  {questions[] {type(13), text, options[], maps_to{entity,field}, required⚠, position,
                branches[] {trigger_option, child_question}},
   answers{} per question, draft_saved_at, submitted_at}

WorkflowStep(action: send_document, template_id, trigger: auto|upon_review,
             completed_when: sent|quote_accepted|contract_signed|invoice_paid|
                             questionnaire_answered|combo…)
```

Key modeling takeaways:

- **One unified Document abstraction** (shared: template origin, send/view tracking, due dates,
  voiding, portal visibility, reminders) with per-type payloads — this is what makes 17hats'
  reminders/portal/activity uniform.
- The **combined document is quote-rooted composition**, not a generic "smart file" — contract and
  invoice are children of the quote with a gate sequence; the invoice's line items are a projection
  of the quote's selected items.
- **Events, not a single status column**: statuses are derived from the activity stream
  (draft = never sent; viewed = has viewed event; etc.) plus explicit flags (accepted_at, voided_at).
- **Templates store relative dates**; documents store absolute ones.

---

## 9. Strengths / weaknesses

### Strengths (copy these)

1. **3-in-1 bundle with enforced sequencing and quote→invoice line-item sync** — the single most
   praised capability; "book clients faster" is the pitch and users echo it.
2. **Three-mode quote items** (standard / choose-one / choose-any + lockable quantities) — simple
   mental model covering packages, tiers, à-la-carte upsells, and quantity-priced goods.
3. **Free unlimited legally-binding e-sign** with multi-signer + countersign + in-contract required
   fields (initials/checkboxes) — no per-document fees.
4. **Tokens as a real expression language** with formatters, spanning contact/project/account/
   document/custom fields; answer mapping closes the loop (questionnaire → CRM → tokens).
5. **Uniform document plumbing**: activity trails, per-type reminders (before + after due, with
   recurrence), voiding semantics, client portal, workflow completion triggers over document events.
6. **If/Then questionnaire branching** with nesting; client "save as draft."
7. **Template ecosystem**: relative dates, sharing via access codes, and a revenue-sharing
   marketplace that outsources vertical content.
8. Automatic **lead→client conversion** on accept/sign/pay — CRM state maintained by document
   events, zero user effort.

### Weaknesses / user complaints (fix these)

1. **No native PDF generation** — "print via browser dialog" is the official answer; no auto-attached
   signed-contract PDF, no archival artifact. (Big trust/legal gap vs. DocuSign-style completion
   PDFs + audit certificates.)
2. **No built-in lawyer-drafted contract library** — repeatedly dinged in comparisons (Dubsado/
   HoneyBook ship starter legal templates); everything must be pasted in or purchased.
3. **Rich-text editor friction** — no Word/PDF import; official workaround is paste-through-Notepad;
   formatting from Word breaks layouts.
4. **Layout/branding rigidity** — limited visual customization of documents (Dubsado allows images,
   file uploads, custom CSS in forms; HoneyBook has hundreds of community file templates). 17hats
   docs are clean but samey; reviewers call the UI dated/clunky and "understanding where and what
   your clients are doing within each tab can get really clunky."
5. **Edit-cascade pain**: editing any part of a partially completed combined doc invalidates prior
   client actions (re-accept + re-sign), with no amendment/addendum concept.
6. **Signature attribution quirk**: last user to edit a contract becomes the signee — surprising in
   multi-user accounts.
7. **Questionnaire notifications** limited (single recipient); question types capped (~13; no
   payment-collecting or scheduling questions inside questionnaires).
8. **Scalability ceiling**: reviewers "outgrew" contracts/bookkeeping once businesses got complex
   (multi-employee, product + service mixes).
9. **Mobile app** barely handles documents (view-only, glitchy) — sellers can't build/send quotes
   well on mobile.
10. **Uncertainty flags** (17hats may or may not have these — verify): unfilled-token warnings,
    signer IP capture/audit certificate, drawn signatures, quote expiry client messaging.

---

## 10. Build recommendations

**Copy (table stakes for this market):**

- The quote-rooted **3-in-1 flow** with tabbed client page, forward-locking (accept → sign → pay),
  and automatic selection→invoice sync. This is the conversion engine; replicate the exact gate
  sequence and footer affordances (acceptance date, signature + date, "view next" buttons).
- **Three line-item modes** + saved products/services autocomplete + client-editable quantities +
  fixed/percent discount + relative valid-until on templates.
- **Contract Forms** (required initials/checkboxes, inline text inputs) + multi-signer ordering +
  countersign + sign-on-creation; free unlimited e-sign as pricing posture.
- **Token language** with object paths and formatters; custom-field tokens; document-type-bound
  email templates that auto-inject the document button.
- **Per-type due dates + configurable upcoming/past-due reminder emails with recurrence**; document
  activity trail (created/sent/viewed/edited/accepted/signed/paid/answered) surfaced on the doc and
  in a project log; document events as workflow triggers and lead→client conversion triggers.
- Questionnaire **answer mapping with pre-population** and **If/Then branching** (nested).
- **Void semantics** per document type; archived-project tombstone page.

**Improve (differentiators over 17hats):**

- **Real PDF generation**: server-rendered PDF of every signed/accepted/paid document, auto-emailed
  to both parties, plus a **signature certificate** (signer identity, email, IP, user agent,
  timestamps, document hash). This single feature answers 17hats' loudest structural gap and the
  e-sign trust question at once.
- **Amendment flow** instead of the re-accept cascade: version the document, show a diff, let the
  client approve the delta; keep prior signatures on the prior version.
- **Document editor**: modern block editor with Word/PDF/Google Docs import and clean-paste by
  default; image/video blocks in quotes and questionnaires; per-template theming (Dubsado-level
  customization with HoneyBook-level ease).
- **Starter legal template pack** (attorney-reviewed, per vertical) in-product — even a small set
  removes the #2 complaint — plus a marketplace later.
- Quote extras 17hats lacks: per-option images, min/max selections on choose-any groups,
  quote-level expiry behavior configuration (hide vs. allow-late-accept), and an explicit
  "deposit due on acceptance" shortcut.
- **Expiration UX**: countdown on the client page, auto-status flip to Expired, one-click "revive &
  extend."
- Multi-recipient + webhook notifications on every document event; unfilled-token linting before
  send.
- Signature capture: typed **and** drawn, stored as vector + rendered into the PDF.

**Skip / deprioritize:**

- A full template *marketplace* with revenue share (heavy ops; do template sharing via link/code
  first — cheap and viral).
- 17hats' separate Lead Capture Form vs Questionnaire duality — build **one form engine** with
  contexts (public lead form vs. sent-to-contact questionnaire) instead of two near-duplicate
  builders.
- The "last editor becomes signee" behavior — model owner signer explicitly.
- Browser print-to-PDF as the only export (see Improve).
- ShootProof-style niche integration tokens until the verticals demand them.

---

## 11. Sources

Primary (help.17hats.com — retrieved via search extraction; gateway-blocked for direct fetch):

- Documents collection: https://help.17hats.com/en/collections/550651-documents
- Combined Documents: https://help.17hats.com/en/articles/924358-combined-documents
- Quote Templates: https://help.17hats.com/en/articles/1698294-quote-templates
- Quote Options: https://help.17hats.com/en/articles/3116500-quote-options
- Quote & Invoice Line Item Settings: https://help.17hats.com/en/articles/3116928-quote-invoice-line-item-settings
- Variable Pricing on Quotes: https://help.17hats.com/en/articles/935049-how-do-i-manage-variable-pricing-on-quotes
- Contract Templates: https://help.17hats.com/en/articles/2350413-contract-templates
- Adding Contract Templates: https://help.17hats.com/en/articles/879490-adding-contract-templates-to-17hats
- Signature Options (owner/user): https://help.17hats.com/en/articles/2868505-user-and-account-owner-contract-signature-options
- More signatures: https://help.17hats.com/en/articles/962028-can-i-add-more-signatures-to-my-contracts
- E-signature legality: https://help.17hats.com/en/articles/927258-are-electronic-signatures-legally-binding
- Contracts collection: https://help.17hats.com/en/collections/550682-contracts
- Questionnaire Templates: https://help.17hats.com/en/articles/897456-questionnaire-templates
- If/Then Questions: https://help.17hats.com/en/articles/4755373-if-then-questions-in-questionnaires
- Answer Mapping: https://help.17hats.com/en/articles/2545940-answer-mapping-in-questionnaires-lead-capture-forms
- Questionnaire save-as-draft: https://help.17hats.com/en/articles/853136-can-my-clients-save-their-questionnaire-and-come-back-later
- Lead Capture Form Question Types: https://help.17hats.com/en/articles/10167140-lead-capture-form-question-types
- Complete List of Tokens: https://help.17hats.com/en/articles/1235598-complete-list-of-tokens
- Custom Fields: https://help.17hats.com/en/articles/2545832-custom-fields
- Email Types: https://help.17hats.com/en/articles/2950670-what-are-the-different-email-types-in-17hats
- How to Send a Document: https://help.17hats.com/en/articles/3250522-how-to-send-a-document
- Viewing Document Activity: https://help.17hats.com/en/articles/849328-viewing-document-activity
- How to Void a Document: https://help.17hats.com/en/articles/3967282-how-to-void-a-document
- Save/Print to PDF: https://help.17hats.com/en/articles/924369-how-to-save-print-to-pdf
- Document Email Reminders: https://help.17hats.com/en/articles/2280471-email-settings-document-email-reminders
- Invoice reminders: https://help.17hats.com/en/articles/879792-how-do-i-set-automatic-invoice-reminders
- Discounts: https://help.17hats.com/en/articles/1052603-discounts-how-to-customize-discounts-and-view-on-your-profit-loss-report
- Scheduled Payments: https://help.17hats.com/en/articles/2548662-scheduled-payments
- Recurring Billing/Auto Payments: https://help.17hats.com/en/articles/4260937-invoice-options-recurring-billing-automatic-payments
- Client Portal Overview: https://help.17hats.com/en/articles/1131267-client-portal-overview
- Client Portal per-contact: https://help.17hats.com/en/articles/3160024-client-portal-customizing-per-contact
- Workflows – Send Quote Completion Triggers: https://help.17hats.com/en/articles/2165100-workflows-send-quote-completion-triggers
- Workflows – Action Items: https://help.17hats.com/en/articles/1037910-workflows-action-items
- Lead→Client conversion: https://help.17hats.com/en/articles/879529-changing-a-lead-to-a-client
- Template mgmt: https://help.17hats.com/en/articles/879803-how-to-create-manage-document-email-templates
- Template Sharing: https://help.17hats.com/en/articles/2551565-template-sharing
- Marketplace: https://help.17hats.com/en/articles/840250-17hats-marketplace
- Related-contact docs: https://help.17hats.com/en/articles/934969-what-is-the-best-way-to-send-contracts-and-invoices-to-related-contacts

Marketing / feature pages:

- 3-in-1: https://www.17hats.com/features/quote-contract-invoice
- Quotes: https://www.17hats.com/features/quotes • Contracts: https://www.17hats.com/features/contract
- Questionnaires: https://www.17hats.com/features/questionnaires • If/Then: https://www.17hats.com/features/questionnaire-if-then-logic
- Document Reminders: https://www.17hats.com/features/document-reminders • Templates: https://www.17hats.com/features/document-templates
- Marketplace: https://marketplace.17hats.com/ • Sellers: https://www.17hats.com/marketplace-sellers

Blog / release notes / education:

- Release notes: https://17hats.releasenotes.io/ (tags: questionnaires, contracts, templates, document activity; Answer Mapping release; Document Email Reminders release; Archived Projects – Incomplete Documents; Client Portal releases)
- Blog: If/Then (blog.17hats.com/dig-deep-with-if-then-questions-in-questionnaires), token spotlight, answer-mapping guide, marketplace install guides, portal filtering release, invoice email reminders
- 17hats University: "Book Clients Faster: Quote, Contract & Invoice" (17hatsuniversity.com), "How To Use Tokens in 17hats", "Creating a Contract Template"

Third-party reviews / comparisons (complaints & context):

- Capterra reviews: https://www.capterra.com/p/144328/17hats/reviews/
- Spruce Rd. review: https://sprucerd.com/blog/17hats/
- Hannah Marie 17hats contracts/invoices/quotes tutorial: https://hannahmarie.ca/17hats-contracts-invoices-quotes/
- Byte Bodega 17hats vs HoneyBook vs Dubsado: https://www.bytebodega.com/17hats-vs-honeybook-vs-dubsado/
- HoneyBook comparison: https://www.honeybook.com/blog/17hats-vs-honeybook-vs-dubsado
- Improve Photography in-depth review; ShootProof blog review; Beth Rowles setup guide (bethrowles.com); letnicolehelp.com Action Completed settings; Jaimie Dee review (jaimiedee.com)

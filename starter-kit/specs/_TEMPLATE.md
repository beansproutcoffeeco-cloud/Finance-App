# Spec: <feature name>

<!--
HOW TO USE THIS TEMPLATE
1. Copy to specs/features/<phase>-<feature-name>.md
2. In Claude Code, say: "Interview me with questions, one round at a time, until this
   spec is complete enough to build from. Then fill in every section."
3. Read the finished spec YOURSELF. Fix anything that isn't what you meant.
4. Start a FRESH Claude Code session: "Implement specs/features/<file>.md. Explore the
   relevant code first, present a plan, then build it."
Status: draft → agreed → building → shipped
-->

**Status:** draft
**Phase:** <from ROADMAP.md>
**Depends on:** <specs/features that must be shipped first>

## 1. What & why (2–4 sentences)

What the user can do after this ships, and why it matters. Written in plain language —
if you can't explain it simply here, the spec isn't ready.

## 2. User stories

- As a business owner, I can … so that …
- As a client (public-facing), I can … so that …

## 3. Requirements (testable statements)

Number them. Each must be checkable — someone can answer yes/no "does the app do this?"

- R1: …
- R2: …
- R3 (edge case): what happens when …
- R4 (permissions): who can/can't do this; what does a logged-out visitor see

## 4. Out of scope

Explicitly list nearby things this feature will NOT do (they go to a later spec).

## 5. Data model changes

New/changed tables and columns. Every tenant-owned table: `tenant_id uuid not null`
+ RLS policy. Note any new indexes, enums, or relations to existing tables.

## 6. Screens & flows

For each screen: route, what's on it, what actions exist, empty state, error state.
A rough text sketch is fine:

```
/invoices            — list: status filter tabs, table (number, client, total, status, due)
/invoices/new        — form: client picker, line items, due date → Save draft / Send
/pay/[token]         — PUBLIC: invoice summary + Pay button → Stripe Checkout
```

## 7. External services touched

Stripe / Resend / e-sign / etc. — which API calls, which webhooks, what happens if the
service errors or the webhook arrives twice.

## 8. Verification plan (write BEFORE building)

How we'll know it works. Must produce a pass/fail:

- Unit/integration tests to write: …
- Manual test script: step-by-step clicks + expected results
- The tenant-isolation check: user B cannot see/modify user A's <records>

## 9. Tasks

Filled in during planning; each small enough for one session. Check off as completed.

- [ ] …

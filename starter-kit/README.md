# Business Manager — Project Starter Kit

Copy-ready templates for organizing a large, multi-module web app (a 17hats-style
all-in-one business manager: CRM, quotes, contracts + e-sign, invoicing/payments,
scheduling, automated workflows, bookkeeping) built solo with Claude Code.

This kit pairs with the research report ("Organizing a Big Coding Project — The
Overnight Playbook"). The report explains *why*; these files are the *what to copy*.

## What's in the kit

| File | What it is | When you use it |
|---|---|---|
| `CLAUDE.md` | Lean root context file for Claude Code | Copy to new repo root on day one, fill in the blanks |
| `TASKS.md` | Task board template with Phase 0 pre-filled | Copy to repo root; update it every session |
| `ROADMAP.md` | The full phased build plan (Phases 0–6) | Copy to repo root; this is your milestone map |
| `specs/_TEMPLATE.md` | Feature spec template (Requirements → Design → Tasks) | Duplicate it for every feature before building it |
| `specs/product.md` | Steering doc: what the product is, module map | Copy as-is, adjust to your vision |
| `specs/tech.md` | Steering doc: stack decisions + services | Copy as-is, check off services as you set them up |
| `specs/structure.md` | Steering doc: folder layout + conventions | Copy as-is; Claude reads this to know where code goes |
| `DATA-MODEL.md` | Starter database schema for all modules | Reference when building each module's tables |
| `SETUP-CHECKLIST.md` | Every account/service to create, in order | Work through it before writing any code |

## How to bootstrap the new project (day one)

1. **Create a new empty GitHub repo** (e.g. `business-manager`). Do NOT build this
   inside the Finance-App repo — it's a separate product.
2. **Start from the starter template.** In Claude Code, ask it to scaffold from
   [`KolbySisk/next-supabase-stripe-starter`](https://github.com/KolbySisk/next-supabase-stripe-starter)
   (Next.js + Supabase + Stripe + Resend + Tailwind + shadcn/ui) — or use
   `npx create-next-app` and add Supabase/Stripe per `specs/tech.md`.
3. **Copy this kit in:** `CLAUDE.md`, `TASKS.md`, `ROADMAP.md` to the repo root;
   the `specs/` folder as-is; `DATA-MODEL.md` and `SETUP-CHECKLIST.md` into a `docs/` folder.
4. **Work through `SETUP-CHECKLIST.md`** (Supabase project, Stripe test account, etc.).
5. **Then follow `ROADMAP.md` Phase 0.** One feature at a time: write the spec from
   `_TEMPLATE.md` first, review it, then have Claude Code implement it in a fresh session.

## The golden rules (from the research)

- **Spec first, code second.** Have Claude interview you until the spec is complete,
  write it to `specs/`, then implement from a fresh session.
- **One phase at a time, one feature at a time.** Never "build the whole module."
- **Every table gets `tenant_id` + a Row Level Security policy.** No exceptions, from day one.
- **If you can't verify it, don't ship it.** Every feature needs a test or a checkable
  pass/fail signal before you move on.
- **Keep `CLAUDE.md` short.** Bloated context files get ignored. Details live in `specs/`.

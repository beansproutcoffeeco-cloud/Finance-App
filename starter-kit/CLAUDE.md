# Business Manager

All-in-one small-business management app (like 17hats): CRM, quotes, contracts,
invoicing, scheduling, workflows, bookkeeping. Solo project, built with Claude Code.

## Read these before non-trivial work

- `specs/product.md` — what we're building and why
- `specs/tech.md` — stack + service decisions (don't introduce new services without asking)
- `specs/structure.md` — where code goes, naming conventions
- `ROADMAP.md` — current phase; don't build ahead of it
- `TASKS.md` — live task board; update it when you finish anything

## Workflow (non-negotiable)

- New feature → write/refine a spec in `specs/features/` FIRST (interview me with
  questions until it's complete), then implement in a fresh session from that spec.
- Explore → Plan → Implement → Commit. Use plan mode for anything non-trivial.
- Never mark a task done without a passing verification (test, build, or manual check script).

## Critical gotchas

- EVERY tenant-owned table has `tenant_id uuid not null` + an RLS policy. A new table
  without RLS is a data leak across customers. See `docs/DATA-MODEL.md`.
- Never trust client-supplied `tenant_id` — derive tenant from the authenticated user's
  membership, server-side.
- Stripe webhooks: verify the signature, handle retries idempotently (dedup on `event.id`),
  and return 2xx fast. Money state changes ONLY via verified webhook events, never from
  client-side success redirects.
- Secrets live in `.env.local` (gitignored) and Vercel/Supabase env settings — never in code.

## Commands

<!-- Fill in once the repo is scaffolded -->
- `npm run dev` — start dev server
- `npm run test` — run tests
- `npm run lint && npm run typecheck` — must pass before any commit

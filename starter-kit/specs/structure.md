# Steering doc: Structure

<!-- Where code goes. Claude Code: follow this exactly; propose changes here before deviating. -->

## Shape: modular monolith, grouped by feature

One deployable app. Code is grouped by business feature (module), not by technical
layer — everything about invoices lives in `features/invoices/`, not scattered across
global `components/`, `hooks/`, `api/` folders. This keeps each Claude Code session
scoped to one folder and keeps modules from tangling.

```
business-manager/
├── CLAUDE.md                  # lean root context (pointers + gotchas only)
├── TASKS.md                   # live task board
├── ROADMAP.md                 # phases
├── specs/
│   ├── product.md  tech.md  structure.md     # steering docs (this file)
│   └── features/                             # one spec per feature, numbered by phase
├── docs/
│   ├── DATA-MODEL.md
│   └── SETUP-CHECKLIST.md
├── supabase/
│   └── migrations/            # ALL schema changes live here, numbered
├── src/
│   ├── app/                   # Next.js routes only — thin pages that call features
│   │   ├── (app)/             # logged-in owner app: /contacts /quotes /invoices ...
│   │   ├── (public)/          # client-facing: /pay/[token] /book/[slug] /sign/[token] /q/[token]
│   │   └── api/               # route handlers: webhooks/stripe, webhooks/esign
│   ├── features/              # THE CORE — one folder per module
│   │   ├── contacts/
│   │   │   ├── CLAUDE.md      # 5–15 lines: local conventions, gotchas for this module
│   │   │   ├── components/    # UI used only by this module
│   │   │   ├── server/        # queries + mutations (server-side, tenant-scoped)
│   │   │   └── types.ts
│   │   ├── quotes/
│   │   ├── invoices/
│   │   ├── payments/          # Stripe glue: checkout creation, webhook handling
│   │   ├── scheduling/
│   │   ├── contracts/
│   │   ├── workflows/         # event bus + trigger/action engine + run log
│   │   ├── bookkeeping/
│   │   └── todos/
│   ├── components/            # ONLY truly shared UI (layout, nav, form primitives)
│   │   └── ui/                # shadcn/ui generated components
│   └── lib/                   # ONLY truly shared code
│       ├── supabase/          # client factories (server, browser)
│       ├── tenant.ts          # getCurrentTenant() — THE tenant-scoping helper
│       ├── events.ts          # emitEvent() — all modules emit through this
│       └── email/             # Resend + React Email templates
└── tests/                     # cross-module integration/smoke tests
```

## Rules

1. **Features don't import from each other's internals.** If quotes needs contact data,
   it goes through `features/contacts/server/` exported functions — never reaches into
   its components or queries directly. If two modules need the same thing, it moves to `lib/`.
2. **Routes are thin.** Pages in `app/` compose feature components and call feature
   server functions; business logic never lives in a page file.
3. **All data access is server-side and tenant-scoped** through the helper in
   `lib/tenant.ts`. No direct table access from client components.
4. **Every module emits its events** via `lib/events.ts` (even before the workflow
   engine exists — Phase 5 depends on this).
5. **Each feature folder gets its own small `CLAUDE.md`** once the module has real
   code: local naming, gotchas, invariants. Keep the root `CLAUDE.md` lean.
6. **Public client-facing pages live in `(public)`** and authenticate by signed token
   in the URL, never by session.

## Naming

- Files/folders: kebab-case. Components: PascalCase. DB tables: snake_case plural
  (`contacts`, `invoice_items`).
- Feature specs: `specs/features/<phase>-<name>.md` (e.g. `2-invoices.md`).
- Migrations: Supabase CLI timestamped, one concern per migration.

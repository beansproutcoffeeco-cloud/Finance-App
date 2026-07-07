# Steering doc: Tech

<!-- Stack decisions. Claude Code: do not introduce alternatives to these without asking. -->

## Stack (decided)

| Layer | Choice | Why |
|---|---|---|
| Framework | **Next.js** (App Router, TypeScript) | One codebase for app + public client pages; huge ecosystem; AI tools know it deeply |
| Database + Auth + Storage | **Supabase** (managed Postgres) | Auth, DB, file storage, and serverless functions in one platform; native Row Level Security for tenant isolation; official MCP server + AI prompt library for Claude Code |
| Payments | **Stripe** (Checkout + webhooks) | Industry standard; hosted checkout means card data never touches our code |
| Email | **Resend** + React Email templates | Simple API, templates as code |
| Hosting | **Vercel** | Push-to-deploy from GitHub; preview deploys per branch |
| UI | Tailwind CSS + shadcn/ui | Copy-in components, consistent look without design skills |
| E-signature | **TBD in Phase 4** | Evaluate then: Documenso (open-source), SignWell, Dropbox Sign — compare current pricing + API + legal compliance (ESIGN/UETA) |
| SMS | **TBD in Phase 6** (likely Twilio) | Real per-message cost; defer |
| Starter template | [KolbySisk/next-supabase-stripe-starter](https://github.com/KolbySisk/next-supabase-stripe-starter) | Same stack pre-wired incl. Stripe↔Supabase webhook sync; group-by-feature folder structure |

## Rules

- **Managed over self-hosted, always.** We never run our own servers, email infra,
  auth, or card handling.
- **Two environments:** local dev (Supabase local or a dev project + Stripe test mode)
  and production. Secrets in `.env.local` / platform env settings only.
- **Database changes only via migration files** committed to the repo — never by
  clicking around the Supabase dashboard in production.
- **Tenant isolation in the database** (RLS policies), never only in app code.
  See `docs/DATA-MODEL.md`.
- **Webhooks are the source of truth for money.** Stripe webhook handlers verify
  signatures, dedupe by event id, and are safe to run twice.

## Costs (verify current pricing before committing — these move)

Everything above has a free tier or free start that should cover development and early
real use; the meaningful early costs are usually a domain name (~$10–20/yr), Stripe's
per-transaction fee (roughly 3% — a cost of getting paid, not a subscription), and
paid tiers of Supabase/Vercel/Resend/e-sign as usage grows (typically ~$20–25/mo each
when you outgrow free tiers). Check each provider's pricing page when you get there —
none of these numbers were verifiable as of the research date and they change often.

## Claude Code integration

- Install the **Supabase MCP server** (`@supabase/mcp-server-supabase`) so Claude can
  inspect schema and write migrations against the dev project.
- Use Supabase's published **AI prompts** (auth setup, declarative schema, RLS policies,
  edge functions) when building those pieces: supabase.com/docs/guides/getting-started/ai-prompts

# Setup checklist — accounts & services

Work through this top to bottom before Phase 0 coding. Everything here has a free
tier/test mode to start. Keep one password-manager entry per service; enable 2FA on all.

## Accounts to create

- [ ] **GitHub repo** — new empty repo (e.g. `business-manager`), private
- [ ] **Vercel** — sign up with GitHub; import the repo (after first scaffold push);
      every push to `main` now auto-deploys
- [ ] **Supabase** — create TWO projects: `business-manager-dev` and
      `business-manager-prod`. Never point local dev at prod.
- [ ] **Stripe** — one account; use **test mode** for all development (test cards like
      4242 4242 4242 4242). Don't activate live payments until Phase 2 exit test passes.
- [ ] **Resend** — sign up; verify your sending domain (needs a DNS record on your domain)
- [ ] **Domain name** — buy via any registrar; point at Vercel; also used for email sending
- [ ] Phase 4, later: e-signature provider (evaluate Documenso / SignWell / Dropbox Sign then)
- [ ] Phase 6, later: Twilio (SMS), only if you actually want SMS

## Keys & environment variables

Collect into `.env.local` (never committed) and mirror in Vercel + GitHub Actions secrets:

- [ ] `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY` (dev project)
- [ ] `SUPABASE_SERVICE_ROLE_KEY` — server-only, bypasses RLS, guard it
- [ ] `STRIPE_SECRET_KEY` (test), `NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY` (test),
      `STRIPE_WEBHOOK_SECRET` (from `stripe listen` locally / dashboard for prod)
- [ ] `RESEND_API_KEY`

## Local tooling

- [ ] Node.js (LTS) installed
- [ ] Supabase CLI (`npx supabase`) — for local migrations
- [ ] Stripe CLI — `stripe listen --forward-to localhost:3000/api/webhooks/stripe`
      to test webhooks locally
- [ ] Claude Code with the Supabase MCP server configured against the **dev** project

## Repo bootstrap

- [ ] Scaffold from starter template (see `specs/tech.md`)
- [ ] Copy in this kit: `CLAUDE.md`, `TASKS.md`, `ROADMAP.md`, `specs/`, `docs/`
- [ ] `.gitignore` covers `.env*.local`
- [ ] CI workflow: lint + typecheck + test on every push (GitHub Actions)
- [ ] First deploy succeeds on Vercel; visiting the URL shows the app
- [ ] Branch protection on `main` optional but nice: require CI green

## Safety habits (set once, keep forever)

- [ ] Stripe stays in test mode until the Phase 2 exit test passes end-to-end
- [ ] Supabase prod project: enable daily backups (check plan requirements)
- [ ] Never run schema changes against prod by hand — migrations only
- [ ] A "monthly restore drill" reminder: prove you can restore a backup before you have
      real client data that would hurt to lose

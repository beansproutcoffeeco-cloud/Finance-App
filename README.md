# 💰 Finance Tracker

A personal finance tracker that runs entirely on your device. No accounts, no sync,
no tracking — your financial data lives only in your browser's local storage and
never leaves your phone or computer. (This repo contains only the app code; it holds
no personal data.)

## 📱 Use it on your iPhone

**Live app:** https://beansproutcoffeeco-cloud.github.io/Finance-App/

1. Open that link in **Safari** on your iPhone.
2. Tap the **Share** button → **Add to Home Screen** → **Add**.
3. Launch it from the new 💰 icon. After the first visit it works **offline** —
   it's a real app now, internet not required.

> iOS can't open local HTML files in Safari (the Files app only shows a preview),
> which is why the app is hosted. Hosting serves the *code*; your *data* still
> stays in your browser on your device.

## 💻 Use it on a computer

Either open the same link above in any browser, or download
[`index.html`](index.html) and double-click it — the file also works fully offline
with no hosting at all.

## What it does

- **Import bank CSVs** — download a CSV from your bank's website and import it.
  Column layout is auto-detected (including separate debit/credit columns and
  credit-card files where purchases are positive — use the "flip signs" toggle).
  Ambiguous slash dates like 03/04/2026 are read as MM/DD (US order).
  Re-importing the same or overlapping files is safe: duplicates are skipped automatically.
- **Transfers understood** — payments between your own accounts (credit-card payments,
  moves to savings) are detected by description patterns and by matching opposite
  amounts across accounts, and are **excluded from income/spending totals** so your
  numbers are accurate. Toggle "Show transfers" in Activity to see them.
- **Auto-categorization that learns** — imports are categorized by merchant. Anything
  unrecognized lands in a "Needs review" queue; when you correct a category, the app
  learns a rule and applies it to that merchant everywhere, including future imports.
- **Budgets** — set monthly limits per category (inline on the Overview, in
  Settings, or from suggestions based on your 3-month averages — a guided setup
  card gets you started). The Overview leads with a **"Left to spend"** hero that
  tracks your pace against a spending curve learned from your own history, plus
  a budget card with per-category traffic-light meters.
- **Savings & investments** — mark accounts as Savings or Investment (in Settings,
  or when importing). Their activity stays out of your spending/income numbers and
  powers the Savings tab instead: total balance, money added per month (with a
  12-month chart), and — for investment accounts — market gains, computed from the
  balance you enter periodically minus the money you contributed in between. The
  Overview also gets a "Saved this month" tile.
- **Views** — monthly overview (net / income / spending, category breakdown),
  12-month trends with a month-by-month table, searchable transaction list with
  inline editing, and automatic detection of recurring subscriptions & bills with
  their monthly and yearly cost.
- **Manual entry** — quick-add form for cash and one-off transactions.

## Backups & moving between devices

Data is stored per browser, per device — the phone and computer each have their own
copy. To back up or move it:

1. **Settings → Export backup** downloads a JSON file with everything.
2. Send that file to the other device (AirDrop, email to yourself, iCloud/Drive).
3. There, open the tracker and use **Settings → Restore backup**.

Do this occasionally — clearing the browser's website data would erase the tracker's
storage too.

## Repo layout

| File | Purpose |
|---|---|
| `index.html` | The entire app — self-contained, works from a URL or as a local file |
| `sw.js` | Service worker so the hosted app works offline |
| `manifest.webmanifest`, `icon-*.png` | Home-screen install metadata |
| `test/smoke.mjs` | Headless-Chromium smoke test (boots the app, drives every view) |
| `package.json` | Dev-only dependencies for the smoke test (the app has none) |
| `.github/workflows/pages.yml` | Auto-deploys to GitHub Pages on every push to `main` |
| `.github/workflows/smoke-test.yml` | Runs the smoke test on PRs and pushes to `main` |
| `TASKS.md` | Coordination doc for parallel work on the single-file app |
| `.claude/skills/` | Claude Code skills (e.g. converting bank statements to app-ready CSVs) |

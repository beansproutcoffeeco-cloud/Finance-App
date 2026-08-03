---
name: finance-report-to-csv
description: Convert any finance report (bank/credit-card statement, spending summary, PDF or export) into an accurate, validated CSV that imports cleanly into this repo's Finance Tracker app. Use when the user uploads a financial document and wants it converted for the app, e.g. "convert this statement", "turn this report into a CSV", "get this into my finance app".
---

# Finance report → app-ready CSV

Convert an uploaded finance report into a CSV the Finance Tracker app (`index.html`
in this repo) imports with zero manual fixes. Accuracy is the whole job: every
transaction copied exactly, every total reconciled, nothing guessed.

## Target CSV contract (what the app expects)

- Header row: `Date,Description,Category,Amount` (Category is optional — the app
  ignores it on import and auto-categorizes by merchant, but keep it when the
  source document provides categories; it's useful reference data).
- `Date`: transaction date in `YYYY-MM-DD`.
- `Description`: merchant/description text exactly as printed in the source.
- `Amount`: decimal with 2 places. **App sign convention: spending NEGATIVE,
  income/refunds/credits POSITIVE.** The app's "Flip signs" import toggle must
  never be required.
- One CSV per request unless the user says otherwise; sort rows by date.
- File name: descriptive (institution + account last-4 if known), e.g.
  `chase_transactions_1234.csv`. Never commit these CSVs to the repo; hand the
  file to the user or import it directly.

## Workflow

### 1. Extract text from the document

For PDFs use `pypdf` in Python. Known environment quirk: the system
`cryptography` package may be broken (`ModuleNotFoundError: _cffi_backend`) —
fix with `pip install -q cffi cryptography pypdf`. If text extraction returns
garbage or empty pages (scanned/image PDF), Read the PDF directly with the Read
tool and transcribe page by page — then be extra rigorous in step 3 since there
is no machine-extracted text to diff against.

### 2. Parse programmatically — never hand-type transactions

Write a script that parses transaction lines with regexes into structured
records (transaction date, posted date if present, description, amount,
category/section if present). Watch for:

- Negative amounts (refunds/credits) — formats vary: `$-29.35`, `-$29.35`,
  `(29.35)`, `29.35 CR`.
- Descriptions containing commas, quotes, or multiple spaces — preserve exactly;
  use Python's `csv` module for output, never string concatenation.
- Multi-page tables where the header repeats and summary/footer lines interleave
  with transaction lines.

### 3. Reconcile against the document's own totals — mandatory

Recompute from your parsed rows and compare against every total printed in the
document: per-category/section subtotals, per-statement totals, grand totals.
Use `Decimal`, never float. **Every printed total must match your computed sum
exactly.** A mismatch means a missed, duplicated, or mis-parsed row — find it;
do not shrug it off or "adjust" a number to force agreement. Report the
reconciliation results to the user (which totals were checked, all matching).

### 4. Determine the sign convention of the SOURCE, then normalize

Source documents differ: credit-card statements usually print purchases as
positive; bank/checking exports usually print debits as negative. Determine
which by looking at labels and known transactions (a coffee shop is spending; a
"payment received"/refund is a credit). Then normalize to the app convention
(spending negative). If the source's convention is genuinely ambiguous, ask the
user — wrong signs silently corrupt their income/spending numbers.

### 5. Ask, don't guess

Use AskUserQuestion for anything that doesn't cleanly fit, e.g.:

- Rows that fail to parse or amounts that look malformed.
- Both a transaction date and posted date exist and the user hasn't previously
  chosen (default recommendation: transaction date).
- The document mixes multiple accounts (the app imports into one account at a
  time — ask whether to split into one CSV per account).
- Balance rows, interest, fees, or payment-to-card rows that may be transfers
  (the app auto-detects transfers by description, but flag anything odd).

Do not re-ask things already answered in the conversation or evident from the
document.

### 6. Verify with the app's own import code

Run `scripts/verify_app_import.mjs` (in this skill's directory) — it extracts
`parseCSV`/`detectMapping`/`extractRows` from the app's `index.html` and runs
them on the generated CSV:

```bash
node .claude/skills/finance-report-to-csv/scripts/verify_app_import.mjs <csv-path> [index.html-path]
```

Required outcome: header + all columns auto-detected, `invalid: 0`, `flip`
not needed, and the sum matches your reconciled total. If `index.html` isn't in
the working tree, get it from git (`git show <default-branch>:index.html`).

### 7. Deliver

- Send the CSV to the user with SendUserFile so they can download it. Deliver
  via file only — never commit the CSV to the repo (it contains personal
  financial data).
- Summarize: row count per source document, reconciliation results (totals
  checked and matched), the sign convention applied, any refunds/credits, and
  a reminder that the app skips duplicates so re-imports are safe.

## Established user preferences (from prior sessions)

- Date column: **transaction date** (not posted date).
- Signs: **spending negative** (app-native; no flip toggle).
- Keep the source's category names verbatim in the Category column.

/**
 * CI smoke-test for the single-file offline Finance Tracker PWA.
 *
 * Loads index.html in headless Chromium, seeds a small realistic dataset into
 * localStorage, reloads so the app boots with data, then drives every view and
 * asserts the app renders without throwing. Also checks a couple of data
 * invariants. Exits 0 on success, non-zero (throws) on any failure.
 *
 * Target file can be overridden with the SMOKE_TARGET env var (absolute path);
 * defaults to ../index.html next to this script. Used by the broken-app check.
 *
 * App-globals contract this test depends on (script-scope names in index.html
 * that must stay reachable from page scope — renaming/moving them into a
 * module breaks this test):
 *   data, saveData, uid, merchantKey, state, render,
 *   monthTotals, netWorth, accountBalance
 * It also assumes the default category ids 'income', 'groceries', 'dining',
 * 'shopping', 'uncat' exist, and that categories carry a `budget` field
 * (cents) which drives the dashboard's Left-to-spend hero + budget card.
 */
import { chromium } from 'playwright';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { dirname, resolve } from 'node:path';

const __dirname = dirname(fileURLToPath(import.meta.url));
const TARGET = process.env.SMOKE_TARGET
  ? resolve(process.env.SMOKE_TARGET)
  : resolve(__dirname, '..', 'index.html');
const TARGET_URL = pathToFileURL(TARGET).href;

const VIEWS = ['dashboard', 'trends', 'savings', 'transactions', 'recurring', 'settings'];
// Seed into the REAL current month: the dashboard's Left-to-spend hero only
// renders for the current month (when at least one budget is set), so a
// hardcoded month would silently stop exercising the budgeting UI.
const NOW = new Date();
const SEED_MONTH = `${NOW.getFullYear()}-${String(NOW.getMonth() + 1).padStart(2, '0')}`;

const failures = [];
function check(label, cond, detail) {
  if (cond) {
    console.log(`  PASS  ${label}`);
  } else {
    console.log(`  FAIL  ${label}${detail ? ' — ' + detail : ''}`);
    failures.push(label + (detail ? ' — ' + detail : ''));
  }
}

// Runs in the page: builds a small realistic dataset using the app's own
// categories/helpers, writes it to localStorage. Returns nothing meaningful.
function seedInPage(month) {
  if (typeof data === 'undefined' || typeof saveData !== 'function') {
    throw new Error('app globals (data/saveData) not reachable from page scope');
  }
  const tx = (o) => Object.assign({
    id: uid(),
    merchantKey: merchantKey(o.desc),
    isTransfer: false,
    source: 'smoke',
    fp: 'smoke-' + uid(),
  }, o);

  data.accounts = [
    { id: 'manual', name: 'Cash / Manual', type: 'cash', startingBalance: 0 },
    { id: 'checking', name: 'Everyday Checking', type: 'bank', startingBalance: 120000 },
    { id: 'brokerage', name: 'Growth Brokerage', type: 'investment', startingBalance: 0 },
  ];

  data.transactions = [
    // income / paycheck
    tx({ date: month + '-01', amount: 320000, desc: 'ACME PAYROLL DIRECT DEP', categoryId: 'income', accountId: 'checking' }),
    // ordinary expenses
    tx({ date: month + '-03', amount: -8500, desc: 'WHOLE FOODS MARKET', categoryId: 'groceries', accountId: 'checking' }),
    tx({ date: month + '-10', amount: -4200, desc: 'CHIPOTLE ONLINE', categoryId: 'dining', accountId: 'checking' }),
    // positive refund against an expense category
    tx({ date: month + '-12', amount: 2500, desc: 'AMAZON REFUND', categoryId: 'shopping', accountId: 'checking' }),
    // a transfer pair between accounts (excluded from spending/income analytics)
    tx({ date: month + '-15', amount: -50000, desc: 'TRANSFER TO BROKERAGE', categoryId: 'uncat', accountId: 'checking', isTransfer: true }),
    tx({ date: month + '-15', amount: 50000, desc: 'TRANSFER FROM CHECKING', categoryId: 'uncat', accountId: 'brokerage', isTransfer: true }),
  ];

  // A balance snapshot for the investment account (drives the Savings view).
  data.balances = [
    { id: uid(), accountId: 'brokerage', date: month + '-14', balance: 1500000 },
  ];

  // Budgets on two categories so the dashboard renders the Left-to-spend hero
  // and the budget card with per-category meters.
  const budgets = { groceries: 60000, dining: 15000 };
  for (const c of data.categories) if (budgets[c.id]) c.budget = budgets[c.id];

  saveData();
}

async function main() {
  console.log(`Smoke test target: ${TARGET_URL}`);
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext();
  const page = await context.newPage();

  const pageErrors = [];
  page.on('pageerror', (err) => pageErrors.push(err));

  try {
    // 1) Initial boot (empty app) so the app scripts + globals are present.
    await page.goto(TARGET_URL, { waitUntil: 'load' });

    // 2) Seed a realistic dataset, then reload so the app boots WITH data.
    await page.evaluate(seedInPage, SEED_MONTH);
    await page.reload({ waitUntil: 'load' });
    await page.waitForTimeout(50); // let any async errors surface

    check('app boots with data (no page errors so far)', pageErrors.length === 0,
      pageErrors.map((e) => e.message).join(' | '));

    const bootLen = await page.evaluate(() => document.querySelector('#app').innerHTML.length);
    check('#app has meaningful content after boot', bootLen > 50, `length=${bootLen}`);

    // 3) Drive every view. A throw inside render() rejects the evaluate call.
    for (const v of VIEWS) {
      const before = pageErrors.length;
      let len = 0;
      let threw = null;
      try {
        len = await page.evaluate((view) => {
          state.view = view;
          state.editingId = null;
          render();
          return document.querySelector('#app').innerHTML.length;
        }, v);
      } catch (e) {
        threw = e.message;
      }
      await page.waitForTimeout(20);
      const newErrors = pageErrors.slice(before).map((e) => e.message).join(' | ');
      check(`view '${v}' renders without throwing`, threw === null && !newErrors,
        threw || newErrors);
      check(`view '${v}' produced meaningful #app content`, len > 50, `length=${len}`);
    }

    // 4) Budgeting UI: with budgets seeded on the current month, the dashboard
    // must show the Left-to-spend hero and at least one per-category meter.
    const dash = await page.evaluate(() => {
      state.view = 'dashboard';
      state.editingId = null;
      render();
      const app = document.querySelector('#app');
      return {
        hasHero: app.textContent.includes('Left to spend'),
        hasMeter: !!app.querySelector('.meter[data-cat]'),
      };
    });
    check("dashboard shows 'Left to spend' hero (budgets + current month)", dash.hasHero);
    check('dashboard shows a per-category budget meter', dash.hasMeter);

    // 5) Data invariants.
    const inv = await page.evaluate((month) => {
      const mt = monthTotals(month);
      const nw = netWorth();
      const sum = data.accounts.reduce((s, a) => s + accountBalance(a.id), 0);
      return { income: mt.income, spending: mt.spending, netWorth: nw, sumBalances: sum };
    }, SEED_MONTH);

    check(`monthTotals('${SEED_MONTH}').income > 0`, inv.income > 0, `income=${inv.income}`);
    check('netWorth() === sum of accountBalance() over accounts',
      inv.netWorth === inv.sumBalances, `netWorth=${inv.netWorth} sum=${inv.sumBalances}`);

    check('no uncaught page errors overall', pageErrors.length === 0,
      pageErrors.map((e) => e.message).join(' | '));
  } finally {
    await browser.close();
  }
}

main()
  .then(() => {
    console.log('');
    if (failures.length) {
      console.log(`SMOKE TEST FAILED — ${failures.length} failing check(s):`);
      for (const f of failures) console.log('  - ' + f);
      process.exit(1);
    }
    console.log('SMOKE TEST PASSED — app booted and all views rendered cleanly.');
    process.exit(0);
  })
  .catch((err) => {
    console.log('');
    console.error('SMOKE TEST FAILED — harness error:');
    console.error(err && err.stack ? err.stack : err);
    process.exit(1);
  });

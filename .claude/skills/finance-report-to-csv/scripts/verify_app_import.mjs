#!/usr/bin/env node
// Verify a generated CSV against the Finance Tracker app's REAL import code.
// Extracts parseCSV/parseDateStr/parseAmountStr/detectMapping/extractRows from
// index.html and runs them on the CSV, so the check exercises exactly what the
// app will do at import time.
//
// Usage: node verify_app_import.mjs <csv-path> [index.html-path]
// Exit codes: 0 = clean import; 1 = problems found; 2 = usage/setup error.

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const [, , csvPath, htmlArg] = process.argv;
if (!csvPath) {
  console.error('usage: node verify_app_import.mjs <csv-path> [index.html-path]');
  process.exit(2);
}
const htmlPath = htmlArg || path.join(process.cwd(), 'index.html');
if (!fs.existsSync(csvPath)) { console.error(`CSV not found: ${csvPath}`); process.exit(2); }
if (!fs.existsSync(htmlPath)) {
  console.error(`App not found: ${htmlPath} — pass the path to index.html, or extract it from git first.`);
  process.exit(2);
}

const html = fs.readFileSync(htmlPath, 'utf8');
function grab(name, endMarker) {
  const i = html.indexOf('function ' + name);
  if (i < 0) { console.error(`Could not find function ${name} in ${htmlPath}`); process.exit(2); }
  const j = html.indexOf(endMarker, i);
  if (j < 0) { console.error(`Could not find end marker after ${name}`); process.exit(2); }
  return html.slice(i, j);
}

// Dependency of parseDateStr inside the app.
const MONTH_NAMES = ['January','February','March','April','May','June',
  'July','August','September','October','November','December'];

const src =
  grab('parseCSV', 'function parseDateStr') +
  grab('parseDateStr', 'function parseAmountStr') +
  grab('parseAmountStr', '// Guess which columns') +
  grab('detectMapping', 'function extractRows') +
  grab('extractRows', 'function fingerprintBase') +
  '\nreturn { parseCSV, detectMapping, extractRows };';
const { parseCSV, detectMapping, extractRows } = new Function('MONTH_NAMES', src)(MONTH_NAMES);

const text = fs.readFileSync(csvPath, 'utf8');
const rows = parseCSV(text);
const map = detectMapping(rows);
const parsed = extractRows(rows, map);
const ok = parsed.filter(r => r.ok);
const bad = parsed.filter(r => !r.ok);
const cents = ok.reduce((s, r) => s + r.amount, 0);
const spend = ok.filter(r => r.amount < 0).length;
const income = ok.filter(r => r.amount > 0).length;

console.log('detected mapping :', JSON.stringify(map));
console.log('rows parsed      :', parsed.length);
console.log('ok               :', ok.length);
console.log('invalid          :', bad.length);
console.log('net total        : $' + (cents / 100).toFixed(2));
console.log('spending rows    :', spend, '(negative amounts)');
console.log('income/credit rows:', income, '(positive amounts)');

let fail = false;
if (!map.hasHeader) { console.error('FAIL: header row not detected'); fail = true; }
if (map.dateCol < 0 || map.descCol < 0 || map.amountCol < 0) {
  console.error('FAIL: app could not auto-detect date/description/amount columns'); fail = true;
}
if (bad.length) {
  console.error(`FAIL: ${bad.length} row(s) would be rejected by the app:`);
  for (const r of bad.slice(0, 10)) console.error('  ', JSON.stringify(r.raw));
  fail = true;
}
if (income > spend) {
  console.error('WARNING: more positive rows than negative — sign convention may be flipped ' +
    '(app expects spending NEGATIVE). Double-check before delivering.');
  fail = true;
}
console.log(fail ? '\nRESULT: FAIL' : '\nRESULT: PASS — CSV imports cleanly with no toggles');
process.exit(fail ? 1 : 0);

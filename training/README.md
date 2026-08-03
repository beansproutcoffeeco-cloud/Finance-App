# Snowboard Pre-Season Training System — 2026

18 weeks · Mon/Wed/Sat · **Aug 24 → Dec 24, 2026** · 53 sessions, every one in a
gym version (≤60 min) *and* a home version (≤40 min, dumbbells/bands/bodyweight).

This is training programming, not medical advice. Anything that hurts (beyond
normal muscle burn) is a physio question, not a push-through question — knee
pain during single-leg work especially (see the knee notes on circuit stations).

## What's here

| File | What it is |
|---|---|
| `program.json` | Source of truth — all 53 sessions × 2 variants, structured |
| `exercises.json` | Exercise library — form, cues, mistakes, home swaps, videos |
| `generate_program.py` | Regenerates `program.json`, `program.csv`, `training-plan.ics` |
| `push_to_notion.py` | Creates/updates the Notion workspace (idempotent) |
| `program.csv` | Flat export — drops straight into Google Sheets |
| `training-plan.ics` | One-time import into Google Calendar (America/Chicago) |
| `docs/` | Research briefs + the approved design proposal |
| `constraints.local.md` | **Gitignored.** Personal injury/limit notes — never synced |

## How the program works

- **Blocks:** 1 Base (W1–4) → 2 Strength (W5–8) → 3 Strength→Power (W9–12) →
  4 Power + quad-endurance peak (W13–16) → 5 Taper (W17–18).
  Deloads on weeks 4/8/12/16: volume −~40%, loads stay.
- **Archetypes:** Mon A = lower strength + anti-rotation core · Wed B = power +
  balance (all jump volume lives here) · Sat C = quad-endurance circuit +
  aerobic finisher. The C-day circuit is the "legs burn out after 3 runs" fix.
- **Jump contacts** ramp 55/week → 131/week (NSCA novice→intermediate range),
  monotonically within each block; Block 4 raises intensity, not count.
- **No lunge patterns anywhere** — step-ups, Spanish squats, split-squat *holds*
  (short, with a reduce-depth regression) carry single-leg work instead.

## How to log a session (Notion)

1. Open today's page in **Sessions** (calendar or This Week view).
2. Set **Location** = Gym or Home — the page body shows both prescriptions.
3. For each working set add a **Set Log** row: Exercise, Set #, Reps, Weight,
   RPE, Location. The row's Volume/e1RM compute themselves.
4. Set Status = Done, fill Duration and Session RPE. Two minutes, tops.

## How progression is decided

**Double progression.** Each exercise has a rep range (e.g. 3×8–10). Start at
the bottom with a load that leaves ~3 reps in the tank (RPE 7). When **all sets
hit the top of the range** at or under target RPE → next session add **+5 lb**
(lower body) / **+2.5 lb** (upper), or **+1 rep / +5 s hold / +2 contacts**
where load can't move. The Exercise Library's PR Weight / Best e1RM / Last
Logged rollups show where you stand; if last session hit the range top, add.

- **Missed session:** skip it — mark Skipped, do the next scheduled session.
  Never shift the calendar. **2+ misses in one week → repeat that week's loads
  the following week** instead of progressing.
- **Missed whole week:** step back to the previous week's loads and re-run the
  missed week's session types once before continuing the plan (dates stay as
  scheduled — you're repeating loads, not rescheduling days).
- **Bad-feeling day:** keep the exercises, drop everything to RPE 6 (~−10%
  load). That session doesn't count toward a progression decision.
- **Travel week:** run the home versions. Holds, tempo work and jump contacts
  progress as scheduled; barbell lifts pause and resume at last gym load
  (after 3+ weeks away: 90% of it).

## How to swap gym ↔ home

Every session page carries both prescriptions — same qualities, same intent,
volume/tempo adjusted for lighter equipment (slower eccentrics + a few more
reps replace plate loading). Log sets with the **Location** field and the
progression math survives the swap: dumbbell loads track their own double
progression, and everything load-independent (holds, contacts, tempo reps)
progresses globally. A whole week at home still moves the program forward.

## How to regenerate after edits

```bash
# 1. Edit the tables/templates in generate_program.py (or exercises.json)
python3 training/generate_program.py     # rebuilds JSON + CSV + ICS, re-validates
python3 training/push_to_notion.py       # upserts Notion — no duplicates
```

`generate_program.py` hard-fails if an edit breaks the invariants (gym >60 min,
home >40 min, >10% weekly volume jump, non-monotonic contacts, missing variant).
`push_to_notion.py` keys on Session Id / exercise Id, so re-runs update in
place. After the first push it writes `notion_links.json`; re-run the generator
once more and the `.ics` descriptions gain Notion links. Re-import the `.ics`
only if dates/times changed (delete the old calendar first — UIDs are stable).

Calendar defaults: Mon/Wed 5:30 PM, Sat 9:00 AM Central — edit
`SESSION_LOCAL_TIME` in the generator to change.

## Notion setup (first push)

```bash
export NOTION_TOKEN=secret_xxx           # notion.so/my-integrations
export NOTION_PARENT_PAGE_ID=xxxx        # share the target page with the integration
python3 training/push_to_notion.py
```

One manual step (the API can't create views): on **Sessions**, add a Calendar
view by Date and a "This Week" table filtered to `Date is within → this week`.

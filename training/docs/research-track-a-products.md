# Track A — Comparable Products Research Brief

## How the categories behave

**Tracker apps.** Hevy and Strong are log-first: no scheduling engine, so "missed
sessions" don't exist — you just do the next workout, and previous-session values
("ghost values") pre-fill every set. Strong is fastest to log (auto rest timer on set
completion, pre-loaded prior weights). Boostcamp is program-first: multi-week
mesocycles, per-set RPE/RIR fields, and programmatic weight/rep recommendations
(linear + double progression baked into programs like GZCLP, 5/3/1). TrainHeroic
layers a pre-session readiness survey and percentage-of-working-max programming.
Fitbod and JuggernautAI are algorithmic: Fitbod re-generates each session from muscle
"freshness" and skipping patterns (it never reschedules — it re-estimates); JuggernautAI
prescribes target RPE per set and recalibrates loads from logged RPE-vs-actual.

**Snow-specific programs.** MTI's Backcountry Ski Pre-Season plan is 7 weeks /
6 days-week, each weekday owning a fixed quality (eccentric leg strength via Leg
Blasters, leg lactate tolerance, chassis integrity/core, step-up uphill endurance),
with week 7 as assessment/taper. MobilityDuo's Shred 4.0 is 12–15 weeks in 4 phases
with built-in recovery weeks, baseline testing at 4 checkpoints, a per-level dropdown
(Beginner/Int/Adv) and an alternative movement for nearly every exercise. Fit 2 Shred
emphasizes joint/connective-tissue prep and an "acid tolerance" anaerobic protocol.
Fitness Blender and EōS are free content (follow-along videos / listicles) — no
progression model, useful only as exercise-selection references.

## 5 patterns worth copying

1. **Ghost values: pre-fill every set with last session's weight × reps (Strong/Hevy).**
   In Notion this is a rollup ("last weight," "last reps") from Set Log onto the
   exercise row — the single biggest tap-saver, and it makes double progression
   self-evident without any algorithm.
2. **Double progression with explicit rep ranges (Boostcamp-style, e.g. GZCLP).**
   "3×8–12; when all sets hit 12, add load" is deterministic, needs zero computation
   Notion can't do with a simple formula, and doesn't require a tested 1RM.
3. **Named session archetypes per weekday quality (MTI).** "Each day owns a quality"
   maps cleanly to 3 sessions/week with stable templates — sessions become reusable
   patterns rather than 53 bespoke pages, and the qualities are snowboard-relevant.
4. **Per-exercise alternative + level variant (Shred 4.0).** Every Exercise Library row
   gets a home variant and easier/harder self-relations; this is how gym+home duality
   should work — one program with swappable movements, not two parallel programs.
5. **Skip = re-estimate, don't backfill (Fitbod's philosophy, simplified).** Never shift
   the calendar; a missed session is marked Skipped and the week continues, with one
   manual rule: 2+ misses in a week → repeat that week's loads instead of progressing.
   Keeps the .ics calendar static and trustworthy.

## 3 patterns worth avoiding

1. **RPE-driven autoregulation as the core progression (JuggernautAI).** Needs per-set
   RPE honesty, daily recalculation, and e1RM trend math — overkill outside meet prep;
   in Notion it becomes manual spreadsheet work that won't be sustained. RPE stays a
   target/notes-level field.
2. **Daily-generated, non-repeating workouts (Fitbod).** The variety engine destroys
   week-over-week comparability — with no repeated exercise exposure, ghost values and
   double progression can't function. A fixed 18-week plan is the point.
3. **Pre-session readiness surveys and %-of-working-max loading (TrainHeroic).** Five
   wellness questions before logging adds friction a solo user skips by week 3, and
   %-based loading is fragile without a coach maintaining the maxes.

## Notion template relation structure

The dominant pattern is three databases: **Sessions** (one page per dated workout),
**Exercise Library** (one row per movement: muscle group, equipment, video link,
difficulty/type selects), and **Set Log** (one row per set: weight, reps, relation to
both the Session and the Exercise). Exercise Library acts as the aggregation hub:
rollups over Set Log give "last weight," "max weight (auto-PR)," and "last logged
date," while formulas compute volume (sets × reps × weight) and estimated 1RM. Session
pages use a filtered linked view of Set Log (relation = this session) so mid-workout
logging is "open today's page, fill rows"; the mobile-critical trick is keeping Set Log
properties minimal (exercise, weight, reps, done-checkbox) so a set is loggable in 2–3
taps. Our tracker mirrors this, adding Week/Block properties on Sessions to drive
deload and progression views.

Sources: Strong vs Hevy (RepReturn), Boostcamp features page, JuggernautAI reviews,
Fitbod Algorithm Q&A, MTI Backcountry Ski plan, MobilityDuo Shred 4.0, Fit 2 Shred
(Movement Gym), TrainHeroic support docs, Nodi Pro Gym Tracker (Notion), EōS Fitness
snowboard exercise guide.

# Phase 1 Design Proposal — Snowboard Pre-Season Training System

Program: Mon 2026-08-24 → Thu 2026-12-24, Mon/Wed/Sat, **53 sessions**
(weeks 1–17 full = 51, week 18 has Mon Dec 21 + Wed Dec 23 only; Sat Dec 26 falls
past program_end). Timezone: America/Chicago.

## Block structure (adjusted from the suggested 6/5/5/2 split)

| Block | Weeks | Focus | Deload |
|---|---|---|---|
| 1 — Base | 1–4 | Movement quality, tendon/joint prep, hypertrophy 8–12 reps, landing mechanics + low-amplitude plyos, aerobic base, holds 20–40 s | W4 |
| 2 — Strength | 5–8 | Compounds to 5–8 reps, eccentric-emphasis quad work (3–4 s lowering), moderate plyos, holds 40–60 s | W8 |
| 3 — Strength → Power | 9–12 | Retain strength 2×/wk, introduce jump squats/loaded jumps, tempo-quad circuits ramp, holds 60–90 s, second interval dose | W12 |
| 4 — Power + quad-endurance peak | 13–16 | Reactive plyos, light contrast pairings, leg-blaster-style eccentric circuits, holds 90–120 s | W16 |
| 5 — Peak / pre-season | 17–18 | Volume −40–50%, intensity held, balance/proprioception density up, arrive fresh | taper |

**Why adjusted:** the suggested split (Base 1–6 / Strength 7–11 / Power 12–16 / Peak
17–18) puts every deload mid-block, and week 12's deload would land on the *first week*
of the power block — starting your priority block at 60% volume. Aligning 4-week waves
to the deloads (4/8/12/16) gives each block a clean push→push→push→deload shape and a
natural double-progression reset point. Track B supports this: for a novice,
periodization *type* barely matters (Williams et al. 2017), so calendar alignment wins;
strength-first sequencing is preserved (contrast/PAPE work stays out until Block 4
because sub-1-year lifters show little potentiation effect — Cormier et al. 2020); and
tendon adaptation needs >12 weeks, so isometric/heavy-slow quad loading runs through
every block, not just Block 3+.

## Session archetypes (rotate Mon/Wed/Sat, content shifts by block)

- **Mon — A: Lower strength + anti-rotation core.** Squat or hinge primary, one
  single-leg pattern, one efficient upper push/pull, Pallof/carry variation, wall sit.
- **Wed — B: Power + balance.** All plyo volume lives here (48–72 h from other leg
  work), med-ball rotational work, single-leg stability, calf/ankle endurance.
- **Sat — C: Quad endurance circuit + aerobic finisher.** Tempo/eccentric/isometric
  quad circuit (the "legs burn out" fix) + Zone 2 bike finisher; one weekly 4×4-min
  interval dose replaces part of the finisher from Block 3 on.

No heavy lower loading on consecutive calendar days by construction (Mon/Wed/Sat).

**Knee constraint (details in local gitignored file):** no dynamic lunge patterns
anywhere in the program. Single-leg work uses box step-ups, Spanish squats, single-leg
RDLs, glute bridges, band lateral walks; split-squat *isometric holds* appear only as
short static holds with a reduced-depth regression and an explicit drop-if-painful rule.

## Progression

**Double progression:** work at the bottom of the rep range; when all sets hit the top
at target RPE, add +5 lb (lower) / +2.5 lb (upper) next session, or +1 rep / +5 s hold
/ +2 contacts where load can't move. RPE cap 8 through Block 1 (RPE 7 on quad work in
week 1 while confirming the knee tolerates loading).

- **Missed session:** never reschedule — mark Skipped, do the next scheduled session as
  planned. 2+ misses in one week → repeat that week's loads the following week.
- **Bad-feeling day:** keep the movements, drop all working sets to RPE 6 (≈ −10%
  load); that session doesn't count toward a progression decision.
- **Travel week:** run home versions (they progress the same qualities); bodyweight-only
  fallbacks noted per session. Loaded-lift progression pauses; holds/plyo/tempo
  progression continues.
- **Gym↔home:** same session intent, same tracker, `location` field on every logged
  set. DB loads progress on their own double-progression track; after 2+ consecutive
  home weeks, resume gym lifts at last gym load (3+ weeks: 90% of it).

## Plyometric ramp (weekly jump contacts, NSCA novice guidance)

| Wk | 1 | 2 | 3 | 4D | 5 | 6 | 7 | 8D | 9 | 10 | 11 | 12D | 13 | 14 | 15 | 16D | 17 | 18 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Contacts | 55 | 65 | 75 | 40 | 80 | 90 | 100 | 50 | 100 | 110 | 120 | 60 | 110 | 115 | 120 | 60 | 80 | 60 |

Blocks 1–2 extensive only (pogos, drop-to-stick, submaximal jumps); Block 3 moderate
(jump squats, lateral bounds); Block 4 reactive/intensive at held volume — intensity
rises, count doesn't (novice tendons are the limiter). Contacts are monotonic within
each block outside deloads. Taper keeps intent, cuts volume.

## Rest periods

| Type | Rest | Rationale |
|---|---|---|
| Strength compounds | 120–180 s | Near-full recovery so load, not fatigue, drives adaptation |
| Power / plyo | 60–120 s | Power quality dies with fatigue; the rep's intent is the stimulus |
| Endurance circuit | 15 s transitions, 90 s between rounds | Incomplete recovery *is* the stimulus for fatigue resistance |
| Accessory / core | 45–60 s | Small muscle groups recover fast; protects the 60-min cap |

## Sample week — Week 1 (both variants, computed durations)

### W01 D1 — Mon Aug 24 — A: Lower Strength + Core

**GYM (54 min):** warmup 8 (bike 3 min + leg swings, squats, glute bridges, band
lateral walks, 2 light ramp-up sets)
| Exercise | Sets×Reps | RPE | Tempo | Rest | Time |
|---|---|---|---|---|---|
| Goblet squat | 3×8–10 | 7 | 3-1-1 | 120 s | 8.5 |
| DB Romanian deadlift | 3×8–10 | 7 | 2-1-1 | 120 s | 8.3 |
| Box step-up (low) | 3×8/leg | 7 | 2-0-1 | 90 s | 8.0 |
| DB bench press | 3×8–12 | 7 | — | 90 s | 6.5 |
| Pallof press | 3×10/side | — | — | 60 s | 5.5 |
| Wall sit | 3×30 s | — | iso | 60 s | 4.5 |

Main ≈ 40 min (last rest dropped) + cooldown 6 (quad/hip-flexor/calf/hamstring
stretch, 1 min down-regulation breathing) = **54 ≤ 60 ✓**

**HOME (38 min):** warmup 6 · goblet squat 3×10–12 @3-1-1, rest 90 · DB RDL 3×10–12,
rest 90 · stair step-up 2×10/leg, rest 75 · push-up 3×8–15, rest 60 · band Pallof
2×12/side, rest 45 · wall sit 3×30 s, rest 45 → main ≈ 28 + cooldown 4 = **38 ≤ 40 ✓**
Slower tempo + higher reps compensate the lighter DB load; same qualities, same order.

### W01 D2 — Wed Aug 26 — B: Power + Balance (55 contacts)

**GYM (52 min):** warmup 8 (bike 3 + ankle rocks, hip openers, light hop prep)
| Exercise | Sets×Reps | Contacts | Rest | Time |
|---|---|---|---|---|
| Box drop-to-stick (12″) | 4×4 | 16 | 60 s | 6.3 |
| Pogo hops (low) | 3×10 | 30 | 60 s | 4.0 |
| Broad jump to stick | 3×3 | 9 | 90 s | 5.8 |
| Med-ball rotational scoop toss | 3×5/side | — | 60 s | 5.0 |
| Single-leg RDL (light DB) | 3×6/leg | — | 60 s | 6.5 |
| SL balance, pad/eyes-closed | 3×30 s/leg | — | 30 s | 4.5 |
| Calf raise 2-1-2 | 3×15 | — | 60 s | 6.0 |

Main ≈ 38 + cooldown 5 = **52 ≤ 60 ✓**

**HOME (33 min):** warmup 6 · snap-down landings 4×4 · pogo hops 3×10 · broad jump to
stick 3×3 (clear floor space) · band rotational chop 3×8/side · SL RDL bodyweight
3×8/leg · SL balance 3×30 s/leg · stair calf raise 3×15 → main ≈ 24 + cooldown 3 =
**33 ≤ 40 ✓** Identical contact count — plyo needs no equipment.

### W01 D3 — Sat Aug 29 — C: Quad Endurance Circuit + Aerobic Finisher

**GYM (46 min):** warmup 7 · **circuit ×3 rounds** (15 s transitions, 90 s between
rounds, ≈ 6 min/round): tempo goblet squat 3-0-3 ×10 → wall sit 30 s → box step-up
×8/leg → Spanish squat (band) ×12 slow → band lateral walk ×10/side → side plank
20 s/side. Circuit ≈ 21 min · **finisher:** Zone 2 bike 12 min (conversational) ·
cooldown 6 = **46 ≤ 60 ✓** (headroom is deliberate — the finisher and hold times grow
through the blocks and this session peaks near 58 by Block 4)

**HOME (37 min):** warmup 5 · same circuit with DB + band anchored low ≈ 20 min ·
finisher: 8 min continuous easy step-up/march circuit at Zone 2 effort · cooldown 4 =
**37 ≤ 40 ✓**

## Weekly goal coverage (every week, both variants)

- **Quad endurance:** C-day circuit + wall sits on A-day + tempo eccentrics — measurable
  via hold duration and circuit round times.
- **Lower-body power:** B-day contacts + (from Block 3) loaded jumps — measurable via
  weekly contact count and jump-squat load.
- Upper/core stays at 1–2 efficient slots per session, supporting riding posture and
  crash resilience only.

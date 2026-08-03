#!/usr/bin/env python3
"""Snowboard pre-season training program generator.

Single source of truth: edit the templates/tables below, re-run, and
program.json, program.csv and training-plan.ics are regenerated together.

    python3 training/generate_program.py

Design decisions (see docs/phase1-design-proposal.md):
- 18 weeks, Mon/Wed/Sat from 2026-08-24; sessions after 2026-12-24 are dropped.
- Blocks: 1 Base (W1-4), 2 Strength (W5-8), 3 Strength->Power (W9-12),
  4 Power+Quad-endurance peak (W13-16), 5 Peak/taper (W17-18).
  Deloads: W4/8/12/16 (volume ~-40%, intensity held).
- Archetypes: Mon A lower strength + core, Wed B power + balance,
  Sat C quad-endurance circuit + aerobic finisher.
- Every session has a gym variant (<=60 min) and a home variant (<=40 min).
- No dynamic lunge patterns anywhere (knee-friendly substitutions).
"""

import csv
import json
from datetime import date, datetime, timedelta
from pathlib import Path

HERE = Path(__file__).resolve().parent

START = date(2026, 8, 24)          # Monday, week 1
PROGRAM_END = date(2026, 12, 24)
N_WEEKS = 18
DELOAD_WEEKS = {4, 8, 12, 16}
DAY_OFFSETS = {1: 0, 2: 2, 3: 5}   # Mon, Wed, Sat
ARCHETYPES = {1: "A", 2: "B", 3: "C"}
ARCH_NAMES = {
    "A": "Lower Strength + Core",
    "B": "Power + Balance",
    "C": "Quad Endurance + Aerobic",
}
TZID = "America/Chicago"
SESSION_LOCAL_TIME = {1: (17, 30), 2: (17, 30), 3: (9, 0)}  # Mon/Wed 5:30pm, Sat 9am

TRANSITION_SEC = 15        # between exercises in a superset / circuit stations
CONTRAST_EXTRA_SEC = 30    # walk-to-box time inside a contrast pair (folded into jump work_sec)

# warmup / cooldown minutes per (archetype, location)
WU_CD = {
    ("A", "gym"): (8, 6), ("B", "gym"): (8, 5), ("C", "gym"): (7, 6),
    ("A", "home"): (5, 4), ("B", "home"): (5, 3), ("C", "home"): (5, 4),
}


def block_of(week):
    return 1 if week <= 4 else 2 if week <= 8 else 3 if week <= 12 else 4 if week <= 16 else 5


def rpe_for(week):
    if week in DELOAD_WEEKS:
        return 6
    return 7 if block_of(week) == 1 else 8


def E(ex, sets, reps, rest, work, rpe=None, tempo=None, notes="", group=None, contacts=0):
    """One prescription line. work = estimated seconds per set (or per hold)."""
    return {
        "exercise_id": ex, "sets": sets, "rep_range": reps, "target_RPE": rpe,
        "rest_sec": rest, "tempo": tempo, "work_sec": work, "notes": notes,
        "superset_group": group, "contacts_per_set": contacts,
    }


# ---------------------------------------------------------------------------
# Warmups / cooldowns
# ---------------------------------------------------------------------------

def warmup(arch, loc, block):
    if arch == "A":
        base = (["Bike easy — 3 min"] if loc == "gym" else ["March in place / jumping jacks — 2 min"])
        return base + ["Leg swings ×10/direction", "Bodyweight squats ×10",
                       "Glute bridges ×12", "Band lateral walks ×10/side",
                       "Light ramp-up set(s) of the first lift"]
    if arch == "B":
        base = (["Bike easy — 3 min"] if loc == "gym" else ["Jumping jacks — 2 min"])
        out = base + ["Ankle rocks ×10/side", "Hip openers ×8/side",
                      "Pogo prep — 2×10 small hops", "A-skips or line hops — 2×15 s"]
        if block >= 2:
            out.append("Single-leg balance — 60 s/leg (firm ground, then eyes closed)")
        return out
    base = (["Bike easy — 3 min"] if loc == "gym" else ["March in place — 2 min"])
    return base + ["Bodyweight squats ×10", "Band lateral walks ×10/side", "Calf raises ×10"]


def cooldown(arch, loc):
    out = ["Couch/quad stretch — 45 s/side", "Hip flexor stretch — 45 s/side",
           "Hamstring stretch — 45 s/side", "Calf stretch — 45 s/side",
           "Down-regulation breathing — 1 min"]
    if arch == "C" and loc == "gym":
        out.insert(0, "Easy spin — 1 min")
    return out


# ---------------------------------------------------------------------------
# A day — Lower strength + anti-rotation core
# ---------------------------------------------------------------------------

def gym_A(w):
    b, dl, rpe = block_of(w), w in DELOAD_WEEKS, rpe_for(w)
    if b == 1:
        hold = {1: 30, 2: 35, 3: 40, 4: 30}[w]
        gob = 2 if dl else (4 if w == 3 else 3)
        s = 2 if dl else 3
        return [
            E("goblet_squat", gob, "8-10", 120, 50, rpe, "3-1-1"),
            E("db_rdl", s, "8-10", 120, 45, rpe, "2-1-1"),
            E("box_step_up", s, "8/leg", 90, 70, rpe, "2-0-1",
              notes="Low box; control the descent"),
            E("db_bench_press", s, "8-12", 90, 40, rpe),
            E("pallof_press", s, "10/side", 60, 50),
            E("wall_sit", s, f"{hold} s", 60, hold, tempo="iso"),
        ]
    if b == 2:
        sq = 2 if dl else (3 if w == 5 else 4)
        s = 2 if dl else 3
        return [
            E("back_squat", sq, "5-6", 150, 40, rpe, "3-0-1",
              notes="Eccentric emphasis — 3 s down"),
            E("bb_rdl", s, "6-8", 150, 40, rpe, "2-1-1"),
            E("box_step_up", 2, "8/leg", 90, 70, rpe, "2-0-1", notes="Hold DBs"),
            E("db_bench_press", s, "8-10", 0, 40, rpe, group="S1"),
            E("one_arm_db_row", s, "8-10/arm", 60, 70, rpe, group="S1",
              notes="Superset with DB bench"),
            E("pallof_press", s, "10/side", 60, 50),
        ]
    if b == 3:
        s = 2 if dl else 3
        return [
            E("back_squat", 2 if dl else 4, "4-6", 180, 40, rpe, "3-0-1",
              notes="Eccentric emphasis — 3 s down"),
            E("bb_rdl", s, "6-8", 150, 40, rpe, "2-1-1"),
            E("hip_thrust", 2, "8-10", 90, 45, rpe),
            E("db_overhead_press", s, "6-8", 0, 35, rpe, group="S1"),
            E("one_arm_db_row", s, "8-10/arm", 60, 70, rpe, group="S1",
              notes="Superset with OHP"),
            E("suitcase_carry", 2, "30 s/side", 60, 70),
        ]
    if b == 4:
        if dl:
            return [
                E("back_squat", 2, "5", 150, 40, rpe, "2-0-1"),
                E("bb_rdl", 2, "6-8", 120, 40, rpe),
                E("db_bench_press", 2, "8-10", 0, 40, rpe, group="S1"),
                E("one_arm_db_row", 2, "8-10/arm", 60, 70, rpe, group="S1"),
                E("pallof_press", 2, "10/side", 60, 50),
            ]
        return [
            E("back_squat", 3, "4-5", 0, 40, rpe, "2-0-1", group="C1",
              notes="Contrast pair — squat, then jumps"),
            E("box_jump", 3, "3", 150, 45, tempo=None, group="C1", contacts=3,
              notes="Contrast pair: 30 s after squat set; max intent, step down"),
            E("bb_rdl", 3, "6-8", 120, 40, rpe, "2-1-1"),
            E("sl_glute_bridge", 2, "10/leg", 60, 70),
            E("db_bench_press", 3, "8-10", 0, 40, rpe, group="S1"),
            E("one_arm_db_row", 3, "8-10/arm", 60, 70, rpe, group="S1"),
            E("pallof_press", 3, "10/side", 60, 50),
        ]
    # block 5 taper
    out = [
        E("back_squat", 2, "4-5", 0, 40, rpe, "2-0-1", group="C1",
          notes="Contrast pair — crisp, no grinding"),
        E("box_jump", 2, "3", 150, 45, group="C1", contacts=3,
          notes="Contrast pair: 30 s after squat set; max intent"),
        E("db_rdl", 2, "6-8", 120, 45, rpe),
    ]
    if w == 17:
        out += [E("db_bench_press", 2, "8-10", 0, 40, rpe, group="S1"),
                E("one_arm_db_row", 2, "8-10/arm", 60, 70, rpe, group="S1")]
    out += [E("sl_balance", 3, "30 s/leg", 30, 70,
              notes="Pad or eyes closed — proprioception density"),
            E("pallof_press", 2, "10/side", 60, 50)]
    return out


def home_A(w):
    b, dl, rpe = block_of(w), w in DELOAD_WEEKS, rpe_for(w)
    if b == 1:
        hold = {1: 30, 2: 35, 3: 40, 4: 30}[w]
        s = 2 if dl else 3
        return [
            E("goblet_squat", s, "10-12", 90, 55, rpe, "3-1-1",
              notes="Heaviest DB; slower tempo offsets lighter load"),
            E("db_rdl", s, "10-12", 90, 50, rpe, "2-1-1"),
            E("box_step_up", 2, "10/leg", 75, 80, rpe, "2-0-1",
              notes="Stair or sturdy step"),
            E("push_up", s, "8-15", 45, 40, rpe),
            E("pallof_press", 2, "12/side", 45, 55,
              notes="Band on door anchor; no anchor -> dead bug 2×8/side"),
            E("wall_sit", s, f"{hold} s", 30, hold, tempo="iso"),
        ]
    if b == 2:
        s = 2 if dl else 3
        return [
            E("goblet_squat", s, "6-8", 105, 45, rpe, "4-0-1",
              notes="Heavy DB, 4 s eccentric = back-squat stand-in"),
            E("db_rdl", s, "8-10", 90, 45, rpe, "2-1-1"),
            E("push_up", s, "8-12", 0, 40, rpe, group="S1",
              notes="Elevate feet when 12 is easy"),
            E("one_arm_db_row", s, "10/arm", 60, 70, rpe, group="S1"),
            E("dead_bug", 2, "8/side", 45, 50),
            E("wall_sit", 2, "45 s", 45, 45, tempo="iso"),
        ]
    if b == 3:
        s = 2 if dl else 3
        return [
            E("goblet_squat", s, "6-8", 105, 45, rpe, "4-0-1", notes="Heavy DB"),
            E("db_rdl", s, "6-8", 90, 45, rpe, "2-1-1"),
            E("sl_glute_bridge", 2, "10/leg", 60, 70),
            E("push_up", s, "8-12", 0, 40, rpe, group="S1",
              notes="Deficit (hands on books) when easy"),
            E("one_arm_db_row", s, "8-10/arm", 60, 70, rpe, group="S1"),
            E("dead_bug", 2, "8/side", 45, 50),
        ]
    if b == 4:
        if dl:
            return [
                E("goblet_squat", 2, "5", 90, 40, rpe, "2-0-1"),
                E("db_rdl", 2, "6-8", 90, 45, rpe),
                E("push_up", 2, "8-12", 45, 40, rpe),
                E("dead_bug", 2, "8/side", 45, 50),
                E("wall_sit", 2, "60 s", 45, 60, tempo="iso"),
            ]
        return [
            E("goblet_squat", 3, "5", 0, 40, rpe, "2-0-1", group="C1",
              notes="Contrast pair — heavy DB, then jumps"),
            E("jump_squat", 3, "3", 120, 45, group="C1", contacts=3,
              notes="Contrast pair: 30 s after squat set; bodyweight, max intent"),
            E("db_rdl", 3, "6-8", 90, 45, rpe, "2-1-1"),
            E("sl_glute_bridge", 2, "10/leg", 60, 70),
            E("push_up", 3, "8-12", 45, 40, rpe),
            E("dead_bug", 2, "8/side", 45, 50),
        ]
    out = [
        E("goblet_squat", 2, "5", 0, 40, rpe, "2-0-1", group="C1",
          notes="Contrast pair — crisp"),
        E("jump_squat", 2, "3", 120, 45, group="C1", contacts=3,
          notes="Contrast pair: 30 s after squat set; max intent"),
        E("db_rdl", 2, "6-8", 90, 45, rpe),
    ]
    if w == 17:
        out.append(E("push_up", 2, "8-12", 45, 40, rpe))
    out += [E("sl_balance", 3, "30 s/leg", 30, 70,
              notes="Pad/pillow or eyes closed"),
            E("dead_bug", 2, "8/side", 45, 50)]
    return out


# ---------------------------------------------------------------------------
# B day — Power + balance.  Jump tables: (exercise, sets, reps, rest, work, contacts/set)
# ---------------------------------------------------------------------------

JUMPS_GYM = {
    1:  [("drop_to_stick", 4, "4", 60, 35, 4), ("pogo_hop", 3, "10", 60, 20, 10), ("broad_jump_stick", 3, "3", 90, 25, 3)],
    2:  [("drop_to_stick", 4, "4", 60, 35, 4), ("pogo_hop", 4, "10", 60, 20, 10), ("broad_jump_stick", 3, "3", 90, 25, 3)],
    3:  [("drop_to_stick", 4, "4", 60, 35, 4), ("pogo_hop", 4, "12", 60, 25, 12), ("broad_jump_stick", 4, "3", 90, 25, 3)],
    4:  [("drop_to_stick", 3, "3", 60, 30, 3), ("pogo_hop", 2, "10", 60, 20, 10), ("broad_jump_stick", 3, "3", 90, 25, 3)],
    5:  [("box_jump", 4, "4", 75, 20, 4), ("pogo_hop", 4, "10", 60, 20, 10), ("drop_to_stick", 3, "4", 60, 35, 4), ("broad_jump_stick", 4, "3", 90, 25, 3)],
    6:  [("box_jump", 4, "4", 75, 20, 4), ("pogo_hop", 5, "10", 60, 20, 10), ("drop_to_stick", 3, "4", 60, 35, 4), ("broad_jump_stick", 4, "3", 90, 25, 3)],
    7:  [("box_jump", 5, "4", 75, 20, 4), ("pogo_hop", 5, "12", 60, 25, 12), ("drop_to_stick", 3, "4", 60, 35, 4), ("broad_jump_stick", 3, "3", 90, 25, 3)],
    8:  [("box_jump", 3, "3", 75, 15, 3), ("pogo_hop", 3, "10", 60, 20, 10), ("broad_jump_stick", 3, "3", 90, 25, 3)],
    9:  [("jump_squat", 4, "5", 90, 20, 5), ("lateral_bound", 4, "3/side", 75, 25, 6), ("pogo_hop", 4, "10", 60, 20, 10), ("box_jump", 4, "4", 75, 20, 4)],
    10: [("jump_squat", 5, "5", 90, 20, 5), ("lateral_bound", 4, "3/side", 75, 25, 6), ("pogo_hop", 4, "10", 60, 20, 10), ("box_jump", 5, "4", 75, 20, 4)],
    11: [("jump_squat", 5, "5", 90, 20, 5), ("lateral_bound", 5, "3/side", 75, 25, 6), ("pogo_hop", 4, "12", 60, 25, 12), ("box_jump", 4, "4", 75, 20, 4)],
    12: [("jump_squat", 3, "4", 90, 15, 4), ("pogo_hop", 3, "10", 60, 20, 10), ("lateral_bound", 3, "3/side", 75, 25, 6)],
    13: [("depth_jump", 4, "4", 90, 20, 4), ("sl_hop_stick", 4, "4/leg", 75, 40, 8), ("lateral_bound", 4, "3/side", 75, 25, 6), ("pogo_hop", 4, "10", 60, 20, 10)],
    14: [("depth_jump", 4, "4", 90, 20, 4), ("sl_hop_stick", 4, "4/leg", 75, 40, 8), ("lateral_bound", 5, "3/side", 75, 25, 6), ("pogo_hop", 4, "10", 60, 20, 10)],
    15: [("depth_jump", 5, "4", 90, 20, 4), ("sl_hop_stick", 4, "4/leg", 75, 40, 8), ("lateral_bound", 5, "3/side", 75, 25, 6), ("pogo_hop", 4, "10", 60, 20, 10)],
    16: [("box_jump", 3, "3", 75, 15, 3), ("sl_hop_stick", 3, "3/leg", 75, 30, 6), ("pogo_hop", 3, "10", 60, 20, 10)],
    17: [("box_jump", 4, "3", 90, 15, 3), ("sl_hop_stick", 3, "4/leg", 75, 40, 8), ("pogo_hop", 3, "10", 60, 20, 10), ("jump_squat", 3, "4", 90, 15, 4)],
    18: [("box_jump", 3, "3", 75, 15, 3), ("sl_hop_stick", 3, "3/leg", 75, 30, 6), ("pogo_hop", 3, "10", 60, 20, 10)],
}

# Home substitutions keep contact counts identical (no box / med ball needed).
HOME_JUMP_SUB = {"drop_to_stick": "snap_down", "depth_jump": "snap_down",
                 "box_jump": "broad_jump_stick"}


def jump_entries(w, loc):
    out = []
    for ex, sets, reps, rest, work, cps in JUMPS_GYM[w]:
        notes = "Max intent, stick every landing; full recovery between sets"
        if loc == "home":
            new = HOME_JUMP_SUB.get(ex, ex)
            if new != ex:
                notes += f" (home swap for {ex.replace('_', ' ')})"
            ex = new
            rest = max(45, rest - 15)
        out.append(E(ex, sets, reps, rest, work, notes=notes, contacts=cps))
    return out


def b_accessories(w, loc):
    b, dl = block_of(w), w in DELOAD_WEEKS
    if loc == "gym":
        if b == 1:
            s = 2 if dl else 3
            return [
                E("mb_rotational_throw", s, "5/side", 60, 40,
                  notes="Full-body rotation — throw hard"),
                E("sl_rdl", s, "6/leg", 60, 70, rpe_for(w), notes="Light DB, slow"),
                E("sl_balance", s, "30 s/leg", 30, 70, notes="Pad, then eyes closed"),
                E("calf_raise", s, "15", 60, 60, rpe_for(w), "2-1-2"),
            ]
        if b == 2:
            s = 2 if dl else 3
            return [E("mb_rotational_throw", s, "5/side", 60, 40),
                    E("sl_rdl", s, "6/leg", 60, 70, rpe_for(w)),
                    E("calf_raise", s, "12", 45, 50, rpe_for(w), "2-1-2")]
        if b == 3:
            s = 3 if w == 9 else 2
            return [E("mb_rotational_throw", s, "5/side", 60, 40),
                    E("sl_rdl", s, "6/leg", 60, 70, rpe_for(w)),
                    E("calf_raise", s, "12", 45, 50, rpe_for(w), "2-1-2")]
        if b == 4:
            out = [E("mb_rotational_throw", 2, "5/side", 60, 40)]
            if w != 15:
                out.append(E("sl_rdl", 2, "6/leg", 60, 70, rpe_for(w)))
            out.append(E("calf_raise", 2, "12", 45, 50, rpe_for(w), "2-1-2"))
            return out
        out = [E("sl_balance", 3, "30 s/leg", 30, 70,
                 notes="Pad + eyes closed — pre-season proprioception")]
        if w == 17:
            out.append(E("mb_rotational_throw", 2, "5/side", 60, 40))
        out.append(E("calf_raise", 2, "12", 45, 50, rpe_for(w), "2-1-2"))
        return out
    # home
    out = [E("band_rotational_chop", 2, "8/side", 45, 45, notes="Fast, athletic stance")]
    if b in (1, 2):
        out.append(E("sl_rdl", 2, "6/leg", 45, 70, rpe_for(w), notes="Bodyweight or light DB"))
    if b == 1 or b == 5:
        out.append(E("sl_balance", 2 if b == 1 else 3, "30 s/leg", 30, 70))
    out.append(E("calf_raise", 2, "15", 45, 60, rpe_for(w), "2-1-2", notes="On stair edge"))
    return out


def gym_B(w):
    return jump_entries(w, "gym") + b_accessories(w, "gym")


def home_B(w):
    return jump_entries(w, "home") + b_accessories(w, "home")


# ---------------------------------------------------------------------------
# C day — quad-endurance circuit + aerobic finisher
# ---------------------------------------------------------------------------

WALL_SIT_C = {1: 30, 2: 35, 3: 40, 4: 25, 5: 45, 6: 50, 7: 60, 8: 40, 9: 65,
              10: 75, 11: 90, 12: 60, 13: 90, 14: 105, 15: 120, 16: 75, 17: 90}


def c_stations(w):
    b = block_of(w)
    ws = WALL_SIT_C[w]
    wall = ("wall_sit", f"{ws} s", ws, "iso", "The 'legs burn out' fix — breathe, stay tall")
    knee_note = "Reduce depth or skip if any knee pain; sub +15 s wall sit"
    if b == 1:
        return [
            ("goblet_squat", "10", 60, "3-0-3", "Continuous tension, no lockout rest"),
            wall,
            ("box_step_up", "8/leg", 60, "2-0-1", ""),
            ("spanish_squat", "12", 50, "3-0-3", "Band behind knees, sit back"),
            ("band_lateral_walk", "10/side", 40, None, ""),
            ("side_plank", "20 s/side", 45, "iso", ""),
        ]
    if b == 2:
        return [
            ("goblet_squat", "8", 55, "3-1-3", ""),
            wall,
            ("eccentric_step_down", "6/leg", 75, "5-0-1", knee_note),
            ("spanish_squat", "12", 60, "3-0-3", ""),
            ("split_squat_iso", "20 s/side", 55, "iso", knee_note),
            ("side_plank", "30 s/side", 65, "iso", ""),
        ]
    if b == 3:
        return [
            ("goblet_squat", "10", 60, "3-0-3", ""),
            wall,
            ("eccentric_step_down", "8/leg", 90, "5-0-1", knee_note),
            ("spanish_squat", "15", 60, "3-0-3", ""),
            ("split_squat_iso", "30 s/side", 75, "iso", knee_note),
            ("band_lateral_walk", "12/side", 45, None, ""),
        ]
    if b == 4:
        return [
            ("goblet_squat", "10", 60, "4-0-1", "Leg-blaster-style eccentric emphasis"),
            wall,
            ("eccentric_step_down", "8/leg", 90, "5-0-1", knee_note),
            ("spanish_squat", "15", 60, "3-0-3", ""),
            ("split_squat_iso", "40 s/side", 95, "iso", knee_note),
            ("calf_raise", "15", 60, "3-0-3", "Slow — toeside-pressure endurance"),
        ]
    return [  # block 5 (W17 only — W18 has no Saturday)
        ("goblet_squat", "8", 55, "3-0-3", "Sharpen, don't bury yourself"),
        wall,
        ("spanish_squat", "12", 50, "3-0-3", ""),
        ("split_squat_iso", "30 s/side", 75, "iso", knee_note),
        ("calf_raise", "12", 50, "3-0-3", ""),
        ("sl_balance", "30 s/leg", 70, None, "Pad or eyes closed"),
    ]


# (finisher_exercise, sets, work_sec, rest_sec, rep_range)
def c_finisher(w, loc):
    b, dl = block_of(w), w in DELOAD_WEEKS
    if loc == "gym":
        if b == 1:
            m = {1: 12, 2: 14, 3: 16, 4: 10}[w]
            return ("bike_z2", 1, m * 60, 0, f"{m} min steady")
        if b == 2:
            m = {5: 16, 6: 18, 7: 20, 8: 12}[w]
            return ("bike_z2", 1, m * 60, 0, f"{m} min steady")
        if b == 3:
            if dl:
                return ("bike_z2", 1, 12 * 60, 0, "12 min steady")
            return ("bike_intervals", 4, 180, 120, "4×3 min hard / 2 min easy")
        if b == 4:
            if dl:
                return ("bike_z2", 1, 10 * 60, 0, "10 min steady")
            return ("bike_intervals", 3, 180, 120, "3×3 min hard / 2 min easy")
        return ("bike_z2", 1, 12 * 60, 0, "12 min steady")
    # home
    if b == 3 and not dl:
        return ("home_intervals", 3, 180, 120, "3×3 min hard / 2 min easy")
    if b == 4 and not dl:
        return ("home_intervals", 2, 180, 120, "2×3 min hard / 2 min easy")
    m = 6 if dl or b == 2 else 8
    return ("home_aerobic_circuit", 1, m * 60, 0, f"{m} min continuous easy pace")


def c_rounds(w, loc):
    dl = w in DELOAD_WEEKS
    if loc == "gym":
        return 2 if (dl or w == 17) else 3
    return 2 if (dl or block_of(w) >= 3 or w == 17) else 3


def c_session(w, loc):
    rounds = c_rounds(w, loc)
    round_rest = 90 if loc == "gym" else 60
    stations = []
    for ex, reps, work, tempo, note in c_stations(w):
        if loc == "home" and ex == "box_step_up":
            note = (note + "; stair or sturdy step").strip("; ")
        stations.append(E(ex, rounds, reps, TRANSITION_SEC, work, tempo=tempo,
                          notes=("Circuit station — " + note).rstrip(" —"),
                          rpe=None))
    fex, fsets, fwork, frest, freps = c_finisher(w, loc)
    z2note = "Conversational pace (Zone 2)" if fsets == 1 else \
        "Hard = RPE 8-9 breathing, easy = spin/march it out"
    stations.append(E(fex, fsets, freps, frest, fwork,
                      notes="Aerobic finisher — " + z2note))
    structure = {"type": "circuit+finisher", "rounds": rounds,
                 "round_rest_sec": round_rest, "transition_sec": TRANSITION_SEC}
    return stations, structure


# ---------------------------------------------------------------------------
# Duration model
# ---------------------------------------------------------------------------

def straight_duration_sec(entries):
    """Sum grouped straight sets; supersets share rest. Last rest is dropped."""
    total, i, last_rest = 0, 0, 0
    while i < len(entries):
        g = entries[i].get("superset_group")
        j = i + 1
        if g:
            while j < len(entries) and entries[j].get("superset_group") == g:
                j += 1
        grp = entries[i:j]
        sets = grp[0]["sets"]
        works = sum(e["work_sec"] for e in grp)
        intra = TRANSITION_SEC * (len(grp) - 1)
        rest = grp[-1]["rest_sec"]
        total += sets * (works + intra + rest)
        last_rest = rest
        i = j
    return total - last_rest


def circuit_duration_sec(entries, structure):
    stations = [e for e in entries if not e["notes"].startswith("Aerobic finisher")]
    fin = [e for e in entries if e["notes"].startswith("Aerobic finisher")][0]
    r = structure["rounds"]
    work = sum(e["work_sec"] for e in stations)
    trans = structure["transition_sec"] * (len(stations) - 1)
    circ = r * (work + trans) + (r - 1) * structure["round_rest_sec"]
    fin_t = fin["sets"] * (fin["work_sec"] + fin["rest_sec"]) - fin["rest_sec"]
    return circ + fin_t


def session_minutes(arch, loc, entries, structure):
    wu, cd = WU_CD[(arch, loc)]
    main = circuit_duration_sec(entries, structure) if structure else \
        straight_duration_sec(entries)
    return round(wu + main / 60 + cd, 1)


# ---------------------------------------------------------------------------
# Build
# ---------------------------------------------------------------------------

BUILDERS = {("A", "gym"): gym_A, ("A", "home"): home_A,
            ("B", "gym"): gym_B, ("B", "home"): home_B}


def build_sessions():
    sessions = []
    for w in range(1, N_WEEKS + 1):
        monday = START + timedelta(days=7 * (w - 1))
        for d in (1, 2, 3):
            day = monday + timedelta(days=DAY_OFFSETS[d])
            if day > PROGRAM_END:
                continue
            arch = ARCHETYPES[d]
            for loc in ("gym", "home"):
                if arch == "C":
                    entries, structure = c_session(w, loc)
                else:
                    entries, structure = BUILDERS[(arch, loc)](w), None
                est = session_minutes(arch, loc, entries, structure)
                cap = 60 if loc == "gym" else 40
                assert est <= cap, f"W{w:02d}D{d} {loc} runs {est} min (cap {cap})"
                notes = []
                if w in DELOAD_WEEKS:
                    notes.append("DELOAD — volume cut ~40%, keep loads where they were")
                if block_of(w) == 5:
                    notes.append("Taper — low volume, maximum crispness")
                if w == 1:
                    notes.append("Baseline week — find loads that leave 3 reps in the tank (RPE 7)")
                sessions.append({
                    "week": w, "block": block_of(w),
                    "session_id": f"W{w:02d}D{d}", "date": day.isoformat(),
                    "archetype": f"{arch} — {ARCH_NAMES[arch]}",
                    "location_variant": loc,
                    "deload": w in DELOAD_WEEKS,
                    "warmup": warmup(arch, loc, block_of(w)),
                    "blocks": entries,
                    "cooldown": cooldown(arch, loc),
                    "session_note": "; ".join(notes),
                    "est_duration_min": est,
                    "jump_contacts": sum(e["sets"] * e["contacts_per_set"] for e in entries),
                    "structure": structure,
                })
    return sessions


def weekly_stats(sessions):
    stats = {}
    for s in (x for x in sessions if x["location_variant"] == "gym"):
        st = stats.setdefault(s["week"], {"sets": 0, "contacts": 0, "block": s["block"],
                                          "deload": s["deload"]})
        st["contacts"] += s["jump_contacts"]
        for e in s["blocks"]:
            if e["exercise_id"] in ("bike_z2", "home_aerobic_circuit"):
                continue
            st["sets"] += e["sets"]
    return stats


def validate(sessions):
    stats = weekly_stats(sessions)
    prev = None
    for w in sorted(stats):
        st = stats[w]
        if prev and not st["deload"] and not prev["deload"] and prev["block"] == st["block"]:
            jump = (st["sets"] - prev["sets"]) / prev["sets"]
            assert jump <= 0.10, f"Week {w}: weekly set volume jumps {jump:.0%} (> 10%)"
            if st["block"] < 5:  # block 5 is the taper — contacts drop by design
                assert st["contacts"] >= prev["contacts"], \
                    f"Week {w}: contacts {st['contacts']} < week {w-1} ({prev['contacts']})"
        prev = st
    ids = {(s["session_id"], s["location_variant"]) for s in sessions}
    n = len({s["session_id"] for s in sessions})
    assert len(ids) == 2 * n, "every session needs exactly gym + home variants"
    # home/gym contact parity so the plyo ramp survives location swaps
    by = {}
    for s in sessions:
        by.setdefault(s["session_id"], {})[s["location_variant"]] = s["jump_contacts"]
    for sid, v in by.items():
        assert v["gym"] == v["home"], f"{sid}: contact mismatch gym {v['gym']} home {v['home']}"
    return stats, n


# ---------------------------------------------------------------------------
# Outputs
# ---------------------------------------------------------------------------

def write_json(sessions, stats, n):
    meta = {
        "name": "Snowboard Pre-Season 2026",
        "start": START.isoformat(), "end": PROGRAM_END.isoformat(),
        "weeks": N_WEEKS, "sessions": n, "records": len(sessions),
        "timezone": TZID, "training_days": ["Mon", "Wed", "Sat"],
        "deload_weeks": sorted(DELOAD_WEEKS),
        "blocks": {"1": "Base (W1-4)", "2": "Strength (W5-8)",
                   "3": "Strength->Power (W9-12)",
                   "4": "Power + quad-endurance peak (W13-16)",
                   "5": "Peak / taper (W17-18)"},
        "progression": ("Double progression: top of rep range on all sets at target RPE "
                        "-> +5 lb lower / +2.5 lb upper next session (or +1 rep / +5 s hold "
                        "where load can't move). RPE cap 8 through Block 1."),
        "weekly_jump_contacts": {str(w): stats[w]["contacts"] for w in sorted(stats)},
    }
    (HERE / "program.json").write_text(
        json.dumps({"meta": meta, "sessions": sessions}, indent=1) + "\n")


def write_csv(sessions):
    cols = ["session_id", "date", "week", "block", "archetype", "location_variant",
            "deload", "slot", "exercise_id", "sets", "rep_range", "target_RPE",
            "rest_sec", "tempo", "superset_group", "notes", "est_duration_min"]
    with open(HERE / "program.csv", "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(cols)
        for s in sessions:
            for i, e in enumerate(s["blocks"], 1):
                wr.writerow([s["session_id"], s["date"], s["week"], s["block"],
                             s["archetype"], s["location_variant"], s["deload"], i,
                             e["exercise_id"], e["sets"], e["rep_range"],
                             e["target_RPE"], e["rest_sec"], e["tempo"],
                             e["superset_group"], e["notes"], s["est_duration_min"]])


VTIMEZONE = """BEGIN:VTIMEZONE
TZID:America/Chicago
BEGIN:DAYLIGHT
TZOFFSETFROM:-0600
TZOFFSETTO:-0500
TZNAME:CDT
DTSTART:19700308T020000
RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU
END:DAYLIGHT
BEGIN:STANDARD
TZOFFSETFROM:-0500
TZOFFSETTO:-0600
TZNAME:CST
DTSTART:19701101T020000
RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU
END:STANDARD
END:VTIMEZONE"""


def ics_escape(text):
    return text.replace("\\", "\\\\").replace(",", "\\,").replace(";", "\\;").replace("\n", "\\n")


def write_ics(sessions):
    links = {}
    link_file = HERE / "notion_links.json"
    if link_file.exists():
        links = json.loads(link_file.read_text())
    gym = [s for s in sessions if s["location_variant"] == "gym"]
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0",
             "PRODID:-//snowboard-preseason//training-plan//EN",
             "CALSCALE:GREGORIAN", "X-WR-CALNAME:Snowboard Pre-Season Training"]
    lines += VTIMEZONE.split("\n")
    stamp = datetime(2026, 8, 3, 12, 0, 0)
    for s in gym:
        d = date.fromisoformat(s["date"])
        dnum = int(s["session_id"][4])
        h, m = SESSION_LOCAL_TIME[dnum]
        start = datetime(d.year, d.month, d.day, h, m)
        dur = max(30, int(-(-s["est_duration_min"] // 5) * 5))
        end = start + timedelta(minutes=dur)
        title = f"W{s['week']:02d} D{dnum} — {s['archetype'].split(' — ')[1]}"
        main = "; ".join(f"{e['exercise_id'].replace('_', ' ')} {e['sets']}×{e['rep_range']}"
                         for e in s["blocks"])
        desc = (f"{s['archetype']} | Block {s['block']}"
                + (" | DELOAD" if s["deload"] else "")
                + f" | gym ≈{s['est_duration_min']} min (home variant ≈"
                + next(str(x['est_duration_min']) for x in sessions
                       if x['session_id'] == s['session_id'] and x['location_variant'] == 'home')
                + f" min)\nMain: {main}")
        url = links.get("session_urls", {}).get(s["session_id"]) or links.get("sessions_db_url")
        if url:
            desc += f"\nNotion: {url}"
        lines += ["BEGIN:VEVENT",
                  f"UID:{s['session_id']}@snowboard-preseason-2026",
                  f"DTSTAMP:{stamp.strftime('%Y%m%dT%H%M%SZ')}",
                  f"DTSTART;TZID={TZID}:{start.strftime('%Y%m%dT%H%M%S')}",
                  f"DTEND;TZID={TZID}:{end.strftime('%Y%m%dT%H%M%S')}",
                  f"SUMMARY:{ics_escape(title)}",
                  f"DESCRIPTION:{ics_escape(desc)}",
                  "END:VEVENT"]
    lines.append("END:VCALENDAR")
    (HERE / "training-plan.ics").write_text("\r\n".join(lines) + "\r\n")


def main():
    sessions = build_sessions()
    stats, n = validate(sessions)
    write_json(sessions, stats, n)
    write_csv(sessions)
    write_ics(sessions)
    gym = [s for s in sessions if s["location_variant"] == "gym"]
    home = [s for s in sessions if s["location_variant"] == "home"]
    print(f"sessions: {n} (records incl. home variants: {len(sessions)})")
    print(f"gym duration  min/max: {min(s['est_duration_min'] for s in gym)} / "
          f"{max(s['est_duration_min'] for s in gym)}")
    print(f"home duration min/max: {min(s['est_duration_min'] for s in home)} / "
          f"{max(s['est_duration_min'] for s in home)}")
    print("week | block | dl | sets | contacts")
    for w in sorted(stats):
        st = stats[w]
        print(f"  W{w:02d} |   {st['block']}   | {'Y' if st['deload'] else ' '} "
              f"| {st['sets']:4d} | {st['contacts']}")


if __name__ == "__main__":
    main()

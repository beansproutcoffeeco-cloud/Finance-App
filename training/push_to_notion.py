#!/usr/bin/env python3
"""Push the training program into Notion. Idempotent — safe to re-run.

Creates (or finds, by title/key) under a parent page:
  - Exercise Library DB  (one page per exercises.json record, video embedded)
  - Sessions DB          (one page per session_id; page body holds BOTH the
                          gym and home prescriptions; Location select records
                          which variant you actually did)
  - Set Log DB           (empty; one row per logged set, related to Session +
                          Exercise, with Location so progression math survives
                          gym<->home swaps)
  - Progression rollups on Exercise Library: PR weight, best e1RM, total sets,
    last-logged date. Set Log rows carry Volume and e1RM formulas.

Usage:
    export NOTION_TOKEN=secret_xxx          # internal integration token
    export NOTION_PARENT_PAGE_ID=xxxx       # page the integration is shared with
    python3 training/push_to_notion.py [--dry-run]

The Notion public API cannot create database *views*; after the first run, add
manually (once): Sessions -> calendar view by Date, and a "This Week" table
filtered to Date is within "this week". Everything else is created here.

After pushing, optionally write training/notion_links.json:
    {"sessions_db_url": "https://www.notion.so/..."}
and re-run generate_program.py so the .ics events link to Notion.
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
API = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

TOKEN = os.environ.get("NOTION_TOKEN")
PARENT = os.environ.get("NOTION_PARENT_PAGE_ID")
DRY = False


def req(method, path, body=None):
    if DRY:
        print(f"[dry-run] {method} {path}")
        return {"id": "dry-run-id", "results": [], "url": ""}
    data = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(f"{API}{path}", data=data, method=method, headers={
        "Authorization": f"Bearer {TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json",
    })
    for attempt in range(5):
        try:
            with urllib.request.urlopen(r) as resp:
                return json.load(resp)
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** attempt)
                continue
            print(f"Notion API error {e.code}: {e.read().decode()[:500]}", file=sys.stderr)
            raise
    raise RuntimeError("Notion API kept failing after retries")


def rt(text):
    return [{"type": "text", "text": {"content": str(text)[:2000]}}]


def find_child_database(title):
    """Find an existing child database of PARENT by exact title (idempotency)."""
    cursor, params = None, ""
    while True:
        resp = req("GET", f"/blocks/{PARENT}/children?page_size=100" + params)
        for b in resp.get("results", []):
            if b.get("type") == "child_database" and \
                    b["child_database"]["title"] == title:
                return b["id"]
        if not resp.get("has_more"):
            return None
        cursor = resp["next_cursor"]
        params = f"&start_cursor={cursor}"


def create_database(title, properties):
    existing = find_child_database(title)
    if existing:
        print(f"  found existing DB: {title}")
        return existing
    resp = req("POST", "/databases", {
        "parent": {"type": "page_id", "page_id": PARENT},
        "title": rt(title), "properties": properties,
    })
    print(f"  created DB: {title}")
    return resp["id"]


def query_by_key(db_id, prop, value):
    resp = req("POST", f"/databases/{db_id}/query", {
        "filter": {"property": prop, "rich_text": {"equals": value}}, "page_size": 1})
    results = resp.get("results", [])
    return results[0]["id"] if results else None


def upsert_page(db_id, key_prop, key_value, properties, children=None):
    page_id = None if DRY else query_by_key(db_id, key_prop, key_value)
    if page_id:
        req("PATCH", f"/pages/{page_id}", {"properties": properties})
        return page_id, False
    body = {"parent": {"database_id": db_id}, "properties": properties}
    if children:
        body["children"] = children[:100]  # API cap per create
    resp = req("POST", "/pages", body)
    return resp["id"], True


# ---------------------------------------------------------------------------


def build_exercise_library():
    props = {
        "Name": {"title": {}},
        "Id": {"rich_text": {}},
        "Category": {"select": {"options": [
            {"name": c} for c in ("strength", "power", "endurance",
                                  "mobility", "balance", "core")]}},
        "Why for Snowboarding": {"rich_text": {}},
        "Home Alternative": {"rich_text": {}},
        "Regression": {"rich_text": {}},
        "Progression": {"rich_text": {}},
        "Video": {"url": {}},
        "Video Backup Query": {"rich_text": {}},
    }
    return create_database("Exercise Library", props)


def push_exercises(db_id, exercises):
    pages = {}
    for ex in exercises:
        props = {
            "Name": {"title": rt(ex["name"])},
            "Id": {"rich_text": rt(ex["id"])},
            "Category": {"select": {"name": ex["category"]}},
            "Why for Snowboarding": {"rich_text": rt(ex["why_for_snowboarding"])},
            "Home Alternative": {"rich_text": rt(ex["home_alternative"])},
            "Regression": {"rich_text": rt(ex["regression"])},
            "Progression": {"rich_text": rt(ex["progression"])},
            "Video": {"url": ex["video_url"]},
            "Video Backup Query": {"rich_text": rt(ex["video_backup_query"])},
        }
        children = [
            {"object": "block", "type": "heading_2",
             "heading_2": {"rich_text": rt("Setup & execution")}},
        ] + [
            {"object": "block", "type": "numbered_list_item",
             "numbered_list_item": {"rich_text": rt(step)}}
            for step in ex["setup_and_execution"]
        ] + [
            {"object": "block", "type": "heading_2",
             "heading_2": {"rich_text": rt("Coaching cues")}},
        ] + [
            {"object": "block", "type": "bulleted_list_item",
             "bulleted_list_item": {"rich_text": rt(c)}} for c in ex["coaching_cues"]
        ] + [
            {"object": "block", "type": "heading_2",
             "heading_2": {"rich_text": rt("Common mistakes")}},
        ] + [
            {"object": "block", "type": "bulleted_list_item",
             "bulleted_list_item": {"rich_text": rt(m)}} for m in ex["common_mistakes"]
        ]
        if ex["video_url"]:
            children.append({"object": "block", "type": "embed",
                             "embed": {"url": ex["video_url"]}})
        page_id, created = upsert_page(db_id, "Id", ex["id"], props, children)
        pages[ex["id"]] = page_id
        print(f"  {'created' if created else 'updated'} exercise: {ex['id']}")
    return pages


def build_sessions_db():
    props = {
        "Name": {"title": {}},
        "Session Id": {"rich_text": {}},
        "Date": {"date": {}},
        "Week": {"number": {}},
        "Block": {"select": {"options": [{"name": f"Block {i}"} for i in range(1, 6)]}},
        "Archetype": {"select": {"options": [
            {"name": "A — Lower Strength + Core"},
            {"name": "B — Power + Balance"},
            {"name": "C — Quad Endurance + Aerobic"}]}},
        "Location": {"select": {"options": [{"name": "Gym"}, {"name": "Home"}]}},
        "Status": {"select": {"options": [
            {"name": "Planned"}, {"name": "Done"}, {"name": "Skipped"}]}},
        "Deload": {"checkbox": {}},
        "Planned Gym Min": {"number": {}},
        "Planned Home Min": {"number": {}},
        "Duration (min)": {"number": {}},
        "Session RPE": {"number": {}},
        "Jump Contacts": {"number": {}},
        "Notes": {"rich_text": {}},
    }
    return create_database("Sessions", props)


def variant_blocks(variant):
    loc = variant["location_variant"]
    head = (f"{loc.capitalize()} — ≈{variant['est_duration_min']} min"
            + (" (circuit)" if variant.get("structure") else ""))
    out = [{"object": "block", "type": "heading_2",
            "heading_2": {"rich_text": rt(head)}},
           {"object": "block", "type": "paragraph",
            "paragraph": {"rich_text": rt("Warmup: " + "; ".join(variant["warmup"]))}}]
    if variant.get("structure"):
        s = variant["structure"]
        out.append({"object": "block", "type": "paragraph", "paragraph": {"rich_text": rt(
            f"Circuit: {s['rounds']} rounds, {s['round_rest_sec']} s between rounds, "
            f"{s['transition_sec']} s between stations")}})
    for e in variant["blocks"]:
        line = f"{e['exercise_id'].replace('_', ' ')} — {e['sets']}×{e['rep_range']}"
        if e["target_RPE"]:
            line += f" @RPE {e['target_RPE']}"
        if e["tempo"]:
            line += f", tempo {e['tempo']}"
        line += f", rest {e['rest_sec']} s"
        if e["superset_group"]:
            line += f" [{'contrast' if e['superset_group'].startswith('C') else 'superset'} {e['superset_group']}]"
        if e["notes"]:
            line += f" — {e['notes']}"
        out.append({"object": "block", "type": "bulleted_list_item",
                    "bulleted_list_item": {"rich_text": rt(line)}})
    out.append({"object": "block", "type": "paragraph",
                "paragraph": {"rich_text": rt("Cooldown: " + "; ".join(variant["cooldown"]))}})
    return out


def push_sessions(db_id, program):
    by_id = {}
    for s in program["sessions"]:
        by_id.setdefault(s["session_id"], {})[s["location_variant"]] = s
    urls = {}
    for sid in sorted(by_id):
        gym, home = by_id[sid]["gym"], by_id[sid]["home"]
        dnum = sid[4]
        title = f"W{gym['week']:02d} D{dnum} — {gym['archetype'].split(' — ')[1]}"
        props = {
            "Name": {"title": rt(title)},
            "Session Id": {"rich_text": rt(sid)},
            "Date": {"date": {"start": gym["date"]}},
            "Week": {"number": gym["week"]},
            "Block": {"select": {"name": f"Block {gym['block']}"}},
            "Archetype": {"select": {"name": gym["archetype"]}},
            "Location": {"select": {"name": "Gym"}},
            "Status": {"select": {"name": "Planned"}},
            "Deload": {"checkbox": gym["deload"]},
            "Planned Gym Min": {"number": gym["est_duration_min"]},
            "Planned Home Min": {"number": home["est_duration_min"]},
            "Jump Contacts": {"number": gym["jump_contacts"]},
            "Notes": {"rich_text": rt(gym["session_note"])},
        }
        children = []
        if gym["session_note"]:
            children.append({"object": "block", "type": "callout", "callout": {
                "rich_text": rt(gym["session_note"]), "icon": {"emoji": "📌"}}})
        children += variant_blocks(gym) + variant_blocks(home)
        page_id, created = upsert_page(db_id, "Session Id", sid, props, children)
        urls[sid] = f"https://www.notion.so/{page_id.replace('-', '')}" if not DRY else ""
        print(f"  {'created' if created else 'updated'} session: {sid}")
    return urls


def build_set_log(sessions_db, exercises_db):
    props = {
        "Name": {"title": {}},
        "Session": {"relation": {"database_id": sessions_db,
                                 "single_property": {}}},
        "Exercise": {"relation": {"database_id": exercises_db,
                                  "single_property": {}}},
        "Set #": {"number": {}},
        "Reps": {"number": {}},
        "Weight": {"number": {}},
        "RPE": {"number": {}},
        "Location": {"select": {"options": [{"name": "Gym"}, {"name": "Home"}]}},
        "Logged": {"created_time": {}},
        "Volume": {"formula": {"expression": 'prop("Reps") * prop("Weight")'}},
        "e1RM": {"formula": {
            "expression": 'prop("Weight") * (1 + prop("Reps") / 30)'}},
    }
    return create_database("Set Log", props)


def add_rollups(exercises_db, sessions_db, setlog_db):
    """Progression rollups. Relation back-references are auto-created by Notion;
    we find their names, then attach rollups."""
    if DRY:
        return
    for db_id, rollups in (
        (exercises_db, {
            "PR Weight": ("Weight", "max"),
            "Best e1RM": ("e1RM", "max"),
            "Total Sets Logged": ("Set #", "count"),
            "Last Logged": ("Logged", "latest_date"),
        }),
        (sessions_db, {
            "Sets Logged": ("Set #", "count"),
            "Session Volume": ("Volume", "sum"),
        }),
    ):
        db = req("GET", f"/databases/{db_id}")
        rel_name = next((name for name, p in db["properties"].items()
                         if p["type"] == "relation"
                         and p["relation"]["database_id"].replace("-", "")
                         == setlog_db.replace("-", "")), None)
        if not rel_name:
            print(f"  WARNING: no back-relation to Set Log on {db_id}; skip rollups")
            continue
        patch = {}
        for roll_name, (target, fn) in rollups.items():
            if roll_name in db["properties"]:
                continue
            patch[roll_name] = {"rollup": {
                "relation_property_name": rel_name,
                "rollup_property_name": target, "function": fn}}
        if patch:
            req("PATCH", f"/databases/{db_id}", {"properties": patch})
            print(f"  rollups added: {', '.join(patch)}")


def main():
    global DRY
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    DRY = ap.parse_args().dry_run
    if not DRY and (not TOKEN or not PARENT):
        sys.exit("Set NOTION_TOKEN and NOTION_PARENT_PAGE_ID (see README.md)")

    program = json.loads((HERE / "program.json").read_text())
    exercises = json.loads((HERE / "exercises.json").read_text())

    print("Exercise Library…")
    ex_db = build_exercise_library()
    push_exercises(ex_db, exercises)
    print("Sessions…")
    sess_db = build_sessions_db()
    session_urls = push_sessions(sess_db, program)
    print("Set Log…")
    log_db = build_set_log(sess_db, ex_db)
    print("Rollups…")
    add_rollups(ex_db, sess_db, log_db)

    if not DRY:
        links = {"sessions_db_url": f"https://www.notion.so/{sess_db.replace('-', '')}",
                 "session_urls": session_urls}
        (HERE / "notion_links.json").write_text(json.dumps(links, indent=1))
        print("Wrote notion_links.json — re-run generate_program.py to put "
              "Notion links into training-plan.ics")
    print("\nManual once-only step (API can't create views): add a Calendar view "
          "by Date and a 'This Week' filtered table to the Sessions DB.")


if __name__ == "__main__":
    main()

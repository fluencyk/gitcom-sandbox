#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
multidays_commit_test.py

Execution + optional git push version.
This version WILL leave real commits on remote GitHub.
"""

from pathlib import Path
from datetime import datetime, timedelta
import subprocess
import random
import os
from core.time_set import time_injection
from core.git_push import git_push

# --------------------------------------------------
# Path configuration
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parents[1]          # gitcom_sandbox/src
SANDBOX_DIR = SRC_DIR.parent                           # gitcom_sandbox
REPO_DIR = SANDBOX_DIR / "gitcom-test"                 # target repo

RES_DIR = SRC_DIR / "res"
SNAP_PATH = RES_DIR / "latest_struct_snap.txt"
STORIES_DIR = RES_DIR / "stories"

# --------------------------------------------------
# Utilities
# --------------------------------------------------

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)

def daterange(start, end):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=1)

def git_commit_with_date(message: str, date_str: str):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = date_str
    env["GIT_COMMITTER_DATE"] = date_str

    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=REPO_DIR,
        env=env,
        check=True
    )

# --------------------------------------------------
# Snap
# --------------------------------------------------

def read_snap():
    paths = []
    with SNAP_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            paths.append(line)
    return paths

def write_snap(paths):
    with SNAP_PATH.open("w", encoding="utf-8") as f:
        f.write("# latest_struct_snap\n")
        f.write("# updated after multidays execution\n\n")
        for p in sorted(paths):
            f.write(f"{p}\n")

# --------------------------------------------------
# Anti-timedox
# --------------------------------------------------

def anti_timedox(existing, actions):
    valid = []
    existing = set(existing)

    for act in actions:
        t = act["type"]

        if t == "add":
            valid.append(act)
            existing.add(act["path"])

        elif t == "rename" and act["target"] in existing:
            valid.append(act)
            existing.remove(act["target"])
            existing.add(act["new_path"])

        elif t == "delete" and act["target"] in existing:
            valid.append(act)
            existing.remove(act["target"])

    return valid

# --------------------------------------------------
# Planning
# --------------------------------------------------

def plan_one_day(date, existing):
    r = random.random()
    actions = []

    if r < 0.5:
        actions.append({
            "type": "add",
            "path": f"src/note_{date.strftime('%m%d')}.md",
            "reason": "exploratory notes"
        })

    elif r < 0.8:
        md_files = [p for p in existing if p.endswith(".md")]
        if md_files:
            target = random.choice(md_files)
            actions.append({
                "type": "rename",
                "target": target,
                "new_path": target.replace(".md", "_v2.md"),
                "reason": "naming refinement"
            })

    else:
        candidates = [p for p in existing if "note" in p]
        if candidates:
            target = random.choice(candidates)
            actions.append({
                "type": "delete",
                "target": target,
                "reason": "temporary cleanup"
            })

    return actions

def plan_multidays(start, end, initial):
    all_days = []
    current = list(initial)

    for d in daterange(start, end):
        raw = plan_one_day(d, current)
        valid = anti_timedox(current, raw)

        for a in valid:
            if a["type"] == "add":
                current.append(a["path"])
            elif a["type"] == "rename":
                current.remove(a["target"])
                current.append(a["new_path"])
            elif a["type"] == "delete":
                current.remove(a["target"])

        all_days.append({
            "date": d,
            "actions": valid
        })

    return all_days

# --------------------------------------------------
# Story
# --------------------------------------------------

def write_story(start, end, initial, days):
    name = f"story_{start:%Y-%m-%d}__{end:%Y-%m-%d}.md"
    path = STORIES_DIR / name

    with path.open("w", encoding="utf-8") as f:
        f.write(f"# Story: {start:%Y-%m-%d} → {end:%Y-%m-%d}\n\n")
        f.write("Repo: gitcom-test\n")
        f.write("Mode: multidays (execution + push)\n")
        f.write("Starting snap: latest_struct_snap.txt\n\n")

        f.write("Initial known structure:\n")
        for p in initial:
            f.write(f"- {p}\n")

        f.write("\n---\n")

        for d in days:
            f.write(f"\n## {d['date']:%Y-%m-%d}\n")
            if not d["actions"]:
                f.write("- (no actions)\n")
            for a in d["actions"]:
                if a["type"] == "add":
                    f.write(f"- add `{a['path']}` — {a['reason']}\n")
                elif a["type"] == "rename":
                    f.write(f"- rename `{a['target']}` → `{a['new_path']}` — {a['reason']}\n")
                elif a["type"] == "delete":
                    f.write(f"- delete `{a['target']}` — {a['reason']}\n")

# --------------------------------------------------
# Execution
# --------------------------------------------------

def execute_actions(days):
    current = read_snap()

    for d in days:
        # 关键：当天的拟真时间（中午，防 UTC 跨日）
        commit_date = d["date"].strftime("%Y-%m-%d 12:00:00")

        for a in d["actions"]:
            if a["type"] == "add":
                p = REPO_DIR / a["path"]
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text(
                    f"# {a['path']}\n\n{a['reason']}\n",
                    encoding="utf-8"
                )
                run(["git", "add", a["path"]], cwd=REPO_DIR)
                git_commit_with_date(
                    f"add {a['path']}",
                    commit_date
                )
                current.append(a["path"])

            elif a["type"] == "rename":
                run(
                    ["git", "mv", a["target"], a["new_path"]],
                    cwd=REPO_DIR
                )
                git_commit_with_date(
                    f"rename {a['target']}",
                    commit_date
                )
                current.remove(a["target"])
                current.append(a["new_path"])

            elif a["type"] == "delete":
                run(
                    ["git", "rm", a["target"]],
                    cwd=REPO_DIR
                )
                git_commit_with_date(
                    f"delete {a['target']}",
                    commit_date
                )
                current.remove(a["target"])

    return current

# --------------------------------------------------
# Entry
# --------------------------------------------------

def run_multidays(start, end, do_push=True):
    initial = read_snap()
    plan = plan_multidays(start, end, initial)
    write_story(start, end, initial, plan)
    final_state = execute_actions(plan)
    write_snap(final_state)

    if do_push:
        git_push(REPO_DIR)

if __name__ == "__main__":
    # === Human-in-the-loop time configuration ===
    start_date, end_date = time_injection()

    print(
        f"[INFO] Multidays time window configured: "
        f"{start_date.date()} → {end_date.date()}"
    )

    run_multidays(
        start_date,
        end_date,
        do_push=True,   # False 可 dry run
    )

    print("[DONE] multidays execution finished")


#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import subprocess
import json
from datetime import datetime, timedelta, timezone

# =========================
# Runtime mode
# =========================
RUN_MODE = "soft_run"
# options: "dry_run", "soft_run", "full_run"

# =========================
# Paths
# =========================

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
RES_DIR = os.path.join(os.path.dirname(CORE_DIR), "res")

# =========================
# Message system
# =========================

from msg.msg_selector import MsgSelector

with open(os.path.join(RES_DIR, "msg_lexicon.json"), "r", encoding="utf-8") as f:
    LEXICON = json.load(f)

MSG_SELECTOR = MsgSelector(LEXICON)

TIMELINE_CTX = {
    "phase_type": "bootstrap",
    "tempo": "steady",
    "self_assessment": "early but promising"
}

# =========================
# Git helpers
# =========================

REMOTE = "origin"


def run(cmd):
    subprocess.run(cmd, check=True)


def inject_commit_time(day):
    dt = datetime.strptime(day, "%Y-%m-%d")
    return dt.replace(
        hour=12, minute=0, second=0,
        tzinfo=timezone.utc
    ).isoformat()


# =========================
# Core simulation
# =========================

def simulate(start_date, end_date):
    day = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    delta = timedelta(days=1)

    while day <= end:
        day_str = day.strftime("%Y-%m-%d")

        # -------------------------
        # Example action
        # (replace with real action logic)
        # -------------------------
        action = {
            "action_type": "edit",
            "target": "README.md"
        }

        # -------------------------
        # Generate commit message
        # -------------------------
        commit_msg = MSG_SELECTOR.generate(action, TIMELINE_CTX)
        commit_time = inject_commit_time(day_str)

        print(f"\n[{day_str}] {commit_msg}")

        if RUN_MODE == "dry_run":
            print("  [DRY-RUN] skip commit & push")

        else:
            run(["git", "add", "-A"])

            run([
                "git", "commit",
                "--allow-empty",
                "-m", commit_msg,
                "--date", commit_time
            ])

            if RUN_MODE == "full_run":
                run(["git", "push", REMOTE, "main"])
            else:
                print("  [SOFT-RUN] commit created locally, push skipped")

        day += delta


# =========================
# Entry
# =========================

if __name__ == "__main__":
    simulate(
        start_date="2022-04-25",
        end_date="2022-04-27"
    )

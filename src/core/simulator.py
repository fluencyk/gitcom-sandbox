#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Simulator main entry (Dry Run / Real Run compatible)

Message semantics (NEW WORLD):
- No default message
- Message ONLY comes from prepared resource (human_said_path)
- Missing message == SILENT (allowed)
"""

import os
import json
import subprocess
from pathlib import Path
from datetime import datetime, timedelta
import random

# ============================================================
# Load repo_config.json
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]   # gitcom_sandbox/
CONFIG_PATH = BASE_DIR / "src" / "res" / "repo_config.json"

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    CONFIG = json.load(f)

# ============================================================
# Basic config
# ============================================================

EXEC_REPO = Path(CONFIG["execution_repo"]["path"])
REPO_STATES = Path(CONFIG["repo_states"]["path"])

TIME_BEGIN = datetime.strptime(CONFIG["time_window"]["begin"], "%Y-%m-%d")
TIME_END = datetime.strptime(CONFIG["time_window"]["end"], "%Y-%m-%d")
INCLUSIVE = CONFIG["time_window"].get("inclusive", True)

TIMEZONE = CONFIG["time_injection"]["timezone"]
HOUR_RANGE = CONFIG["time_injection"]["hour_range"]

# ============================================================
# Message config (NEW)
# ============================================================

msg_cfg = CONFIG.get("message", {})
human_said_path = msg_cfg.get("human_said_path")
allow_silent = msg_cfg.get("allow_silent", False)

HUMAN_SAID_MAP = {}

if human_said_path:
    msg_path = Path(human_said_path)
    if msg_path.exists():
        with open(msg_path, "r", encoding="utf-8") as f:
            HUMAN_SAID_MAP = json.load(f)

# ============================================================
# Utils
# ============================================================

def iter_days(start, end, inclusive=True):
    curr = start
    last = end if inclusive else end - timedelta(days=1)
    while curr <= last:
        yield curr
        curr += timedelta(days=1)


def inject_time(day):
    hour = random.randint(HOUR_RANGE[0], HOUR_RANGE[1])
    minute = random.randint(0, 59)
    second = random.randint(0, 59)
    return f"{day.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:{second:02d} {TIMEZONE}"


def git(cmd, cwd):
    subprocess.run(cmd, cwd=cwd, check=True)


# ============================================================
# Core simulation
# ============================================================

def simulate_day(day):
    date_str = day.strftime("%Y-%m-%d")

    # ---------------------------
    # Message selection (ONLY HERE)
    # ---------------------------
    commit_msg = None  # SILENT by default

    if HUMAN_SAID_MAP:
        commit_msg = HUMAN_SAID_MAP.get(date_str)

    # ---------------------------
    # Dummy file touch (example)
    # ---------------------------
    dummy_file = EXEC_REPO / "README.md"
    if not dummy_file.exists():
        dummy_file.write_text("# Dry Run Repo\n", encoding="utf-8")
    else:
        dummy_file.write_text(
            dummy_file.read_text(encoding="utf-8") + f"\nupdate {date_str}\n",
            encoding="utf-8"
        )

    git(["git", "add", "."], cwd=EXEC_REPO)

    injected_time = inject_time(day)

    # ---------------------------
    # Commit execution
    # ---------------------------
    if commit_msg is None:
        if not allow_silent:
            raise RuntimeError(f"SILENT commit not allowed: {date_str}")

        git(
            ["git", "commit", "--allow-empty-message", "-m", "", "--date", injected_time],
            cwd=EXEC_REPO
        )
    else:
        git(
            ["git", "commit", "-m", commit_msg, "--date", injected_time],
            cwd=EXEC_REPO
        )


def simulate():
    os.chdir(EXEC_REPO)

    for day in iter_days(TIME_BEGIN, TIME_END, INCLUSIVE):
        print(f"\n=== Simulating {day.strftime('%Y-%m-%d')} ===")
        simulate_day(day)


# ============================================================
# Entry
# ============================================================

if __name__ == "__main__":
    simulate()

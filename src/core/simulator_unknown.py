#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import json
import random
from datetime import datetime, timedelta, timezone


# =========================
# Load config
# =========================

CORE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.dirname(CORE_DIR)
RES_DIR = os.path.join(SRC_DIR, "res")
CONFIG_PATH = os.path.join(RES_DIR, "repo_config.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    cfg = json.load(f)

GIT_USER = cfg["git_identity"]["username"]
GIT_EMAIL = cfg["git_identity"]["email"]

REPO_STATES_DIR = cfg["repo_states"]["path"]
EXEC_REPO = cfg["execution_repo"]["path"]
REMOTE = cfg["execution_repo"].get("remote", "origin")

TIME_BEGIN = datetime.fromisoformat(cfg["time_window"]["begin"])
TIME_END = datetime.fromisoformat(cfg["time_window"]["end"])
INCLUSIVE = cfg["time_window"].get("inclusive", True)

TZ_OFFSET = cfg["time_injection"]["timezone"]  # e.g. "-0500"
HOUR_RANGE = cfg["time_injection"]["hour_range"]

COMMIT_MSG = cfg["message"]["default"]


# =========================
# Safety / protection layer
# =========================

# 永远不允许被 repo_states 删除的文件 / 目录
PROTECTED_NAMES = {
    ".git",
    ".gitignore",
    ".github",
}


def is_protected(name: str) -> bool:
    return name in PROTECTED_NAMES


# =========================
# Helpers
# =========================

def run(cmd, cwd=None):
    subprocess.run(cmd, cwd=cwd, check=True)


def inject_commit_time(day: datetime) -> str:
    """
    关键修复点：
    - 固定使用「中午时间」避免 UTC 跨日
    - 不再随机到晚间
    """
    hour = random.randint(11, 15)  # 安全区间
    minute = random.randint(0, 59)
    second = random.randint(0, 59)

    t = day.replace(hour=hour, minute=minute, second=second)
    return t.strftime(f"%Y-%m-%d %H:%M:%S {TZ_OFFSET}")


def apply_repo_state(day_str: str):
    """
    将 repo_states/<day> 覆盖式应用到 execution repo，
    但跳过 PROTECTED_NAMES
    """
    src_dir = os.path.join(REPO_STATES_DIR, day_str)

    if not os.path.isdir(src_dir):
        print(f"[skip] no repo_state for {day_str}")
        return False

    # 删除 execution repo 中的非保护项
    for name in os.listdir(EXEC_REPO):
        if is_protected(name):
            continue
        path = os.path.join(EXEC_REPO, name)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)

    # 拷贝新状态
    for name in os.listdir(src_dir):
        if is_protected(name):
            continue
        src = os.path.join(src_dir, name)
        dst = os.path.join(EXEC_REPO, name)
        if os.path.isdir(src):
            shutil.copytree(src, dst)
        else:
            shutil.copy2(src, dst)

    return True


# =========================
# Main simulation
# =========================

os.chdir(EXEC_REPO)

run(["git", "config", "user.name", GIT_USER])
run(["git", "config", "user.email", GIT_EMAIL])

day = TIME_BEGIN
delta = timedelta(days=1)

while True:
    if day > TIME_END:
        break

    day_str = day.strftime("%Y-%m-%d")
    print(f"\n=== Simulating {day_str} ===")

    changed = apply_repo_state(day_str)

    if not changed:
        day += delta
        continue

    run(["git", "add", "-A"])

    commit_time = inject_commit_time(day)

    run([
        "git", "commit",
        "--allow-empty",
        "-m", COMMIT_MSG,
        "--date", commit_time
    ])

    run(["git", "push", REMOTE, "main"])

    day += delta

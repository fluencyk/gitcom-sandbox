# src/test/oneday_commit_test.py

import sys
import subprocess
from pathlib import Path

# === ensure src/ in PYTHONPATH ===
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from core.identity import assert_identity
from core.time_engine import clear, inject
from mod.file_rename import file_rename


def run_oneday_commit(
    date_str: str,
    message: str,
    allowed_emails=None,
):
    """
    oneday（rename 版）：
    1. identity
    2. time
    3. rename 原子行为
    4. git add / commit / push
    """

    # --- 1. identity ---
    ident = assert_identity(allowed_emails=allowed_emails)
    print(f"[identity] OK: {ident}")

    # --- 2. time ---
    clear()
    inject(date_str)
    print(f"[time] injected: {date_str}")

    repo_root = Path(__file__).resolve().parents[2]

    # --- 3. rename behavior ---
    renamed = file_rename(
        repo_root=repo_root,
        old_relpath="sandbox/add_2022_06_07.txt",
        new_relpath="sandbox/renamed_2022_06_09.txt",
    )
    print(f"[rename] -> {renamed}")

    # --- 4. git ops ---
    def git(cmd):
        subprocess.check_call(cmd, cwd=repo_root)

    git(["git", "add", "-A"])
    git(["git", "commit", "-m", message])
    git(["git", "push"])

    print("[commit] pushed successfully")


if __name__ == "__main__":
    run_oneday_commit(
        date_str="2022-06-09 12:00:00 -0500",
        message="noise: TDD rename oneday backfill for 2022-06-09",
        allowed_emails={"244898831@qq.com"},
    )

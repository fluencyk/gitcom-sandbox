# src/test/oneday_commit_test.py

import sys
import subprocess
from pathlib import Path

# === ensure src in PYTHONPATH ===
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from core.identity import assert_identity
from core.time_engine import clear, inject
from mod.file_delete import file_delete


def run_oneday_commit(
    date_str: str,
    message: str,
    allowed_emails=None,
):
    """
    oneday (delete 版)：
    1) 身份校验
    2) 时间注入
    3) delete 原子行为
    4) git add / commit / push
    """

    # 身份
    ident = assert_identity(allowed_emails=allowed_emails)
    print(f"[identity] OK: {ident}")

    # 时间
    clear()
    inject(date_str)
    print(f"[time] injected: {date_str}")

    repo_root = Path(__file__).resolve().parents[2]

    # delete
    deleted = file_delete(
        repo_root=repo_root,
        relpath="sandbox/renamed_2022_06_09.txt",
    )
    print(f"[delete] removed: {deleted}")

    # git ops
    def git(cmd):
        subprocess.check_call(cmd, cwd=repo_root)

    git(["git", "add", "-A"])
    git(["git", "commit", "-m", message])
    git(["git", "push"])

    print("[commit] pushed successfully")


if __name__ == "__main__":
    run_oneday_commit(
        date_str="2022-06-11 12:00:00 -0500",
        message="noise: TDD delete oneday backfill for 2022-06-11",
        allowed_emails={"244898831@qq.com"},
    )

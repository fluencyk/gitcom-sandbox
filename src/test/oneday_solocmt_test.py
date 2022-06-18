# src/test/oneday_solocmt_test.py

"""
oneday_solocmt_test.py

Integration test:
- Single day
- Single commit
- Real GitHub push
"""

import sys
from pathlib import Path

# --------------------------------------------------
# ensure src in path
# --------------------------------------------------
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

# --------------------------------------------------
# core imports
# --------------------------------------------------
from core.identity import assert_identity
from core.time_set_oneday_test import time_injection_oneday
from core.beh_layout import generate_behavior_layout
from core.solo_cmt_plan import plan_single_commit

from core.git_commit_oneday import git_commit_oneday
print("[debug] git_commit_oneday =", git_commit_oneday)
print("[debug] git_commit_oneday module =", git_commit_oneday.__module__)

from core.git_push_test import git_push_test

# --------------------------------------------------
def report(msg: str):
    print(msg)


def load_latest_struct_snap(path: Path) -> list:
    if not path.exists():
        report(f"[snap] NOT FOUND: {path}")
        return []

    struct = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            struct.append(line)

    report(f"[snap] loaded {len(struct)} structural entries")
    return struct


# --------------------------------------------------
def run_oneday_solocmt():
    report("=== oneday SOLO commit REAL start ===")

    repo_root = Path(__file__).resolve().parents[2]

    # 1. identity guard
    assert_identity(report=report)

    # 2. time injection
    commit_time = time_injection_oneday(
        date_str="2022-06-18",
        tz_offset_hours=0,
        report=report,
    )

    # 3. load snapshot
    snap_struct = load_latest_struct_snap(
        Path("res/latest_struct_snap.txt")
    )
    report(f"[snap] initial struct: {snap_struct}")

    # 4. behavior layout
    behaviors, final_struct = generate_behavior_layout(
        snap_struct=snap_struct,
        report=report,
    )

    report(f"[oneday] behaviors: {behaviors}")
    report(f"[oneday] final struct: {final_struct}")

    # 5. solo commit plan
    commit_batches = plan_single_commit(
        behaviors=behaviors,
        report=report,
    )

    # 6. real git commit (single batch)
    commit_message = (
        f"research(onetime): "
        f"{', '.join(commit_batches[0])}"
    )

    # solo plan gives one batch; use that as the commit's behaviors
    commit_batches = plan_single_commit(
        behaviors=behaviors,
        report=report,
    )

    commit_behaviors = commit_batches[0]          # ← 关键：真正传入 commit 的行为列表
    commit_message = f"oneday research: {', '.join(commit_behaviors)}"

    git_commit_oneday(
        behaviors=commit_behaviors,               # ← 必须有这一行
        commit_time=commit_time,
        message=commit_message,
        repo_root=repo_root,
        report=report,
    )

    # 7. real push (safe wrapper)
    git_push_test(
        repo_root=repo_root,
        report=report,
    )

    report("=== oneday SOLO commit REAL end ===")


# --------------------------------------------------
if __name__ == "__main__":
    run_oneday_solocmt()

# src/test/oneday_mulcmts_test.py

"""
oneday_mulcmts_test.py

Test driver:
- Single day
- FORCE multiple commits
- Print-only (no side effects)

This file is used for manual inspection of multi-commit rhythm.
"""

import sys
from pathlib import Path

# --------------------------------------------------
# ensure src is in PYTHONPATH
# --------------------------------------------------
SRC_ROOT = Path(__file__).resolve().parents[1]
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

# --------------------------------------------------
# core imports
# --------------------------------------------------
from core.beh_layout import generate_behavior_layout
from core.multi_cmt_plan import plan_multiple_commits
from core.git_push_standby import report_push_standby


# --------------------------------------------------
# unified reporter
# --------------------------------------------------
def report(msg: str):
    print(msg)


# --------------------------------------------------
# load latest structure snapshot
# --------------------------------------------------
def load_latest_struct_snap(path: Path) -> list:
    """
    Load latest_struct_snap.txt
    Ignore metadata lines starting with '#'
    """
    if not path.exists():
        report(f"[snap] NOT FOUND: {path}")
        return []

    struct = []
    with path.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            struct.append(line)

    report(f"[snap] loaded {len(struct)} structural entries")
    return struct


# --------------------------------------------------
# main orchestration
# --------------------------------------------------
def run_oneday_mulcmts(
    date_str: str,
    snap_path: Path,
):
    report("=== oneday MULTI commits test start ===")

    # 1. load structure snapshot
    snap_struct = load_latest_struct_snap(snap_path)
    report(f"[snap] initial struct: {snap_struct}")

    # 2. behavior layout
    behaviors, final_struct = generate_behavior_layout(
        snap_struct=snap_struct,
        report=report,
    )

    report(f"[oneday-multi] planned behaviors: {behaviors}")
    report(f"[oneday-multi] final virtual struct: {final_struct}")

    # 3. force multiple commits
    commit_batches = plan_multiple_commits(
        behaviors=behaviors,
        report=report,
    )

    # 4. standby git report
    report_push_standby(
        date=date_str,
        commit_batches=commit_batches,
        final_struct=final_struct,
        report=report,
    )

    report("=== oneday MULTI commits test end ===")


# --------------------------------------------------
# entry
# --------------------------------------------------
if __name__ == "__main__":
    run_oneday_mulcmts(
        date_str="2022-06-18",
        snap_path=Path("res/latest_struct_snap.txt"),
    )

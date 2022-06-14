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
from core.anti_timedox import AntiTimeDox
from core.git_push import git_push

from mod.file_add import file_add
from mod.file_rename import file_rename
from mod.file_delete import file_delete


# ----------------------------
# local reporting helper
# ----------------------------
def report(msg: str):
    print(msg)


# ----------------------------
# snap writer (oneday responsibility)
# ----------------------------
def dump_latest_snap(curr_files):
    """
    Write current structural snapshot to src/res/latest_struct_snap.txt
    """
    res_dir = SRC_ROOT / "res"
    res_dir.mkdir(parents=True, exist_ok=True)

    snap_path = res_dir / "latest_struct_snap.txt"
    snap_path.write_text(
        "\n".join(sorted(curr_files)),
        encoding="utf-8",
    )

    report(f"[snap] written to {snap_path}")


# ----------------------------
# oneday runner
# ----------------------------
def run_oneday_commit(
    date_str: str,
    message: str,
    allowed_emails=None,
):
    report("=== oneday start ===")

    # --- identity ---
    ident = assert_identity(allowed_emails=allowed_emails)
    report(f"[identity] OK: {ident}")

    # --- time ---
    clear()
    inject(date_str)
    report(f"[time] injected: {date_str}")

    repo_root = SRC_ROOT.parent

    # --- anti paradox mechanism ---
    anti = AntiTimeDox(curr_files=[])
    report("[anti_timedox] initialized (empty curr_files)")

    # ==================================================
    # Day behavior (kept simple on purpose)
    # ==================================================
    report("\n[actions] add / rename / delete")

    # add
    if anti.check_add("sandbox/day_2022_06_14.txt"):
        file_add(
            repo_root,
            "sandbox/day_2022_06_14.txt",
            "generated on 2022-06-14\n",
        )
        anti.apply_add("sandbox/day_2022_06_14.txt")
    else:
        report("Paradox happened!")

    # rename (intentional failure-safe example)
    if anti.check_rename("sandbox/x.txt", "sandbox/y.txt"):
        file_rename(repo_root, "sandbox/x.txt", "sandbox/y.txt")
        anti.apply_rename("sandbox/x.txt", "sandbox/y.txt")
    else:
        report("Paradox happened!")

    # delete (intentional failure-safe example)
    if anti.check_delete("sandbox/y.txt"):
        file_delete(repo_root, "sandbox/y.txt")
        anti.apply_delete("sandbox/y.txt")
    else:
        report("Paradox happened!")

    # ==================================================
    # git commit & push
    # ==================================================
    def git(cmd):
        subprocess.check_call(cmd, cwd=repo_root)

    report("\n[git] staging")
    git(["git", "add", "-A"])

    report("[git] committing")
    git(["git", "commit", "-m", message])

    report("[git] pushing")
    git_push(repo_root)

    # ==================================================
    # dump structural snapshot
    # ==================================================
    dump_latest_snap(anti.curr_files)

    report("=== oneday done ===")


# ----------------------------
# entry
# ----------------------------
if __name__ == "__main__":
    run_oneday_commit(
        date_str="2022-06-14 12:00:00 -0500",
        message="noise: oneday snapshot generation (2022-06-14)",
        allowed_emails={"244898831@qq.com"},
    )

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
# oneday runner
# ----------------------------
def run_oneday_commit(
    date_str: str,
    message: str,
    allowed_emails=None,
):
    """
    oneday (improved & locked version)

    Responsibilities:
    - identity validation
    - time injection
    - anti-time-paradox validation
    - orchestration of add / rename / delete
    - real git commit & push

    NOTE:
    - all reporting stays here
    - no logic leakage into mod / core
    """

    report("=== oneday start ===")

    # --- identity ---
    ident = assert_identity(allowed_emails=allowed_emails)
    report(f"[identity] OK: {ident}")

    # --- time ---
    clear()
    inject(date_str)
    report(f"[time] injected: {date_str}")

    repo_root = Path(__file__).resolve().parents[2]

    # --- anti paradox mechanism ---
    anti = AntiTimeDox(curr_files=[])
    report("[anti_timedox] initialized (empty curr_files)")

    # ==================================================
    # Round 1: rename → delete → add
    # ==================================================
    report("\n[Round 1] rename → delete → add")

    if anti.check_rename("a.txt", "b.txt"):
        file_rename(repo_root, "a.txt", "b.txt")
        anti.apply_rename("a.txt", "b.txt")
    else:
        report("Paradox happened!")

    if anti.check_delete("b.txt"):
        file_delete(repo_root, "b.txt")
        anti.apply_delete("b.txt")
    else:
        report("Paradox happened!")

    if anti.check_add("sandbox/a.txt"):
        file_add(repo_root, "sandbox/a.txt", "init a\n")
        anti.apply_add("sandbox/a.txt")
    else:
        report("Paradox happened!")

    # ==================================================
    # Round 2: delete → add → rename
    # ==================================================
    report("\n[Round 2] delete → add → rename")

    if anti.check_delete("c.txt"):
        file_delete(repo_root, "c.txt")
        anti.apply_delete("c.txt")
    else:
        report("Paradox happened!")

    if anti.check_add("sandbox/c.txt"):
        file_add(repo_root, "sandbox/c.txt", "init c\n")
        anti.apply_add("sandbox/c.txt")
    else:
        report("Paradox happened!")

    if anti.check_rename("sandbox/c.txt", "sandbox/d.txt"):
        file_rename(repo_root, "sandbox/c.txt", "sandbox/d.txt")
        anti.apply_rename("sandbox/c.txt", "sandbox/d.txt")
    else:
        report("Paradox happened!")

    # ==================================================
    # Round 3: add → add
    # ==================================================
    report("\n[Round 3] add → add")

    ok = True
    for name in ["sandbox/x.txt", "sandbox/y.txt"]:
        if anti.check_add(name):
            file_add(repo_root, name, f"init {name}\n")
            anti.apply_add(name)
        else:
            report("Paradox happened!")
            ok = False

    if ok:
        report("Okay, passed!")

    # ==================================================
    # Round 4: rename → delete
    # ==================================================
    report("\n[Round 4] rename → delete")

    if anti.check_rename("sandbox/x.txt", "sandbox/z.txt"):
        file_rename(repo_root, "sandbox/x.txt", "sandbox/z.txt")
        anti.apply_rename("sandbox/x.txt", "sandbox/z.txt")
    else:
        report("Paradox happened!")

    if anti.check_delete("sandbox/z.txt"):
        file_delete(repo_root, "sandbox/z.txt")
        anti.apply_delete("sandbox/z.txt")
    else:
        report("Paradox happened!")

    # ==================================================
    # git commit & push
    # ==================================================
    def git(cmd):
        subprocess.check_call(cmd, cwd=repo_root)

    report("\n[git] staging changes")
    git(["git", "add", "-A"])

    report("[git] committing")
    git(["git", "commit", "-m", message])

    report("[git] pushing")
    git_push(repo_root)

    report("=== oneday done ===")


# ----------------------------
# entry
# ----------------------------
if __name__ == "__main__":
    run_oneday_commit(
        date_str="2022-06-13 12:00:00 -0500",
        message="noise: oneday multi-action anti-paradox run (2022-06-13)",
        allowed_emails={"244898831@qq.com"},
    )

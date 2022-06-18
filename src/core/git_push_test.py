# src/core/git_push_test.py

"""
git_push_test.py

Safe / staging variant of git_push.

Design intent:
- Core-level unit (NOT a test harness)
- Based on git_push.py
- Adds explicit logging and safety context
- Used during integration phase
"""

import subprocess
from pathlib import Path


def git_push_test(repo_root: Path, report=print):
    """
    Safe wrapper around real `git push`.

    Parameters
    ----------
    repo_root : Path
        Root directory of the git repository
    report : callable
        Logging function (default: print)
    """

    report("[git_push_test] start real git push")
    report(f"[git_push_test] repo_root = {repo_root}")

    try:
        subprocess.check_call(
            ["git", "push"],
            cwd=repo_root,
        )
        report("[git_push_test] git push SUCCESS")
    except Exception as e:
        report("[git_push_test] git push FAILED")
        report(str(e))
        raise

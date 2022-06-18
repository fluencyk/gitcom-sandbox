# src/core/git_commit_oneday.py

"""
git_commit_oneday.py

Minimal real commit executor for one day / one commit.
"""

import os
import subprocess
from pathlib import Path
from datetime import datetime


def git_commit_oneday(
    behaviors,
    commit_time,
    message=None,
    repo_root=None,
    report=print,
):
    """
    Execute ONE real git commit for a given day.

    Parameters
    ----------
    behaviors : list[str]
        Planned behaviors (for fallback commit message)
    commit_time : datetime
        Commit timestamp (timezone-aware)
    message : str | None
        Explicit commit message (preferred)
    repo_root : Path | None
        Git repo root (default: cwd)
    report : callable
        Logger
    """

    if repo_root is None:
        repo_root = Path.cwd()

    if message is None:
        message = f"oneday research: {', '.join(behaviors)}"

    report("[git_commit_oneday] preparing real commit")
    report(f"[git_commit_oneday] message = {message}")
    report(f"[git_commit_oneday] time = {commit_time.isoformat()}")
    report(f"[git_commit_oneday] repo_root = {repo_root}")

    env = os.environ.copy()
    iso_time = commit_time.isoformat()

    env["GIT_AUTHOR_DATE"] = iso_time
    env["GIT_COMMITTER_DATE"] = iso_time

    subprocess.check_call(
        ["git", "add", "."],
        cwd=repo_root,
        env=env,
    )

    subprocess.check_call(
        ["git", "commit", "-m", message],
        cwd=repo_root,
        env=env,
    )

    report("[git_commit_oneday] commit SUCCESS")

# src/core/commit_executor.py
# --------------------------
# Execute ONE real git commit (physical layer)

import subprocess
import os
import shutil
from datetime import datetime
from typing import List


class CommitExecutionError(Exception):
    pass


def execute_one_commit(
    *,
    repo_path: str,
    username: str,
    email: str,
    base_date: str,
    git_cmd_pack: List[str],
    commit_index: int = 1
) -> None:
    """
    Execute exactly ONE git commit.

    Parameters:
    - repo_path: path to git repository
    - username / email: commit identity
    - base_date: YYYY-MM-DD
    - git_cmd_pack: semantic git commands (from commit_parser)
    - commit_index: nth commit of the day (used for time offset)
    """

    env = os.environ.copy()
    env["GIT_AUTHOR_NAME"] = username
    env["GIT_AUTHOR_EMAIL"] = email
    env["GIT_COMMITTER_NAME"] = username
    env["GIT_COMMITTER_EMAIL"] = email

    commit_time = _build_commit_time(base_date, commit_index)
    env["GIT_AUTHOR_DATE"] = commit_time
    env["GIT_COMMITTER_DATE"] = commit_time

    # 1. Apply semantic commands to working tree
    _apply_git_cmd_pack(repo_path, git_cmd_pack)

    # 2. Stage changes
    _run(["git", "add", "."], cwd=repo_path, env=env)

    # 3. Commit
    message = _build_commit_message(git_cmd_pack)
    _run(
        ["git", "commit", "-m", message],
        cwd=repo_path,
        env=env
    )


# ---------- helpers ----------

def _apply_git_cmd_pack(repo_path: str, git_cmd_pack: List[str]) -> None:
    """
    Apply semantic commands (ADD / EDIT / DELETE) to working tree.
    """
    for cmd in git_cmd_pack:
        action, path = cmd.split(" ", 1)
        full_path = os.path.join(repo_path, path)

        if action == "ADD":
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, "a", encoding="utf-8") as f:
                f.write(f"# created at {datetime.now()}\n")

        elif action == "EDIT":
            with open(full_path, "a", encoding="utf-8") as f:
                f.write(f"# edited at {datetime.now()}\n")

        elif action == "DELETE":
            if os.path.exists(full_path):
                if os.path.isfile(full_path):
                    os.remove(full_path)
                elif os.path.isdir(full_path):
                    shutil.rmtree(full_path)


def _build_commit_time(base_date: str, index: int) -> str:
    """
    Build commit time string with slight offset per commit.
    """
    hour = 10 + index
    return f"{base_date}T{hour:02d}:00:00"


def _build_commit_message(git_cmd_pack: List[str]) -> str:
    """
    Build a simple commit message from semantic commands.
    """
    summary = ", ".join(cmd.split(" ", 1)[0].lower() for cmd in git_cmd_pack)
    return f"research: {summary}"


def _run(cmd, *, cwd, env):
    result = subprocess.run(
        cmd,
        cwd=cwd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    if result.returncode != 0:
        raise CommitExecutionError(result.stderr)

# src/core/commit_executor.py
# --------------------------------------------------
# Git Commit Executor
# --------------------------------------------------

import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

from src.core.msg_lib import MsgLibrary


# --------------------------------------------------
# Msg library (GLOBAL, stable)
# --------------------------------------------------

_MSG_LIB = MsgLibrary(
    Path("src/res/gitcom_msgs.json")
)


# --------------------------------------------------
# Public Entry
# --------------------------------------------------

def execute_one_commit(
    repo_path: Path,
    git_cmd_pack: List[Dict[str, Any]],
    commit_time: datetime,
    commit_index: int,
):
    """
    Execute ONE git commit with a pack of structured file commands.

    Contract:
    - git_cmd_pack must be List[dict]
    - each cmd must contain:
        {
            "type": "add|edit|delete|rename",
            "path": str,
            ...
        }
    """

    _validate_cmd_pack(git_cmd_pack)

    _apply_git_cmd_pack(repo_path, git_cmd_pack)

    commit_msg = _MSG_LIB.pick(commit_index)

    _git_commit(repo_path, commit_msg, commit_time)


# --------------------------------------------------
# Validation (CRITICAL)
# --------------------------------------------------

def _validate_cmd_pack(git_cmd_pack):
    if not isinstance(git_cmd_pack, list):
        raise TypeError(
            f"[executor] git_cmd_pack must be list, got {type(git_cmd_pack)}"
        )

    for i, cmd in enumerate(git_cmd_pack):
        if not isinstance(cmd, dict):
            raise TypeError(
                f"[executor] cmd[{i}] must be dict, got {type(cmd)}: {cmd}"
            )

        if "type" not in cmd:
            raise KeyError(f"[executor] cmd[{i}] missing 'type': {cmd}")

        if cmd["type"] not in {"add", "edit", "delete", "rename"}:
            raise ValueError(
                f"[executor] unknown cmd type: {cmd['type']}"
            )


# --------------------------------------------------
# Apply Commands
# --------------------------------------------------

def _apply_git_cmd_pack(repo_path: Path, git_cmd_pack):
    for cmd in git_cmd_pack:
        _apply_one_cmd(repo_path, cmd)


def _apply_one_cmd(repo_path: Path, cmd: Dict[str, Any]):
    cmd_type = cmd["type"]

    if cmd_type == "add":
        _cmd_add(repo_path, cmd)

    elif cmd_type == "edit":
        _cmd_edit(repo_path, cmd)

    elif cmd_type == "delete":
        _cmd_delete(repo_path, cmd)

    elif cmd_type == "rename":
        _cmd_rename(repo_path, cmd)


# --------------------------------------------------
# Command Implementations
# --------------------------------------------------

def _cmd_add(repo_path: Path, cmd):
    path = cmd["path"]
    full_path = repo_path / path
    full_path.parent.mkdir(parents=True, exist_ok=True)

    if not full_path.exists():
        full_path.write_text("", encoding="utf-8")


def _cmd_edit(repo_path: Path, cmd):
    path = cmd["path"]
    full_path = repo_path / path

    if full_path.exists():
        with open(full_path, "a", encoding="utf-8") as f:
            f.write("\n")


def _cmd_delete(repo_path: Path, cmd):
    path = cmd["path"]
    full_path = repo_path / path

    if full_path.exists() and full_path.is_file():
        full_path.unlink()


def _cmd_rename(repo_path: Path, cmd):
    src = repo_path / cmd["src"]
    dst = repo_path / cmd["dst"]

    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        src.rename(dst)


# --------------------------------------------------
# Git Commit
# --------------------------------------------------

def _git_commit(repo_path: Path, message: str, commit_time: datetime):
    env = os.environ.copy()
    env["GIT_AUTHOR_DATE"] = commit_time.isoformat()
    env["GIT_COMMITTER_DATE"] = commit_time.isoformat()

    subprocess.run(
        ["git", "add", "."],
        cwd=repo_path,
        check=True,
        env=env,
    )

    subprocess.run(
        ["git", "commit", "-m", message],
        cwd=repo_path,
        check=True,
        env=env,
    )

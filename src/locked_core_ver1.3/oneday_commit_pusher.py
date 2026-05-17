"""
oneday_commit_pusher.py

Single-day noise simulation orchestrator.
Executor is atomic; identity is bound here.
"""

from pathlib import Path
from datetime import datetime, timedelta
import subprocess

from src.core.repo_truth import load_head_structure
from src.core.snap_state import load_last_snap, persist_snap
from src.core.day_decision import decide_day_state, decide_commit_mode
from src.core.action_layout import generate_actions
from src.core.anti_timedox import validate_actions
from src.core.commit_parser import parse_actions
from src.core.commit_executor import execute_one_commit
from src.core.commit_prep import prepare_day_context


# --------------------------------------------------
# experimental switch
# --------------------------------------------------

FORCE_WORK = True   # 临时调试用，关掉即可恢复真实 rest 行为


# --------------------------------------------------
# helpers
# --------------------------------------------------

def _ensure_git_identity(repo_path: str, username: str, email: str):
    subprocess.run(
        ["git", "config", "user.name", username],
        cwd=repo_path,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.email", email],
        cwd=repo_path,
        check=True,
    )


def _inject_commit_time(base_date: str, commit_index: int) -> datetime:
    day = datetime.strptime(base_date, "%Y-%m-%d")
    base_time = day.replace(hour=10, minute=30, second=0)
    return base_time + timedelta(minutes=17 * (commit_index - 1))


def _text_cmds_to_structured(cmd_lines: list[str]) -> list[dict]:
    structured = []

    for line in cmd_lines:
        parts = line.strip().split(maxsplit=1)
        if not parts:
            continue

        op = parts[0].lower()
        path = parts[1] if len(parts) > 1 else None

        if op == "add":
            structured.append({"type": "add", "path": path})
        elif op == "delete":
            structured.append({"type": "delete", "path": path})
        elif op == "edit":
            structured.append({"type": "edit", "path": path})
        else:
            raise ValueError(f"Unknown cmd op: {op}")

    return structured


# --------------------------------------------------
# core
# --------------------------------------------------

def run_one_day(
    *,
    repo_path: str,
    identity_file: Path,
    snap_dir: Path,
    input_date: str | None = None,
) -> None:

    # 1. prepare day context
    day_ctx = prepare_day_context(identity_file, input_date)
    print(f"[day] date = {day_ctx.base_date}")

    _ensure_git_identity(repo_path, day_ctx.username, day_ctx.email)

    # 2. repo truth
    truth_paths = load_head_structure(repo_path)
    print(f"[truth] {len(truth_paths)} tracked paths")

    # 3. snap
    last_snap = load_last_snap(snap_dir)
    print(f"[snap] loaded {len(last_snap)} paths")

    # 4. decision
    day_state = decide_day_state()
    print(f"[decision] day_state = {day_state}")

    if day_state == "rest":
        if FORCE_WORK:
            print("[decision] rest OVERRIDDEN → force work")
            day_state = "work"
        else:
            print("[decision] rest day, no commits")
            return

    commit_mode = decide_commit_mode()
    print(f"[decision] commit_mode = {commit_mode}")

    # 5. actions
    actions = generate_actions(list(last_snap))
    print(f"[action] generated {len(actions)} actions")

    valid_actions = validate_actions(
        last_snap=list(last_snap),
        actions=actions,
    )
    print(f"[timedox] {len(valid_actions)} actions survived")

    if not valid_actions:
        print("[day] no valid actions, skip")
        return

    # 6. parse & structure commands
    text_cmds = parse_actions(valid_actions)
    git_cmd_pack = _text_cmds_to_structured(text_cmds)

    # 7. execute commit (single for now)
    commit_index = 1
    commit_time = _inject_commit_time(day_ctx.base_date, commit_index)

    execute_one_commit(
        repo_path=Path(repo_path),
        git_cmd_pack=git_cmd_pack,
        commit_time=commit_time,
        commit_index=commit_index,
    )
    print("[commit] executed 1 commit")

    # 8. update snap
    new_snap = set(last_snap)
    for act in valid_actions:
        if act["type"] == "add":
            new_snap.add(act["path"])
        elif act["type"] == "delete":
            new_snap.discard(act["path"])

    persist_snap(snap_dir, new_snap)
    print(f"[snap] updated to {len(new_snap)} paths")


# --------------------------------------------------
# entry
# --------------------------------------------------

if __name__ == "__main__":
    run_one_day(
        repo_path=".",
        identity_file=Path("src/res/identity.txt"),
        snap_dir=Path("src/res"),
        input_date=None,
    )

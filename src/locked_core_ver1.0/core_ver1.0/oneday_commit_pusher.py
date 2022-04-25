"""
oneday_commit_pusher.py

Single-day noise simulation orchestrator.
Built strictly from existing core modules.
"""

from pathlib import Path

# --- core modules ---
from src.core.repo_truth import load_head_structure
from src.core.snap_state import load_last_snap, persist_snap
from src.core.day_decision import decide_day_state, decide_commit_mode
from src.core.action_layout import generate_actions
from src.core.anti_timedox import validate_actions
from src.core.commit_parser import parse_actions
from src.core.commit_executor import execute_one_commit
from src.core.commit_prep import prepare_day_context


def run_one_day(
    *,
    repo_path: str,
    identity_file: Path,
    snap_dir: Path,
    input_date: str | None = None,
) -> None:
    """
    Run ONE simulated day (noise line).

    Execution pipeline:
        truth -> snap -> day decision -> action gen
        -> anti_timedox -> commit parse -> commit exec -> snap persist
    """

    # --------------------------------------------------
    # 1. Prepare day context (identity + date)
    # --------------------------------------------------
    day_ctx = prepare_day_context(identity_file, input_date)
    print(f"[day] date = {day_ctx.base_date}")

    # --------------------------------------------------
    # 2. Load repo truth (HEAD)
    # --------------------------------------------------
    truth_paths = load_head_structure(repo_path)
    print(f"[truth] {len(truth_paths)} tracked paths")

    # --------------------------------------------------
    # 3. Load last snap (execution memory)
    # --------------------------------------------------
    last_snap = load_last_snap(snap_dir)
    print(f"[snap] loaded {len(last_snap)} paths")

    # --------------------------------------------------
    # 4. Decide day state
    # --------------------------------------------------
    day_state = decide_day_state()
    print(f"[decision] day_state = {day_state}")

    if day_state == "rest":
        print("[decision] rest day, no commits")
        return

    commit_mode = decide_commit_mode()
    print(f"[decision] commit_mode = {commit_mode}")

    # --------------------------------------------------
    # 5. Generate actions (ONE commit only for now)
    # --------------------------------------------------
    actions = generate_actions(list(last_snap))
    print(f"[action] generated {len(actions)} actions")

    # --------------------------------------------------
    # 6. Anti-timedox validation
    # --------------------------------------------------
    valid_actions = validate_actions(
        last_snap=list(last_snap),
        actions=actions,
    )
    print(f"[timedox] {len(valid_actions)} actions survived")

    # --------------------------------------------------
    # 7. Translate actions to semantic git commands
    # --------------------------------------------------
    git_cmd_pack = parse_actions(valid_actions)

    # --------------------------------------------------
    # 8. Execute ONE commit
    # --------------------------------------------------
    execute_one_commit(
        repo_path=repo_path,
        username=day_ctx.username,
        email=day_ctx.email,
        base_date=day_ctx.base_date,
        git_cmd_pack=git_cmd_pack,
        commit_index=1,
    )
    print("[commit] executed 1 commit")

    # --------------------------------------------------
    # 9. Update snap
    # --------------------------------------------------
    new_snap = set(last_snap)
    for act in valid_actions:
        if act["type"] == "add":
            new_snap.add(act["path"])
        elif act["type"] == "delete":
            new_snap.discard(act["path"])

    persist_snap(snap_dir, new_snap)
    print(f"[snap] updated to {len(new_snap)} paths")


# ==================================================
# CLI entry
# ==================================================

if __name__ == "__main__":
    run_one_day(
        repo_path=r"C:\Clouds\OneDrive\__MacWin_Sync\From_Mac_Wkspc\research\gitcom_stories\gitcom-test",
        identity_file=Path("src/res/identity.txt"),
        snap_dir=Path("src/res"),
        input_date=None,  # prompt user
    )

# src/core/multi_cmt_plan.py

"""
multi_cmt_plan.py

Purpose:
- Experimental commit plan
- FORCE behaviors to be split into multiple commits
- Used for manual inspection of multi-commit days
"""

import random

def plan_multiple_commits(
    behaviors: list,
    min_splits: int = 2,
    report=None,
) -> list:
    """
    Force behaviors to be split into multiple commits.

    Strategy:
    - If behavior count < 2 -> fallback to single commit
    - Otherwise -> randomly split into >= min_splits commits

    Parameters
    ----------
    behaviors : list[str]
        Behavior sequence
    min_splits : int
        Minimum number of commits to generate
    report : callable or None

    Returns
    -------
    commit_batches : list[list[str]]
    """

    n = len(behaviors)

    if n < 2:
        if report:
            report("[multi_cmt_plan] behaviors < 2, fallback to single commit")
        return [list(behaviors)]

    # Max possible splits is n (each action its own commit)
    max_splits = min(n, min_splits + 1)

    # Decide actual split count
    split_count = random.randint(min_splits, max_splits)

    if report:
        report(
            f"[multi_cmt_plan] force multi commits: "
            f"{split_count} commits for {n} behaviors"
        )

    # Choose split points
    # e.g. n=5, split_count=3 -> choose 2 cut points
    cut_points = sorted(
        random.sample(range(1, n), split_count - 1)
    )

    commit_batches = []
    prev = 0
    for cp in cut_points + [n]:
        commit_batches.append(behaviors[prev:cp])
        prev = cp

    return commit_batches

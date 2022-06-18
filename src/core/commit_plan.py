# src/core/commit_plan.py
import random

def plan_commits_from_behaviors(
    behaviors,
    threshold_range=(3, 5),
    seed=None,
    report=None,
):
    """
    Input : behaviors -> List[str]
    Output: commit_batches -> List[List[str]]
    """
    if seed is not None:
        random.seed(seed)

    action_count = len(behaviors)
    threshold = random.randint(*threshold_range)

    if report:
        report(
            f"[commit_plan] action_count={action_count}, "
            f"threshold={threshold}"
        )

    # default: single commit
    commit_batches = [behaviors]

    if action_count >= threshold and action_count >= 2:
        trigger_prob = min(
            0.25 + 0.15 * (action_count - threshold + 1),
            0.75,
        )
        roll = random.random()

        if report:
            report(
                f"[commit_plan] trigger_prob={trigger_prob:.2f}, "
                f"roll={roll:.2f}"
            )

        if roll < trigger_prob:
            split_point = random.randint(1, action_count - 1)
            commit_batches = [
                behaviors[:split_point],
                behaviors[split_point:],
            ]

            if report:
                report(
                    f"[commit_plan] split behaviors at index {split_point}"
                )

    if report:
        report(f"[commit_plan] commit_batches={commit_batches}")

    return commit_batches

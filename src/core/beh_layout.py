# src/core/beh_layout.py
import random
from core.anti_timedox import AntiTimeDox

BEHAVIOR_POOL = ["add", "rename", "delete"]

def generate_behavior_layout(
    snap_struct: list,
    min_actions=1,
    max_actions=5,
    seed=None,
    report=None,
):
    """
    Generate a feasible behavior layout for one day.

    This function:
    - OWNS the structure state during planning
    - Uses anti_timedox to avoid paradoxical behaviors

    Parameters
    ----------
    snap_struct : list
        Structure snapshot loaded from latest snap
    min_actions : int
    max_actions : int
    seed : int or None
    report : callable or None

    Returns
    -------
    behaviors : list[str]
        Planned behavior sequence (paradox-free)
    final_struct : list
        Final virtual structure after all behaviors
    """

    if seed is not None:
        random.seed(seed)

    anti = AntiTimeDox()

    # 🔑 beh_layout 接管 snap 状态
    curr_struct = list(snap_struct)

    behaviors = []
    target_len = random.randint(min_actions, max_actions)

    if report:
        report(f"[beh_layout] init struct: {curr_struct}")
        report(f"[beh_layout] target actions: {target_len}")

    attempts = 0
    while len(behaviors) < target_len:
        attempts += 1
        if attempts > target_len * 10:
            # 防止极端死循环
            break

        action = random.choice(BEHAVIOR_POOL)

        if not anti.can_apply(action, curr_struct):
            if report:
                report(
                    f"[beh_layout] skip infeasible action '{action}' "
                    f"under struct {curr_struct}"
                )
            continue

        # 合法行为：接受并推进虚拟结构
        curr_struct = anti.apply_virtual(action, curr_struct)
        behaviors.append(action)

        if report:
            report(
                f"[beh_layout] accept '{action}', "
                f"struct -> {curr_struct}"
            )

    return behaviors, curr_struct

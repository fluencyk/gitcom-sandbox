# src/core/action_layout.py
# ------------------------
# Generate actions for ONE commit only

import random
from typing import List, Dict


Action = Dict[str, str]
# Example:
# {
#   "type": "add" | "edit" | "delete" | "rename",
#   "path": "src/note_0618.md"
# }


def generate_actions(
    last_snap: List[str],
    max_actions: int = 3
) -> List[Action]:
    """
    Generate actions for a single commit.

    Rules:
    - At least one action
    - Action count is small (human-scale)
    - Based on last snapshot state
    """
    if max_actions < 1:
        raise ValueError("max_actions must be >= 1")

    action_count = random.randint(1, max_actions)
    actions: List[Action] = []

    for _ in range(action_count):
        action_type = _choose_action_type(last_snap)
        action = _generate_action(action_type, last_snap)
        actions.append(action)

    return actions


# ---------- helpers ----------

def _choose_action_type(last_snap: List[str]) -> str:
    """
    Choose action type based on current repository state.
    """
    if not last_snap:
        return "add"

    return random.choices(
        population=["add", "edit", "delete"],
        weights=[0.5, 0.35, 0.15],
        k=1
    )[0]


def _generate_action(action_type: str, last_snap: List[str]) -> Action:
    """
    Generate a single action dict.
    """
    if action_type == "add":
        filename = f"note_{random.randint(1000, 9999)}.md"
        return {
            "type": "add",
            "path": f"src/{filename}"
        }

    if action_type == "edit" and last_snap:
        target = random.choice(last_snap)
        return {
            "type": "edit",
            "path": target
        }

    if action_type == "delete" and last_snap:
        target = random.choice(last_snap)
        return {
            "type": "delete",
            "path": target
        }

    # fallback safety
    return {
        "type": "add",
        "path": f"src/note_{random.randint(1000, 9999)}.md"
    }

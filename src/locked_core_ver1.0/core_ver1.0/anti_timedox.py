# src/core/anti_timedox.py
# -----------------------
# Validate actions against last snapshot (anti-paradox mechanism)

from typing import List, Dict


Action = Dict[str, str]


def validate_actions(
    last_snap: List[str],
    actions: List[Action]
) -> List[Action]:
    """
    Validate and sanitize actions to avoid paradoxes.

    Rules enforced:
    - Cannot edit or delete a file that does not exist
    - Duplicate actions on the same path are reduced
    - At least one action must survive
    """
    validated: List[Action] = []
    existing = set(last_snap)
    touched = set()

    for action in actions:
        action_type = action.get("type")
        path = action.get("path")

        if not action_type or not path:
            continue

        # prevent duplicate touches in one commit
        if path in touched:
            continue

        if action_type == "add":
            validated.append(action)
            existing.add(path)
            touched.add(path)

        elif action_type == "edit":
            if path in existing:
                validated.append(action)
                touched.add(path)

        elif action_type == "delete":
            if path in existing:
                validated.append(action)
                existing.remove(path)
                touched.add(path)

    # safety fallback: ensure at least one action
    if not validated:
        validated.append({
            "type": "add",
            "path": "src/fallback_note.md"
        })

    return validated

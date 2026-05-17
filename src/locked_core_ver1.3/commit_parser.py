# src/core/commit_parser.py
# ------------------------
# Translate actions into git command semantics

from typing import List, Dict


Action = Dict[str, str]


def parse_actions(actions: List[Action]) -> List[str]:
    """
    Translate actions into git command descriptions.

    NOTE:
    - This does NOT execute git commands
    - It returns semantic instructions for the executor
    """
    commands: List[str] = []

    for action in actions:
        action_type = action["type"]
        path = action["path"]

        if action_type == "add":
            commands.append(f"ADD {path}")

        elif action_type == "edit":
            commands.append(f"EDIT {path}")

        elif action_type == "delete":
            commands.append(f"DELETE {path}")

    return commands

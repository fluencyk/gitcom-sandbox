# -*- coding: utf-8 -*-
"""
message_preview.py

Isolated preview tool for inspecting how commit messages would look
over a multi-day timeline, WITHOUT executing simulator or git actions.

This script is intentionally placed under src/mock/.
"""

import json
from pathlib import Path
from typing import List, Dict

# ✅ 关键：使用绝对包路径导入
from core.msg.msg_selector import MsgSelector


# ---------- mock input layer ----------

def load_mock_multiday_actions() -> List[Dict]:
    """
    Mocked commit-level actions.
    Replace or extend this when wiring to real repo_states.
    """
    return [
        {
            "date": "2022-04-25",
            "action": {"action_type": "add", "target": "src/core/simulator.py"}
        },
        {
            "date": "2022-04-25",
            "action": {"action_type": "add", "target": "README.md"}
        },
        {
            "date": "2022-04-26",
            "action": {"action_type": "edit", "target": "src/core/simulator.py"}
        },
        {
            "date": "2022-04-26",
            "action": {"action_type": "add", "target": "res/msg_lexicon.json"}
        },
        {
            "date": "2022-04-27",
            "action": {"action_type": "edit", "target": "README.md"}
        }
    ]


def load_timeline_bundle() -> Dict:
    """
    Minimal timeline context.
    Later this can be loaded from a real timeline_bundle.json.
    """
    return {
        "phase_type": "bootstrap",
        "tempo": "steady",
        "self_assessment": "early but promising"
    }


def load_lexicon() -> Dict:
    """
    Load message lexicon from res/.
    Path is resolved relative to src/.
    """
    lexicon_path = Path(__file__).resolve().parents[1] / "res" / "msg_lexicon.json"
    with lexicon_path.open("r", encoding="utf-8") as f:
        return json.load(f)


# ---------- preview core ----------

def preview_messages(
    actions: List[Dict],
    timeline_ctx: Dict,
    selector: MsgSelector
) -> None:
    """
    Print messages grouped by date for human inspection.
    """

    current_date = None

    for entry in actions:
        date = entry["date"]
        action = entry["action"]

        if date != current_date:
            current_date = date
            print(f"\n=== {current_date} ===")

        msg = selector.generate(action, timeline_ctx)
        print(f"- {msg}")


# ---------- main ----------

def main():
    lexicon = load_lexicon()
    selector = MsgSelector(lexicon)

    actions = load_mock_multiday_actions()
    timeline_ctx = load_timeline_bundle()

    preview_messages(actions, timeline_ctx, selector)


if __name__ == "__main__":
    main()

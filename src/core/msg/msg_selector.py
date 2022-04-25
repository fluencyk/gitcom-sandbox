# src/msg/msg_selector.py
# -*- coding: utf-8 -*-

import random
from typing import Dict


class MsgSelector:
    """
    MsgSelector is responsible for translating *already happened*
    commit actions into human-like commit messages.

    It does NOT decide what happened.
    It only decides how a human might casually describe it.
    """

    def __init__(self, lexicon: Dict):
        """
        lexicon: loaded from msg_lexicon.json
        """
        self.lexicon = lexicon

    # -------- public API --------

    def generate(
        self,
        action: Dict,
        timeline_ctx: Dict
    ) -> str:
        """
        Main entry point.

        action example:
        {
            "action_type": "add",
            "target": "src/core/simulator.py"
        }

        timeline_ctx example:
        {
            "phase_type": "bootstrap",
            "tempo": "steady",
            "self_assessment": "early but promising"
        }
        """

        action_type = action.get("action_type")
        target = self._simplify_target(action.get("target", ""))

        # Step 1: select lexical mood
        mood = self._select_mood(timeline_ctx)

        # Step 2: pick verb phrase
        verb = self._pick_verb(action_type, mood)

        # Step 3: optional qualifier
        qualifier = self._pick_qualifier(mood)

        # Step 4: optional filler
        filler = self._pick_filler(mood)

        # Step 5: assemble message
        msg = self._assemble(verb, qualifier, target, filler)

        return msg.strip()

    # -------- internal mechanics --------

    def _select_mood(self, timeline_ctx: Dict) -> str:
        """
        Decide linguistic mood based on research phase and tempo.
        This is NOT sentiment analysis.
        This is phase-aware behavior emulation.
        """
        phase = timeline_ctx.get("phase_type", "generic")
        tempo = timeline_ctx.get("tempo", "normal")

        if phase == "bootstrap":
            return "early"
        if tempo == "fast":
            return "rough"
        if tempo == "slow":
            return "careful"

        return "neutral"

    def _pick_verb(self, action_type: str, mood: str) -> str:
        verbs = self.lexicon["verbs"].get(action_type, [])
        if not verbs:
            return action_type

        return random.choice(verbs)

    def _pick_qualifier(self, mood: str) -> str:
        pool = self.lexicon.get("qualifiers", {}).get(mood, [])
        return random.choice(pool) if pool and random.random() < 0.6 else ""

    def _pick_filler(self, mood: str) -> str:
        fillers = self.lexicon.get("fillers", [])
        return random.choice(fillers) if fillers and random.random() < 0.3 else ""

    def _assemble(self, verb: str, qualifier: str, target: str, filler: str) -> str:
        parts = [verb]

        if qualifier:
            parts.append(qualifier)

        if target:
            parts.append(target)

        msg = " ".join(parts)

        if filler:
            msg = f"{msg} {filler}"

        return msg

    def _simplify_target(self, path: str) -> str:
        """
        Humans rarely write full paths in commit messages.
        """
        if not path:
            return ""

        return path.split("/")[-1]

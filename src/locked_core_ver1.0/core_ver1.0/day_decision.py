# src/core/day_decision.py
# -----------------------
# Decide high-level day behavior (work/rest, commit mode)

import random


def decide_day_state(work_probability: float = 0.85) -> str:
    """
    Decide whether the day is a working day or a rest day.

    Returns:
        "work" or "rest"
    """
    if not 0.0 <= work_probability <= 1.0:
        raise ValueError("work_probability must be between 0 and 1")

    return "work" if random.random() < work_probability else "rest"


def decide_commit_mode(
    multi_commit_probability: float = 0.35
) -> str:
    """
    Decide whether the day uses single-commit or multi-commit mode.

    Returns:
        "single" or "multiple"
    """
    if not 0.0 <= multi_commit_probability <= 1.0:
        raise ValueError("multi_commit_probability must be between 0 and 1")

    return "multiple" if random.random() < multi_commit_probability else "single"

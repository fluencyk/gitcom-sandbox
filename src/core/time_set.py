"""
time_set.py

Human-in-the-loop time configuration for multidays execution.

This module is intentionally minimal.
It only collects and validates a date range,
without modeling rest days or intensity.
"""

from datetime import datetime


def time_injection():
    raw = input(
        "Enter multidays date range "
        "(YYYY-MM-DD__YYYY-MM-DD), e.g. 2022-06-23__2022-06-25:\n> "
    ).strip()

    try:
        start_str, end_str = raw.split("__")
        start_date = datetime.strptime(start_str, "%Y-%m-%d")
        end_date = datetime.strptime(end_str, "%Y-%m-%d")
    except Exception as e:
        raise ValueError(
            "Invalid input format. Expected YYYY-MM-DD__YYYY-MM-DD"
        ) from e

    if end_date < start_date:
        raise ValueError("End date must not be earlier than start date.")

    # === Human confirmation step (HCI safety) ===
    confirm = input(
        f"Confirm date range [{start_str} → {end_str}] ? (y/N): "
    ).strip().lower()

    if confirm != "y":
        raise RuntimeError("Multidays execution cancelled by user.")

    return start_date, end_date

# src/core/commit_prep.py
# -----------------------
# Prepare identity and date context for a single simulated day

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass
class DayContext:
    username: str
    email: str
    base_date: str  # YYYY-MM-DD


# ---------- identity ----------

def load_identity(identity_file: Path) -> tuple[str, str]:
    """
    Load identity from a text file.

    Expected format (identity.txt):
        username=Your Name
        email=you@example.com
    """
    if not identity_file.exists():
        raise FileNotFoundError(f"Identity file not found: {identity_file}")

    username = None
    email = None

    with identity_file.open("r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key == "username":
                username = value
            elif key == "email":
                email = value

    if not username or not email:
        raise ValueError("Identity file must contain username and email")

    return username, email


# ---------- date ----------

def select_date(input_date: str | None = None) -> str:
    """
    Select a target date for simulation.

    - If input_date is provided, validate and return it
    - Otherwise, prompt user input
    """
    if input_date is None:
        input_date = input("Enter target date (YYYY-MM-DD): ").strip()

    try:
        datetime.strptime(input_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("Invalid date format, expected YYYY-MM-DD")

    return input_date


# ---------- context ----------

def prepare_day_context(identity_file: Path, input_date: str | None = None) -> DayContext:
    """
    Prepare and return a DayContext object.
    """
    username, email = load_identity(identity_file)
    base_date = select_date(input_date)

    return DayContext(
        username=username,
        email=email,
        base_date=base_date,
    )

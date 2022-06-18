# src/core/time_set_oneday_test.py

"""
time_set_oneday_test.py

Single-day time injection with optional human input.
Designed for patch-style oneday replay / backfill.
"""

from datetime import datetime, timezone, timedelta


def time_injection_oneday(
    date_str: str | None = None,
    tz_offset_hours: int = 0,
    interactive: bool = True,
    report=None,
):
    """
    Inject a fixed datetime for a single day execution.

    Parameters
    ----------
    date_str : str | None
        Date in 'YYYY-MM-DD' format.
        If None and interactive=True, prompt user.
    tz_offset_hours : int
        Timezone offset in hours (e.g. -5, +8).
    interactive : bool
        Whether to allow human input if date_str is None.
    report : callable or None

    Returns
    -------
    commit_datetime : datetime
        Time-aware datetime for git commit.
    """

    if date_str is None:
        if not interactive:
            raise ValueError(
                "date_str is None and interactive=False"
            )
        date_str = input(
            "Enter commit date (YYYY-MM-DD): "
        ).strip()

    try:
        base_date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError as e:
        raise ValueError(
            f"Invalid date_str: {date_str}, expected YYYY-MM-DD"
        ) from e

    tz = timezone(timedelta(hours=tz_offset_hours))

    # Noon anchor — safest for GitHub visualization
    commit_time = datetime(
        year=base_date.year,
        month=base_date.month,
        day=base_date.day,
        hour=12,
        minute=0,
        second=0,
        tzinfo=tz,
    )

    if report:
        report(
            f"[time_set_oneday] injected time: "
            f"{commit_time.isoformat()}"
        )

    return commit_time

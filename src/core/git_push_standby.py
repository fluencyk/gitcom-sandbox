# src/core/git_push_standby.py

def report_push_standby(
    date: str,
    commit_batches: list,
    final_struct: list,
    report,
):
    report("[git_push_standby] --- audit begin ---")
    report(f"[git_push_standby] date: {date}")
    report(f"[git_push_standby] commits_count: {len(commit_batches)}")

    for idx, batch in enumerate(commit_batches, start=1):
        report(
            f"[git_push_standby] commit #{idx}: "
            f"{len(batch)} actions -> {batch}"
        )

    report(f"[git_push_standby] final_struct_count: {len(final_struct)}")
    report(f"[git_push_standby] final_struct: {final_struct}")
    report("[git_push_standby] --- audit end ---")

from pathlib import Path

# ==================================================
# Snap file path
# ==================================================

SNAP_FILENAME = "latest_struct_snap.txt"


# ==================================================
# Load snap
# ==================================================

def load_last_snap(snap_dir):
    """
    Load last execution snapshot from disk.
    Returns a set of paths.
    """
    snap_path = Path(snap_dir) / SNAP_FILENAME

    if not snap_path.exists():
        print("[snap] NOT FOUND, initialize empty snap")
        return set()

    with open(snap_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    return set(lines)


# ==================================================
# Internal write logic (DO NOT CALL DIRECTLY)
# ==================================================

def _write_latest_struct_snap(snap_dir, snap):
    """
    Internal snap write implementation.
    """
    snap_path = Path(snap_dir) / SNAP_FILENAME

    with open(snap_path, "w", encoding="utf-8") as f:
        for p in sorted(snap):
            f.write(f"{p}\n")


# ==================================================
# Canonical public API (STABLE)
# ==================================================

def persist_snap(snap_dir, snap):
    """
    Canonical snap persistence API.

    This is the ONLY function orchestrators (oneday / multidays)
    should call to write snapshot state.
    """
    _write_latest_struct_snap(snap_dir, snap)

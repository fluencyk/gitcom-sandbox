# src/core/repo_truth.py
# ----------------------
# Read ground-truth repository structure from Git

import subprocess
from typing import List


class RepoTruthError(Exception):
    pass


def load_head_structure(repo_path: str) -> List[str]:
    """
    Load tracked file paths at current HEAD.

    This is the ground-truth structure of the repository,
    independent of any local snapshots or simulation state.

    Returns:
        List of file paths (e.g. ["src/a.py", "README.md"])
    """
    try:
        result = subprocess.run(
            ["git", "ls-tree", "-r", "--name-only", "HEAD"],
            cwd=repo_path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        raise RepoTruthError(
            f"Failed to read repo truth at HEAD:\n{e.stderr}"
        )

    paths = [
        line.strip()
        for line in result.stdout.splitlines()
        if line.strip()
    ]

    return paths

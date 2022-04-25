import subprocess
from pathlib import Path


def push_gitcom_repo(
    *,
    repo_path: str,
    dry_run: bool = False,
) -> None:
    """
    Final pusher: push commits to remote.

    This module is intentionally SIMPLE.
    It assumes commits are already created locally.
    """

    print(f"[pusher] pushing repo at '{repo_path}' ...")

    if dry_run:
        print("[pusher] dry_run=True, skip actual push")
        return

    try:
        subprocess.run(
            ["git", "push"],
            cwd=repo_path,
            check=True,
        )
    except subprocess.CalledProcessError as e:
        print("[pusher] push failed")
        raise e

    print("[pusher] push completed")


# --------------------------------------------------
# Repo path resolver (shared infra)
# --------------------------------------------------

def _resolve_repo_path(
    *,
    repo_name: str,
    repopath_file: Path,
) -> str:
    """
    Resolve repo path from repopath txt file.

    repopath file example:
        [windows]
        gitcom-test=C:\\path\\to\\gitcom-test

        [mac]
        gitcom-test=/Users/xxx/gitcom-test
    """
    if not repopath_file.exists():
        raise FileNotFoundError(f"repopath file not found: {repopath_file}")

    import platform

    system = platform.system().lower()
    if system.startswith("win"):
        section = "[windows]"
    else:
        section = "[mac]"

    current = None
    mapping = {}

    with open(repopath_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("["):
                current = line
                continue
            if current == section and "=" in line:
                k, v = line.split("=", 1)
                mapping[k.strip()] = v.strip()

    if repo_name not in mapping:
        raise KeyError(f"repo '{repo_name}' not found in {section}")

    return mapping[repo_name]

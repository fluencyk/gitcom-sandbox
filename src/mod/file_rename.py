# src/mod/file_rename.py

from pathlib import Path


def file_rename(repo_root: Path, old_relpath: str, new_relpath: str) -> Path:
    """
    最小 rename 原子操作：

    - old_relpath 必须存在
    - new_relpath 必须不存在
    - 只做文件重命名
    """

    src = repo_root / old_relpath
    dst = repo_root / new_relpath

    if not src.exists():
        raise RuntimeError(f"RENAME failed: source missing -> {old_relpath}")

    if dst.exists():
        raise RuntimeError(f"RENAME failed: target exists -> {new_relpath}")

    dst.parent.mkdir(parents=True, exist_ok=True)
    src.rename(dst)

    return dst

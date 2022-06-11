# src/mod/file_delete.py

from pathlib import Path


def file_delete(repo_root: Path, relpath: str) -> Path:
    """
    最小 DELETE 原子操作：

    - repo_root: 仓库根路径
    - relpath:   相对路径删除的对象
    - 文件必须存在且是文件
    - 返回被删除的 Path
    """

    target = repo_root / relpath

    if not target.exists():
        raise RuntimeError(f"DELETE failed: file not found -> {relpath}")

    if target.is_dir():
        raise RuntimeError(f"DELETE failed: target is a directory -> {relpath}")

    target.unlink()

    return target

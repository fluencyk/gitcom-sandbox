# src/mod/file_add.py

from pathlib import Path


def file_add(repo_root: Path, relpath: str, content: str = "") -> Path:
    """
    最小 add 原子操作：

    - repo_root: 仓库根目录（Path）
    - relpath:   相对仓库根的文件路径（str）
    - content:   写入内容（可空）

    约束：
    - 文件必须不存在
    - 只做文件创建 + 写入
    """

    target = repo_root / relpath

    if target.exists():
        raise RuntimeError(f"ADD failed: file already exists -> {relpath}")

    target.parent.mkdir(parents=True, exist_ok=True)

    with target.open("w", encoding="utf-8") as f:
        f.write(content)

    return target

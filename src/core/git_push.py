import subprocess
from pathlib import Path


def git_push(repo_root: Path):
    """
    最小 git push 执行器：
    - 不关心 commit 内容
    - 不关心时间 / 身份
    - 不关心 branch（使用当前）
    """
    subprocess.check_call(
        ["git", "push"],
        cwd=repo_root,
    )

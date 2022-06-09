# src/core/time_engine.py

import os

_AUTHOR = "GIT_AUTHOR_DATE"
_COMMIT = "GIT_COMMITTER_DATE"


def clear():
    """
    清理所有时间戳环境变量，防止历史污染
    """
    os.environ.pop(_AUTHOR, None)
    os.environ.pop(_COMMIT, None)


def inject(timestamp: str):
    """
    注入回溯时间戳
    timestamp 示例：
    "2022-06-05 12:00:00 -0500"
    """
    os.environ[_AUTHOR] = timestamp
    os.environ[_COMMIT] = timestamp


def current():
    """
    读取当前时间戳（用于调试 / 验证）
    """
    return {
        _AUTHOR: os.environ.get(_AUTHOR),
        _COMMIT: os.environ.get(_COMMIT),
    }

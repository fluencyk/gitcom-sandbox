import subprocess


def _git_config(key: str) -> str:
    try:
        return subprocess.check_output(
            ["git", "config", "--get", key],
            stderr=subprocess.DEVNULL,
        ).decode().strip()
    except Exception:
        return ""


def assert_identity(allowed_emails=None, report=None):
    """
    最小身份校验：
    - 必须存在 user.name
    - 必须存在 user.email
    - 若提供 allowed_emails，则 email 必须命中
    """
    name = _git_config("user.name")
    email = _git_config("user.email")

    if report:
        report(f"[identity] name = {name}")
        report(f"[identity] email = {email}")

    if not name or not email:
        raise RuntimeError("Git identity missing: user.name or user.email")

    if allowed_emails and email not in allowed_emails:
        raise RuntimeError(f"Email not allowed: {email}")

    return {
        "name": name,
        "email": email,
    }

# src/core/anti_timedox.py

class AntiTimeDox:
    """
    Anti Time Paradox Mechanism
    维护并校验当前“存在态”的合法性
    """

    def __init__(self, curr_files=None):
        self.curr_files = list(curr_files) if curr_files else []

    def check_add(self, name: str) -> bool:
        return name not in self.curr_files

    def check_rename(self, old: str, new: str) -> bool:
        return old in self.curr_files and new not in self.curr_files

    def check_delete(self, name: str) -> bool:
        return name in self.curr_files

    def apply_add(self, name: str):
        self.curr_files.append(name)

    def apply_rename(self, old: str, new: str):
        self.curr_files.remove(old)
        self.curr_files.append(new)

    def apply_delete(self, name: str):
        self.curr_files.remove(name)

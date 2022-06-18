# src/core/anti_timedox.py

class AntiTimeDox:
    """
    AntiTimeDox (planning mode)

    Role:
    - Structural feasibility checker
    - Stateless with respect to ownership of structure
    """

    def can_apply(self, action: str, struct_state: list) -> bool:
        if action == "add":
            return True

        if action in ("rename", "delete"):
            if not struct_state:
                return False

            # ✨ 新增：保护规则
            candidate = struct_state[-1]

            # 不删 README
            if candidate == "README.md":
                return False

            # 不删目录占位
            if candidate.endswith("/"):
                return False

            return True

        return False


    def apply_virtual(self, action: str, struct_state: list) -> list:
        """
        Apply an action virtually and return a NEW structure state.

        NOTE:
        - This does NOT mutate input struct_state.
        - Caller (beh_layout) owns the returned state.

        Parameters
        ----------
        action : str
        struct_state : list

        Returns
        -------
        list
            Updated structure state
        """
        new_state = list(struct_state)

        if action == "add":
            new_state.append(f"file_{len(new_state)+1}.txt")

        elif action == "rename":
            # rename last file (simplest deterministic choice)
            old = new_state.pop()
            new_state.append(f"renamed_{old}")

        elif action == "delete":
            new_state.pop()

        return new_state

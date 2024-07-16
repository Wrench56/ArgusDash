class Flag:
    def __init__(self, default: bool = True) -> None:
        self._flag = default

    def set(self) -> None:
        self._flag = True

    def reset(self) -> None:
        self._flag = False

    def get(self) -> bool:
        return self._flag

    def __repr__(self) -> str:
        return f'Flag({self._flag})'

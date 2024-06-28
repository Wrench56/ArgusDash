from typing import List

_settings: List[str] = ['E', 'E']


def update_setting(id_: int, value: str) -> bool:
    _settings[id_] = value
    return True


def get_all() -> List[str]:
    return _settings.copy()


def get_setting(id_: int) -> str:
    return _settings[id_]


def get_default() -> List[str]:
    return ["F" for _ in range(len(_settings))]

from typing import Generator, List, Tuple

import logging

from utils.const import PLUGINS_DIR

_PRIORITIES: List[Tuple[str, int]] = []


def fetch_plugins() -> Generator[Tuple[str, int], None, None]:
    with open(f'{PLUGINS_DIR}/priorities.csv', 'r', encoding='utf-8') as f:
        name, priority = f.readline().strip().split(',')
        _PRIORITIES.append((name, int(priority)))
        yield (name, int(priority))
        f.close()


def add_new_plugin(name: str, priority: int) -> None:
    for pp_pair in _PRIORITIES:
        if pp_pair[0] == name:
            return
    _PRIORITIES.append((name, priority))
    _sort_priorities()
    _save_priorities()


def change_plugin_priority(name: str, priority: int) -> None:
    for i, pp_pair in enumerate(_PRIORITIES):
        if pp_pair[0] == name:
            _PRIORITIES[i] = (name, priority)


def remove_plugin(name: str) -> None:
    for i, pp_pair in enumerate(_PRIORITIES):
        if name == pp_pair[0]:
            _PRIORITIES.pop(i)
            _save_priorities()
            return
    logging.warning(f'Plugin "{name}" was not found in the priority list')


def length() -> int:
    return len(_PRIORITIES)


def _save_priorities() -> None:
    with open(f'{PLUGINS_DIR}/priorities.csv', 'w', encoding='utf-8') as f:
        for prio in _PRIORITIES:
            f.write(f'{prio[0]},{prio[1]}\n')
        f.close()


def _sort_priorities() -> None:
    _PRIORITIES.sort(key=lambda o: o[1])

from typing import Dict, List

import logging
from pathlib import Path

from utils.const import WIDGET_CSV_PATH

_WIDGETS: Dict[str, List[str]] = {}


def register(plugin_name: str, path: str) -> None:
    widgets = [
        file.name.replace('.svelte', '')
        for file in Path(path).glob('*.svelte')
        if 'Setting.svelte' not in file.name
    ]

    _WIDGETS[plugin_name] = []
    with open(WIDGET_CSV_PATH, 'a', encoding='utf-8') as f:
        for widget in widgets:
            _WIDGETS[plugin_name].append(widget)
            f.write(f'{plugin_name},{widget}')


def load_all() -> None:
    with open(WIDGET_CSV_PATH, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            plugin, widget = line.strip().split(',', maxsplit=1)
            if _WIDGETS.get(plugin) is None:
                _WIDGETS[plugin] = []
            if widget in _WIDGETS[plugin]:
                continue
            _WIDGETS[plugin].append(widget)
            logging.info(f'Loaded widget "{widget}"')


def get() -> Dict[str, List[str]]:
    return _WIDGETS

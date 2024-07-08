from typing import Optional

import importlib
import logging

from plugins.base_plugin import Plugin
from plugins import priority


def load_all() -> None:
    for plugin_name, prio in priority.fetch_plugins():
        logging.info(f'Loading plugin "{plugin_name}" with priority {prio}')
        plugin = load(plugin_name)
        if plugin is not None:
            plugin.load()


def load(name: str) -> Optional[Plugin]:
    try:
        source = f'plugins.plugins.{name}.backend.main'
        plugin: Plugin = importlib.import_module(source).init()
        return plugin
    except TypeError:
        # Abstract class (Plugin) does not implement methods like load & unload
        logging.error(f'Plugin "{name}" does not implement abstract methods')
    except AttributeError:
        # No init() function
        logging.error(f'Plugin "{name}" does not provide an init() function')
    except ModuleNotFoundError:
        # No such file
        logging.error(f'Plugin "{name}" does not exist')

    return None

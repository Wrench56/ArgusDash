from typing import Dict, Tuple, Optional

import importlib
import logging

from api import expose
from plugins.base_plugin import Plugin
from plugins import priority


_PLUGINS: Dict[str, Plugin] = {}


def load_all() -> None:
    loaded = 0
    for plugin_name, _ in priority.fetch_plugins():
        plugin = load(plugin_name)
        if plugin is not None:
            loaded += 1

    log = f'Loaded {loaded}/{priority.length()} plugins'
    if loaded == priority.length():
        logging.info(log)
        return
    logging.warning(log)


def load(name: str) -> Optional[Plugin]:
    try:
        source = f'plugins.plugins.{name}.backend.main'
        plugin: Plugin = importlib.import_module(source).init()
        if plugin:
            _PLUGINS[name] = plugin
            plugin.load()
            logging.info(f'Loaded plugin "{name}" successfully')
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


def unload(name: str) -> bool:
    plugin = _PLUGINS.get('name')
    if plugin is None:
        logging.warning(f'Plugin "{name}" is not loaded')
        return False
    _PLUGINS[name] = None
    if not plugin.unload():
        logging.error(f'Plugin "{name}" could not be unloaded')
        return False

    # Remove all subscription
    expose.unload_plugin(name)

    logging.info(f'Plugin "{name}" has been unloaded')
    return True


def unload_all() -> bool:
    success = True
    for plugin in _PLUGINS.values():
        if not plugin.unload():
            logging.error(f'Plugin "{plugin.name}" could not be unloaded')
            success = False
        logging.info(f'Plugin "{plugin.name}" has been unloaded')

    _PLUGINS.clear()
    return success


def get_plugin_names() -> Tuple[str, ...]:
    return tuple(_PLUGINS.keys())

from typing import Optional

from plugins import dependencies, handler, priority, unpack, validate
from server import build
from utils.const import PLUGINS_DOWNLOAD

import logging
import tomllib

import requests


def from_url(url: str) -> bool:
    plugin_toml = _download_plugin_toml(url)
    if plugin_toml is None:
        return False

    config = tomllib.loads(plugin_toml)
    if not validate.validate_toml(config):
        return False

    name = config['plugin'].get('name').replace('-', '_')
    handler.unload(name)
    priority.remove_plugin(name)

    zip_url = config['plugin'].get('zip_url')

    try:
        if not _download_plugin_zip(zip_url, name):
            return False
        if not unpack.unzip(name):
            unpack.revert(name)
            return False
        if not unpack.unpack(name, 'Plugin.toml'):
            unpack.revert(name)
            return False
        if not unpack.distribute(name):
            unpack.revert(name)
            return False
        if not dependencies.python(name):
            unpack.revert(name)
            return False
        if not dependencies.node(name):
            unpack.revert(name)
            return False

        build.build_frontend()
    except Exception as e:
        unpack.revert(name)
        raise e

    priority.add_new_plugin(name, 2)
    handler.load(name)
    logging.info(f'Plugin "{name}" installed successfully')
    return True


def _download_plugin_toml(url: str) -> Optional[str]:
    res = requests.get(url, timeout=10)
    if not res.ok:
        logging.error(f'Can\'t download Plugin.toml at "{url}"')
        return None
    return res.text


def _download_plugin_zip(url: str, name: str) -> bool:
    if not url:
        logging.error(f'Invalid url for plugin zip: "{url}"')
        return False
    if not name:
        logging.error('No name defined for plugin')
        return False

    res = requests.get(url, timeout=10)
    if not res.ok:
        logging.error(f'Can\'t download {name}.zip at "{url}"')
        return False

    with open(f'{PLUGINS_DOWNLOAD}/{name}.zip', 'wb') as zip_:
        zip_.write(res.content)
        zip_.close()

    return True

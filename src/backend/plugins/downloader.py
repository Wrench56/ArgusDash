from typing import Optional

from plugins import unpack
from utils.const import PLUGINS_DIR, PLUGINS_DOWNLOAD

from configparser import ConfigParser
import logging

import requests


def from_url(url: str) -> bool:
    plugin_ini = _download_plugin_ini(url)
    if plugin_ini is None:
        return False

    config = ConfigParser()
    config.read_string(plugin_ini)
    name = config['package'].get('name')
    zip_url = config['package'].get('zip_url')

    if not _download_plugin_zip(zip_url, name):
        return False
    if not unpack.unzip(name):
        return False
    if not unpack.unpack(f'{PLUGINS_DIR}/{name}', 'plugin.ini'):
        return False

    return True


def _download_plugin_ini(url: str) -> Optional[str]:
    res = requests.get(url, timeout=10)
    if not res.ok:
        logging.error(f'Can\'t download plugin.ini at "{url}"')
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

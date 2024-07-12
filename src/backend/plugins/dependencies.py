import json
import logging
import os
import subprocess
import sys

from plugins import unpack
from utils import config
from utils.const import FRONTEND_PATH, PLUGINS_DIR


def python(plugin_name: str) -> bool:
    req_path = f'{PLUGINS_DIR}/{plugin_name}/requirements.txt'
    if not os.path.exists(req_path):
        logging.warning(f'"requirements.txt" for plugin "{
            plugin_name}" does not exist')
        return True

    # TODO: Check the returned value
    try:
        subprocess.check_call(
            [sys.executable, '-m', *config.fetch().get('backend').get('install_plugin_deps').split(' '), req_path])
    except Exception as e:
        unpack.revert(plugin_name)
        raise e

    return True


def node(plugin_name: str) -> bool:
    plugin_dir = f'{PLUGINS_DIR}/{plugin_name}'
    if not os.path.exists(f'{plugin_dir}/package.json'):
        logging.warning(f'"package.json" for plugin "{
            plugin_name}" does not exist')
        return True

    if not _merge_dependencies(plugin_dir):
        return False

    # TODO: Check the returned value
    subprocess.check_call(args=config.fetch().get('frontend').get(
        'install').split(' '), cwd=FRONTEND_PATH, shell=True)
    return True


def _merge_dependencies(plugin_dir: str) -> bool:
    with open(f'{plugin_dir}/package.json', 'r', encoding='utf-8') as f:
        source_data = json.load(f)
        plugin_dependencies = source_data.get('dependencies')
        f.close()

    with open(f'{FRONTEND_PATH}/package.json', 'r', encoding='utf-8') as f:
        package_json = json.load(f)
        f.close()
    if package_json.get('dependencies') is None:
        logging.error('Frontend\'s package.json is corrupted')
        return False

    package_json['dependencies'].update(plugin_dependencies)

    with open(f'{FRONTEND_PATH}/package.json', 'w', encoding='utf-8') as f:
        json.dump(package_json, f, indent=2)
        f.write('\n')
        f.close()

    return True

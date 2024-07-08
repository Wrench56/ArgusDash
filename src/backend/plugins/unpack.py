from typing import Optional

from utils.const import (
    FRONTEND_PAGES_DIR,
    FRONTEND_PLUGINS_DIR,
    PLUGINS_DIR,
    PLUGINS_DOWNLOAD,
)

import logging
import os
import shutil
import zipfile


def unzip(name: str) -> bool:
    _clear_prev_installation(name)
    with zipfile.ZipFile(f'{PLUGINS_DOWNLOAD}/{name}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{PLUGINS_DIR}/{name}')

    return True


def _clear_prev_installation(name: str) -> None:
    if os.path.exists(f'{PLUGINS_DIR}/{name}'):
        shutil.rmtree(f'{PLUGINS_DIR}/{name}')


def _find_target_file(root_dir: str, target: str) -> Optional[str]:
    for dirpath, _, filenames in os.walk(root_dir):
        if target in filenames:
            return dirpath
    return None


def _move_contents(target_folder, root_dir) -> bool:
    for item in os.listdir(target_folder):
        source = os.path.join(target_folder, item)
        destination = os.path.join(root_dir, item)
        if os.path.isdir(source):
            shutil.move(source, destination)
        else:
            shutil.move(source, root_dir)

    # Clean up the now empty target_folder
    os.rmdir(target_folder)

    return True


def unpack(plugin_name: str, target: str) -> bool:
    root_dir = f'{PLUGINS_DIR}/{plugin_name}'
    target_folder = _find_target_file(root_dir, target)
    if target_folder:
        logging.info(f'Found {target} in {target_folder}')
        _move_contents(target_folder, root_dir)

        logging.info('Plugin unpacked')
        return True

    logging.error(f'{target} not found in the plugin folder')
    return False


def distribute(plugin_name: str) -> bool:
    # Make sure previous installations are deleted
    _clear_frontend_installation(plugin_name)
    root_dir = f'{PLUGINS_DIR}/{plugin_name}'
    if os.path.exists(f'{root_dir}/frontend'):
        shutil.move(f'{root_dir}/frontend', f'{FRONTEND_PLUGINS_DIR}/{plugin_name}')
    else:
        logging.warning(f'Frontend directorty of plugin "{plugin_name}" does not exist')

    if os.path.exists(f'{root_dir}/pages'):
        shutil.move(f'{root_dir}/pages', f'{FRONTEND_PAGES_DIR}/{plugin_name}')
    else:
        logging.warning(f'Pages directory of plugin "{plugin_name}" does not exist')
    return True


def _clear_frontend_installation(name: str) -> None:
    if os.path.exists(f'{FRONTEND_PLUGINS_DIR}/{name}'):
        shutil.rmtree(f'{FRONTEND_PLUGINS_DIR}/{name}')
    if os.path.exists(f'{FRONTEND_PAGES_DIR}/{name}'):
        shutil.rmtree(f'{FRONTEND_PAGES_DIR}/{name}')

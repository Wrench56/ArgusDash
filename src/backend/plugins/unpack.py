from typing import Optional

from utils.const import PLUGINS_DIR, PLUGINS_DOWNLOAD

import logging
import os
import shutil
import zipfile


def unzip(name: str) -> bool:
    with zipfile.ZipFile(f'{PLUGINS_DOWNLOAD}/{name}.zip', 'r') as zip_ref:
        zip_ref.extractall(f'{PLUGINS_DIR}/{name}')

    return True


def _find_target_file(root_dir: str, target: str) -> Optional[str]:
    for dirpath, _, filenames in os.walk(root_dir):
        if target in filenames:
            return dirpath
    return None


def _move_contents(target_folder, root_dir) -> bool:
    root_parent_folder = os.path.dirname(root_dir)
    for item in os.listdir(target_folder):
        source = os.path.join(target_folder, item)
        destination = os.path.join(root_parent_folder, item)

        if os.path.isdir(source):
            shutil.move(source, destination)
        else:
            shutil.move(source, root_parent_folder)

    # Clean up the now empty target_folder
    os.rmdir(target_folder)

    return True


def unpack(root_dir: str, target: str):
    target_folder = _find_target_file(root_dir, target)
    if target_folder:
        logging.info(f'Found {target} in {target_folder}')
        _move_contents(target_folder, root_dir)

        # Remove the root folder after moving contents
        shutil.rmtree(root_dir)
        logging.info('Plugin unpacked')
    else:
        logging.error(f'{target} not found in the plugin folder')

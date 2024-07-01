from typing import List

import logging

from utils import config

_FILE_OF_FEATURE = {
    'STATUS_IN_SETTINGS': 'routes/setting/+page.svelte'
}


def disable_feature(feature: str) -> None:
    filename = _decode_feature_file(feature)
    if len(filename) == 0:
        return
    lines = _read_file(filename)
    line_num = _find_feature(feature, lines)
    if line_num < 0:
        return
    lines[line_num].replace('-->', '')
    _write_file(filename, lines)


def enable_feature(feature: str) -> None:
    filename = _decode_feature_file(feature)
    if len(filename) == 0:
        return
    lines = _read_file(filename)
    line_num = _find_feature(feature, lines)
    if line_num < 0:
        return
    if lines[-1] != feature[-1]:
        logging.error(f'Corrupted feature definition for feature "{feature}"')
        return
    lines[line_num] += '-->'
    _write_file(filename, lines)


def get_features() -> List[str]:
    return list(_FILE_OF_FEATURE.keys())

def _decode_feature_file(feature: str) -> str:
    filename = _FILE_OF_FEATURE.get(feature)
    if not filename:
        logging.error(f'Non-existing feature: "{feature}"')
        return ""
    path = config.get('frontend').get('path')
    return f'{path}/{filename}'


def _find_feature(feature: str, lines: list) -> int:
    for i, line in enumerate(lines):
        if line.startswith(f'<!--{feature}'):
            return i
    logging.error(f'Couldn\'t find feature definition "{feature}" in file')
    return -1


def _read_file(filename: str) -> list:
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        f.close()
    return lines


def _write_file(filename: str, lines: list) -> None:
    with open(filename, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        f.close()

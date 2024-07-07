from typing import Dict, List, Optional, Tuple

import logging

from utils import config

_FILE_OF_FEATURE: Dict[str, Tuple] = {
    'STATUS_IN_SETTINGS': ('src/routes/settings/+page.svelte', 'src/lib/components/settings/Box.svelte',),
    '!STATUS_IN_SETTINGS': ('src/lib/components/settings/Box.svelte',)
}


def disable_feature(feature: str, _recursive: bool = True) -> None:
    unused_warn = True
    if _recursive:
        enable_feature(f'!{feature}', False)
    filenames = _decode_feature_files(feature)
    if not filenames:
        return
    for filename in filenames:
        lines = _read_file(filename)
        for line_num in _find_html_features(feature, lines):
            lines[line_num] = lines[line_num].replace('-->', '')
            unused_warn = False
        for line_num in _find_css_js_features(feature, lines):
            lines[line_num] = lines[line_num].replace('*/', '')
            unused_warn = False
        if unused_warn:
            logging.warning(f'Couldn\'t find feature "{feature}" in file "{filename}"')
        _write_file(filename, lines)


def enable_feature(feature: str, _recursive: bool = True) -> None:
    def _enable_feature_at(lines: list, line_num: int, feature: str, enable_str: str) -> None:
        if lines[line_num].strip()[-1] != feature[-1]:
            print(lines[line_num])
            print(feature[-1])
            print(lines[line_num])
            logging.error(f'Corrupted feature definition for feature "{feature}"')
            return
        lines[line_num] = lines[line_num].strip()
        lines[line_num] += enable_str

    unused_warn = True
    if _recursive:
        disable_feature(f'!{feature}', False)
    filenames = _decode_feature_files(feature)
    if not filenames:
        return
    for filename in filenames:
        lines = _read_file(filename)
        for line_num in _find_html_features(feature, lines):
            _enable_feature_at(lines, line_num, feature, '-->\n')
            unused_warn = False
        for line_num in _find_css_js_features(feature, lines):
            _enable_feature_at(lines, line_num, feature, '*/\n')
            unused_warn = False
        if unused_warn:
            logging.warning(f'Couldn\'t find feature "{feature}" in file "{filename}"')
        _write_file(filename, lines)


def get_features() -> List[str]:
    return list(_FILE_OF_FEATURE.keys())


def _decode_feature_files(feature: str) -> Optional[List[str]]:
    filenames = _FILE_OF_FEATURE.get(feature)
    if not filenames:
        logging.error(f'Non-existing feature: "{feature}"')
        return None
    path = config.fetch().get('frontend').get('path')
    return [f'{path}/{filename}' for filename in filenames]


def _find_html_features(feature: str, lines: list) -> List[int]:
    return _find_features(lines, f'<!--{feature}')


def _find_css_js_features(feature: str, lines: list) -> List[int]:
    return _find_features(lines, f'/*{feature}')


def _find_features(lines: list, search_for: str) -> List[int]:
    features = []
    for i, line in enumerate(lines):
        if line.strip().startswith(search_for):
            features.append(i)
    return features


def _read_file(filename: str) -> list:
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
            f.close()
        return lines
    except FileNotFoundError:
        logging.error(f'File "{filename}" containing a feature does not exist')
        return []


def _write_file(filename: str, lines: list) -> None:
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.writelines(lines)
            f.close()
    except FileNotFoundError:
        logging.error(f'File "{filename}" containing a feature does not exist')

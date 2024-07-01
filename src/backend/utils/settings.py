from typing import Dict, List, Optional

from utils import feature_build

_settings: Dict[str, str] = {
    'BUILD_MODE': 'E',
    'STATUS_IN_SETTINGS': 'E'
}


def update_setting(id_: str, value: str) -> bool:
    if id_ in feature_build.get_features():
        if value == 'E':
            feature_build.enable_feature(id_)
        else:
            feature_build.disable_feature(id_)
    _settings[id_] = value
    return True


def get_all() -> List[str]:
    return list(_settings.values())


def get_setting(id_: str) -> Optional[str]:
    return _settings.get(id_)


def get_default() -> List[str]:
    return ["F" for _ in range(len(_settings))]

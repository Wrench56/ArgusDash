from configparser import ConfigParser
from typing import Any, Optional
import logging

_config: ConfigParser = ConfigParser()


def load() -> None:
    _config.read('config/config.ini')
    logging.info('Config loaded')


def get(field: str) -> Optional[Any]:
    return _config[field]

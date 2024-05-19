from configparser import ConfigParser
from typing import Any, Optional
import logging

_config: ConfigParser = None

def load() -> None:
    global _config
    
    _config = ConfigParser()
    _config.read('config/config.ini')
    logging.info('Config loaded')

def get(field: str) -> Optional[Any]:
    return _config[field]

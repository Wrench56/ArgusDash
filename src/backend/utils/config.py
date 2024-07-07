import tomllib
from typing import Any, Dict, Optional
import logging


class Wrapper:
    def __init__(self) -> None:
        self.config: Optional[Dict[Any, Any]] = None

    def set(self, config: Dict[Any, Any]) -> None:
        self.config = config

    def get(self) -> Optional[Dict[Any, Any]]:
        return self.config


_config: Wrapper = Wrapper()


def load() -> None:
    with open("config/config.toml", "rb") as f:
        _config.set(tomllib.load(f))
        f.close()
    logging.info('Config loaded')


def fetch() -> Dict[Any, Any]:
    dict_ = _config.get()
    if dict_ is None:
        logging.critical('Config used before being loaded')
        return {}
    return dict_

import logging
import subprocess
from configparser import ConfigParser
from typing import List

import processes


def _load_config() -> List[str]:
    config = ConfigParser()
    config.read('config/config.ini')

    return config


def _start_frontend_build(config: ConfigParser) -> subprocess.Popen:
    return processes.add_subprocess(subprocess.Popen(
        config['frontend']['build'].split(' '),
        cwd=config['frontend'].get('path'),
        stdout=None if config['frontend'].get('show_output') else subprocess.DEVNULL,
        shell=True
    ))


def build_frontend() -> bool:
    logging.info('Loading config.ini')
    config = _load_config()
    logging.info('Starting frontend build')
    proc = _start_frontend_build(config)
    proc.wait()
    logging.info('Frontend build done')
    
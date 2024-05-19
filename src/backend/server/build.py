import logging
import subprocess
from typing import Tuple

from utils import config, perf, processes


def _start_frontend_build() -> Tuple[subprocess.Popen, int]:
    conf = config.get('frontend')
    return processes.add_subprocess(
        subprocess.Popen(
            conf.get('build').split(' '),
            cwd=conf.get('path'),
            stdout=(
                None
                if conf.get('show_output').lower() == 'true'
                else subprocess.DEVNULL
            ),
            shell=True,
        )
    )


def build_frontend() -> bool:
    start = perf.current_time_ms()

    logging.info('Starting frontend build')
    proc, index = _start_frontend_build()
    proc.wait()
    processes.remove_subprocess(index)

    logging.info(f'Frontend built in {perf.current_time_ms() - start}ms')

import logging
import subprocess

from utils import perf, config

import utils.processes as processes


def _start_frontend_build() -> subprocess.Popen:
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
            shell=True
        )
    )


def build_frontend() -> bool:
    start = perf.current_time_ms()

    logging.info('Starting frontend build')
    proc = _start_frontend_build()
    proc.wait()

    logging.info(f'Frontend built in {perf.current_time_ms() - start}ms')

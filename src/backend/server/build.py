from typing import Tuple

import logging
import subprocess

from pathlib import Path
from utils import config, perf, processes


def _start_frontend_build() -> subprocess.Popen:
    conf = config.fetch().get('frontend')
    return processes.add_subprocess(
        subprocess.Popen(
            conf.get('build').split(' '),
            cwd=conf.get('path'),
            stdout=(
                None
                if conf.get('show_output')
                else subprocess.DEVNULL
            ),
            shell=True,
        )
    )


def build_frontend() -> int:
    start = perf.current_time_ms()

    logging.info('Starting frontend build')
    proc = _start_frontend_build()
    proc.wait()
    processes.remove_subprocess(proc)

    build_time = perf.current_time_ms() - start
    logging.info(f'Frontend built in {build_time}ms')

    return build_time


def get_frontend_size() -> Tuple[float, str]:
    root_directory = Path(config.fetch().get('frontend').get('build_path'))
    return _format_units(
        sum(f.stat().st_size for f in root_directory.glob('**/*') if f.is_file())
    )


def _format_units(num_bytes: int) -> Tuple[float, str]:
    if num_bytes > 1024*1024*1024:
        return round(num_bytes / (1024*1024*1024), 2), 'GB'
    if num_bytes > 1024*1024:
        return round(num_bytes / (1024*1024), 2), 'MB'
    if num_bytes > 1024:
        return round(num_bytes / 1024, 2), "KB"
    return num_bytes, "B"

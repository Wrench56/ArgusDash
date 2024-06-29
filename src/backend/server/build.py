import logging
import subprocess

from utils import config, perf, processes


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

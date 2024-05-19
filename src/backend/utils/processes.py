import logging
import subprocess
from typing import List

_processes: List[subprocess.Popen] = []


def add_subprocess(subproc: subprocess.Popen) -> subprocess.Popen:
    logging.info(f'Subprocess "{subproc}" created')
    _processes.append(subproc)
    return subproc


def terminate_subprocesses() -> None:
    for subproc in _processes:
        logging.info(f'Terminating "{subproc}"')
        subproc.terminate()
        subproc.wait()

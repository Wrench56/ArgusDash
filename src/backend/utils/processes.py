import logging
import subprocess
from collections import deque
from typing import Deque

_processes: Deque[subprocess.Popen] = deque()


def add_subprocess(subproc: subprocess.Popen) -> subprocess.Popen:
    logging.info(f'Subprocess "{subproc}" created')
    _processes.append(subproc)
    return subproc


def remove_subprocess(subproc: subprocess.Popen) -> None:
    _processes.remove(subproc)


def terminate_subprocesses() -> None:
    for subproc in _processes:
        logging.info(f'Terminating "{subproc}"')
        subproc.terminate()
        subproc.wait()

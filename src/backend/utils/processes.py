import logging
import subprocess
from collections import deque
from typing import Deque, Tuple

_processes: Deque[subprocess.Popen] = deque()


def add_subprocess(subproc: subprocess.Popen) -> Tuple[subprocess.Popen, int]:
    logging.info(f'Subprocess "{subproc}" created')
    _processes.append(subproc)
    return (subproc, len(_processes) - 1)


def remove_subprocess(index: int) -> None:
    logging.info(f"Removing subprocess")
    if len(_processes) - 1 == index:
        _processes.pop()
        return

    _processes.remove(_processes[index])


def terminate_subprocesses() -> None:
    for subproc in _processes:
        logging.info(f'Terminating "{subproc}"')
        subproc.terminate()
        subproc.wait()

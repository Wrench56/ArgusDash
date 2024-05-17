from typing import List

import subprocess

_processes: List[subprocess.Popen] = []
def add_subprocess(subproc: subprocess.Popen) -> subprocess.Popen:
    _processes.append(subproc)
    return subproc

def terminate_subprocesses() -> None:
    for subproc in _processes:
        subproc.terminate()
        subproc.wait()

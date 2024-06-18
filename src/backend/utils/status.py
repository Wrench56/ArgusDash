import subprocess
import sys

from typing import Dict, Optional
from utils import config, processes

_status: Dict[str, str] = {}


def get() -> Dict[str, str]:
    return _status


def update() -> None:
    cwd = config.get('frontend').get('path')
    stdout = None if config.get('status').get('show_output').lower() == 'true' else subprocess.DEVNULL
    disabled = tuple(map(str.strip, config.get('status').get('disable_statuses').split(',')))

    if 'npm_doct' not in disabled:
        _status['npm_doct'] = _run_npm_doctor(cwd, stdout)
    if 'ncu' not in disabled:
        _status['ncu'] = _run_ncu(cwd, stdout)
    if 'version' not in disabled:
        _status['version'] = 'wait'
    if 'npm_audit' not in disabled:
        _status['npm_audit'] = _run_npm_audit(cwd, stdout)


def _run_npm_doctor(cwd: str, stdout: Optional[int]) -> str:
    proc = processes.add_subprocess(
        subprocess.Popen(
            (
                'npm',
                'doctor',
            ),
            cwd=cwd,
            stdout=stdout,
            stderr=stdout,
            shell=True,
        )
    )
    proc.wait(timeout=15)
    processes.remove_subprocess(proc)

    return ' ok ' if proc.returncode == 0 else 'fail'


def _run_ncu(cwd: str, stdout: Optional[int]) -> str:
    proc = processes.add_subprocess(
        subprocess.Popen(
            (
                'npm',
                'exec',
                'npm-check-updates',
            ),
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=stdout,
            shell=True,
        )
    )
    proc.wait(timeout=15)
    stdout_string = proc.stdout.read().decode()
    if stdout is not subprocess.DEVNULL:
        sys.stdout.write(stdout_string)
    processes.remove_subprocess(proc)
    if 'All dependencies match the latest' in stdout_string:
        return ' ok '
    return 'fail'


def _run_npm_audit(cwd: str, stdout: Optional[int]) -> str:
    proc = processes.add_subprocess(
        subprocess.Popen(
            (
                'npm',
                'audit',
            ),
            cwd=cwd,
            stdout=stdout,
            stderr=stdout,
            shell=True,
        )
    )
    proc.wait(timeout=15)
    processes.remove_subprocess(proc)

    return ' ok ' if proc.returncode == 0 else 'fail'

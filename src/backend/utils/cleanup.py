from types import FrameType
from typing import Optional

import logging
import signal
import threading
import sys

from utils import flag, processes

_SHUTDOWN_FLAG = flag.Flag(False)
_HANDLERS = {}


def _timeout() -> None:
    logging.error('Graceful cleanup timeout! Shutting down forcefully...')
    sys.exit()


_GRACEFUL_TIMER = threading.Timer(2.5, _timeout)


def init(context: str) -> None:
    _HANDLERS[2] = signal.getsignal(signal.SIGINT)
    _HANDLERS[15] = signal.getsignal(signal.SIGTERM)
    signal.signal(signal.SIGINT, lambda s, f: cleanup(s, f, context))
    signal.signal(signal.SIGTERM, lambda s, f: cleanup(s, f, context))


def cleanup(sig: int, frame: Optional[FrameType], context: str) -> None:
    logging.info(f'(Context: {context}) Cleaning up...')
    _SHUTDOWN_FLAG.set()
    processes.terminate_subprocesses()
    handler = _HANDLERS[sig]
    if callable(handler):
        handler(sig, frame)
    logging.info(f'(Context: {context}) Cleanup done!{
                 " Bye-bye!" if context == "main" else ""}')

    # Set forceful cleanup timeout to 2.5 seconds
    if not _GRACEFUL_TIMER.is_alive():
        _GRACEFUL_TIMER.start()

    # Stop timeout timer if everything finished
    elif context == 'main':
        _GRACEFUL_TIMER.cancel()


def get_flag() -> bool:
    return _SHUTDOWN_FLAG.get()

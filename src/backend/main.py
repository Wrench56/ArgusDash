import logging
import logging.config

import asyncio
import atexit
import signal
import sys

from server import build, start
from utils import config, processes, status


def main() -> None:
    # Initialize logging
    init_logger()

    # Load config.ini
    config.load()

    # Cache status
    status.update()

    # Register cleanup functions
    atexit.register(lambda: cleanup)
    signal.signal(signal.SIGTERM, lambda _, __: cleanup())
    signal.signal(signal.SIGINT, lambda _, __: cleanup())

    # Build the frontend with Vite
    build.build_frontend()

    # Start the ASGI uvicorn server
    start.run()


def init_logger():
    logging.config.fileConfig('config/logger.config.ini')
    logging.info('Logging init done')


def cleanup() -> None:
    logging.info('Cleaning up...')
    processes.terminate_subprocesses()
    loop = asyncio.get_event_loop()
    for task in asyncio.all_tasks(loop=loop):
        task.cancel()
    loop.stop()

    # Raises SystemExit
    sys.exit()


if __name__ == '__main__':
    main()

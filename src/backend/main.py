import logging
import logging.config

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
    processes.terminate_subprocesses()

    # Raises SystemExit
    sys.exit()


if __name__ == '__main__':
    main()

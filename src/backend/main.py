import logging
import logging.config

import atexit
import signal
import sys

from utils import processes

from server import build, start

def main() -> None:
    init_logger()

    # Register cleanup functions
    atexit.register(cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    signal.signal(signal.SIGINT, cleanup)

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
import logging
import logging.config

from server import build, start
from utils import config, cleanup, status


def main() -> None:
    # Initialize logging
    init_logger()

    # Load config.ini
    config.load()

    # Cache status
    status.update()

    # Register cleanup functions
    cleanup.init('main')

    # Build the frontend with Vite
    build.build_frontend()

    # Start the ASGI uvicorn server
    start.run()


def init_logger():
    logging.config.fileConfig('config/logger.config.ini')
    logging.info('Logging init done')


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass

import logging
import subprocess

import uvicorn


def run() -> None:
    logging.info('Starting FastAPI server...')
    uvicorn.run(
        'server.main:app',
        log_config='config/logger.config.ini',
        host='0.0.0.0',
        port=10000,
    )

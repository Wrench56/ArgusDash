import logging
import subprocess

import processes

def init() -> subprocess.Popen:
    logging.info('Starting FastAPI server...')
    return processes.add_subprocess(subprocess.Popen(
        [
            'uvicorn',
            'server.main:app',
            '--log-config',
            'config/logger.config.ini',
            '--host',
            '0.0.0.0',
            '--port',
            '10000',
        ],
        shell=True,
    ))

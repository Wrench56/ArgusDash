import subprocess
import logging

def init() -> subprocess.CompletedProcess:
    logging.info('Starting FastAPI server...')
    return subprocess.run(['uvicorn', 'server.main:app',
                           '--log-config', 'config/logger.config.ini',
                           '--port', '10000'
                          ])

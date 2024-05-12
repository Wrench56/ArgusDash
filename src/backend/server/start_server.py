import subprocess
import logging

def init() -> subprocess.Popen:
    logging.info('Starting FastAPI server...')
    return subprocess.Popen(['uvicorn', 'server.main:app',
                           '--log-config', 'config/logger.config.ini',
                           '--port', '10000'
                          ], shell=True)

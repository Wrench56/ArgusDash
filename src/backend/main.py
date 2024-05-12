import logging
import logging.config

import atexit
import signal
import sys
import subprocess

from server import start_server

def main() -> None:
    init_logger()
    proc = start_server.init()
    
    # Register cleanup function
    atexit.register(lambda: cleanup(proc))
    signal.signal(signal.SIGTERM, lambda: cleanup(proc))
    signal.signal(signal.SIGINT, lambda: cleanup(proc))

    # Block
    proc.wait()

def init_logger():
    logging.config.fileConfig('config/logger.config.ini')
    logging.info('Logging init done')

def cleanup(process: subprocess.Popen) -> None:
    logging.info('Cleanup function called')
    process.terminate()
    process.wait()
    logging.info('Cleanup successful')
    
    # Raises SystemExit
    sys.exit()

if __name__ == '__main__':
    main()
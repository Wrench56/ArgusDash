import logging
import logging.config

from server import start_server

def main() -> None:
    init_logger()
    start_server.init()
    
def init_logger():
    logging.config.fileConfig('config/logger.config.ini')
    logging.info('Logging init done')

if __name__ == '__main__':
    main()
import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO)

def get_logger():
    return logging.getLogger("api-comparison")
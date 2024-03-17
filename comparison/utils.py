import logging

def setup_logging() -> None:
    logging.basicConfig(level=logging.INFO)

def get_logger() -> logging.Logger:
    return logging.getLogger("api-comparison")
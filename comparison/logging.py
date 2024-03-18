import atexit
import logging
import logging.handlers
import pendulum
import queue
from pathlib import Path

import comparison.constants as c

class SydneyTimeFormatter(logging.Formatter):
    def formatTime(self, record: logging.LogRecord, datefmt: str | None = None) -> str:
        dt = pendulum.from_timestamp(record.created, tz="Australia/Sydney")
        return dt.strftime(datefmt) if datefmt else dt.to_iso8601_string()


def setup_logging(log_file: Path = c.LOGS_DIR / "api-comparison.log") -> None:
    log_file.parent.mkdir(exist_ok=True)

    log_format = "%(asctime)s | %(levelname)s:%(name)s:%(message)s"
    formatter = SydneyTimeFormatter(log_format)

    # Stdout handler
    stdout_handler = logging.StreamHandler()
    stdout_handler.setFormatter(formatter)
    stdout_handler.setLevel(logging.INFO)

    # File handler
    file_handler = logging.handlers.RotatingFileHandler(
        log_file, maxBytes=10_000_000, backupCount=3
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)

    # Queue handler
    log_queue = queue.Queue(-1)
    queue_handler = logging.handlers.QueueHandler(log_queue)
    queue_listener = logging.handlers.QueueListener(
        log_queue, file_handler, stdout_handler, respect_handler_level=True
    )
    queue_listener.start()
    atexit.register(queue_listener.stop)

    root_logger = logging.getLogger()
    root_logger.addHandler(queue_handler)
    root_logger.setLevel(logging.DEBUG)


def get_logger() -> logging.Logger:
    return logging.getLogger("justin-utils")

import logging
import sys


def get_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Configure and return a logger with a structured format.
    Avoids duplicate handlers.
    """

    logger = logging.getLogger(name)

    # Prevent adding multiple handlers if already configured
    if logger.hasHandlers():
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S",
    )

    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(console_handler)

    return logger
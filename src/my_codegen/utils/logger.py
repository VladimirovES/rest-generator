import logging
import sys
from typing import Optional


def configure_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        level: Logging level (default: INFO)

    Returns:
        Configured logger instance
    """
    logger = logging.getLogger("my_codegen")

    # Prevent duplicate handlers
    if logger.handlers:
        return logger

    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    return logger


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance"""
    if name:
        return logging.getLogger(f"my_codegen.{name}")
    return logging.getLogger("my_codegen")


# Configure the main logger
configure_logging()
logger = get_logger()

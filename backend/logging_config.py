"""
Logging configuration for the LeetCode Stats application.

This module sets up structured logging with both file and console handlers.
Logs are written to both a file and the console with appropriate formatting.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import Optional
from config import settings


def setup_logging(log_file: Optional[str] = None) -> None:
    """Set up logging configuration.

    Args:
        log_file: Optional[str] - Path to log file (defaults to settings.LOG_FILE)
    """
    # Create logs directory if it doesn't exist
    log_file = log_file or settings.LOG_FILE
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Create logger
    logger = logging.getLogger("leetcode_stats")
    logger.setLevel(settings.LOG_LEVEL)

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatters
    file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_formatter = logging.Formatter(
        "%(levelname)s: %(message)s"
    )

    # File handler (with rotation)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setLevel(settings.LOG_LEVEL)
    file_handler.setFormatter(file_formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(settings.LOG_LEVEL)
    console_handler.setFormatter(console_formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Log initial message
    logger.info("Logging system initialized")


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance with the specified name.

    Args:
        name: str - Name of the logger

    Returns:
        logging.Logger: Configured logger instance
    """
    return logging.getLogger(f"leetcode_stats.{name}")

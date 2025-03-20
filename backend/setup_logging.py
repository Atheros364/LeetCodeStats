"""
Setup logging configuration for the LeetCode Stats application.
"""

import os
import logging
from pathlib import Path
from .config import settings


def setup_logging():
    """
    Set up logging configuration and create necessary directories.
    """
    # Create logs directory if it doesn't exist
    log_path = Path(settings.LOG_FILE)
    log_dir = log_path.parent
    log_dir.mkdir(parents=True, exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format=settings.LOG_FORMAT,
        handlers=[
            # File handler with rotation
            logging.handlers.RotatingFileHandler(
                settings.LOG_FILE,
                maxBytes=10*1024*1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            ),
            # Console handler
            logging.StreamHandler()
        ]
    )

    # Log initial message
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized. Log file: {settings.LOG_FILE}")
    logger.info(f"Log level set to: {settings.LOG_LEVEL}")

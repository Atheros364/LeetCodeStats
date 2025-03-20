"""
Configuration management for the LeetCode Stats application.

This module handles all configuration settings using Pydantic's BaseSettings.
Settings are loaded from environment variables with sensible defaults.
"""

from pydantic_settings import BaseSettings
from typing import Optional
from functools import lru_cache
import os
from pathlib import Path


class Settings(BaseSettings):
    """Application settings."""

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./leetcode_stats.db"

    # LeetCode API
    LEETCODE_SESSION: Optional[str] = None

    # API Settings
    API_V1_PREFIX: str = "/api/v1"
    DEBUG: bool = False

    # Polling Settings
    POLL_INTERVAL: int = 300  # 5 minutes
    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: float = 2.0
    HISTORICAL_FETCH_LIMIT: int = 5000

    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "logs/app.log"

    # Timezone
    TIMEZONE: str = "UTC"

    class Config:
        # Get the directory containing this config.py file
        env_file = os.path.join(os.path.dirname(__file__), ".env")
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance.

    Returns:
        Settings: Application settings
    """
    return Settings()


# Create a settings instance for direct import
settings = get_settings()

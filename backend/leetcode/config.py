import os
from dotenv import load_dotenv
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Get the backend directory path (parent of this file)
BACKEND_DIR = Path(__file__).parent.parent

# Load environment variables from .env file
load_dotenv(BACKEND_DIR / '.env')

# LeetCode configuration
LEETCODE_SESSION = os.getenv('LEETCODE_SESSION')


def validate_session_token() -> bool:
    """Validate if the session token is set and not empty."""
    if not LEETCODE_SESSION:
        logger.error(
            "LEETCODE_SESSION environment variable is not set. "
            "Please get your session token from your browser's cookies and add it to the .env file."
        )
        return False
    return True

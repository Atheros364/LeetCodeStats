import httpx
from typing import Optional, Dict
import logging
from .config import LEETCODE_SESSION, validate_session_token

logger = logging.getLogger(__name__)


class AuthenticationManager:
    def __init__(self):
        if not validate_session_token():
            logger.warning(
                "AuthenticationManager initialized without valid session token. "
                "Some operations may fail."
            )
        self.session_token = LEETCODE_SESSION
        self.session: Optional[httpx.AsyncClient] = None
        self.base_url = "https://leetcode.com"
        self.graphql_url = f"{self.base_url}/graphql"
        logger.info("Initialized AuthenticationManager")

    async def initialize_session(self) -> bool:
        """Initialize the session with the provided token."""
        if not self.session_token:
            logger.error(
                "Cannot initialize session: No session token available")
            return False

        try:
            logger.info("Initializing session with existing token...")

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Origin': self.base_url,
                'Referer': self.base_url,
                'Cookie': f'LEETCODE_SESSION={self.session_token}'
            }

            # Create a new client if one doesn't exist
            if not self.session:
                self.session = httpx.AsyncClient(follow_redirects=True)

            # Test the session with a simple query
            test_query = {
                "operationName": "globalData",
                "query": """
                query globalData {
                    userStatus {
                        isSignedIn
                        username
                    }
                }
                """
            }

            response = await self.session.post(
                self.graphql_url,
                json=test_query,
                headers=headers
            )

            if response.status_code != 200:
                logger.error(
                    f"Session validation failed with status code: {response.status_code}")
                return False

            data = response.json()

            if 'errors' in data:
                logger.error(f"GraphQL errors: {data['errors']}")
                return False

            user_status = data.get('data', {}).get('userStatus', {})
            if not user_status.get('isSignedIn'):
                logger.error("Session token is invalid or expired")
                return False

            logger.info(
                f"Successfully initialized session for user: {user_status.get('username')}")
            return True

        except Exception as e:
            logger.error(
                f"Session initialization error: {str(e)}", exc_info=True)
            return False

    async def refresh_session(self) -> bool:
        """Check if the session is still valid."""
        if not self.session:
            logger.info("No active session found, initializing with token...")
            return await self.initialize_session()
        logger.debug("Session exists, no refresh needed")
        return True

    async def get_auth_headers(self) -> Dict[str, str]:
        """Get headers with valid session for GraphQL requests."""
        if not await self.refresh_session():
            logger.error("Failed to refresh session")
            raise Exception("Failed to refresh session")

        headers = {
            'Content-Type': 'application/json',
            'Cookie': f'LEETCODE_SESSION={self.session_token}'
        }
        logger.debug("Generated auth headers with session cookie")
        return headers

    async def close(self):
        """Close the session."""
        if self.session:
            logger.info("Closing LeetCode session")
            await self.session.aclose()
            self.session = None
            logger.debug("Session closed successfully")

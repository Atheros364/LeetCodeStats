import httpx
from bs4 import BeautifulSoup
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class AuthenticationManager:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session: Optional[httpx.AsyncClient] = None
        self.csrf_token: Optional[str] = None
        self.base_url = "https://leetcode.com"

    async def login(self) -> bool:
        """Login to LeetCode and get session cookie."""
        try:
            async with httpx.AsyncClient() as client:
                # Get CSRF token
                response = await client.get(f"{self.base_url}/accounts/login/")
                soup = BeautifulSoup(response.text, 'html.parser')
                csrf_input = soup.find(
                    'input', {'name': 'csrfmiddlewaretoken'})
                if not csrf_input:
                    logger.error("Failed to get CSRF token")
                    return False
                self.csrf_token = csrf_input['value']

                # Login
                login_data = {
                    'csrfmiddlewaretoken': self.csrf_token,
                    'login': self.username,
                    'password': self.password,
                    'next': '/'
                }
                response = await client.post(
                    f"{self.base_url}/accounts/login/",
                    data=login_data,
                    headers={'Referer': f"{self.base_url}/accounts/login/"}
                )

                if response.status_code != 200:
                    logger.error(
                        f"Login failed with status code: {response.status_code}")
                    return False

                # Store session cookie
                self.session = client
                return True

        except Exception as e:
            logger.error(f"Login error: {str(e)}")
            return False

    async def refresh_session(self) -> bool:
        """Refresh the session if it's expired."""
        if not self.session:
            return await self.login()
        return True

    async def get_auth_headers(self) -> Dict[str, str]:
        """Get headers with valid session for GraphQL requests."""
        if not await self.refresh_session():
            raise Exception("Failed to refresh session")

        return {
            'Content-Type': 'application/json',
            'X-CSRFToken': self.csrf_token or '',
            'Cookie': self.session.cookies.get('LEETCODE_SESSION', '')
        }

    async def close(self):
        """Close the session."""
        if self.session:
            await self.session.aclose()
            self.session = None

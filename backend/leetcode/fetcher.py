import httpx
from typing import Dict, List, Optional
import logging
from datetime import datetime
import asyncio

from .auth import AuthenticationManager

logger = logging.getLogger(__name__)


class LeetCodeDataFetcher:
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.base_url = "https://leetcode.com/graphql"
        self.retry_delay = 1.0  # Initial delay in seconds
        self.max_retries = 3

    async def _execute_query(self, query: str, variables: Dict) -> Optional[Dict]:
        """Execute a GraphQL query with retry logic."""
        for attempt in range(self.max_retries):
            try:
                headers = await self.auth_manager.get_auth_headers()
                response = await self.auth_manager.session.post(
                    self.base_url,
                    json={'query': query, 'variables': variables},
                    headers=headers
                )

                if response.status_code == 429:  # Rate limit
                    delay = self.retry_delay * \
                        (2 ** attempt)  # Exponential backoff
                    logger.warning(f"Rate limited. Waiting {delay} seconds...")
                    await asyncio.sleep(delay)
                    continue

                response.raise_for_status()
                return response.json()

            except Exception as e:
                logger.error(
                    f"Query execution error (attempt {attempt + 1}/{self.max_retries}): {str(e)}")
                if attempt < self.max_retries - 1:
                    await asyncio.sleep(self.retry_delay * (2 ** attempt))
                else:
                    logger.error("Max retries reached")
                    return None

    async def fetch_recent_submissions(self, limit: int = 15) -> List[Dict]:
        """Fetch recent accepted submissions."""
        query = """
        query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
                status
                runtime
                memory
                code
            }
        }
        """

        variables = {
            "username": self.auth_manager.username,
            "limit": limit
        }

        result = await self._execute_query(query, variables)
        if not result or 'data' not in result:
            return []

        return result['data']['recentAcSubmissionList']

    async def fetch_historical_submissions(self, limit: int = 5000) -> List[Dict]:
        """Fetch historical submissions."""
        return await self.fetch_recent_submissions(limit)

    async def fetch_question_metadata(self, title_slug: str) -> Optional[Dict]:
        """Fetch question metadata by title slug."""
        query = """
        query questionContent($titleSlug: String!) {
            question(titleSlug: $titleSlug) {
                questionId
                title
                titleSlug
                difficulty
                content
                topicTags {
                    name
                    id
                    slug
                }
            }
        }
        """

        variables = {"titleSlug": title_slug}

        result = await self._execute_query(query, variables)
        if not result or 'data' not in result:
            return None

        return result['data']['question']

    async def fetch_user_status(self) -> Optional[Dict]:
        """Fetch user status information."""
        query = """
        query globalData {
            userStatus {
                userId
                isSignedIn
                isMockUser
                isPremium
                isVerified
                username
                avatar
                isAdmin
                isSuperuser
                permissions
                isTranslator
                activeSessionId
                checkedInToday
                notificationStatus {
                    lastModified
                    numUnread
                }
            }
        }
        """

        result = await self._execute_query(query, {})
        if not result or 'data' not in result:
            return None

        return result['data']['userStatus']

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
        self._username = None
        logger.info("Initialized LeetCodeDataFetcher")

    async def _get_username(self) -> Optional[str]:
        """Get the username from user status."""
        if self._username:
            return self._username

        user_status = await self.fetch_user_status()
        if user_status and user_status.get('username'):
            self._username = user_status['username']
            return self._username
        return None

    async def _execute_query(self, query: str, variables: Dict) -> Optional[Dict]:
        """Execute a GraphQL query with retry logic."""
        for attempt in range(self.max_retries):
            try:
                logger.debug(
                    f"Executing GraphQL query (attempt {attempt + 1}/{self.max_retries})")
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
                result = response.json()

                if 'errors' in result:
                    logger.error(f"GraphQL errors: {result['errors']}")
                    return None

                logger.debug(
                    f"Query executed successfully (attempt {attempt + 1})")
                return result

            except Exception as e:
                logger.error(
                    f"Query execution error (attempt {attempt + 1}/{self.max_retries}): {str(e)}",
                    exc_info=True
                )
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    logger.debug(f"Retrying in {delay} seconds...")
                    await asyncio.sleep(delay)
                else:
                    logger.error("Max retries reached")
                    return None

    async def fetch_recent_submissions(self, limit: int = 15) -> List[Dict]:
        """Fetch recent accepted submissions."""
        username = await self._get_username()
        if not username:
            logger.error("Failed to get username for fetching submissions")
            return []

        logger.info(
            f"Fetching {limit} recent submissions for user: {username}")
        query = """
        query recentAcSubmissions($username: String!, $limit: Int!) {
            recentAcSubmissionList(username: $username, limit: $limit) {
                id
                title
                titleSlug
                timestamp
                lang
            }
        }
        """

        variables = {
            "username": username,
            "limit": limit
        }

        result = await self._execute_query(query, variables)
        if not result or 'data' not in result:
            logger.error("Failed to fetch recent submissions")
            return []

        submissions = result['data']['recentAcSubmissionList']
        logger.info(
            f"Successfully fetched {len(submissions)} recent submissions")
        return submissions

    async def fetch_historical_submissions(self, limit: int = 5000) -> List[Dict]:
        """Fetch historical submissions."""
        logger.info(f"Fetching historical submissions (limit: {limit})")
        return await self.fetch_recent_submissions(limit)

    async def fetch_question_metadata(self, title_slug: str) -> Optional[Dict]:
        """Fetch question metadata by title slug."""
        logger.info(f"Fetching metadata for question: {title_slug}")
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
            logger.error(
                f"Failed to fetch metadata for question: {title_slug}")
            return None

        question_data = result['data']['question']
        logger.info(
            f"Successfully fetched metadata for question: {title_slug}")
        return question_data

    async def fetch_user_status(self) -> Optional[Dict]:
        """Fetch user status information."""
        logger.info("Fetching user status information")
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
            logger.error("Failed to fetch user status")
            return None

        user_status = result['data']['userStatus']
        logger.info(
            f"Successfully fetched user status for: {user_status.get('username')}")
        return user_status

    async def fetch_user_problems_solved(self) -> Optional[Dict]:
        """Fetch user's problems solved statistics."""
        username = await self._get_username()
        if not username:
            logger.error("Failed to get username for fetching problems solved")
            return None

        logger.info(f"Fetching problems solved for user: {username}")
        query = """
        query userProblemsSolved($username: String!) {
            allQuestionsCount {
                difficulty
                count
            }
            matchedUser(username: $username) {
                problemsSolvedBeatsStats {
                    difficulty
                    percentage
                }
                submitStatsGlobal {
                    acSubmissionNum {
                        difficulty
                        count
                    }
                }
            }
        }
        """

        variables = {"username": username}
        result = await self._execute_query(query, variables)
        if not result or 'data' not in result:
            logger.error("Failed to fetch problems solved")
            return None

        return result['data']

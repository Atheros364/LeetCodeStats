import httpx
from typing import Dict, List, Optional
import logging
from datetime import datetime
import asyncio
import json
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

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

    async def fetch_all_solved_questions(self, db: AsyncSession) -> List[Dict]:
        """Fetch all questions solved by the user."""
        username = await self._get_username()
        if not username:
            logger.error(
                "Failed to get username for fetching solved questions")
            return []

        # Get last submission timestamps from our database
        query = """
        SELECT q.title_slug, MAX(s.submitted_at) as last_submission
        FROM questions q
        LEFT JOIN submissions s ON q.id = s.question_id
        GROUP BY q.title_slug
        """
        result = await db.execute(text(query))
        last_submissions = {
            row.title_slug: row.last_submission for row in result}

        logger.info(f"Fetching all solved questions for user: {username}")
        query = """
        query userProgressQuestionList($filters: UserProgressQuestionListInput) {
            userProgressQuestionList(filters: $filters) {
                totalNum
                questions {
                    translatedTitle
                    frontendId
                    title
                    titleSlug
                    difficulty
                    lastSubmittedAt
                    numSubmitted
                    questionStatus
                    lastResult
                    topicTags {
                        name
                        nameTranslated
                        slug
                    }
                }
            }
        }
        """

        # Fetch all solved questions in batches of 50
        batch_size = 50
        offset = 0
        all_questions = []

        while True:
            variables = {
                "filters": {
                    "skip": offset,
                    "limit": batch_size
                }
            }

            result = await self._execute_query(query, variables)
            if not result or 'data' not in result:
                logger.error("Failed to fetch solved questions")
                break

            questions_data = result['data']['userProgressQuestionList']
            if not questions_data or not questions_data.get('questions'):
                break

            questions = questions_data['questions']

            # Filter questions that have new submissions
            for question in questions:
                try:
                    # Handle both integer timestamps and ISO format datetime strings
                    last_submitted_at = question['lastSubmittedAt']
                    if isinstance(last_submitted_at, str):
                        # Parse ISO format datetime string
                        last_submitted_at = datetime.fromisoformat(
                            last_submitted_at.replace('Z', '+00:00'))
                    else:
                        # Handle integer timestamp
                        last_submitted_at = datetime.fromtimestamp(
                            int(last_submitted_at))

                    db_last_submission = last_submissions.get(
                        question['titleSlug'])

                    if not db_last_submission or last_submitted_at > db_last_submission:
                        all_questions.append(question)
                        logger.info(
                            f"Found new activity for question: {question['titleSlug']}")
                except (ValueError, TypeError) as e:
                    logger.error(
                        f"Error parsing timestamp for question {question['titleSlug']}: {str(e)}")
                    continue

            # If we got fewer questions than the batch size, we're done
            if len(questions) < batch_size:
                break

            offset += batch_size
            # Add a small delay to avoid rate limiting
            await asyncio.sleep(0.5)

        logger.info(f"Found {len(all_questions)} questions with new activity")
        return all_questions

    async def fetch_submissions_for_question(self, title_slug: str, db: AsyncSession) -> List[Dict]:
        """Fetch all submissions for a specific question."""
        username = await self._get_username()
        if not username:
            logger.error("Failed to get username for fetching submissions")
            return []

        # Get the last submission timestamp from our database
        query = """
        SELECT MAX(submitted_at) as last_submission
        FROM submissions s
        JOIN questions q ON s.question_id = q.id
        WHERE q.title_slug = :title_slug
        """
        result = await db.execute(text(query), {"title_slug": title_slug})
        last_submission = result.scalar_one_or_none()

        logger.info(f"Fetching submissions for question: {title_slug}")
        query = """
        query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!) {
            questionSubmissionList(
                offset: $offset
                limit: $limit
                lastKey: $lastKey
                questionSlug: $questionSlug
            ) {
                lastKey
                hasNext
                submissions {
                    id
                    title
                    titleSlug
                    status
                    statusDisplay
                    lang
                    langName
                    runtime
                    timestamp
                    url
                    isPending
                    memory
                    hasNotes
                    notes
                    flagType
                    frontendId
                    topicTags {
                        id
                    }
                }
            }
        }
        """

        all_submissions = []
        offset = 0
        limit = 20
        last_key = None

        while True:
            variables = {
                "offset": offset,
                "limit": limit,
                "lastKey": last_key,
                "questionSlug": title_slug
            }

            try:
                result = await self._execute_query(query, variables)
                if not result or 'data' not in result:
                    logger.error(
                        f"Failed to fetch submissions for question: {title_slug}")
                    break

                submission_list = result['data']['questionSubmissionList']
                if not submission_list or not submission_list.get('submissions'):
                    break

                submissions = submission_list['submissions']

                # Filter out submissions we already have
                new_submissions = []
                for submission in submissions:
                    submission_time = datetime.fromtimestamp(
                        int(submission['timestamp']))
                    if not last_submission or submission_time > last_submission:
                        new_submissions.append(submission)
                    else:
                        # If we hit an old submission, we can stop fetching more pages
                        return all_submissions

                all_submissions.extend(new_submissions)

                # Check if there are more pages
                if not submission_list.get('hasNext'):
                    break

                last_key = submission_list.get('lastKey')
                offset += limit

                # Add a small delay to avoid rate limiting
                await asyncio.sleep(0.5)

            except Exception as e:
                logger.error(
                    f"Error fetching submissions for question {title_slug}: {str(e)}")
                break

        if not all_submissions:
            logger.info(f"No new submissions found for question: {title_slug}")
        else:
            logger.info(
                f"Successfully fetched {len(all_submissions)} new submissions for question: {title_slug}")

        return all_submissions

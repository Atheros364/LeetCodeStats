import logging
from typing import Optional
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import json

from .auth import AuthenticationManager
from .fetcher import LeetCodeDataFetcher
from .writer import DatabaseWriter
from ..database import get_db
from ..config import settings

logger = logging.getLogger(__name__)


class LeetCodeService:
    def __init__(self):
        self.auth_manager = AuthenticationManager()
        self.data_fetcher = LeetCodeDataFetcher(self.auth_manager)
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    async def start(self):
        """Start the LeetCode service."""
        if self.is_running:
            return

        # Initialize session
        if not await self.auth_manager.initialize_session():
            logger.error("Failed to initialize LeetCode session")
            return

        # Schedule regular polling
        self.scheduler.add_job(
            self.poll_data,
            IntervalTrigger(minutes=settings.POLL_INTERVAL // 60),
            id='leetcode_poll',
            replace_existing=True
        )
        self.scheduler.start()
        self.is_running = True

        # Initial data fetch
        await self.fetch_historical_data()

    async def stop(self):
        """Stop the LeetCode service."""
        if not self.is_running:
            return

        self.scheduler.shutdown()
        await self.auth_manager.close()
        self.is_running = False

    async def poll_data(self):
        """Poll for new submissions and update the database."""
        try:
            async for db in get_db():
                writer = DatabaseWriter(db)

                # Fetch recent submissions
                submissions = await self.data_fetcher.fetch_recent_submissions()
                logger.info(f"Found {len(submissions)} recent submissions")

                for submission in submissions:
                    # First fetch and store question metadata
                    question_data = await self.data_fetcher.fetch_question_metadata(
                        submission['titleSlug']
                    )
                    if question_data:
                        question = await writer.store_question(question_data)
                        if question and 'topicTags' in question_data:
                            await writer.store_tags(question, question_data['topicTags'])

                        # Now store the submission since we have the question
                        await writer.store_submission(submission)
                    else:
                        logger.warning(
                            f"Failed to fetch question data for submission: {submission['titleSlug']}")

        except Exception as e:
            logger.error(f"Error in poll_data: {str(e)}")

    async def fetch_historical_data(self):
        """Fetch historical submission data."""
        try:
            async for db in get_db():
                writer = DatabaseWriter(db)

                # Fetch all solved questions
                solved_questions = await self.data_fetcher.fetch_all_solved_questions()
                logger.info(f"Found {len(solved_questions)} solved questions")

                # Process each solved question
                for question_data in solved_questions:
                    title_slug = question_data.get('titleSlug')
                    if not title_slug:
                        logger.warning("Question data missing titleSlug")
                        continue

                    logger.info(f"Processing question: {title_slug}")
                    logger.debug(
                        f"Question data: {json.dumps(question_data, indent=2)}")

                    # Prepare question metadata from the progress data
                    question_metadata = {
                        'questionId': question_data['frontendId'],
                        'title': question_data['title'],
                        'titleSlug': title_slug,
                        'difficulty': question_data['difficulty'],
                        'content': '',  # We'll fetch this separately if needed
                        'topicTags': [
                            {'name': tag['name'], 'id': '',
                                'slug': tag['slug']}
                            for tag in question_data.get('topicTags', [])
                        ]
                    }

                    # Store question and tags
                    logger.info(f"Storing question: {title_slug}")
                    question = await writer.store_question(question_metadata)

                    if question:
                        logger.info(
                            f"Successfully stored question: {title_slug}")
                        if 'topicTags' in question_metadata:
                            logger.info(
                                f"Storing {len(question_metadata['topicTags'])} tags for question: {title_slug}")
                            success = await writer.store_tags(question, question_metadata['topicTags'])
                            if success:
                                logger.info(
                                    f"Successfully stored tags for question: {title_slug}")
                            else:
                                logger.error(
                                    f"Failed to store tags for question: {title_slug}")
                    else:
                        logger.error(f"Failed to store question: {title_slug}")
                        continue

                    # Fetch recent submissions for this question
                    logger.info(
                        f"Fetching submissions for question: {title_slug}")
                    submissions = await self.data_fetcher.fetch_submissions_for_question(title_slug)
                    logger.info(
                        f"Found {len(submissions)} submissions for question: {title_slug}")

                    # Store each submission
                    for submission in submissions:
                        logger.info(
                            f"Storing submission for question: {title_slug}")
                        success = await writer.store_submission(submission)
                        if success:
                            logger.info(
                                f"Successfully stored submission for question: {title_slug}")
                        else:
                            logger.error(
                                f"Failed to store submission for question: {title_slug}")

        except Exception as e:
            logger.error(
                f"Error in fetch_historical_data: {str(e)}", exc_info=True)

    async def check_user_status(self) -> Optional[dict]:
        """Check the current user's status."""
        return await self.data_fetcher.fetch_user_status()

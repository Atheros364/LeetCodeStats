import logging
from typing import Optional
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from .auth import AuthenticationManager
from .fetcher import LeetCodeDataFetcher
from .writer import DatabaseWriter
from ..database import get_db
from ..config import settings

logger = logging.getLogger(__name__)


class LeetCodeService:
    def __init__(self):
        self.auth_manager = AuthenticationManager(
            settings.LEETCODE_USERNAME,
            settings.LEETCODE_PASSWORD
        )
        self.data_fetcher = LeetCodeDataFetcher(self.auth_manager)
        self.scheduler = AsyncIOScheduler()
        self.is_running = False

    async def start(self):
        """Start the LeetCode service."""
        if self.is_running:
            return

        # Initial login
        if not await self.auth_manager.login():
            logger.error("Failed to login to LeetCode")
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
                    # Store submission
                    if await writer.store_submission(submission):
                        # If submission is new, fetch and store question metadata
                        question_data = await self.data_fetcher.fetch_question_metadata(
                            submission['titleSlug']
                        )
                        if question_data:
                            question = await writer.store_question(question_data)
                            if question and 'topicTags' in question_data:
                                await writer.store_tags(question, question_data['topicTags'])

        except Exception as e:
            logger.error(f"Error in poll_data: {str(e)}")

    async def fetch_historical_data(self):
        """Fetch historical submission data."""
        try:
            async for db in get_db():
                writer = DatabaseWriter(db)

                # Fetch historical submissions
                submissions = await self.data_fetcher.fetch_historical_submissions()
                logger.info(f"Found {len(submissions)} historical submissions")

                for submission in submissions:
                    # Store submission
                    if await writer.store_submission(submission):
                        # If submission is new, fetch and store question metadata
                        question_data = await self.data_fetcher.fetch_question_metadata(
                            submission['titleSlug']
                        )
                        if question_data:
                            question = await writer.store_question(question_data)
                            if question and 'topicTags' in question_data:
                                await writer.store_tags(question, question_data['topicTags'])

        except Exception as e:
            logger.error(f"Error in fetch_historical_data: {str(e)}")

    async def check_user_status(self) -> Optional[dict]:
        """Check the current user's status."""
        return await self.data_fetcher.fetch_user_status()

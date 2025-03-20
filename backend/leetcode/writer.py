from typing import Dict, List, Optional
import logging
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update
from sqlalchemy.dialects.sqlite import insert as sqlite_insert

from ..models import Question, Tag, Submission
from ..database import get_db

logger = logging.getLogger(__name__)


class DatabaseWriter:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def store_submission(self, submission: Dict) -> bool:
        """Store a submission in the database."""
        try:
            # Get question by leetcode_id
            question = await self.db.execute(
                select(Question).where(
                    Question.leetcode_id == submission['id'])
            )
            question = question.scalar_one_or_none()

            if not question:
                logger.warning(
                    f"Question not found for submission: {submission['id']}")
                return False

            # Convert timestamp to datetime
            submitted_at = datetime.fromtimestamp(submission['timestamp'])

            # Prepare submission data
            submission_data = {
                'question_id': question.id,
                'submitted_at': submitted_at,
                'status': 'Accepted'  # All submissions from recentAcSubmissionList are accepted
            }

            # Use SQLite's UPSERT
            stmt = sqlite_insert(Submission).values(submission_data)
            stmt = stmt.on_conflict_do_update(
                index_elements=['question_id', 'submitted_at'],
                set_=submission_data
            )

            await self.db.execute(stmt)
            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"Error storing submission: {str(e)}")
            await self.db.rollback()
            return False

    async def store_question(self, question_data: Dict) -> Optional[Question]:
        """Store a question in the database."""
        try:
            # Prepare question data
            question_dict = {
                'leetcode_id': question_data['questionId'],
                'title': question_data['title'],
                'difficulty': question_data['difficulty'].lower(),
                'description': question_data['content']
            }

            # Use SQLite's UPSERT
            stmt = sqlite_insert(Question).values(question_dict)
            stmt = stmt.on_conflict_do_update(
                index_elements=['leetcode_id'],
                set_=question_dict
            )

            result = await self.db.execute(stmt)
            await self.db.commit()

            # Get the question instance
            question = await self.db.execute(
                select(Question).where(Question.leetcode_id ==
                                       question_data['questionId'])
            )
            return question.scalar_one()

        except Exception as e:
            logger.error(f"Error storing question: {str(e)}")
            await self.db.rollback()
            return None

    async def store_tags(self, question: Question, tags: List[Dict]) -> bool:
        """Store tags for a question."""
        try:
            for tag_data in tags:
                # Insert tag if it doesn't exist
                tag_stmt = sqlite_insert(Tag).values(
                    {'name': tag_data['name']})
                tag_stmt = tag_stmt.on_conflict_do_nothing()
                await self.db.execute(tag_stmt)

                # Get the tag
                tag = await self.db.execute(
                    select(Tag).where(Tag.name == tag_data['name'])
                )
                tag = tag.scalar_one()

                # Link tag to question
                link_stmt = sqlite_insert(Question.tags.association_table).values({
                    'question_id': question.id,
                    'tag_id': tag.id
                })
                link_stmt = link_stmt.on_conflict_do_nothing()
                await self.db.execute(link_stmt)

            await self.db.commit()
            return True

        except Exception as e:
            logger.error(f"Error storing tags: {str(e)}")
            await self.db.rollback()
            return False

"""
Database CRUD operations for the LeetCode Stats application.

This module contains all database queries and operations used by the application.
It provides functions to:
- Get statistics about solved problems and streaks
- Retrieve daily submission counts for visualization
- Get tag-based statistics
- Generate personalized problem recommendations

All functions are async and use SQLAlchemy's async session.
"""

from sqlalchemy import func, select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from typing import List, Optional
from models import Question, Tag, Submission
from schemas import DailyStats, TagStats


async def get_total_solved(db: AsyncSession) -> int:
    """Get total number of accepted submissions.

    Args:
        db: AsyncSession - The database session

    Returns:
        int: Total number of unique questions with accepted submissions
    """
    result = await db.execute(
        select(func.count(func.distinct(Submission.question_id)))
        .where(Submission.status == 'Accepted')
    )
    return result.scalar()


async def get_current_streak(db: AsyncSession) -> int:
    """Get current streak of days with accepted submissions.

    A streak is defined as the number of consecutive days with at least one
    accepted submission. The streak breaks if a day is missed.

    Args:
        db: AsyncSession - The database session

    Returns:
        int: Current streak length (0 if no submissions)
    """
    # Get all dates with accepted submissions
    query = """
    WITH daily_solved AS (
        SELECT 
            DATE(submitted_at) as solve_date,
            COUNT(DISTINCT question_id) as problems_solved
        FROM submissions
        WHERE status = 'Accepted'
        GROUP BY DATE(submitted_at)
        HAVING problems_solved > 0
    ),
    streak_groups AS (
        SELECT 
            solve_date,
            DATE(solve_date, '-' || ROW_NUMBER() OVER (ORDER BY solve_date) || ' days') as group_start
        FROM daily_solved
    )
    SELECT COUNT(*) as current_streak
    FROM streak_groups
    WHERE group_start = (
        SELECT group_start 
        FROM streak_groups 
        WHERE solve_date = (SELECT MAX(solve_date) FROM daily_solved)
    )
    """
    result = await db.execute(query)
    return result.scalar() or 0


async def get_best_streak(db: AsyncSession) -> int:
    """Get best streak of days with accepted submissions.

    Similar to current streak but finds the maximum streak length achieved
    across all submission history.

    Args:
        db: AsyncSession - The database session

    Returns:
        int: Best streak length achieved (0 if no submissions)
    """
    # Similar to current streak but find the maximum streak length
    query = """
    WITH daily_solved AS (
        SELECT 
            DATE(submitted_at) as solve_date,
            COUNT(DISTINCT question_id) as problems_solved
        FROM submissions
        WHERE status = 'Accepted'
        GROUP BY DATE(submitted_at)
        HAVING problems_solved > 0
    ),
    streak_groups AS (
        SELECT 
            solve_date,
            DATE(solve_date, '-' || ROW_NUMBER() OVER (ORDER BY solve_date) || ' days') as group_start
        FROM daily_solved
    )
    SELECT MAX(streak_length) as best_streak
    FROM (
        SELECT COUNT(*) as streak_length
        FROM streak_groups
        GROUP BY group_start
    )
    """
    result = await db.execute(query)
    return result.scalar() or 0


async def get_top_tags(db: AsyncSession, limit: int = 5) -> List[TagStats]:
    """Get top tags by number of accepted submissions.

    Args:
        db: AsyncSession - The database session
        limit: int - Maximum number of tags to return (default: 5)

    Returns:
        List[TagStats]: List of tags sorted by submission count
    """
    query = """
    SELECT 
        t.name,
        COUNT(DISTINCT s.question_id) as count
    FROM tags t
    JOIN question_tags qt ON t.id = qt.tag_id
    JOIN submissions s ON qt.question_id = s.question_id
    WHERE s.status = 'Accepted'
    GROUP BY t.name
    ORDER BY count DESC
    LIMIT :limit
    """
    result = await db.execute(query, {"limit": limit})
    return [TagStats(tag=row.name, count=row.count) for row in result]


async def get_daily_stats(
    db: AsyncSession,
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None
) -> List[DailyStats]:
    """Get submission counts for each day.

    Args:
        db: AsyncSession - The database session
        start_date: Optional[datetime] - Start date for the range (default: 1 year ago)
        end_date: Optional[datetime] - End date for the range (default: current date)

    Returns:
        List[DailyStats]: List of daily submission counts
    """
    if not start_date:
        start_date = datetime.utcnow() - timedelta(days=365)
    if not end_date:
        end_date = datetime.utcnow()

    query = """
    SELECT 
        DATE(submitted_at) as date,
        COUNT(DISTINCT question_id) as count
    FROM submissions
    WHERE submitted_at BETWEEN :start_date AND :end_date
    GROUP BY DATE(submitted_at)
    ORDER BY date
    """
    result = await db.execute(
        query,
        {"start_date": start_date, "end_date": end_date}
    )
    return [DailyStats(date=str(row.date), count=row.count) for row in result]


async def get_tag_stats(
    db: AsyncSession,
    start_date: datetime,
    end_date: datetime
) -> List[dict]:
    """Get statistics grouped by problem tags.

    For each tag, returns:
    - Total number of solved problems
    - Count of solved problems by difficulty level

    Args:
        db: AsyncSession - The database session
        start_date: datetime - Start date for the range
        end_date: datetime - End date for the range

    Returns:
        List[dict]: List of tag statistics with difficulty breakdowns
    """
    query = """
    SELECT 
        t.name as tag_name,
        COUNT(DISTINCT s.question_id) as total_solved,
        SUM(CASE WHEN q.difficulty = 'easy' THEN 1 ELSE 0 END) as easy_count,
        SUM(CASE WHEN q.difficulty = 'medium' THEN 1 ELSE 0 END) as medium_count,
        SUM(CASE WHEN q.difficulty = 'hard' THEN 1 ELSE 0 END) as hard_count
    FROM tags t
    JOIN question_tags qt ON t.id = qt.tag_id
    JOIN submissions s ON qt.question_id = s.question_id
    JOIN questions q ON s.question_id = q.id
    WHERE s.status = 'Accepted'
        AND s.submitted_at BETWEEN :start_date AND :end_date
    GROUP BY t.name
    ORDER BY total_solved DESC
    """
    result = await db.execute(
        query,
        {"start_date": start_date, "end_date": end_date}
    )
    return [
        {
            "name": row.tag_name,
            "total_solved": row.total_solved,
            "easy_count": row.easy_count,
            "medium_count": row.medium_count,
            "hard_count": row.hard_count
        }
        for row in result
    ]


async def get_recommendations(
    db: AsyncSession,
    difficulty_counts: dict[str, int] = None,
    days_not_attempted: int = 5
) -> List[dict]:
    """Get personalized problem recommendations.

    Args:
        db: AsyncSession - The database session
        difficulty_counts: dict[str, int] - Number of problems to return for each difficulty
            (default: {"easy": 3, "medium": 2, "hard": 2})
        days_not_attempted: int - Number of days a problem should not have been attempted
            (default: 5)

    Returns:
        List[dict]: List of recommended problems with metadata

    Example:
        >>> await get_recommendations(db, {"easy": 2, "medium": 1, "hard": 1}, days_not_attempted=7)
    """
    if difficulty_counts is None:
        difficulty_counts = {"easy": 3, "medium": 2, "hard": 2}

    query = """
    WITH recently_solved AS (
        SELECT DISTINCT question_id
        FROM submissions
        WHERE status = 'Accepted'
        AND submitted_at >= CURRENT_DATE - INTERVAL ':days days'
    ),
    candidates AS (
        SELECT 
            q.id,
            q.title,
            q.difficulty,
            t.name as tag_name
        FROM questions q
        JOIN submissions s ON q.id = s.question_id
        LEFT JOIN question_tags qt ON q.id = qt.question_id
        LEFT JOIN tags t ON qt.tag_id = t.id
        WHERE s.status = 'Accepted'
        AND q.id NOT IN (SELECT question_id FROM recently_solved)
    ),
    ranked_candidates AS (
        SELECT 
            id,
            title,
            difficulty,
            tag_name,
            ROW_NUMBER() OVER (PARTITION BY difficulty ORDER BY RANDOM()) as rn
        FROM candidates
    ),
    difficulty_counts AS (
        SELECT difficulty, COUNT(*) as count
        FROM ranked_candidates
        GROUP BY difficulty
    )
    SELECT 
        rc.id,
        rc.title,
        rc.difficulty,
        rc.tag_name
    FROM ranked_candidates rc
    JOIN difficulty_counts dc ON rc.difficulty = dc.difficulty
    WHERE (rc.difficulty = 'easy' AND rc.rn <= LEAST(:easy_count, dc.count))
       OR (rc.difficulty = 'medium' AND rc.rn <= LEAST(:medium_count, dc.count))
       OR (rc.difficulty = 'hard' AND rc.rn <= LEAST(:hard_count, dc.count))
    ORDER BY rc.difficulty, rc.rn
    """
    result = await db.execute(
        query,
        {
            "days": days_not_attempted,
            "easy_count": difficulty_counts.get("easy", 3),
            "medium_count": difficulty_counts.get("medium", 2),
            "hard_count": difficulty_counts.get("hard", 2)
        }
    )
    return [
        {
            "id": row.id,
            "title": row.title,
            "difficulty": row.difficulty,
            "tags": [row.tag_name] if row.tag_name else []
        }
        for row in result
    ]

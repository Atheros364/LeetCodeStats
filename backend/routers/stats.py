"""
Statistics router for the LeetCode Stats API.

This router provides endpoints for retrieving various statistics about the user's
LeetCode activity, including:
- Overview statistics (total solved, streaks, top tags)
- Daily submission counts for visualization
- Tag-based statistics
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from datetime import datetime
from typing import Optional
from ..crud import (
    get_total_solved,
    get_current_streak,
    get_best_streak,
    get_top_tags,
    get_daily_stats,
    get_tag_stats
)
from ..schemas import OverviewStats, DailyStats

router = APIRouter()


@router.get("/overview", response_model=OverviewStats)
async def get_overview(db: AsyncSession = Depends(get_db)):
    """Get high-level statistics about LeetCode activity.

    Returns:
        OverviewStats: Object containing:
            - total_solved: Total number of unique problems solved
            - current_streak: Current streak of days with submissions
            - best_streak: Best streak achieved
            - top_tags: Most used problem tags
            - daily_stats: Submission counts for the last year

    Raises:
        HTTPException: 500 if database error occurs
    """
    try:
        total_solved = await get_total_solved(db)
        current_streak = await get_current_streak(db)
        best_streak = await get_best_streak(db)
        top_tags = await get_top_tags(db)
        daily_stats = await get_daily_stats(db)

        return OverviewStats(
            total_solved=total_solved,
            current_streak=current_streak,
            best_streak=best_streak,
            top_tags=top_tags,
            daily_stats=daily_stats
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/daily", response_model=dict)
async def get_daily_stats_endpoint(
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
):
    """Get submission counts for each day (for heatmap visualization).

    Args:
        start_date: Optional[str] - Start date in ISO format (YYYY-MM-DD)
        end_date: Optional[str] - End date in ISO format (YYYY-MM-DD)
        db: AsyncSession - Database session (injected)

    Returns:
        dict: Object containing list of daily submission counts

    Raises:
        HTTPException: 
            - 400 if date format is invalid
            - 500 if database error occurs
    """
    try:
        start = datetime.fromisoformat(start_date) if start_date else None
        end = datetime.fromisoformat(end_date) if end_date else None

        submissions = await get_daily_stats(db, start, end)
        return {"submissions": submissions}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/tags")
async def get_tag_stats_endpoint(
    start_date: str,
    end_date: str,
    db: AsyncSession = Depends(get_db)
):
    """Get statistics grouped by problem tags.

    Args:
        start_date: str - Start date in ISO format (YYYY-MM-DD)
        end_date: str - End date in ISO format (YYYY-MM-DD)
        db: AsyncSession - Database session (injected)

    Returns:
        dict: Object containing list of tag statistics with difficulty breakdowns

    Raises:
        HTTPException:
            - 400 if date format is invalid
            - 500 if database error occurs
    """
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)

        tags = await get_tag_stats(db, start, end)
        return {"tags": tags}
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

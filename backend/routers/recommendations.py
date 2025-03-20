"""
Recommendations router for the LeetCode Stats API.

This router provides endpoints for getting personalized problem recommendations
based on the user's solving history and patterns.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_db
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from ..crud import get_recommendations
from ..schemas import Recommendation

router = APIRouter()


@router.get("/", response_model=dict)
async def get_recommendations_endpoint(
    easy_count: int = Query(
        3, ge=0, le=10, description="Number of easy problems to recommend"),
    medium_count: int = Query(
        2, ge=0, le=10, description="Number of medium problems to recommend"),
    hard_count: int = Query(
        2, ge=0, le=10, description="Number of hard problems to recommend"),
    days_not_attempted: int = Query(
        5, ge=1, le=30, description="Number of days a problem should not have been attempted"),
    db: AsyncSession = Depends(get_db)
):
    """Get personalized problem recommendations.

    Args:
        easy_count: int - Number of easy problems to recommend (default: 3)
        medium_count: int - Number of medium problems to recommend (default: 2)
        hard_count: int - Number of hard problems to recommend (default: 2)
        days_not_attempted: int - Number of days a problem should not have been attempted (default: 5)
        db: AsyncSession - Database session (injected)

    Returns:
        dict: Object containing list of recommended problems with metadata

    Raises:
        HTTPException: 500 if database error occurs

    Example:
        GET /api/recommendations/?easy_count=2&medium_count=1&hard_count=1&days_not_attempted=7
    """
    try:
        difficulty_counts = {
            "easy": easy_count,
            "medium": medium_count,
            "hard": hard_count
        }
        recommendations = await get_recommendations(db, difficulty_counts, days_not_attempted)
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

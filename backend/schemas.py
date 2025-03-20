from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class TagBase(BaseModel):
    name: str


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    leetcode_id: str
    title: str
    difficulty: str
    description: str


class QuestionCreate(QuestionBase):
    pass


class Question(QuestionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    tags: List[Tag] = []

    class Config:
        from_attributes = True


class SubmissionBase(BaseModel):
    question_id: int
    submitted_at: datetime
    status: str
    runtime_ms: Optional[int] = None
    memory_kb: Optional[int] = None
    code: Optional[str] = None


class SubmissionCreate(SubmissionBase):
    pass


class Submission(SubmissionBase):
    id: int
    question: Question

    class Config:
        from_attributes = True


class DailyStats(BaseModel):
    date: str
    count: int


class TagStats(BaseModel):
    tag: str
    count: int


class OverviewStats(BaseModel):
    total_solved: int
    current_streak: int
    best_streak: int
    top_tags: List[TagStats]
    daily_stats: List[DailyStats]


class Recommendation(BaseModel):
    question: Question
    last_attempted: Optional[datetime]
    difficulty: str

from datetime import datetime
from typing import List, Optional

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table, text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

# Association table for question-tag many-to-many relationship
question_tags = Table(
    'question_tags',
    Base.metadata,
    Column('question_id', Integer, ForeignKey(
        'questions.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey(
        'tags.id', ondelete='CASCADE'), primary_key=True)
)


class Question(Base):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    leetcode_id = Column(Integer, unique=True, nullable=False)
    title = Column(String, nullable=False)
    title_slug = Column(String, unique=True, nullable=False)
    # Constraint enforced by trigger
    difficulty = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=text(
        'CURRENT_TIMESTAMP'), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=text(
        'CURRENT_TIMESTAMP'), nullable=False)

    # Relationships
    tags = relationship('Tag', secondary=question_tags,
                        back_populates='questions')
    submissions = relationship(
        'Submission', back_populates='question', cascade='all, delete-orphan')


class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=text(
        'CURRENT_TIMESTAMP'), nullable=False)

    # Relationships
    questions = relationship(
        'Question', secondary=question_tags, back_populates='tags')


class Submission(Base):
    __tablename__ = 'submissions'

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey(
        'questions.id', ondelete='CASCADE'), nullable=False)
    submitted_at = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False)  # Constraint enforced by trigger
    created_at = Column(DateTime(timezone=True), server_default=text(
        'CURRENT_TIMESTAMP'), nullable=False)

    # Relationships
    question = relationship('Question', back_populates='submissions')

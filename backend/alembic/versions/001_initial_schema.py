"""initial schema

Revision ID: 001
Revises: 
Create Date: 2024-03-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create questions table
    op.create_table(
        'questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('leetcode_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('title_slug', sa.String(), nullable=False),
        sa.Column('difficulty', sa.String(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index('idx_questions_leetcode_id', 'questions',
                    ['leetcode_id'], unique=True)
    op.create_index('idx_questions_title_slug', 'questions',
                    ['title_slug'], unique=True)

    # Create tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    # Create question_tags table
    op.create_table(
        'question_tags',
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('question_id', 'tag_id')
    )

    # Create submissions table
    op.create_table(
        'submissions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_id', sa.Integer(), nullable=False),
        sa.Column('submitted_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True),
                  server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.ForeignKeyConstraint(
            ['question_id'], ['questions.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('question_id', 'submitted_at',
                            name='unique_submission')
    )
    op.create_index('idx_submissions_submitted_at',
                    'submissions', ['submitted_at'])

    # Add triggers for difficulty and status constraints
    op.execute("""
        CREATE TRIGGER check_difficulty
        BEFORE INSERT ON questions
        BEGIN
            SELECT CASE
                WHEN NEW.difficulty NOT IN ('easy', 'medium', 'hard')
                THEN RAISE(ABORT, 'Invalid difficulty value')
            END;
        END;
    """)

    op.execute("""
        CREATE TRIGGER check_status
        BEFORE INSERT ON submissions
        BEGIN
            SELECT CASE
                WHEN NEW.status NOT IN ('Accepted', 'Wrong Answer', 'Time Limit Exceeded', 'Runtime Error', 'Compile Error')
                THEN RAISE(ABORT, 'Invalid status value')
            END;
        END;
    """)


def downgrade() -> None:
    # Drop triggers first
    op.execute("DROP TRIGGER IF EXISTS check_difficulty")
    op.execute("DROP TRIGGER IF EXISTS check_status")

    # Drop indexes
    op.drop_index('idx_submissions_submitted_at')
    op.drop_index('idx_questions_title_slug')
    op.drop_index('idx_questions_leetcode_id')

    # Drop tables in reverse order
    op.drop_table('submissions')
    op.drop_table('question_tags')
    op.drop_table('tags')
    op.drop_table('questions')

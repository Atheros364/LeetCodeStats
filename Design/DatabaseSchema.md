# Database Schema

## Tables

### questions
Stores metadata about LeetCode problems.

```sql
CREATE TABLE questions (
    id INTEGER PRIMARY KEY,
    leetcode_id VARCHAR(50) UNIQUE NOT NULL,  -- LeetCode's question ID/slug
    title VARCHAR(255) NOT NULL,
    difficulty VARCHAR(10) NOT NULL CHECK (difficulty IN ('easy', 'medium', 'hard')),
    description TEXT NOT NULL,                -- Full formatted question text
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### tags
Stores problem tags/categories.

```sql
CREATE TABLE tags (
    id INTEGER PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### question_tags
Many-to-many relationship between questions and tags.

```sql
CREATE TABLE question_tags (
    question_id INTEGER,
    tag_id INTEGER,
    PRIMARY KEY (question_id, tag_id),
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (tag_id) REFERENCES tags(id)
);
```

### submissions
Stores user's submission history.

```sql
CREATE TABLE submissions (
    id INTEGER PRIMARY KEY,
    question_id INTEGER NOT NULL,
    submitted_at TIMESTAMP NOT NULL,
    status VARCHAR(50) NOT NULL CHECK (status IN ('Accepted', 'Wrong Answer', 'Time Limit Exceeded', 'Runtime Error', 'Compile Error')),
    runtime_ms INTEGER NULL,                  -- Runtime in milliseconds (optional)
    memory_kb INTEGER NULL,                   -- Memory usage in KB (optional)
    code TEXT NULL,                           -- Actual submitted code (optional)
    FOREIGN KEY (question_id) REFERENCES questions(id),
    UNIQUE (question_id, submitted_at)
);
```

## Indexes

```sql
-- For faster lookups of LeetCode IDs
CREATE INDEX idx_questions_leetcode_id ON questions(leetcode_id);

-- For date-range queries on submissions
CREATE INDEX idx_submissions_submitted_at ON submissions(submitted_at);

-- For joining submissions with questions
CREATE INDEX idx_submissions_question_id ON submissions(question_id);

-- For status-based queries
CREATE INDEX idx_submissions_status ON submissions(status);

-- For faster filtering of accepted submissions
CREATE INDEX idx_submissions_accepted ON submissions(question_id, status) WHERE status = 'Accepted';
```

## Example Queries

### Get total solved count
```sql
SELECT COUNT(DISTINCT question_id) as total_solved
FROM submissions
WHERE status = 'Accepted';
```

### Get daily submission statistics
```sql
SELECT 
    DATE(submitted_at) as submission_date,
    COUNT(*) as total_submissions,
    SUM(CASE WHEN status = 'Accepted' THEN 1 ELSE 0 END) as accepted_submissions
FROM submissions
WHERE submitted_at BETWEEN :start_date AND :end_date
GROUP BY DATE(submitted_at)
ORDER BY submission_date;
```

### Get problems solved by difficulty
```sql
SELECT 
    q.difficulty,
    COUNT(DISTINCT s.question_id) as solved_count
FROM questions q
JOIN submissions s ON q.id = s.question_id
WHERE s.status = 'Accepted'
GROUP BY q.difficulty;
```

### Get problems solved by tag in date range
```sql
SELECT 
    t.name as tag_name,
    COUNT(DISTINCT s.question_id) as solved_count
FROM tags t
JOIN question_tags qt ON t.id = qt.tag_id
JOIN submissions s ON qt.question_id = s.question_id
WHERE s.status = 'Accepted'
    AND s.submitted_at BETWEEN :start_date AND :end_date
GROUP BY t.name;
```

### Get current streak
```sql
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
        DATE_SUB(solve_date, INTERVAL ROW_NUMBER() OVER (ORDER BY solve_date) DAY) as group_start
    FROM daily_solved
)
SELECT COUNT(*) as current_streak
FROM streak_groups
WHERE group_start = (
    SELECT group_start 
    FROM streak_groups 
    WHERE solve_date = (SELECT MAX(solve_date) FROM streak_groups)
);
```

### Get top tags
```sql
SELECT 
    t.name,
    COUNT(DISTINCT s.question_id) as count
FROM tags t
JOIN question_tags qt ON t.id = qt.tag_id
JOIN submissions s ON qt.question_id = s.question_id
WHERE s.status = 'Accepted'
GROUP BY t.name
ORDER BY count DESC
LIMIT 5;
```

### Get least practiced tags (for recommendations)
```sql
SELECT 
    t.name as tag_name,
    COUNT(DISTINCT s.question_id) as solved_count,
    MAX(s.submitted_at) as last_solved_date
FROM tags t
LEFT JOIN question_tags qt ON t.id = qt.tag_id
LEFT JOIN submissions s ON qt.question_id = s.question_id
    AND s.status = 'Accepted'
GROUP BY t.name
ORDER BY solved_count ASC, last_solved_date ASC NULLS FIRST
LIMIT 5;
```
```
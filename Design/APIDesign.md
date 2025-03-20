# API Design Specification

## Base URL
All endpoints are prefixed with `/api/v1`

## Statistics Router (`/stats`)

### GET /stats/overview
Returns high-level statistics including:
- Total problems solved
- Current streak
- Problems solved by difficulty
- Most used tags

Response:
```json
{
  "total_solved": 150,
  "current_streak": 5,
  "by_difficulty": {
    "easy": 70,
    "medium": 60,
    "hard": 20
  },
  "top_tags": [
    {"name": "Array", "count": 45},
    {"name": "Dynamic Programming", "count": 30}
  ]
}
```

### GET /stats/daily
Returns submission counts for each day (for heatmap).
Query params:
- start_date (optional): ISO date string
- end_date (optional): ISO date string

Response:
```json
{
  "submissions": [
    {"date": "2024-03-20", "count": 3},
    {"date": "2024-03-21", "count": 1}
  ]
}
```

### GET /stats/tags
Returns statistics grouped by problem tags.
Query params:
- start_date: ISO date string
- end_date: ISO date string

Response:
```json
{
  "tags": [
    {
      "name": "Array",
      "total_solved": 45,
      "easy_count": 20,
      "medium_count": 15,
      "hard_count": 10
    }
  ]
}
```

## Recommendations Router (`/recommendations`)

### GET /recommendations
Returns recommended problems based on user's solving history. Always returns 7 problems:
- 3 easy problems
- 2 medium problems
- 2 hard problems

The recommendation logic:
1. Finds questions with accepted submissions not attempted in last 5 days
2. Selects 3 easy, 2 medium, and 2 hard problems from this set
3. If not enough problems of a certain difficulty, returns all available problems of that difficulty

SQL Query:
```sql
WITH recently_solved AS (
    SELECT DISTINCT question_id
    FROM submissions
    WHERE status = 'Accepted'
    AND submitted_at >= CURRENT_DATE - INTERVAL '5 days'
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
WHERE (rc.difficulty = 'easy' AND rc.rn <= LEAST(3, dc.count))
   OR (rc.difficulty = 'medium' AND rc.rn <= LEAST(2, dc.count))
   OR (rc.difficulty = 'hard' AND rc.rn <= LEAST(2, dc.count))
ORDER BY rc.difficulty, rc.rn;
```

Response:
```json
{
  "recommendations": [
    {
      "id": "two-sum",
      "title": "Two Sum",
      "difficulty": "easy",
      "tags": ["Array", "Hash Table"],
      "reason": "You haven't practiced Array problems recently"
    }
  ]
}
```

### GET /recommendations/weak-topics
Returns topics that need more practice based on solving history.

Response:
```json
{
  "weak_topics": [
    {
      "tag": "Dynamic Programming",
      "solved_count": 5,
      "last_solved": "2024-02-15",
      "recommended_problems": [
        {
          "id": "climbing-stairs",
          "title": "Climbing Stairs",
          "difficulty": "easy"
        }
      ]
    }
  ]
}
```

## Error Responses
All endpoints may return the following error responses:

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid date format for start_date"
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```
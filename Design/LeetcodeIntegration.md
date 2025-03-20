# LeetCode Integration Design

## Overview
This document outlines the design for integrating with LeetCode's GraphQL API to fetch user submission history and question metadata. The integration includes both regular polling for new submissions and historical data gathering.

## Authentication

### Session Management
- Uses LEETCODE_SESSION cookie for authentication
- Session refresh required when cookie expires
- Credentials stored in config file

### Login Process
1. POST request to `https://leetcode.com/accounts/login/`
2. Extract CSRF token from response
3. Submit login form with credentials
4. Extract LEETCODE_SESSION cookie
5. Store session cookie for future requests

## GraphQL Queries

### 1. User Profile and Solved Questions
```graphql
query userProgressQuestionList($filters: UserProgressQuestionListInput) {
  userProgressQuestionList(filters: $filters) {
    totalNum
    questions {
      translatedTitle
      frontendId
      title
      titleSlug
      difficulty
      lastSubmittedAt
      numSubmitted
      questionStatus
      lastResult
      topicTags {
        name
        nameTranslated
        slug
      }
    }
  }
}
```
This query provides:
- Total number of solved questions
- List of all solved questions with:
  - Question metadata (title, difficulty, etc.)
  - Number of submissions per question
  - Last submission timestamp
  - Question status and result
  - Topic tags

### 2. Recent Submissions
```graphql
query recentAcSubmissions($username: String!, $limit: Int!) {
    recentAcSubmissionList(username: $username, limit: $limit) {
        id
        title
        titleSlug
        timestamp
        lang
    }
}
```
This query provides:
- Recent accepted submissions
- Basic submission information

### 3. Question Submissions
```graphql
query submissionList($offset: Int!, $limit: Int!, $lastKey: String, $questionSlug: String!, $lang: String) {
  submissionList(offset: $offset, limit: $limit, lastKey: $lastKey, questionSlug: $questionSlug, lang: $lang) {
    lastKey
    hasNext
    submissions {
      id
      statusDisplay
      lang
      runtime
      timestamp
      url
      isPending
      memory
      submissionComment {
        comment
      }
      runtimeDisplay
      memoryDisplay
      code
      compareResult
      titleDisplay
      titleSlug
      date
      statusCode
    }
  }
}
```
This query provides:
- Paginated list of all submissions for a specific question
- Detailed submission information including runtime, memory, and code
- Support for pagination with offset and lastKey

### 4. Question Metadata
```graphql
query questionContent($titleSlug: String!) {
  question(titleSlug: $titleSlug) {
    questionId
    title
    titleSlug
    difficulty
    content
    topicTags {
      name
      id
      slug
    }
  }
}
```

## Service Components

### 1. Configuration
```python
class Config:
    LEETCODE_USERNAME: str
    LEETCODE_PASSWORD: str
    DATABASE_URL: str
    POLL_INTERVAL: int = 300  # 5 minutes
    MAX_RETRIES: int = 3
    BACKOFF_FACTOR: float = 2.0
    HISTORICAL_FETCH_LIMIT: int = 5000
```

### 2. Authentication Manager
```python
class AuthenticationManager:
    def __init__(self, username: str, password: str):
        self.username = username
        self.password = password
        self.session = None
        self.csrf_token = None

    async def login(self):
        # Implementation for login process
        pass

    async def refresh_session(self):
        # Implementation for session refresh
        pass

    async def get_auth_headers(self):
        # Returns headers with valid session
        pass
```

### 3. Data Fetcher
```python
class LeetCodeDataFetcher:
    def __init__(self, auth_manager: AuthenticationManager):
        self.auth_manager = auth_manager
        self.base_url = "https://leetcode.com/graphql"

    async def fetch_recent_submissions(self, limit: int = 15):
        # Implementation for fetching recent submissions
        pass

    async def fetch_historical_submissions(self, limit: int = 5000):
        # Implementation for fetching historical submissions
        pass

    async def fetch_question_metadata(self, question_id: str):
        # Implementation for fetching question metadata
        pass

    async def _execute_query(self, query: str, variables: Dict):
        # Implementation for executing GraphQL queries
        pass
```

### 4. Database Writer
```python
class DatabaseWriter:
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.session = None

    async def store_submission(self, submission: Dict):
        # Implementation for storing submission
        pass

    async def store_question(self, question: Dict):
        # Implementation for storing question
        pass

    async def store_tags(self, question_id: int, tags: List[str]):
        # Implementation for storing tags
        pass
```

## Regular Polling Service

### Flow
```
Start Poll
├── Check/Refresh Session
├── Fetch Recent Submissions
│   └── For each submission:
│       ├── Check if exists in DB
│       └── If new, store submission
├── For new submissions:
│   ├── Check if question exists in DB
│   └── If new, fetch and store question metadata
└── Log completion
```

### Error Handling
```
On Error
├── Log error details
├── Implement exponential backoff
├── If max retries reached:
│   └── Log failure and wait for next interval
└── If network error:
    └── Log and wait for next interval
```

## Historical Data Gathering

### Flow
```
Start Historical Fetch
├── Initialize Database Connection
├── Fetch All Solved Questions
│   └── Use userProgressQuestionList query to get:
│       ├── Total number of solved questions
│       └── List of all solved questions with:
│           ├── Question metadata
│           ├── Number of submissions
│           └── Topic tags
├── For Each Solved Question:
│   ├── Store Question Metadata
│   │   └── Store tags
│   └── Fetch Recent Submissions
│       └── Use recentAcSubmissionList query
│           └── Store each submission
└── Log completion
```

### Progress Tracking
- Log total number of solved questions
- Log progress for each question
- Track pagination state for question list
- Log number of submissions per question

### Error Handling
```
On Error
├── Log error details
├── Save progress (last processed question)
├── Implement exponential backoff
└── Resume from last processed question
```

## Database Operations

### 1. Submission Upsert
```sql
INSERT INTO submissions (question_id, submitted_at, status, runtime_ms, memory_kb, code)
VALUES (:question_id, :submitted_at, :status, :runtime_ms, :memory_kb, :code)
ON CONFLICT (question_id, submitted_at) DO UPDATE
SET status = EXCLUDED.status,
    runtime_ms = EXCLUDED.runtime_ms,
    memory_kb = EXCLUDED.memory_kb,
    code = EXCLUDED.code
```

### 2. Question Insert
```sql
INSERT INTO questions (leetcode_id, title, difficulty, description)
VALUES (:leetcode_id, :title, :difficulty, :description)
ON CONFLICT (leetcode_id) DO NOTHING
```

### 3. Simplified Tag Management
```sql
-- Insert tags and link to questions in a single operation
INSERT INTO tags (name)
VALUES (:name)
ON CONFLICT (name) DO NOTHING;

INSERT INTO question_tags (question_id, tag_id)
SELECT q.id, t.id
FROM questions q, tags t
WHERE q.leetcode_id = :leetcode_id
AND t.name = :tag_name
ON CONFLICT (question_id, tag_id) DO NOTHING;
```

## Logging

### Info Level
- Poll start/end
- New submissions found
- New questions found
- Successful database operations
- Historical fetch progress

### Warning Level
- Session refresh attempts
- Rate limit warnings

### Error Level
- Authentication failures
- Network errors
- Database errors

## Error Handling
- Log errors and continue with next operation
- Retry failed requests with exponential backoff
- If max retries reached, wait for next interval

## Rate Limiting
- Implement delay between API calls
- Handle pagination carefully
- Use exponential backoff for retries
- Consider implementing request queuing

## Usage Examples

### Regular Polling
```python
# Initialize services
auth_manager = AuthenticationManager(username, password)
data_fetcher = LeetCodeDataFetcher(auth_manager)
db_writer = DatabaseWriter(db_url)

# Start polling service
scheduler = AsyncIOScheduler()
scheduler.add_job(poll_data, 'interval', minutes=5)
scheduler.start()
```

### Historical Data Fetch
```python
# Initialize services
auth_manager = AuthenticationManager()
data_fetcher = LeetCodeDataFetcher(auth_manager)
db_writer = DatabaseWriter(db_url)

# Fetch historical data
await data_fetcher.fetch_all_solved_questions()
# For each question:
await data_fetcher.fetch_submissions_for_question(question_slug)
```

## Error Recovery
1. Network Errors
   - Implement exponential backoff
   - Retry failed requests
   - Log error details

2. Authentication Errors
   - Attempt session refresh
   - If refresh fails, log and wait for next interval

3. Database Errors
   - Log error details
   - Continue with next record
   - Consider implementing transaction rollback

4. API Rate Limiting
   - Implement delays between requests
   - Log rate limit warnings
   - Consider implementing request queuing

# LeetCode Stats Backend

This is the backend service for the LeetCode Stats application. It provides APIs for retrieving statistics and recommendations based on LeetCode submission history.

## Project Structure

```
backend/
├── main.py              # FastAPI application entry point
├── database.py          # Database configuration
├── models.py            # SQLAlchemy models
├── schemas.py           # Pydantic schemas
├── crud.py             # Database CRUD operations
├── routers/            # API routers
│   ├── __init__.py
│   ├── stats.py        # Statistics endpoints
│   └── recommendations.py  # Recommendation endpoints
└── requirements.txt    # Python dependencies
```

## API Endpoints

### Statistics Router (`/api/stats`)

#### GET /overview
Returns high-level statistics including:
- Total problems solved
- Current streak
- Best streak
- Top tags
- Daily submission counts

#### GET /daily
Returns submission counts for each day (for heatmap).
Query parameters:
- `start_date` (optional): ISO date string (YYYY-MM-DD)
- `end_date` (optional): ISO date string (YYYY-MM-DD)

#### GET /tags
Returns statistics grouped by problem tags.
Query parameters:
- `start_date`: ISO date string (YYYY-MM-DD)
- `end_date`: ISO date string (YYYY-MM-DD)

### Recommendations Router (`/api/recommendations`)

#### GET /
Returns personalized problem recommendations based on solving history.

Query parameters:
- `easy_count` (optional): Number of easy problems to recommend (default: 3, range: 0-10)
- `medium_count` (optional): Number of medium problems to recommend (default: 2, range: 0-10)
- `hard_count` (optional): Number of hard problems to recommend (default: 2, range: 0-10)
- `days_not_attempted` (optional): Number of days a problem should not have been attempted (default: 5, range: 1-30)

Example:
```bash
# Get default recommendations (3 easy, 2 medium, 2 hard)
GET /api/recommendations/

# Get custom recommendations
GET /api/recommendations/?easy_count=2&medium_count=1&hard_count=1&days_not_attempted=7
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Initialize the database:
```bash
cd backend && alembic upgrade head && cd..
```

5. Run the development server:
```bash
uvicorn backend.main:app --reload
```

## Development

### Database Schema
See `Design/DatabaseSchema.md` for the complete database schema.

### API Design
See `Design/APIDesign.md` for detailed API specifications.

### Code Style
- Follow PEP 8 guidelines
- Use type hints
- Document all functions and classes
- Keep functions focused and small

### Testing
Run tests with:
```bash
pytest
```

## Error Handling

The API uses standard HTTP status codes:
- 200: Success
- 400: Bad Request (invalid parameters)
- 500: Internal Server Error

All error responses include a JSON object with:
```json
{
    "error": "Error Type",
    "message": "Detailed error message"
}
```

## Logging

Logs are written to `logs/app.log` with the following levels:
- INFO: Normal operations
- WARNING: Non-critical issues
- ERROR: Critical issues requiring attention

## Contributing

1. Create a feature branch
2. Make your changes
3. Add tests
4. Update documentation
5. Submit a pull request

## License

MIT License 
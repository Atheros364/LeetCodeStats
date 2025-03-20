**LeetCode Dashboard – Design Document**

Table of Contents

1. Overview
2. High-Level Architecture
3. Tech Stack
4. Data Model & Schema
5. Backend Services
6. Scheduling & Polling
7. API Endpoints
8. Frontend Design
9. Future Features & Roadmap
10. Deployment & Configuration
11. Logging & Error Handling
12. Security Considerations
13. Conclusion

1\. Overview

This project aims to create a personal dashboard that tracks your LeetCode activity and presents it via a React frontend. The system periodically fetches submission data from the LeetCode GraphQL API, stores it locally, and displays analytics on a dashboard. Features include:

- Tracking daily streaks, total questions solved by difficulty/tags, and daily submission heatmap.
- Storing submission metadata (code, runtime, memory, etc.).
- Recommending problems based on tags not recently practiced.
- Basic search/filter capabilities by date, difficulty, and tag (planned for future).

Since this is a personal project, it will be single-user and run locally. No login flow is required, and credentials are kept in a local .env file.

2\. High-Level Architecture


1. Backend (FastAPI)
    - A scheduler (APScheduler or background task) polls the LeetCode GraphQL API.
    - Data is stored locally in a database (e.g., SQLite or PostgreSQL).
    - REST endpoints serve submission data, metadata, and aggregated statistics to the frontend.
2. Frontend (React)
    - A modern, flat, red-themed UI.
    - Displays current streak, number of questions solved by difficulty/tag, daily heatmap, and basic charts.

3\. Tech Stack

- Language: Python 3.x
- Backend Framework: FastAPI
- Database: SQLite
- Scheduler: APScheduler or FastAPI background tasks
- Frontend: React using an open-source UI library—Material UI
- Styling/Theming: Any CSS solution or theming approach in React (e.g., styled-components, CSS modules, or library-based theming)

Rationale

- FastAPI: Lightweight, modern, async-friendly, and easy to set up for local usage.
- SQLite: Simple local database with zero external dependencies, sufficient for a single-user project.
- React: Flexible, widely used, and has an extensive ecosystem of component libraries for charts and UI elements.

4\. Data Model & Schema

4.1 Database Schema

Check DatabaseSchema.md for the schema

5\. Backend Services

5.1 FastAPI Structure

A possible FastAPI project layout:

backend/

├── main.py

├── database.py

├── models.py (SQLAlchemy models)

├── crud.py (functions to interact with the DB)

├── schemas.py (Pydantic schemas)

├── routers/


│ ├── recommendations.py

│ └── stats.py

├── polling/

│ └── scheduler.py

└── .env

5.2 SQLAlchemy Models

TODO

5.3 CRUD Methods

- Create/Update: Insert new submissions, upsert question metadata.
- Read:
  - Get all submissions in a date range.
  - Get questions by tag/difficulty for recommendation.
  - Aggregate daily submission counts.

5.4 Polling the LeetCode API

- In scheduler.py, implement a function that logs into LeetCode GraphQL, fetches recent submissions, and stores them in DB.
- Poll every 5 minutes (via APScheduler).


- APScheduler:

TODO

7\. API Endpoints

See APIDesign.md for endpoints

8\. Frontend Design

8.1 Framework & Layout

- React app with a single-page structure.
- UI Library: Material UI.
- Theming: Red-based palette with modern flat design.

8.2 Pages / Components

1. Dashboard Page
    - Header: Displays current streak, total questions answered.
    - Charts:
        - Pie Chart for difficulty distribution in selected timeframe.
        - Bar Chart for tag distribution in selected timeframe.
    - Heatmap Calendar:
        - Shows daily submission count.
        - Clicking a day could show a popup with submissions made on that day (if desired).
2. Time Interval Selector
    - A control (range date picker) to update the dashboard.
    - When changed, triggers an API call with start_date/end_date and updates the charts/heatmap.
3. Recommendation List
    - On the dashboard or a separate page, show 4–8 recommended questions by rarely practiced tags.

8.3 Theming & Style

- Use a consistent red-based color scheme for primary actions/menus.
- Keep a flat UI style (Material design).



10\. Deployment & Configuration

- Local Deployment
  - Install dependencies via requirements.txt.
  - Use a .env file to store:
    - LeetCode credentials / session token
    - Database connection string (e.g., sqlite:///local.db)
    - Timezone settings

Example .env:

LEETCODE_USERNAME=myusername

LEETCODE_PASSWORD=mypassword

DATABASE_URL=sqlite:///local.db

TIMEZONE=America/Phoenix  

- Run
    1. Initialize DB: alembic upgrade head or custom DB init script.
    2. Start FastAPI: uvicorn main:app --reload.
    3. Start React dev server: npm start (or yarn start).

11\. Logging & Error Handling

- Local Logs
  - Use Python’s logging module or a library like loguru.
  - Write logs to a local file, e.g., logs/app.log.
  - Each poll attempt logs success or failure.
- Error Handling
  - If an API call to LeetCode fails, log the error and skip until next poll.
  - For user-facing errors (e.g., 500 from the backend), return a descriptive JSON error to the frontend.


12\. Conclusion

This design document provides a detailed plan for building your personal LeetCode dashboard. The system retrieves submissions from the LeetCode GraphQL API every few minutes, stores them locally, and uses a React frontend to visualize progress, streaks, and question statistics. The recommended next steps are to:

1. Set up the project structure, DB, and FastAPI skeleton.
2. Implement the polling logic and test retrieving real submission data.
3. Develop the frontend with a cohesive red-themed design and charts.
4. Iterate with additional features like code search, advanced recommendations, and eventually the LLM integration.

By following this specification, you can create a robust local application that tracks, visualizes, and guides your LeetCode practice journey.
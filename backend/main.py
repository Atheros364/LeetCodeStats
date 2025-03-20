from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .routers import stats, recommendations
from .database import init_db
from .leetcode import LeetCodeService

# Create LeetCode service instance
leetcode_service = LeetCodeService()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    await leetcode_service.start()
    yield
    # Shutdown
    await leetcode_service.stop()

app = FastAPI(
    title="LeetCode Stats API",
    description="API for tracking LeetCode progress and statistics",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(stats.router, prefix="/api/v1/stats", tags=["stats"])
app.include_router(recommendations.router,
                   prefix="/api/v1/recommendations", tags=["recommendations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

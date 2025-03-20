from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .setup_logging import setup_logging
from .config import settings
from .leetcode.service import LeetCodeService
from .routers import stats, recommendations

# Set up logging first
setup_logging()

# Create FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize LeetCode service
leetcode_service = LeetCodeService()

# Include routers
app.include_router(stats.router, prefix=settings.API_V1_PREFIX)
app.include_router(recommendations.router, prefix=settings.API_V1_PREFIX)


@app.on_event("startup")
async def startup_event():
    """Start the LeetCode service on application startup."""
    await leetcode_service.start()


@app.on_event("shutdown")
async def shutdown_event():
    """Stop the LeetCode service on application shutdown."""
    await leetcode_service.stop()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Get the backend directory path
BACKEND_DIR = Path(__file__).parent

# Get the database URL from environment or use default
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    # If DATABASE_URL is set, ensure it's an absolute path
    if DATABASE_URL.startswith("sqlite+aiosqlite:///./"):
        # Convert relative path to absolute
        relative_path = DATABASE_URL.replace("sqlite+aiosqlite:///./", "")
        DATABASE_URL = f"sqlite+aiosqlite:///{BACKEND_DIR / relative_path}"
else:
    # Default to bin/leetcode_stats.db in the backend directory
    DATABASE_URL = f"sqlite+aiosqlite:///{BACKEND_DIR / 'bin' / 'leetcode_stats.db'}"

# Create the database directory if it doesn't exist
db_path = Path(DATABASE_URL.replace("sqlite+aiosqlite:///", ""))
db_path.parent.mkdir(parents=True, exist_ok=True)

engine = create_async_engine(DATABASE_URL, echo=True)
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

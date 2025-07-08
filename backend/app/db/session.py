"""
Database session configuration for ValidateIO.

Handles database connections and session management.
Supports both local PostgreSQL and Supabase.
"""

from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.logging import logger

# Configure database URL
def get_database_url() -> str:
    """Get the appropriate database URL based on configuration."""
    if settings.DATABASE_URL:
        db_url = str(settings.DATABASE_URL)
        # Convert postgresql:// to postgresql+asyncpg:// for async support
        if db_url.startswith("postgresql://"):
            db_url = db_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return db_url
    else:
        # Fallback to local PostgreSQL
        return "postgresql+asyncpg://postgres:postgres@localhost/validateio"

# Create async engine
database_url = get_database_url()
logger.info(f"Connecting to database: {database_url.split('@')[1] if '@' in database_url else database_url}")

engine = create_async_engine(
    database_url,
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,  # Enable connection health checks
    pool_size=5,  # Connection pool size
    max_overflow=10,  # Maximum overflow connections
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to get database session.
    
    Yields:
        Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
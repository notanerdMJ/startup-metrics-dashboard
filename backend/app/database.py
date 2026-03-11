# backend/app/database.py
"""
Database connection and session management.
SQLAlchemy handles the PostgreSQL connection pool.
Each API request gets its own database session via dependency injection.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# Create the SQLAlchemy engine
# pool_pre_ping=True ensures dead connections are recycled
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG  # Log SQL queries in debug mode
)

# SessionLocal class — each instance is a database session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all ORM models
Base = declarative_base()


def get_db():
    """
    Dependency injection for FastAPI routes.
    Yields a database session, ensures it closes after the request.

    Usage in routes:
        @router.get("/items")
        def get_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
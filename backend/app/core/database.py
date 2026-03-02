from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from backend.app.core.config import settings


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    All SQLAlchemy models should inherit from this class
    to ensure proper table metadata is registered.
    """
    pass


def _engine_kwargs() -> dict:
    """
    Returns engine-specific keyword arguments based on the database type.

    SQLite requires 'check_same_thread=False' for multithreaded access.
    Other databases do not need special arguments.
    """
    if settings.database_url.startswith("sqlite"):
        return {"connect_args": {"check_same_thread": False}}
    return {}


# Create the SQLAlchemy engine
# pool_pre_ping=True ensures the connection is validated before use
# future=True enables SQLAlchemy 2.0 style behaviors
engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    future=True,
    **_engine_kwargs(),
)

# Create a session factory bound to the engine
# autoflush=False prevents automatic flushing before queries
# autocommit=False requires explicit commit() calls
SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    class_=Session,
)


def get_db() -> Generator[Session, None, None]:
    """
    Dependency generator for FastAPI routes to provide a database session.

    Usage:
        db: Session = Depends(get_db)

    Yields:
        Session: SQLAlchemy session instance

    Ensures:
        - The session is closed after the request to release connections.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
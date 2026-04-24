from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_engine = None
_session_local = None


def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        if not settings.database_url:
            raise RuntimeError("DATABASE_URL is not configured")
        _engine = create_engine(settings.database_url, pool_pre_ping=True)
    return _engine


def get_session_local():
    global _session_local
    if _session_local is None:
        _session_local = sessionmaker(bind=get_engine(), autoflush=False, autocommit=False, class_=Session)
    return _session_local


def get_db() -> Generator[Session, None, None]:
    db = get_session_local()()
    try:
        yield db
    finally:
        db.close()

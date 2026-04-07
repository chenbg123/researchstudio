from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.gateway.config import get_gateway_config

_engine = None
_SessionLocal = None


def _get_engine():
    global _engine
    if _engine is None:
        config = get_gateway_config()
        _engine = create_engine(config.database_url, future=True, pool_pre_ping=True)
    return _engine


def get_session_factory():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(bind=_get_engine(), autoflush=False, autocommit=False, class_=Session)
    return _SessionLocal


def get_db_session() -> Generator[Session, None, None]:
    factory = get_session_factory()
    db = factory()
    try:
        yield db
    finally:
        db.close()

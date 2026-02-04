from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from infrastructure.config import settings


class Base(DeclarativeBase):
    pass


def get_engine():
    return create_engine(settings.database_url, pool_pre_ping=True)


def get_session_factory():
    engine = get_engine()
    return sessionmaker(bind=engine, autocommit=False, autoflush=False)


SessionLocal = get_session_factory()

import os
from typing import Generator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import sessionmaker, Session, DeclarativeBase


class Base(DeclarativeBase):
    pass


def create_db_engine(db_url: str | None = None) -> Engine:
    url = db_url or os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@db:5432/postgres",
    )

    if not url:
        raise RuntimeError("DATABASE_URL not set")

    return create_engine(
        url,
        pool_pre_ping=True,
    )


engine: Engine = create_db_engine()

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

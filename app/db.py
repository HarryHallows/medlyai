import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@db:5432/postgres"
)


# Use NullPool in short-lived containers/tests to avoid "too many connections"
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Setting autocommit / autoflush to avoid inconsistent behaviour
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = declarative_base()


def get_db():
    """
    FastAPI dependency: yields a DB Session, then ensures that it's closed.
    """

    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()

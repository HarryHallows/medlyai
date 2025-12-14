from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base


class Unit(Base):
    __tablename__ = "Units"

    id = Column(Integer, primary_key=True)
    unit_id = Column(String, unique=True, index=True)
    title = Column(String)

    source = Column(String)
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)


class Topics(Base):
    __tablename__ = "topics"

    id = Column(Integer, primary_key=True)
    topic_id = Column(String, unique=True, index=True)

    unit_id = Column(ForeignKey("units.id"), idex=True)
    title = Column(String)

    source = Column(String)
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True)
    lesson_id = Column(String, unique=True, index=True)
    title = Column(String)

    unit_id = Column(ForeignKey("units.id"), index=True)
    topic_id = Column(ForeignKey("topics.id"), index=True)

    source = Column(String)
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)


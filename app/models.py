from sqlalchemy import String, Integer, ForeignKey, Text, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum
import uuid

from app.db import Base


class SourceType(enum.Enum):
    EXAM = "exam"
    PRACTICE = "practice"


class AttemptType(enum.Enum):
    EXAM = "exam"
    PRACTICE = "practice"


class User(Base):
    __tablename__ = "users"

    firebase_uid: Mapped[str] = mapped_column(String, primary_key=True)
    metadata_jsonb: Mapped[dict] = mapped_column(JSONB, default=dict)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    attempts = relationship("UserAttempt", back_populates="user")


class UserAttempt(Base):
    __tablename__ = "user_attempts"

    attempt_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.firebase_uid"), nullable=False
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("items.question_id"), nullable=False
    )

    attempt_type: Mapped[AttemptType] = mapped_column(Enum(AttemptType), nullable=False)

    score: Mapped[int] = mapped_column(Integer, nullable=False)
    max_score: Mapped[int] = mapped_column(Integer, nullable=False)

    started_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    submitted_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    metadata_jsonb: Mapped[dict] = mapped_column(JSONB, default=dict)

    user = relationship("User", back_populates="attempts")
    item = relationship("Item", back_populates="attempts")


class Lesson(Base):
    __tablename__ = "lessons"

    lesson_id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    unit: Mapped[str] = mapped_column(String, nullable=False)
    topic: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    items = relationship("LessonItem", back_populates="lesson")


class Paper(Base):
    __tablename__ = "papers"

    paper_id: Mapped[str] = mapped_column(String, primary_key=True)
    subject: Mapped[str] = mapped_column(String, nullable=False)
    series: Mapped[str] = mapped_column(String, nullable=False)
    tier: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    items = relationship("PaperItem", back_populates="paper")


class Item(Base):
    __tablename__ = "items"

    question_id: Mapped[str] = mapped_column(String, primary_key=True)
    text: Mapped[str] = mapped_column(Text, nullable=False)
    markscheme: Mapped[str] = mapped_column(Text, nullable=False)
    difficulty: Mapped[int] = mapped_column(Integer, nullable=False)

    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType), nullable=False)
    source_ref: Mapped[str] = mapped_column(String, nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    lesson_links = relationship("LessonItem", back_populates="item")
    paper_links = relationship("PaperItem", back_populates="item")
    attempts = relationship("UserAttempt", back_populates="item")


class LessonItem(Base):
    __tablename__ = "lesson_items"

    lesson_id: Mapped[str] = mapped_column(
        ForeignKey("lessons.lesson_id"), primary_key=True
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("items.question_id"), primary_key=True
    )

    order_index: Mapped[int] = mapped_column(Integer, nullable=False)

    lesson = relationship("Lesson", back_populates="items")
    item = relationship("Item", back_populates="lesson_links")


class PaperItem(Base):
    __tablename__ = "paper_items"

    paper_id: Mapped[str] = mapped_column(
        ForeignKey("papers.paper_id"), primary_key=True
    )
    question_id: Mapped[str] = mapped_column(
        ForeignKey("items.question_id"), primary_key=True
    )

    question_number: Mapped[str] = mapped_column(String, nullable=False)

    paper = relationship("Paper", back_populates="items")
    item = relationship("Item", back_populates="paper_links")

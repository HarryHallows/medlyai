from datetime import UTC, datetime
from sqlalchemy import JSON, Boolean, Column, DateTime, Float, ForeignKey, Integer, String
from app.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String, unique=True, index=True, nullable=False)
    name = Column(String)
    
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC))


class UserAttempt(Base):
    __tablename__ = "user_attempts"

    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey("users.id"), index=True)

    question_id = Column(ForeignKey("questions.id"), index=True)
    question_appearance_id = Column(
        ForeignKey("question_appearances.id"),
        nullable=True,
        index=True,
    )

    is_correct = Column(Boolean, nullable=True)
    score = Column(Float, nullable=True)
    max_score = Column(Float, nullable=True)

    attempt_type = Column(String)  # "practice" | "exam"

    attempted_at = Column(DateTime, index=True)
    metadata_json = Column(JSON)


class UserQuestionStat(Base):
    __tablename__ = "user_question_stats"

    id = Column(Integer, primary_key=True)

    user_id = Column(ForeignKey("users.id"), index=True)
    question_id = Column(ForeignKey("questions.id"), index=True)

    attempts = Column(Integer)
    correct_attempts = Column(Integer)

    last_attempt_at = Column(DateTime)
    mastery_score = Column(Float)

    updated_at = Column(DateTime)


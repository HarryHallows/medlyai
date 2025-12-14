from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB

from app.db import Base


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)

    question_id = Column(String, unique=True, index=True) # external key
    text = Column(Text, nullable=True)

    markscheme = Column(Text, nullable=True)
    difficulty = Column(Integer, nullable=True)
    max_marks = Column(Integer, nullable=True)

    source = Column(String) # exams / practices
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)


class Paper(Base):
    __tablename__ = "papers"

    id = Column(Integer, primary_key=True)

    paper_id = Column(String, unique=True, index=True)
    board = Column(String)
    qualification = Column(String)
    subject = Column(String)
    series = Column(String)
    tier = Column(String)

    source = Column(String)
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)
    

class PracticeBank(Base):
    __tablename__ = "practice_banks"

    id = Column(Integer, primary_key=True)

    practice_id = Column(String, unique=True, index=True)
    lesson_id = Column(ForeignKey("lessons.id"), index=True)

    source = Column(String)
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)


class QuestionAppearance(Base):
    __tablename__ = "question_appearances"

    id = Column(Integer, primary_key=True)

    question_id = Column(ForeignKey("questions.id"), index=True)

    paper_id = Column(ForeignKey("papers.id"), nullable=True, index=True)
    practice_bank_id = Column(ForeignKey("practice_banks.id"), nullable=True, index=True)

    order_index = Column(Integer, nullable=True)
    part_label = Column(String, nullable=True)

    source = Column(String)
    metadata_json = Column(JSONB)

    created_at = Column(DateTime)

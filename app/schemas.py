from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from app.models import AttemptType, SourceType


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class UserBase(ORMModel):
    firebase_uid: str
    metadata: dict = Field(alias="metadata_jsonb")


class UserResponse(UserBase):
    created_at: datetime
    updated_at: datetime


class UserAttemptResponse(ORMModel):
    attempt_id: UUID
    question_id: str
    attempt_type: AttemptType
    score: int
    max_score: int
    started_at: datetime
    submitted_at: datetime
    metadata: dict = Field(alias="metadata_jsonb")


class UserActivityResponse(ORMModel):
    user_id: str
    attempts: List[UserAttemptResponse]


class ItemResponse(ORMModel):
    question_id: str
    text: str
    markscheme: str
    difficulty: int
    source_type: SourceType
    source_ref: str


class LessonItemResponse(ORMModel):
    order_index: int
    item: ItemResponse


class LessonResponse(ORMModel):
    lesson_id: str
    name: str
    unit: str
    topic: str
    items: List[LessonItemResponse]


class PaperItemResponse(ORMModel):
    question_number: str
    item: ItemResponse


class PaperResponse(ORMModel):
    paper_id: str
    subject: str
    series: str
    tier: str
    items: List[PaperItemResponse]


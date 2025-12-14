from typing import Literal, Optional
from pydantic import BaseModel, ConfigDict


class LessonItemSummary(BaseModel):
    question_id: str
    source: Literal["practice", "exam"]


class LessonRead(BaseModel):
    lesson_id: str
    title: Optional[str] = None
    unit: Optional[str] = None
    topic: Optional[str] = None
    items: list[LessonItemSummary] = []

    model_config = ConfigDict(from_attributes=True)

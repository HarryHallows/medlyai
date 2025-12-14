from typing import Any, Optional
from pydantic import BaseModel, ConfigDict


class QuestionOccurrence(BaseModel):
    assessment_type: str
    assessment_id: str
    part_index: Optional[int] = None


class QuestionDetail(BaseModel):
    question_id: str
    mark_max: Optional[str] = None
    difficulty: Optional[str] = None
    content: dict[str, Any]
    appearences: list[QuestionOccurrence] = []

    model_config = ConfigDict(from_attributes=True)

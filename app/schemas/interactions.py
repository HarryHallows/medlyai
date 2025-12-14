from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserInteractionRead(BaseModel):
    question_id: str
    lesson_id: str | None
    paper_id: str | None
    subject: str | None

    is_marked: bool | None
    response_data: dict
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

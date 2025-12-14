from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class UserInteractionRead(BaseModel):
    question_id: str
    lesson_id: Optional[str] = None
    paper_id: Optional[str] = None
    subject: Optional[str] = None

    is_marked: Optional[bool] = None
    response_data: Dict[str, Any]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

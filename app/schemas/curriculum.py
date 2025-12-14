from pydantic import BaseModel, ConfigDict


class LessonItemSummary(BaseModel):
    question_id: str
    source: str # "practice" / "exam"


class LessonRead(BaseModel):
    lesson_id: str
    title: str | None = None
    unit: str | None = None
    topic: str | None = None
    items: list[LessonItemSummary] = []

    model_config = ConfigDict(from_attributes=True)

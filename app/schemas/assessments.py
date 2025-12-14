from pydantic import BaseModel, ConfigDict


class ItemAppearance(BaseModel):
    assessment_type: str
    assessment_id: str
    part_index: int | None = None


class ItemRead(BaseModel):
    question_id: str
    mark_max: str | None = None
    difficulty: str | None = None
    content: dict
    appearences: list[ItemAppearance] = []

    model_config = ConfigDict(from_attributes=True)

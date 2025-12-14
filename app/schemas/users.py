from datetime import datetime
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: str | None = None
    name: str | None = None
    metadata: dict | None = None


class UserRead(UserBase):
    id: int
    firebase_uid: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

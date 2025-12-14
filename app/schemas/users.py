from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel, ConfigDict


class UserBase(BaseModel):
    email: Optional[str] = None
    name: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UserRead(UserBase):
    id: int
    firebase_uid: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

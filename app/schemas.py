from pydantic import BaseModel


class UserOut(BaseModel):
    firebase_uid: str
    name: str | None
    metadata: dict | None

    class Config:
        orm_mode = True

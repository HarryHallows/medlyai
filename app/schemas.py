from pydantic import BaseModel


class UserOut(BaseModel):
    firebase_uid: str
    name: str | None

    class Config:
        from_attributes = True

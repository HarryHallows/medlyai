from datetime import UTC, datetime
from sqlalchemy import JSON, Column, DateTime, Integer, String
from app.db import Base


class User(Base):
    """
    {
        "users/05IsdAyoSnekvovtyr2fC5cNOnF3/subjectsWeb/aqaGCSEBio/mocks/medlymockaqaGCSEBio_Sept_Mock1Higher/questions/aqaGCSEBio_1_1_1_EBc0BgD11T": {
        "createdAt": "2025-09-15T07:53:09.441000+00:00",
        "questionID": "aqaGCSEBio_1_1_1_EBc0BgD11T",
        "canvas": {
            "maths": [],
            "paths": [],
            "textboxes": []
        },
        "isMarked": false
    },...
    """


    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    firebase_uid = Column(String, unique=True, index=True)
    name = Column(String)
    metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.now(UTC))
    updated_at = Column(DateTime, default=datetime.now(UTC))

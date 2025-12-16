from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db import get_db

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health(db: Session = Depends(get_db)):
    try:
        with db.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"status": "ok", "db": "ok"}
    except Exception as err:
        return {"status": "error", "db": str(err)}

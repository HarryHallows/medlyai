from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db
from app.models.users import User
from app.schemas.users import UserOut

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=UserOut)
def get_user(id: str, db: Session = Depends(get_db)):
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found in database")
    return user



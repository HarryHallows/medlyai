from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import SessionLocal, get_db
from app.models.users import User
from app.schemas.interactions import UserInteractionRead
from app.schemas.pagination import PaginatedResponse
from app.schemas.users import UserBase, UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{id}", response_model=UserRead)
def get_user(id: str, db: Session = Depends(get_db)) -> User:
    db: Session = SessionLocal()
    user = db.query(User).filter(User.id == id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found in database")
    return user


@router.get("/{user_id}/activity", response_model=PaginatedResponse[UserRead])
def get_user_activity(
    user_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    subject: str | None = None,
    paper_id: str | None = None,
    lesson_id: str | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(UserInteractionRead).filter(UserInteractionRead.user_id == user_id)

    if subject:
        query = query.filter(UserInteractionRead.subject == subject)
    
    if paper_id:
        query = query.filter(UserInteractionRead.paper_id == paper_id)

    if lesson_id:
        query = query.filter(UserInteractionRead.lesson_id == lesson_id)
    
    total = query.count()
    items = (
        query.order_by(UserInteractionRead.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
        .all()
    )

    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
    }


@router.patch("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int,
    payload: UserBase,
    db: Session = Depends(get_db)
) -> User:
    user = db.get(User, user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found in Database")
    
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.commit()
    db.refresh(user)
    return user


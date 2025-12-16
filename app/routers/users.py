from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import User, UserAttempt
from app.schemas import UserActivityResponse, UserBase, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: str, db: Session = Depends(get_db)) -> UserResponse:
    user = db.query(User).filter(User.firebase_uid == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user



@router.get("/{user_id}/activity", response_model=UserActivityResponse)
def user_activity(
    user_id: str,
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    subject: str | None = None,
    paper_id: str | None = None,
    lesson_id: str | None = None,
    db: Session = Depends(get_db),
) -> UserActivityResponse:
    offset = (page - 1) * size

    query = db.query(UserAttempt).filter(UserAttempt.user_id == user_id)

    if subject:
        query = query.filter(
            UserAttempt.metadata_jsonb["subject"].as_string() == subject
        )

    if paper_id:
        query = query.filter(
            UserAttempt.metadata_jsonb["paper_id"].as_string() == paper_id
        )

    if lesson_id:
        query = query.filter(
            UserAttempt.metadata_jsonb["lesson_id"].as_string() == lesson_id
        )

    attempts = (
        query.order_by(UserAttempt.submitted_at.desc()).offset(offset).limit(size).all()
    )

    # map to response schema
    response_attempts = [
        {
            "attempt_id": attempt.attempt_id,
            "question_id": attempt.question_id,
            "attempt_type": attempt.attempt_type,
            "score": attempt.score,
            "max_score": attempt.max_score,
            "started_at": attempt.started_at,
            "submitted_at": attempt.submitted_at,
            "metadata_jsonb": dict(attempt.metadata_jsonb or {}),
        }
        for attempt in attempts
    ]

    return {
        "user_id": user_id,
        "attempts": response_attempts,
    }


@router.patch("/{user_id}", response_model=UserResponse)
def update_user(user_id: str, payload: UserBase, db: Session = Depends(get_db)) -> UserResponse:
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404)

    if payload.metadata is not None:
        user.metadata_jsonb = payload.metadata

    db.commit()
    db.refresh(user)
    return user

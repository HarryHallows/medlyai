from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.curriculum import Lesson
from app.schemas.curriculum import LessonRead

router = APIRouter(prefix="/lessons", tags=["curriculum"])


@router.get("/{lesson_id}", response_model=LessonRead)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.lesson_id == lesson_id).first()

    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    return lesson


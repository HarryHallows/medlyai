from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db import get_db
from app.models import Item, Lesson, LessonItem, Paper, PaperItem
from app.schemas import ItemResponse, LessonItemResponse, LessonResponse, PaperItemResponse, PaperResponse

router = APIRouter()


@router.get("/lessons/{lesson_id}", response_model=LessonResponse)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)):
    lesson = db.get(Lesson, lesson_id)
    if not lesson:
        raise HTTPException(status_code=404)

    query = (
        select(Item)
        .join(LessonItem)
        .where(LessonItem.lesson_id == lesson_id)
        .order_by(LessonItem.order_index)
    )

    items = db.execute(query).scalars().all()

    lesson_items = [
        LessonItemResponse(
            order_index=i,
            item=ItemResponse(
                question_id=item.question_id,
                text=item.text,
                markscheme=item.markscheme,
                difficulty=item.difficulty,
                source_type=item.source_type,
                source_ref=item.source_ref,
            ),
        )
        for i, item in enumerate(items)
    ]

    return LessonResponse(
        lesson_id=lesson.lesson_id,
        name=lesson.name,
        unit=lesson.unit,
        topic=lesson.topic,
        items=lesson_items,
    )


@router.get("/papers/{paper_id}", response_model=PaperResponse)
def get_paper(paper_id: str, db: Session = Depends(get_db)):
    paper = db.get(Paper, paper_id)
    if not paper:
        raise HTTPException(status_code=404)

    query = (
        select(PaperItem, Item)
        .join(Item, PaperItem.question_id == Item.question_id)
        .where(PaperItem.paper_id == paper_id)
        .order_by(PaperItem.question_number)
    )

    results = db.execute(query).all()

    paper_items = [
        PaperItemResponse(
            question_number=paper_item.question_number,
            item=ItemResponse(
                question_id=item.question_id,
                text=item.text,
                markscheme=item.markscheme,
                difficulty=item.difficulty,
                source_type=item.source_type,
                source_ref=item.source_ref,
            ),
        )
        for paper_item, item in results
    ]

    return PaperResponse(
        paper_id=paper.paper_id,
        subject=paper.subject,
        series=paper.series,
        tier=paper.tier,
        items=paper_items,
    )


@router.get("/items/{question_id}", response_model=ItemResponse)
def get_item(question_id: str, db: Session = Depends(get_db)):
    item = db.get(Item, question_id)
    if not item:
        raise HTTPException(status_code=404)

    return ItemResponse(
        question_id=item.question_id,
        text=item.text,
        markscheme=item.markscheme,
        difficulty=item.difficulty,
        source_type=item.source_type,
        source_ref=item.source_ref,
    )
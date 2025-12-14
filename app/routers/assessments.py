from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.assessments import PracticeBank, Question, QuestionAppearance, Paper
from app.schemas.assessments import QuestionDetail, QuestionOccurrence

router = APIRouter(tags=["assessments"])


@router.get("/items/{paper_id}", response_model=QuestionDetail)
def get_question(question_id: str, db: Session = Depends(get_db)):
    question = db.query(Question).filter(Question.question_id == question_id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    
    appearances: list[QuestionAppearance] = []

    question_appearances = db.query(QuestionAppearance).filter(QuestionAppearance.question_id == question_id).all()

    for _question in question_appearances:
        if _question.paper_id:
            paper = db.query(Paper).filter(Paper.id == _question.paper_id).first()

            if paper:
                appearances.append(
                    QuestionOccurrence(
                        assessment_type="exam",
                        assessment_id=paper.paper_id,
                        part_index=_question.order_idex
                    )
                )

            if _question.practice_bank_id:
                practice = db.query(PracticeBank).filter(PracticeBank.id == _question.practice_bank_id).first()

                if practice:
                    appearances.append(
                        QuestionOccurrence(
                            assessment_type="practice",
                            assessment_id=practice.practice_id,
                            part_index=None
                        )
                    )

        return QuestionDetail(
            question_id=question.question_id,
            mark_max=question.max_marks,
            difficulty=question.difficulty,
            content={"text": question.text, **(question.metadata_json or {})},
            appearences=appearances
        )

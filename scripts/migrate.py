import json
import os
from typing import Any
from app.db import Base, SessionLocal, engine
from app.models import (
    User,
    Lesson,
    Item,
    LessonItem,
    Paper,
    PaperItem,
    SourceType,
)


# NOTE: Env variables should be configured within dedicated Config Class
USER_JSON_PATH = os.getenv("USER_DATA", "user_data/user_data.json")

CURRICULUM_COURSES_PATH = os.getenv(
    "CURRICULUM_COURSES", "curriculum_data/aqaGCSEBio_course.json"
)
CURRICULUM_EXAMS_PATH = os.getenv(
    "CURRICULUM_COURSES", "curriculum_data/aqaGCSEBio_exams.json"
)
CURRICULUM_PRACTICES_PATH = os.getenv(
    "CURRICULUM_COURSES", "curriculum_data/aqaGCSEBio_practices.json"
)


def extract_data(filepath: str) -> Any:
    with open(filepath, "r", encoding="utf-8") as file:
        data = json.load(file)
    return data


def migrate_users():
    data = extract_data(USER_JSON_PATH)
    targets = data.get("targets", {})

    with SessionLocal() as session:
        seen = set()
        created = 0

        for path in targets.keys():
            parts = path.split("/")
            if len(parts) < 2 or parts[0] != "users":
                continue

            uid = parts[1]
            if uid in seen:
                continue
            seen.add(uid)

            exists = session.get(User, uid)
            if exists:
                continue

            session.add(User(firebase_uid=uid, metadata={}))
            created += 1

        session.commit()
        print(f"Inserted {created} users")


def migrate_courses(course_data: list):
    with SessionLocal() as session:
        for unit in course_data:
            unit_title = unit.get("unitTitle")

            for topic in unit.get("topics", []):
                topic_title = topic.get("topicTitle")

                for lesson in topic.get("lessons", []):
                    lesson_id = lesson["lessonID"]

                    if session.get(Lesson, lesson_id):
                        continue

                    session.add(
                        Lesson(
                            lesson_id=lesson_id,
                            name=lesson.get("lessonTitle"),
                            unit=unit_title,
                            topic=topic_title,
                        )
                    )

        session.commit()


def migrate_practices(practices_data: list[dict[str, Any]]):
    with SessionLocal() as session:
        for practice in practices_data:
            lesson_id = practice["lessonID"]

            # 1. Ensure lesson exists
            lesson = session.get(Lesson, lesson_id)
            if not lesson:
                lesson = Lesson(
                    lesson_id=lesson_id,
                    name=practice.get("lesson_title", lesson_id),
                    unit=practice.get("unit_title", "unknown"),
                    topic=practice.get("topic_title", "unknown"),
                )
                session.add(lesson)
                session.flush()

            order_index = 0

            # 2. Iterate questions
            for question in practice.get("items", []):
                question_stem = question.get("question_stem", "")

                # 3. Iterate question parts → Items
                for part in question.get("items", []):
                    question_id = part["questionID"]

                    if session.get(Item, question_id):
                        continue

                    item = Item(
                        question_id=question_id,
                        text=f"{question_stem}\n\n{part.get('question_text', '')}",
                        markscheme=part.get("markscheme", ""),
                        difficulty=int(part.get("difficulty", 1)),
                        source_type=SourceType.PRACTICE,
                        source_ref=lesson_id,
                    )
                    session.add(item)

                    session.add(
                        LessonItem(
                            lesson_id=lesson_id,
                            question_id=question_id,
                            order_index=order_index,
                        )
                    )

                    order_index += 1

        session.commit()


def migrate_exams(exams_data: list):
    with SessionLocal() as session:
        
        # NOTE: If there were more than a single index in the dataset
            # Then this would be handled through iteration dynamically
        paper_subject = exams_data[0]["subject_title"]
        paper_series = exams_data[0]["series"]

        for paper_data in exams_data[0]["papers"]:
            paper_id = paper_data["paper_id"]
            paper_tier = paper_data["tier"]

            paper = session.get(Paper, paper_id)
            if not paper:
                paper = Paper(
                    paper_id=paper_id,
                    subject=paper_subject,
                    series=paper_series,
                    tier=paper_tier,
                )
                session.add(paper)
                session.flush()
            for question in paper_data["questions"]:
                question_stem = question["question_stem"]
                question_number = question["question_number"]
                for item_data in question["items"]:
                    question_id = item_data["questionID"]
                    if not session.get(Item, question_id):
                        session.add(
                            Item(
                                question_id=question_id,
                                text=question_stem,
                                markscheme=item_data.get("markscheme", ""),
                                difficulty=int(item_data.get("difficulty", 1)),
                                source_type=SourceType.EXAM,
                                source_ref=paper_id,
                            )
                        )

                    session.add(
                        PaperItem(
                            paper_id=paper_id,
                            question_id=question_id,
                            question_number=question_number,
                        )
                    )

        session.commit()


def run_migrations():
    Base.metadata.create_all(bind=engine)

    migrate_users()
    migrate_courses(extract_data(CURRICULUM_COURSES_PATH))
    migrate_practices(extract_data(CURRICULUM_PRACTICES_PATH))
    migrate_exams(extract_data(CURRICULUM_EXAMS_PATH))


if __name__ == "__main__":
    run_migrations()

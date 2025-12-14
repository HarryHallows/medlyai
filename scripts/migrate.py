import json
import os
from typing import Any

from app.db import Base, SessionLocal, engine
from app.models import users, curriculum

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
    print("USER MIGRATION STARTED")

    data = extract_data(USER_JSON_PATH)

    with SessionLocal() as session:
        count = 0
        skipped = 0

        targets = data.get("targets", {})
        print(f"Found {len(targets)} interaction records.")

        seen_uids = set()

        for path in targets.keys():
            parts = path.split("/")

            # "users/05IsdAyoSnekvovtyr2fC5cNOnF3/subjectsWeb/aqaGCSEBio/mocks/medlymockaqaGCSEBio_Sept_Mock1Higher/questions/aqaGCSEBio_1_1_1_EBc0BgD11T"
            if len(parts) < 2 or parts[0] != "users":
                skipped += 1
                continue

            firebase_uid = parts[1]
            if firebase_uid in seen_uids:
                continue

            seen_uids.add(firebase_uid)

            user_exists = (
                session.query(users.User)
                .filter(users.User.firebase_uid == firebase_uid)
                .first()
            )

            if user_exists:
                skipped += 1
                continue

            user = users.User(firebase_uid=firebase_uid)
            session.add(user)
            count += 1

    session.commit()
    print(f"Inserted {count} new users to database.")
    print(f"Skipped {skipped} existing/invalid users.")


def migrate_curriculum():
    print("CURRICULUM MIGRATION STARTED")

    course_data = extract_data(CURRICULUM_COURSES_PATH)
    exams_data = extract_data(CURRICULUM_EXAMS_PATH)
    practices_data = extract_data(CURRICULUM_PRACTICES_PATH)

    # ===== Courses =====
    _migrate_courses(course_data)
    
    # ===== Practice Banks =====
    _migrate_practices(practices_data)


    # ======= Papers and Questions =======
    _migrate_exams(exams_data)

def _migrate_courses(course_data: list):
    with SessionLocal() as session:
        unit_count = 0
        topic_count = 0
        lesson_count = 0

        for unit_obj in course_data:  # course_data is a list
            # Units
            unit = curriculum.Unit(
                unit_id=f"unit_{unit_obj['unitIndex']}",
                title=unit_obj.get("unitTitle"),
                source="course",
                metadata_json=unit_obj,
            )
            session.add(unit)
            session.flush()  # flush to get unit.id for FK
            unit_count += 1

            for topic_obj in unit_obj.get("topics", []):
                # Topics
                topic = curriculum.Topic(
                    topic_id=f"topic_{unit_obj['unitIndex']}_{topic_obj['topicIndex']}",
                    unit_id=unit.id,
                    title=topic_obj.get("topicTitle"),
                    source="course",
                    metadata_json=topic_obj,
                )
                session.add(topic)
                session.flush()
                topic_count += 1

                for lesson_obj in topic_obj.get("lessons", []):
                    # Lessons
                    lesson = curriculum.Lesson(
                        lesson_id=lesson_obj.get("lessonID"),
                        title=lesson_obj.get("lessonTitle"),
                        unit_id=unit.id,
                        topic_id=topic.id,
                        source="course",
                        metadata_json=lesson_obj,
                    )
                    session.add(lesson)
                    lesson_count += 1

        session.commit()
        print(
            f"Inserted {unit_count} units, {topic_count} topics, {lesson_count} lessons."
        )

def _migrate_practices(practices_data: list):
    print("PRACTICES MIGRATION STARTED")
    with SessionLocal() as session:
        for practice in practices_data:
            lesson_id = practice.get("lessonID") or practice.get("original_lessonID")
            
            # Insert the lesson reference if needed
            lesson = session.query(curriculum.Lesson).filter_by(lesson_id=lesson_id).first()
            if not lesson:
                lesson = curriculum.Lesson(
                    lesson_id=lesson_id,
                    title=practice.get("lesson_title"),
                    unit_id=None,
                    topic_id=None,
                    source="practice",
                    metadata_json=practice
                )
                session.add(lesson)
        
        session.commit()
        print(f"Inserted {len(practices_data)} practice lessons.")


def _migrate_exams(exams_data: list):
    print(f"Found {len(exams_data)} exam lessons.")
    inserted_lessons = 0
    inserted_questions = 0

    for lesson in exams_data:
        lesson_id: str = lesson.get("lessonID") or lesson.get("original_lessonID")
        lesson_title: str = lesson.get("lesson_title")
        unit_title: str = lesson.get("unit_title")
        topic_title: str = lesson.get("topic_title")

        # Insert the lesson
        _insert_lesson(unit_title, topic_title, lesson_title, lesson_id)
        inserted_lessons += 1

        for item in lesson.get("items", []):  # each question
            question_number = item.get("question_number")
            question_stem = item.get("question_stem")
            validation_comment = item.get("validation_comment")
            validation_reason = item.get("validation_reason")
            question_id = item.get("question_id")

            # Insert the question
            _insert_question(
                lesson_id=lesson_id,
                question_number=question_number,
                question_stem=question_stem,
                validation_comment=validation_comment,
                validation_reason=validation_reason,
                question_id=question_id
            )
            inserted_questions += 1

            # Insert question parts
            for part in item.get("items", []):
                part_number = part.get("question_part")
                part_type = part.get("question_type")
                part_text = part.get("question_text")
                markmax = part.get("markmax")
                markscheme = part.get("markscheme")
                difficulty = part.get("difficulty")
                specification_point = part.get("specification_point")
                part_id = part.get("questionID")

                _insert_question_part(
                    question_id=question_id,
                    part_number=part_number,
                    part_type=part_type,
                    part_text=part_text,
                    markmax=markmax,
                    markscheme=markscheme,
                    difficulty=difficulty,
                    specification_point=specification_point,
                    part_id=part_id
                )

    print(f"Inserted {inserted_lessons} lessons and {inserted_questions} questions.")

def _insert_lesson(
    unit_title: str,
    topic_title: str,
    lesson_title: str,
    lesson_id: str,
    chunks_used=None,
):
    with SessionLocal() as session:
        # Check if lesson already exists
        existing = session.query(curriculum.Lesson).filter_by(lesson_id=lesson_id).first()
        if existing:
            return existing

        # Insert or get unit
        unit = session.query(curriculum.Unit).filter_by(title=unit_title).first()
        if not unit and unit_title:
            unit = curriculum.Unit(unit_id=f"unit_{unit_title}", title=unit_title, source="exam")
            session.add(unit)
            session.flush()

        # Insert or get topic
        topic = session.query(curriculum.Topic).filter_by(title=topic_title).first()
        if not topic and topic_title:
            topic = curriculum.Topic(
                topic_id=f"topic_{unit_title}_{topic_title}",
                title=topic_title,
                unit_id=unit.id if unit else None,
                source="exam"
            )
            session.add(topic)
            session.flush()

        # Insert lesson
        lesson = curriculum.Lesson(
            lesson_id=lesson_id,
            title=lesson_title,
            unit_id=unit.id if unit else None,
            topic_id=topic.id if topic else None,
            source="exam",
            metadata_json={},
        )
        session.add(lesson)
        session.commit()
        return lesson


def _insert_question(
    lesson_id: str,
    question_number: int,
    question_stem: str,
    validation_comment: str,
    validation_reason: str,
    question_id: str,
):
    with SessionLocal() as session:
        existing = session.query(curriculum.Question).filter_by(question_id=question_id).first()
        if existing:
            return existing

        question = curriculum.Question(
            question_id=question_id,
            lesson_id=lesson_id,
            question_number=question_number,
            question_stem=question_stem,
            validation_comment=validation_comment,
            validation_reason=validation_reason,
            metadata_json={}
        )
        session.add(question)
        session.commit()
        return question


def _insert_question_part(
    question_id: str,
    part_number: int,
    part_type: str,
    part_text: str,
    markmax: int,
    markscheme: str,
    difficulty: str,
    specification_point: str,
    part_id: str,
):
    with SessionLocal() as session:
        existing = session.query(curriculum.QuestionPart).filter_by(part_id=part_id).first()
        if existing:
            return existing

        part = curriculum.QuestionPart(
            part_id=part_id,
            question_id=question_id,
            part_number=part_number,
            part_type=part_type,
            part_text=part_text,
            markmax=markmax,
            markscheme=markscheme,
            difficulty=difficulty,
            specification_point=specification_point,
            metadata_json={}
        )
        session.add(part)
        session.commit()
        return part


def run_migrations():
    print("MIGRATIONS STARTED")
    # Ensure all tables exist
    Base.metadata.create_all(bind=engine)

    # Migrate Users
    migrate_users()

    # Migrate Curriculum
    migrate_curriculum()


if __name__ == "__main__":
    run_migrations()

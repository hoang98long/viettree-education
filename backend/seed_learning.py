"""Seed a small, usable learning slice for local development."""
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from app.core.config import get_settings
from app.models.exercise import Difficulty as ExerciseDifficulty, Exercise, Question, QuestionOption, QuestionType
from app.models.learning import Course, Difficulty as LessonDifficulty, Lesson, Subject

settings = get_settings()
engine = create_engine(settings.database_url)


def seed_learning() -> None:
    with Session(engine) as db:
        math_subjects = db.scalars(select(Subject).where(Subject.code.in_(["MATH", "math"]))).all()
        subject = next((item for item in math_subjects if item.code == "MATH"), math_subjects[0] if math_subjects else None)
        if not subject:
            subject = Subject(code="MATH", name="Toán", description="Toán lớp 1", display_order=1, is_active=True)
            db.add(subject)
            db.flush()
        subject.is_active = True
        for duplicate in db.scalars(
            select(Subject).where(Subject.name == subject.name, Subject.id != subject.id)
        ).all():
            duplicate.is_active = False

        course = db.scalar(select(Course).where(Course.subject_id == subject.id, Course.grade == 1))
        if not course:
            course = Course(
                subject_id=subject.id,
                grade=1,
                title="Toán lớp 1",
                description="Làm quen với các phép tính trong phạm vi 10.",
                display_order=1,
                is_published=True,
            )
            db.add(course)
            db.flush()
        else:
            course.title = course.title or "Toán lớp 1"
            course.description = course.description or "Làm quen với các phép tính trong phạm vi 10."
            course.is_published = True
            course.display_order = course.display_order or 1

        lesson = db.scalar(select(Lesson).where(Lesson.course_id == course.id, Lesson.lesson_number == 1))
        if not lesson:
            lesson = Lesson(
                course_id=course.id,
                title="Phép cộng trong phạm vi 10",
                description="Học cách cộng hai số có tổng không vượt quá 10.",
                lesson_number=1,
                estimated_minutes=10,
                difficulty=LessonDifficulty.EASY,
                is_published=True,
            )
            db.add(lesson)
            db.flush()
        else:
            lesson.is_published = True
            lesson.estimated_minutes = lesson.estimated_minutes or 10

        exercise = db.scalar(select(Exercise).where(Exercise.lesson_id == lesson.id))
        if not exercise:
            exercise = Exercise(
                lesson_id=lesson.id,
                title="Thực hành phép cộng",
                description="Chọn đáp án đúng cho mỗi phép tính.",
                difficulty=ExerciseDifficulty.EASY,
                points=3,
                display_order=1,
                is_active=True,
            )
            db.add(exercise)
            db.flush()

            questions = [
                ("2 + 3 bằng bao nhiêu?", ["4", "5", "6"], 1),
                ("1 + 6 bằng bao nhiêu?", ["6", "7", "8"], 1),
                ("4 + 4 bằng bao nhiêu?", ["7", "8", "9"], 1),
            ]
            for index, (text, options, correct_index) in enumerate(questions, start=1):
                question = Question(
                    exercise_id=exercise.id,
                    question_type=QuestionType.SINGLE_CHOICE,
                    question_text=text,
                    explanation="Em đã chọn đúng phép tính.",
                    hint="Hãy đếm lần lượt từ số đầu tiên.",
                    difficulty=ExerciseDifficulty.EASY,
                    points=1,
                    display_order=index,
                )
                db.add(question)
                db.flush()
                for option_index, option_text in enumerate(options, start=1):
                    db.add(QuestionOption(
                        question_id=question.id,
                        option_text=option_text,
                        option_value=option_text,
                        is_correct=option_index - 1 == correct_index,
                        display_order=option_index,
                    ))

        other_subjects = {
            "VN": (["VN", "vietnamese"], "Tiếng Việt", "Luyện đọc và nhận biết vần cơ bản.", "Đọc hiểu: Vần an, ang", "Chọn tiếng có vần an.", ["bàn", "bóng", "cá"]),
            "EN": (["EN", "english"], "Tiếng Anh", "Làm quen với từ vựng tiếng Anh gần gũi.", "My family", "Từ nào có nghĩa là mẹ?", ["mother", "book", "school"]),
        }
        for code, (codes, name, subject_description, lesson_title, question_text, options) in other_subjects.items():
            matching_subjects = db.scalars(select(Subject).where(Subject.code.in_(codes))).all()
            other_subject = next((item for item in matching_subjects if item.code == code), matching_subjects[0] if matching_subjects else None)
            if not other_subject:
                other_subject = Subject(
                    code=code,
                    name=name,
                    description=subject_description,
                    display_order=2 if code == "VN" else 3,
                    is_active=True,
                )
                db.add(other_subject)
                db.flush()
            other_subject.is_active = True
            for duplicate in db.scalars(
                select(Subject).where(Subject.name == name, Subject.id != other_subject.id)
            ).all():
                duplicate.is_active = False

            other_course = db.scalar(
                select(Course).where(Course.subject_id == other_subject.id, Course.grade == 1)
            )
            if not other_course:
                other_course = Course(
                    subject_id=other_subject.id,
                    grade=1,
                    title=f"{name} lớp 1",
                    description=subject_description,
                    display_order=1,
                    is_published=True,
                )
                db.add(other_course)
                db.flush()
            else:
                other_course.is_published = True

            other_lesson = db.scalar(
                select(Lesson).where(Lesson.course_id == other_course.id, Lesson.lesson_number == 1)
            )
            if not other_lesson:
                other_lesson = Lesson(
                    course_id=other_course.id,
                    title=lesson_title,
                    description=subject_description,
                    lesson_number=1,
                    estimated_minutes=10,
                    difficulty=LessonDifficulty.EASY,
                    is_published=True,
                )
                db.add(other_lesson)
                db.flush()
            else:
                other_lesson.is_published = True

            other_exercise = db.scalar(select(Exercise).where(Exercise.lesson_id == other_lesson.id))
            if not other_exercise:
                other_exercise = Exercise(
                    lesson_id=other_lesson.id,
                    title=f"Thực hành {name}",
                    description="Chọn đáp án đúng để luyện tập.",
                    difficulty=ExerciseDifficulty.EASY,
                    points=1,
                    display_order=1,
                    is_active=True,
                )
                db.add(other_exercise)
                db.flush()
                question = Question(
                    exercise_id=other_exercise.id,
                    question_type=QuestionType.SINGLE_CHOICE,
                    question_text=question_text,
                    explanation="Em đã chọn đúng đáp án.",
                    hint="Đọc kỹ từng lựa chọn.",
                    difficulty=ExerciseDifficulty.EASY,
                    points=1,
                    display_order=1,
                )
                db.add(question)
                db.flush()
                for option_index, option_text in enumerate(options):
                    db.add(QuestionOption(
                        question_id=question.id,
                        option_text=option_text,
                        option_value=option_text,
                        is_correct=option_index == 0,
                        display_order=option_index + 1,
                    ))

        db.commit()
        print(f"Learning data ready: course={course.id}, lesson={lesson.id}, exercise={exercise.id}")


if __name__ == "__main__":
    seed_learning()

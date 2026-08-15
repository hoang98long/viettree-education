"""Seed initial data for VietTree Education."""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings
from app.core.database import Base
from app.models.learning import Grade, Subject, Course, Lesson, LessonContent

settings = get_settings()
engine = create_engine(settings.database_url)
SessionLocal = sessionmaker(bind=engine)


def seed_data():
    """Seed initial grades, subjects, courses, and lessons."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    # Clear existing data
    db.query(LessonContent).delete()
    db.query(Lesson).delete()
    db.query(Course).delete()
    db.query(Subject).delete()
    db.query(Grade).delete()
    db.commit()

    # Seed Grades
    grades = [
        Grade(code="G1", name="Lớp 1"),
        Grade(code="G2", name="Lớp 2"),
        Grade(code="G3", name="Lớp 3"),
        Grade(code="G4", name="Lớp 4"),
        Grade(code="G5", name="Lớp 5"),
    ]
    db.add_all(grades)
    db.commit()

    # Seed Subjects
    subjects = [
        Subject(code="MATH", name="Toán", color="#FF9500", is_active=True),
        Subject(code="VN", name="Tiếng Việt", color="#8B4789", is_active=True),
        Subject(code="EN", name="Tiếng Anh", color="#0051BA", is_active=True),
    ]
    db.add_all(subjects)
    db.commit()

    # Seed Courses for Math Grade 1
    math_course_g1 = Course(
        subject_id=subjects[0].id,
        grade_id=grades[0].id,
        title="Toán Lớp 1",
        status="published",
        position=1,
    )
    db.add(math_course_g1)
    db.commit()

    # Seed Lessons for Math Course
    lessons = [
        Lesson(
            course_id=math_course_g1.id,
            title="Phép cộng trong phạm vi 10",
            description="Học cách cộng hai số có tổng không vượt quá 10",
            status="published",
            position=1,
        ),
        Lesson(
            course_id=math_course_g1.id,
            title="Phép trừ trong phạm vi 10",
            description="Học cách trừ hai số trong phạm vi 10",
            status="published",
            position=2,
        ),
    ]
    db.add_all(lessons)
    db.commit()

    # Seed Lesson Contents (blocks)
    blocks = [
        LessonContent(
            lesson_id=lessons[0].id,
            block_type="explanation",
            position=1,
            data={
                "title": "Cộng trong phạm vi 10",
                "body": "Phép cộng là tính tổng của hai số. Ví dụ: 2 + 3 = 5",
            },
        ),
        LessonContent(
            lesson_id=lessons[0].id,
            block_type="image",
            position=2,
            data={
                "fileId": "math-addition-visual",
                "alt": "Hình ảnh minh họa phép cộng với que tính",
            },
        ),
        LessonContent(
            lesson_id=lessons[0].id,
            block_type="exercise",
            position=3,
            data={"exerciseId": "exercise-addition-1", "title": "Thực hành cộng"},
        ),
    ]
    db.add_all(blocks)
    db.commit()

    print("✅ Seed data created successfully!")
    print(f"   Grades: {len(grades)}")
    print(f"   Subjects: {len(subjects)}")
    print(f"   Courses: 1")
    print(f"   Lessons: {len(lessons)}")
    print(f"   Blocks: {len(blocks)}")
    db.close()


if __name__ == "__main__":
    seed_data()

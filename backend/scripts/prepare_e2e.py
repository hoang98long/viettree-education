"""Tạo người dùng/lớp riêng cho browser tests, tuyệt đối không chạy trên DB thật."""

import json
from uuid import uuid4

from app.core.config import settings
from app.core.security import hasher, now
from app.db import db, engine


def main():
    name = engine().url.database
    if name == "viettree-education" or "test" not in name.lower():
        raise RuntimeError("Chỉ được tạo fixture trên database test riêng")
    output = {}
    with engine().begin() as conn:
        db.load(conn)

        def user(key, role="student", grade=4):
            identifier = uuid4()
            username = "e2e-" + identifier.hex
            conn.execute(
                db.table("users")
                .insert()
                .values(
                    id=identifier,
                    username=username,
                    display_name="Kiểm thử " + role,
                    password_hash=hasher.hash(settings().seed_student_password),
                )
            )
            conn.execute(db.table("user_roles").insert().values(user_id=identifier, role=role))
            if role == "student":
                conn.execute(
                    db.table("student_profiles")
                    .insert()
                    .values(student_id=identifier, current_grade=grade)
                )
            output[key] = username
            return identifier

        for key in [
            "E2E_CURRICULUM_USERNAME",
            "E2E_CURRICULUM_MOBILE_USERNAME",
            "E2E_STUDENT_USERNAME",
            "E2E_VIP_STUDENT_USERNAME",
            "E2E_VIP_MOBILE_STUDENT_USERNAME",
            "E2E_VIP_TOOLS_USERNAME",
            "E2E_VIP_TOOLS_MOBILE_USERNAME",
            "E2E_LESSON_USERNAME",
            "E2E_LESSON_MOBILE_USERNAME",
            "E2E_AUTHORING_STUDENT_USERNAME",
        ]:
            user(key)
        for key in ["E2E_GRADE3_USERNAME", "E2E_GRADE3_MOBILE_USERNAME"]:
            user(key, grade=3)
        teacher = user("E2E_ACADEMY_TEACHER_USERNAME", "teacher")
        guardian = user("E2E_ACADEMY_GUARDIAN_USERNAME", "guardian")
        for project in ["DESKTOP", "MOBILE"]:
            student = user("E2E_ACADEMY_" + project + "_USERNAME")
            class_id = uuid4()
            conn.execute(
                db.table("classes")
                .insert()
                .values(
                    id=class_id,
                    code="AI-E2E-" + class_id.hex[:12],
                    name="Lớp AI kiểm thử " + project,
                    grade=4,
                    teacher_user_id=teacher,
                )
            )
            conn.execute(
                db.table("class_enrollments").insert().values(class_id=class_id, student_id=student)
            )
            conn.execute(
                db.table("guardian_students")
                .insert()
                .values(guardian_user_id=guardian, student_id=student, verified_at=now())
            )
            output["E2E_ACADEMY_" + project + "_CLASS_ID"] = str(class_id)
    print(json.dumps(output))


if __name__ == "__main__":
    main()

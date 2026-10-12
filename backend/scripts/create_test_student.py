"""Tạo học sinh browser test mới; chỉ cho phép database test riêng."""

import argparse
from uuid import uuid4

from app.core.config import settings
from app.core.security import hasher
from app.db import db, engine


def main():
    parser = argparse.ArgumentParser(description="Tạo học sinh mới trong database test riêng")
    parser.add_argument("--grade", type=int, choices=range(1, 6), default=4)
    args = parser.parse_args()
    name = engine().url.database
    if name == "viettree-education" or "test" not in name.lower():
        raise RuntimeError("Chỉ được tạo browser test user trong database test riêng")
    password = settings().seed_student_password
    if not password:
        raise RuntimeError("Cần SEED_STUDENT_PASSWORD trong .env local")
    user_id = uuid4()
    username = "e2e-" + str(user_id)
    with engine().begin() as conn:
        db.load(conn)
        conn.execute(
            db.table("users")
            .insert()
            .values(
                id=user_id,
                username=username,
                display_name="Học sinh kiểm thử",
                password_hash=hasher.hash(password),
            )
        )
        conn.execute(db.table("user_roles").insert().values(user_id=user_id, role="student"))
        conn.execute(
            db.table("student_profiles")
            .insert()
            .values(
                student_id=user_id,
                current_grade=args.grade,
                learning_preferences={"language": "vi"},
            )
        )
    # Chỉ in username, không in password hay URL kết nối.
    print(username)


if __name__ == "__main__":
    main()

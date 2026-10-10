import argparse
import json
import sys

from sqlalchemy import select

from app.core.config import ROOT
from app.db import db, engine
from app.personalization.engine import rebuild_statistics, rebuild_student
from app.seed import seed, verify_seed


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="VietTree: thao tác rõ ràng, không reset database")
    parser.add_argument(
        "command",
        choices=[
            "check-schema",
            "import-schema",
            "seed",
            "seed-demo-learners",
            "seed-vip-content",
            "verify-seed",
            "rebuild",
        ],
    )
    parser.add_argument("--reset-demo-passwords", action="store_true")
    args = parser.parse_args()
    if args.command == "import-schema":
        # Import tùy chọn đúng file gốc, không tạo database thay thế.
        raw = engine().raw_connection()
        try:
            raw.driver_connection.execute(
                (ROOT / "database/viettree_education_schema.sql").read_text(encoding="utf-8")
            )
        finally:
            raw.close()
        print("Đã import SQL gốc. Tiếp theo: alembic upgrade head")
        return
    with engine().begin() as conn:
        if args.command == "check-schema":
            db.validate(conn)
            print(
                "Schema đúng: 34 bảng gốc + 2 bảng auth + 6 bảng gói học + 1 bảng quyền câu hỏi + 1 bảng nháp bài học; database="
                + engine().url.database
            )
        else:
            db.load(conn)
            if args.command == "seed":
                print(json.dumps(seed(conn, args.reset_demo_passwords), ensure_ascii=False))
            elif args.command == "seed-demo-learners":
                from app.demo_learners import seed_demo_learners

                print(json.dumps(seed_demo_learners(conn), ensure_ascii=False))
            elif args.command == "seed-vip-content":
                from sqlalchemy import text

                from app.core.config import settings
                from app.seed import seed_advanced_content
                from app.vip_curriculum import VIP_EXTENSION

                if settings().app_env == "production":
                    raise RuntimeError("Nội dung mẫu VIP cần rà soát trước khi nạp production")
                conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
                seed_advanced_content(conn, VIP_EXTENSION)
                print(json.dumps(verify_seed(conn), ensure_ascii=False))
            elif args.command == "verify-seed":
                print(json.dumps(verify_seed(conn), ensure_ascii=False))
            else:
                profiles = db.table("student_profiles")
                for student_id in conn.execute(
                    select(profiles.c.student_id).with_for_update()
                ).scalars():
                    rebuild_student(conn, student_id)
                rebuild_statistics(conn)
                print("Đã rebuild mastery và thống kê từ lịch sử gốc, không xóa lịch sử")


if __name__ == "__main__":
    main()

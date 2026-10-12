import argparse
import getpass
import json
import sys

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import ROOT
from app.db import SchemaNotReady, db, engine
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
            "check-system",
            "cleanup-auth",
            "bootstrap-admin",
            "import-schema",
            "seed",
            "seed-demo-learners",
            "seed-vip-content",
            "seed-grade4-content",
            "seed-grade3-content",
            "seed-grade1-content",
            "seed-grade2-content",
            "seed-ai-academy",
            "verify-ai-academy",
            "verify-seed",
            "rebuild",
        ],
    )
    parser.add_argument("--reset-demo-passwords", action="store_true")
    parser.add_argument("--grade", type=int, choices=range(1, 6), default=4)
    parser.add_argument(
        "--apply", action="store_true", help="Thực hiện cleanup-auth; mặc định chỉ thống kê"
    )
    parser.add_argument("--username")
    parser.add_argument("--display-name")
    parser.add_argument("--retention-days", type=int, choices=range(1, 366), default=30)
    args = parser.parse_args()
    if args.apply and args.command != "cleanup-auth":
        parser.error("--apply chỉ dùng với cleanup-auth")
    if args.command == "bootstrap-admin":
        if not sys.stdin.isatty() or not args.username or not args.display_name:
            parser.error("bootstrap-admin cần terminal tương tác, --username và --display-name")
        password = getpass.getpass("Mật khẩu quản trị mới (tối thiểu 15 ký tự): ")
        if password != getpass.getpass("Nhập lại mật khẩu: "):
            parser.error("Hai mật khẩu không khớp")
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
                "Schema đúng: 34 bảng gốc + 2 bảng auth + 6 bảng gói học + 1 bảng quyền câu hỏi + 1 bảng nháp bài học + 29 bảng AI Academy + 8 bảng lớp/thành tích/giá, đủ cột quản trị tài khoản và quyền AI; database="
                + engine().url.database
            )
        else:
            db.load(conn)
            if args.command == "bootstrap-admin":
                from app.bootstrap import bootstrap_admin

                try:
                    bootstrap_admin(conn, args.username, args.display_name, password)
                except ValidationError:
                    raise SystemExit(
                        "Tên, tên đăng nhập hoặc mật khẩu chưa đúng chính sách; không thay đổi dữ liệu"
                    ) from None
                except ValueError as error:
                    raise SystemExit(str(error)) from None
                print("Đã tạo quản trị đầu tiên. Mật khẩu không được in hoặc lưu vào nhật ký")
            elif args.command == "check-system":
                from app.operations import system_report

                report = system_report(conn)
                print(json.dumps(report, ensure_ascii=False, default=str))
                if report["status"] != "ok":
                    raise SystemExit(1)
            elif args.command == "cleanup-auth":
                from app.operations import cleanup_auth

                print(json.dumps(cleanup_auth(conn, args.retention_days, args.apply)))
            elif args.command == "seed":
                print(json.dumps(seed(conn, args.reset_demo_passwords), ensure_ascii=False))
            elif args.command in {"seed-ai-academy", "verify-ai-academy"}:
                from app.academy.seed import seed as academy_seed
                from app.academy.seed import verify as academy_verify

                print(
                    json.dumps(
                        academy_seed(conn)
                        if args.command == "seed-ai-academy"
                        else academy_verify(conn),
                        ensure_ascii=False,
                    )
                )
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
            elif args.command == "seed-grade4-content":
                from app.seed import seed_grade4_content

                seed_grade4_content(conn)
                print(json.dumps(verify_seed(conn), ensure_ascii=False))
            elif args.command == "seed-grade3-content":
                from app.seed import seed_grade3_content

                seed_grade3_content(conn)
                print(json.dumps(verify_seed(conn, grade=3), ensure_ascii=False))
            elif args.command in {"seed-grade1-content", "seed-grade2-content"}:
                from app.seed import seed_early_primary_content

                grade = 1 if args.command == "seed-grade1-content" else 2
                seed_early_primary_content(conn, grade)
                print(json.dumps(verify_seed(conn, grade=grade), ensure_ascii=False))
            elif args.command == "verify-seed":
                print(json.dumps(verify_seed(conn, grade=args.grade), ensure_ascii=False))
            else:
                profiles = db.table("student_profiles")
                for student_id in conn.execute(
                    select(profiles.c.student_id).with_for_update()
                ).scalars():
                    rebuild_student(conn, student_id)
                rebuild_statistics(conn)
                print("Đã rebuild mastery và thống kê từ lịch sử gốc, không xóa lịch sử")


if __name__ == "__main__":
    try:
        main()
    except (SchemaNotReady, SQLAlchemyError):
        raise SystemExit(
            "Database/schema chưa sẵn sàng; kiểm tra kết nối, quyền DB và alembic upgrade head"
        ) from None

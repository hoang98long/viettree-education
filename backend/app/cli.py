import argparse
import getpass
import json
import sys

from pydantic import ValidationError
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import ROOT
from app.curriculum.seeding import verify_seed
from app.db import SchemaNotReady, db, engine
from app.fixtures.development import seed
from app.personalization.engine import rebuild_statistics, rebuild_student


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description="VietTree: thao tác rõ ràng, không reset database")
    parser.add_argument(
        "command",
        choices=[
            "check-schema",
            "check-system",
            "check-launch",
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
            "seed-grade5-content",
            "seed-grade-content",
            "curriculum-inventory",
            "applied-content-inventory",
            "seed-applied-content",
            "verify-applied-content",
            "supplement-inventory",
            "seed-supplement-content",
            "verify-supplement-content",
            "seed-ai-academy",
            "verify-ai-academy",
            "verify-seed",
            "rebuild",
        ],
    )
    parser.add_argument("--reset-demo-passwords", action="store_true")
    parser.add_argument("--grade", type=int, choices=range(1, 6), default=4)
    parser.add_argument(
        "--grades",
        type=int,
        nargs="+",
        choices=range(1, 6),
        help="Khối cho tài khoản demo hoặc học liệu bổ sung; mặc định 1 2 3 4 5",
    )
    parser.add_argument(
        "--apply", action="store_true", help="Thực hiện cleanup-auth; mặc định chỉ thống kê"
    )
    parser.add_argument("--username")
    parser.add_argument("--display-name")
    parser.add_argument("--retention-days", type=int, choices=range(1, 366), default=30)
    from app.curriculum.supplements.registry import releases

    parser.add_argument(
        "--release", choices=tuple(releases()), help="Mã bộ học liệu cho các lệnh supplement"
    )
    args = parser.parse_args()
    if args.apply and args.command != "cleanup-auth":
        parser.error("--apply chỉ dùng với cleanup-auth")
    if args.grades is not None and args.command not in {
        "seed-demo-learners",
        "seed-applied-content",
        "verify-applied-content",
        "applied-content-inventory",
        "supplement-inventory",
        "seed-supplement-content",
        "verify-supplement-content",
    }:
        parser.error("--grades chỉ dùng với seed-demo-learners hoặc các lệnh học liệu bổ sung")
    supplement_commands = {
        "supplement-inventory",
        "seed-supplement-content",
        "verify-supplement-content",
    }
    if args.command in supplement_commands and not args.release:
        parser.error("Cần chọn bộ học liệu bằng --release")
    if args.release and args.command not in supplement_commands:
        parser.error("--release chỉ dùng với các lệnh supplement")
    if args.command == "supplement-inventory":
        from app.curriculum.supplements.registry import get_release

        print(
            json.dumps(
                get_release(args.release).inventory(args.grades or range(1, 6)), ensure_ascii=False
            )
        )
        return
    if args.command == "applied-content-inventory":
        from app.curriculum.supplements.applied.pack import inventory

        print(json.dumps(inventory(args.grades or range(1, 6)), ensure_ascii=False))
        return
    if args.command in {"seed-grade-content", "curriculum-inventory"}:
        from app.curriculum.registry import SUPPORTED_GRADES

        if args.grade not in SUPPORTED_GRADES:
            parser.error("Khối này chưa có bộ ba môn; chọn --grade 1–5")
    if args.command == "curriculum-inventory":
        from app.curriculum.registry import get_pack, inventory

        report = inventory(args.grade)
        expected = get_pack(args.grade).expected
        print(
            json.dumps(
                {"grade": args.grade, "subjects": report, "matches_expected": report == expected},
                ensure_ascii=False,
            )
        )
        if report != expected:
            raise SystemExit(1)
        return
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
                "Schema đúng: 34 bảng gốc + 2 bảng auth + 6 bảng gói học + 1 bảng quyền câu hỏi + 1 bảng nháp bài học + 29 bảng AI Academy + 8 bảng lớp/thành tích/giá + 1 bảng lưu bài, đủ cột quản trị tài khoản và quyền AI; database="
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
            elif args.command in {"check-system", "check-launch"}:
                from app.operations import launch_report, system_report

                report = (
                    launch_report(conn) if args.command == "check-launch" else system_report(conn)
                )
                print(json.dumps(report, ensure_ascii=False, default=str))
                if report["status"] != "ok":
                    raise SystemExit(1)
            elif args.command == "cleanup-auth":
                from app.operations import cleanup_auth

                print(json.dumps(cleanup_auth(conn, args.retention_days, args.apply)))
            elif args.command == "seed":
                print(json.dumps(seed(conn, args.reset_demo_passwords), ensure_ascii=False))
            elif args.command in {"seed-applied-content", "verify-applied-content"}:
                from app.curriculum.supplements.applied.pack import seed as applied_seed
                from app.curriculum.supplements.applied.pack import verify as applied_verify

                try:
                    report = (
                        applied_seed if args.command == "seed-applied-content" else applied_verify
                    )(conn, args.grades or range(1, 6))
                except ValueError as error:
                    raise SystemExit(str(error)) from None
                print(json.dumps(report, ensure_ascii=False))
            elif args.command in {"seed-supplement-content", "verify-supplement-content"}:
                from app.curriculum.supplements.registry import get_release

                release = get_release(args.release)
                try:
                    report = (
                        release.seed
                        if args.command == "seed-supplement-content"
                        else release.verify
                    )(conn, args.grades or range(1, 6))
                except ValueError as error:
                    raise SystemExit(str(error)) from None
                print(json.dumps(report, ensure_ascii=False))
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
                from app.fixtures.learners import seed_demo_learners

                print(
                    json.dumps(
                        seed_demo_learners(conn, args.grades)
                        if args.grades
                        else seed_demo_learners(conn),
                        ensure_ascii=False,
                    )
                )
            elif args.command in {"seed-grade-content", "seed-grade5-content"}:
                from app.curriculum.seeding import seed_grade_content

                grade = 5 if args.command == "seed-grade5-content" else args.grade
                seed_grade_content(conn, grade)
                print(json.dumps(verify_seed(conn, grade=grade), ensure_ascii=False))
            elif args.command == "seed-vip-content":
                from sqlalchemy import text

                from app.core.config import settings
                from app.curriculum.grades.grade_04.vip import VIP_EXTENSION
                from app.curriculum.seeding import seed_advanced_content

                if settings().app_env == "production":
                    raise RuntimeError("Nội dung mẫu VIP cần rà soát trước khi nạp production")
                conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
                seed_advanced_content(conn, VIP_EXTENSION)
                print(json.dumps(verify_seed(conn), ensure_ascii=False))
            elif args.command == "seed-grade4-content":
                from app.curriculum.seeding import seed_grade4_content

                seed_grade4_content(conn)
                print(json.dumps(verify_seed(conn), ensure_ascii=False))
            elif args.command == "seed-grade3-content":
                from app.curriculum.seeding import seed_grade3_content

                seed_grade3_content(conn)
                print(json.dumps(verify_seed(conn, grade=3), ensure_ascii=False))
            elif args.command in {"seed-grade1-content", "seed-grade2-content"}:
                from app.curriculum.seeding import seed_early_primary_content

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

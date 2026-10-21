"""Manual, read-only release diagnostics; never added to the liveness probe."""

from xml.etree.ElementTree import ParseError

from sqlalchemy import func, select

from app.academy.media import validate_manifest
from app.academy.quality import report as academy_report
from app.curriculum.registry import SUBJECT_CODES, SUPPORTED_GRADES, get_pack
from app.db import db
from app.operations import launch_report

REMEDIES = {
    "migrations": "Người vận hành chạy migration đúng release, sau khi sao lưu.",
    "lesson_policies": "Rà soát quyền truy cập của các bài đã xuất bản trong quản trị nội dung.",
    "assessment_policies": "Bổ sung chính sách Free/VIP cho đề đã xuất bản.",
    "question_policies": "Bổ sung chính sách Free/VIP cho phiên bản câu hỏi đã xuất bản.",
    "assessment_items": "Rà soát các đề rỗng, câu nháp hoặc câu không cùng khối và môn.",
    "guided_hints": "Người vận hành kiểm tra cấu hình quyền gợi ý trong gói VIP.",
    "production_mode": "Người vận hành cấu hình production và HTTPS trên VPS.",
    "review_demo_accounts": "Khóa tài khoản demo hoặc đổi mật khẩu riêng qua quản trị tài khoản.",
    "ready_admin": "Đặt mật khẩu riêng cho quản trị viên và hoàn tất yêu cầu đổi mật khẩu.",
    "runtime_db_role": "Người vận hành cấp role DB runtime ít quyền theo hướng dẫn triển khai.",
    "curriculum_coverage": "Đối chiếu từng khối/môn; nạp học liệu còn thiếu hoặc rà soát các bài đã ẩn.",
    "academy_content": "Rà soát bài AI, phiên bản xuất bản, rubric và ảnh được duyệt; nạp bộ AI nếu còn thiếu.",
    "academy_files": "Người vận hành kiểm tra image ứng dụng có đủ manifest và các file SVG đúng release.",
}


def curriculum_inventory(conn):
    subjects, topics, lessons, questions, versions, assessments = (
        db.table(name)
        for name in (
            "subjects",
            "topics",
            "lessons",
            "questions",
            "question_versions",
            "assessments",
        )
    )
    sources = {
        "lessons": select(topics.c.grade, subjects.c.code, func.count())
        .select_from(lessons.join(topics).join(subjects))
        .where(
            lessons.c.status == "published",
            topics.c.is_active.is_(True),
            subjects.c.is_active.is_(True),
        ),
        "questions": select(
            questions.c.grade, subjects.c.code, func.count(func.distinct(questions.c.id))
        )
        .select_from(questions.join(subjects))
        .join(versions, versions.c.question_id == questions.c.id)
        .where(
            questions.c.is_active.is_(True),
            versions.c.status == "published",
            subjects.c.is_active.is_(True),
        ),
        "assessments": select(assessments.c.grade, subjects.c.code, func.count())
        .select_from(assessments.join(subjects))
        .where(assessments.c.status == "published", subjects.c.is_active.is_(True)),
    }
    counts = {}
    for metric, statement in sources.items():
        table = {"lessons": topics, "questions": questions, "assessments": assessments}[metric]
        counts[metric] = {
            (grade, code): count
            for grade, code, count in conn.execute(
                statement.group_by(table.c.grade, subjects.c.code)
            )
        }
    rows = []
    for grade in SUPPORTED_GRADES:
        for code in SUBJECT_CODES:
            minimum = {
                key: value
                for key, value in get_pack(grade).expected[code].items()
                if key in sources
            }
            actual = {metric: counts[metric].get((grade, code), 0) for metric in sources}
            rows.append(
                {
                    "grade": grade,
                    "subject_code": code,
                    "actual": actual,
                    "minimum": minimum,
                    "ok": all(actual[key] >= value for key, value in minimum.items()),
                }
            )
    return rows


def release_report(conn):
    report = launch_report(conn)
    inventory = curriculum_inventory(conn)
    academy = academy_report(conn)
    try:
        media = {**validate_manifest(), "valid": True}
    except (OSError, ValueError, KeyError, ParseError):
        # A broken image must be visible to operators without exposing local paths.
        media = {"valid": False, "assets": None, "lessons": None}
    report["checks"].extend(
        [
            {
                "code": "curriculum_coverage",
                "label": "Học liệu năm khối, ba môn đạt số lượng tối thiểu",
                "ok": all(row["ok"] for row in inventory),
                "count": sum(not row["ok"] for row in inventory),
            },
            {
                "code": "academy_content",
                "label": "Bài AI đã xuất bản, cấu trúc và ảnh được duyệt hợp lệ",
                "ok": not academy["issues"],
                "count": len(academy["issues"]),
            },
            {
                "code": "academy_files",
                "label": "File minh họa AI đủ và đúng nội dung kiểm tra",
                "ok": media["valid"],
                "count": None,
            },
        ]
    )
    report.update(
        status="ok" if all(check["ok"] for check in report["checks"]) else "attention",
        curriculum=inventory,
        academy=academy,
        media=media,
        next_steps=[
            {"code": check["code"], "instruction": REMEDIES[check["code"]]}
            for check in report["checks"]
            if not check["ok"]
        ],
    )
    return report

import json

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert

from app.academy.access import FREE_CODES
from app.academy.baseline_upgrade import publish_visual_revision
from app.academy.curriculum import COMPETENCIES, content, records
from app.academy.media import MANIFEST, uid, validate_manifest
from app.db import db

RUBRIC = {"understanding": 20, "practice": 30, "creativity": 30, "safety": 20}
MODES = [
    "ExplainConcept",
    "GiveHint",
    "AskSocraticQuestion",
    "ReviewStudentDraft",
    "PracticeEnglish",
    "BrainstormStory",
    "GenerateTeacherDraft",
    "GenerateImagePrompt",
]


def add(conn, name, values):
    conn.execute(insert(db.table(name)).values(**values).on_conflict_do_nothing())


def seed(conn):
    conn.execute(text("SELECT pg_advisory_xact_lock(78249102)"))
    curriculum = records()
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    validate_manifest()
    program_id = uid("program")
    add(
        conn,
        "ai_programs",
        dict(
            id=program_id,
            code="VIETTREE-AI",
            title="VietTree AI Academy",
            description="Khám phá AI · Học cùng AI · Sáng tạo an toàn",
        ),
    )
    for grade in range(1, 6):
        add(
            conn,
            "ai_grades",
            dict(
                grade=grade,
                program_id=program_id,
                curriculum={
                    "competencies": COMPETENCIES,
                    "end_year_goal": "Nhận biết giới hạn AI, sử dụng dữ liệu mẫu, thực hành và kiểm chứng phù hợp lứa tuổi.",
                    "reading": "Tranh và câu ngắn, người lớn hỗ trợ đọc"
                    if grade < 3
                    else "Đọc tình huống, thực hành và giải thích căn cứ",
                    "coverage": "40 bài · 11 chủ đề · học bằng tranh và thao tác chạm",
                    "annual_outline": [dict(code=k, title=v) for k, v in COMPETENCIES.items()],
                },
            ),
        )
        grades = db.table("ai_grades")
        previous = conn.execute(
            select(grades.c.curriculum).where(grades.c.grade == grade)
        ).scalar_one()
        if previous.get("coverage") in {
            "36 tiết đầy đủ",
            "Khung năm học và 3 bài mẫu",
            "36 bài · 9 chủ đề · học bằng tranh và thao tác chạm",
            "38 bài · 10 chủ đề · học bằng tranh và thao tác chạm",
        }:
            conn.execute(
                grades.update()
                .where(grades.c.grade == grade)
                .values(
                    curriculum={
                        **previous,
                        "coverage": "40 bài · 11 chủ đề · học bằng tranh và thao tác chạm",
                        "competencies": COMPETENCIES,
                        "annual_outline": [dict(code=k, title=v) for k, v in COMPETENCIES.items()],
                    }
                )
            )
    for asset in manifest["assets"]:
        add(
            conn,
            "media_assets",
            dict(
                id=uid(asset["code"]),
                bucket_name="ai-academy-bundled",
                object_key=asset["file"],
                mime_type="image/svg+xml",
                file_size_bytes=asset["bytes"],
                sha256=asset["sha256"],
                visibility="public",
            ),
        )
        add(
            conn,
            "ai_media_assets",
            dict(
                id=uid(asset["code"]),
                code=asset["code"],
                category=asset["category"],
                alt=asset["alt"],
                license=asset["license"],
                source=asset["source"],
                status="approved",
                width=asset["width"],
                height=asset["height"],
                bundled=True,
            ),
        )
        add(
            conn,
            "ai_media_variants",
            dict(
                asset_id=uid(asset["code"]),
                kind="original",
                object_key=asset["file"],
                mime_type="image/svg+xml",
                sha256=asset["sha256"],
                width=asset["width"],
                height=asset["height"],
                file_size_bytes=asset["bytes"],
            ),
        )
    for row in curriculum:
        unit_id = uid(row["unit_code"])
        units = db.table("ai_units")
        occupied = conn.execute(
            select(units.c.id).where(
                units.c.grade == row["grade"], units.c.position == row["unit_position"]
            )
        ).scalar()
        unit_position = row["unit_position"]
        if occupied is not None and occupied != unit_id:
            unit_position = (
                conn.execute(
                    select(func.max(units.c.position)).where(units.c.grade == row["grade"])
                ).scalar()
                or 0
            ) + 1
        add(
            conn,
            "ai_units",
            dict(
                id=unit_id,
                grade=row["grade"],
                code=row["unit_code"],
                title=row["unit_title"],
                position=unit_position,
                description=COMPETENCIES[row["unit_code"].split("-")[-1]],
            ),
        )
        lesson_id = uid(row["code"])
        lessons = db.table("ai_lessons")
        occupied = conn.execute(
            select(lessons.c.id).where(
                lessons.c.unit_id == unit_id, lessons.c.position == row["position"]
            )
        ).scalar()
        lesson_position = row["position"]
        if occupied is not None and occupied != lesson_id:
            lesson_position = (
                conn.execute(
                    select(func.max(lessons.c.position)).where(lessons.c.unit_id == unit_id)
                ).scalar()
                or 0
            ) + 1
        add(
            conn,
            "ai_lessons",
            dict(
                id=lesson_id,
                unit_id=unit_id,
                code=row["code"],
                title=row["title"],
                position=lesson_position,
                minimum_plan_code="free" if row["code"] in FREE_CODES else "vip",
            ),
        )
        payload = content(row)
        version_id = publish_visual_revision(conn, row, payload)
        if version_id is not None:
            for code in {
                payload["hero"],
                *payload["cards"],
                *[code for step in payload["steps"] for code in step["media"]],
                *[
                    item["asset"]
                    for step in payload["steps"]
                    if step.get("activity")
                    for item in step["activity"]["items"]
                    if item.get("asset")
                ],
            }:
                add(
                    conn,
                    "ai_media_usages",
                    dict(lesson_version_id=version_id, asset_id=uid(code), purpose="lesson"),
                )
    for grade in range(1, 6):
        add(
            conn,
            "ai_projects",
            dict(
                id=uid(f"project-{grade}"),
                grade=grade,
                code=f"AI-PROJECT-{grade}",
                title="Sản phẩm AI an toàn của em",
                brief="Chọn truyện bốn khung, poster, quiz hoặc bộ phân loại mẫu. Nêu nhiệm vụ, dữ liệu, cách kiểm tra, nguồn hỗ trợ và giới hạn; chỉ gửi riêng cho giáo viên.",
                rubric=RUBRIC,
            ),
        )
    badge_titles = [
        "Bước khám phá đầu tiên",
        "Biết thử lại",
        "Quan sát dữ liệu",
        "Hỏi rõ ràng",
        "Kiểm tra nguồn",
        "Giữ thông tin riêng",
        "Giải thích cách làm",
        "Dùng gợi ý đúng cách",
        "Sáng tạo có trách nhiệm",
        "Hợp tác và cải tiến",
        "Hiểu giới hạn mô hình",
        "Nhà khám phá AI",
    ]
    for i, title in enumerate(badge_titles):
        add(
            conn,
            "ai_badges",
            dict(
                code=f"AI-BADGE-{i + 1}",
                title=title,
                description=f"Hoàn thành {i + 1 if i < 11 else 36} bài học; huy hiệu ghi nhận quá trình, không xếp hạng.",
                threshold=i + 1 if i < 11 else 36,
                asset_id=uid(f"badge-{i}"),
            ),
        )
    for code in [
        "tutor_enabled",
        "image_generation_enabled",
        "voice_enabled",
        "student_creative_enabled",
    ]:
        add(conn, "ai_feature_flags", dict(code=code, enabled=code == "student_creative_enabled"))
    for code in ["simulation", "ollama"]:
        add(
            conn,
            "ai_provider_configs",
            dict(code=code, enabled=code == "simulation", policy_approved=code == "simulation"),
        )
    for mode in MODES:
        add(
            conn,
            "ai_prompt_templates",
            dict(
                mode=mode,
                version=1,
                status="approved",
                template="Chỉ dùng ngữ liệu nội bộ đã duyệt. Hướng dẫn ngắn bằng tiếng Việt phù hợp lớp học, ưu tiên gợi ý và tự kiểm tra. Không trả thông tin cá nhân, liên kết internet, đáp án làm hộ hoặc nội dung ngoài bài học. AI có thể sai và không có cảm xúc thật.",
            ),
        )
    return verify(conn)


def verify(conn):
    from app.academy.quality import report

    lessons, units, versions = (
        db.table(n) for n in ("ai_lessons", "ai_units", "ai_lesson_versions")
    )
    rows = conn.execute(
        select(units.c.grade, func.count())
        .select_from(lessons.join(units).join(versions))
        .where(versions.c.status == "published")
        .group_by(units.c.grade)
    ).all()
    return {
        "lessons": {str(g): count for g, count in rows},
        "media": validate_manifest(),
        "quality": report(conn),
    }

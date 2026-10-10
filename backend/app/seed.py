from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import func, select, text
from sqlalchemy.dialects.postgresql import insert

from app.advanced_curriculum import ADVANCED
from app.core.config import settings
from app.core.security import hasher, now
from app.curriculum import CURRICULUM
from app.db import db
from app.expanded_curriculum import EXPANDED
from app.grade4_curriculum import GRADE4, NEW_TOPICS
from app.vip_curriculum import VIP_EXTENSION


def stable_id(key):
    return uuid5(NAMESPACE_URL, "https://viettree.local/seed/v1/" + key)


def ensure(conn, name, match: dict, values: dict, key: str):
    table = db.table(name)
    row = (
        conn.execute(
            select(table).where(*(table.c[column] == value for column, value in match.items()))
        )
        .mappings()
        .first()
    )
    if row:
        return dict(row), False
    values = {**values, **match}
    if "id" in table.c:
        values["id"] = stable_id(key)
    row = conn.execute(insert(table).values(**values).returning(table)).mappings().one()
    return dict(row), True


def seed_accounts(conn, reset=False):
    config = settings()
    if config.app_env == "production":
        raise RuntimeError("Không seed tài khoản demo trong production")
    for username, role, display_name, password in (
        ("admin", "admin", "Quản trị VietTree", config.seed_admin_password),
        ("longnh", "student", "Học sinh Long (demo)", config.seed_student_password),
    ):
        users, roles = db.table("users"), db.table("user_roles")
        user = (
            conn.execute(select(users).where(func.lower(users.c.username) == username))
            .mappings()
            .first()
        )
        if not user:
            if not password:
                raise RuntimeError(
                    "Cần khai báo SEED_ADMIN_PASSWORD và SEED_STUDENT_PASSWORD trong .env local"
                )
            user, _ = ensure(
                conn,
                "users",
                {"username": username},
                {"display_name": display_name, "password_hash": hasher.hash(password)},
                "user/" + username,
            )
            ensure(
                conn, "user_roles", {"user_id": user["id"], "role": role}, {}, "role/" + username
            )
        else:
            exists = conn.execute(
                select(roles.c.role).where(roles.c.user_id == user["id"], roles.c.role == role)
            ).scalar()
            if not exists:
                raise RuntimeError(
                    f"Tài khoản {username} đã tồn tại với vai trò khác; seed không tự nâng quyền"
                )
            if reset:
                if not password:
                    raise RuntimeError("Chưa cấu hình password seed")
                conn.execute(
                    users.update()
                    .where(users.c.id == user["id"])
                    .values(password_hash=hasher.hash(password))
                )
                sessions = db.table("auth_sessions")
                conn.execute(
                    sessions.update()
                    .where(sessions.c.user_id == user["id"], sessions.c.revoked_at.is_(None))
                    .values(revoked_at=now())
                )
        if role == "student":
            ensure(
                conn,
                "student_profiles",
                {"student_id": user["id"]},
                {
                    "current_grade": 4,
                    "learning_preferences": {"language": "vi", "session_minutes": 15},
                },
                "profile/" + username,
            )


def seed_content(conn):
    for subject_code, topics in CURRICULUM.items():
        subjects = db.table("subjects")
        subject_id = conn.execute(
            select(subjects.c.id).where(subjects.c.code == subject_code)
        ).scalar_one_or_none()
        if subject_id is None:
            raise RuntimeError(f"Thiếu môn {subject_code}; kiểm tra import SQL gốc")
        for topic_order, source in enumerate(topics, 1):
            prefix = f"VT4-{subject_code}-{source['code']}"
            topic, _ = ensure(
                conn,
                "topics",
                {"subject_id": subject_id, "grade": 4, "code": prefix},
                {"title": source["title"], "sort_order": topic_order},
                prefix,
            )
            skill, _ = ensure(
                conn,
                "skills",
                {"code": prefix + "-skill"},
                {
                    "subject_id": subject_id,
                    "topic_id": topic["id"],
                    "grade": 4,
                    "name": source["title"],
                    "sort_order": topic_order,
                },
                prefix + "/skill",
            )
            lessons = []
            for lesson_order, lesson_source in enumerate(source["lessons"], 1):
                code = prefix + f"-lesson-{lesson_order}"
                item, _ = ensure(
                    conn,
                    "lessons",
                    {"topic_id": topic["id"], "code": code},
                    {
                        **lesson_source,
                        "status": "published",
                        "sort_order": lesson_order,
                        "estimated_minutes": 12,
                    },
                    code,
                )
                lessons.append(item)
                ensure(
                    conn,
                    "lesson_skills",
                    {"lesson_id": item["id"], "skill_id": skill["id"]},
                    {"is_primary": True},
                    code + "/skill",
                )
            versions = []
            for question_order, question_source in enumerate(source["questions"], 1):
                code = prefix + f"-q-{question_order:02d}"
                question, _ = ensure(
                    conn,
                    "questions",
                    {"code": code},
                    {"subject_id": subject_id, "topic_id": topic["id"], "grade": 4},
                    code,
                )
                version, created = ensure(
                    conn,
                    "question_versions",
                    {"question_id": question["id"], "version": 1},
                    {**question_source, "status": "published", "published_at": now()},
                    code + "/v1",
                )
                if not created and any(
                    version[key] != question_source[key]
                    for key in ("content", "grading", "explanation", "question_type", "difficulty")
                ):
                    raise RuntimeError(
                        f"Seed conflict {code}: không sửa version đã xuất bản. Tạo version mới bằng migration nội dung được duyệt"
                    )
                versions.append(version)
                ensure(
                    conn,
                    "question_version_access_policies",
                    {"question_version_id": version["id"]},
                    {"minimum_plan_code": "free"},
                    code + "/access",
                )
                ensure(
                    conn,
                    "question_skills",
                    {"question_version_id": version["id"], "skill_id": skill["id"]},
                    {"is_primary": True, "weight": 1},
                    code + "/skill",
                )
                for lesson_item in lessons:
                    ensure(
                        conn,
                        "lesson_questions",
                        {"lesson_id": lesson_item["id"], "question_version_id": version["id"]},
                        {"sort_order": question_order},
                        code + "/lesson",
                    )
            code = prefix + "-practice"
            assessment, created = ensure(
                conn,
                "assessments",
                {"code": code},
                {
                    "subject_id": subject_id,
                    "topic_id": topic["id"],
                    "lesson_id": lessons[-1]["id"],
                    "grade": 4,
                    "title": "Luyện tập: " + source["title"],
                    "status": "published",
                    "description": "8 câu ngắn. Em có thể lưu bài rồi quay lại; đọc lời giải sau khi nộp.",
                    "max_attempts": 5,
                    "published_at": now(),
                },
                code,
            )
            if created:
                for position, version in enumerate(versions, 1):
                    ensure(
                        conn,
                        "assessment_items",
                        {"assessment_id": assessment["id"], "position": position},
                        {"question_version_id": version["id"], "points": 1},
                        code + f"/item/{position}",
                    )
            else:
                table = db.table("assessment_items")
                existing = list(
                    conn.execute(
                        select(table.c.question_version_id)
                        .where(table.c.assessment_id == assessment["id"])
                        .order_by(table.c.position)
                    ).scalars()
                )
                if existing != [version["id"] for version in versions]:
                    raise RuntimeError(f"Seed conflict {code}: không sửa đề đã tồn tại")
        # Kỹ năng phân số dựa trên phép tính; những môn khác không ép prerequisite giả.
        if subject_code == "MATH":
            skill_table = db.table("skills")
            ids = {
                row.code: row.id
                for row in conn.execute(select(skill_table.c.code, skill_table.c.id))
            }
            ensure(
                conn,
                "skill_prerequisites",
                {
                    "skill_id": ids["VT4-MATH-fractions-skill"],
                    "prerequisite_skill_id": ids["VT4-MATH-operations-skill"],
                },
                {},
                "math-prerequisite",
            )


def seed(conn, reset=False):
    # Bảo vệ concurrent seed mà không yêu cầu thay unique constraints schema gốc.
    conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
    db.load(conn)
    seed_accounts(conn, reset)
    seed_content(conn)
    seed_access_policies(conn)
    seed_advanced_content(conn)
    seed_advanced_content(conn, EXPANDED)
    seed_advanced_content(conn, VIP_EXTENSION)
    seed_grade4_content(conn)
    return verify_seed(conn)


def seed_access_policies(conn):
    # Only the original, identified curriculum is initialized free, never arbitrary new content.
    for subject, sources in CURRICULUM.items():
        for source in sources:
            prefix = f"VT4-{subject}-{source['code']}"
            for kind, codes in (
                ("lesson", [prefix + f"-lesson-{i}" for i in (1, 2)]),
                ("assessment", [prefix + "-practice"]),
            ):
                table = db.table("lessons" if kind == "lesson" else "assessments")
                for row in conn.execute(
                    select(table.c.id, table.c.title).where(table.c.code.in_(codes))
                ).mappings():
                    ensure(
                        conn,
                        "content_access_policies",
                        {f"{kind}_id": row["id"]},
                        {"minimum_plan_code": "free", "learning_level": "basic"},
                        f"policy/{row['id']}",
                    )


def seed_advanced_content(conn, curriculum=ADVANCED):
    for subject_code, sources in curriculum.items():
        subjects, topics = db.table("subjects"), db.table("topics")
        subject_id = conn.execute(
            select(subjects.c.id).where(subjects.c.code == subject_code)
        ).scalar_one()
        for index, source in enumerate(sources, 1):
            minimum_plan = source.get("minimum_plan_code", "vip")
            topic = (
                conn.execute(
                    select(topics).where(
                        topics.c.code == f"VT4-{subject_code}-{source['topic']}",
                        topics.c.grade == 4,
                    )
                )
                .mappings()
                .one()
            )
            code = f"VT4-{subject_code}-{source['code']}"
            item, _ = ensure(
                conn,
                "lessons",
                {"code": code + "-lesson", "topic_id": topic["id"]},
                {
                    **source["lesson"],
                    "status": "published",
                    "estimated_minutes": 18,
                    "sort_order": source.get("sort_order", 10 + index),
                },
                code + "/lesson",
            )
            skill = conn.execute(
                select(db.table("skills").c.id).where(
                    db.table("skills").c.code == f"VT4-{subject_code}-{source['topic']}-skill"
                )
            ).scalar_one()
            ensure(
                conn,
                "lesson_skills",
                {"lesson_id": item["id"], "skill_id": skill},
                {"is_primary": True},
                code + "/lesson-skill",
            )
            versions = []
            for position, question in enumerate(source["questions"], 1):
                qcode = code + f"-q-{position:02d}"
                base, _ = ensure(
                    conn,
                    "questions",
                    {"code": qcode},
                    {"subject_id": subject_id, "topic_id": topic["id"], "grade": 4},
                    qcode,
                )
                version, created = ensure(
                    conn,
                    "question_versions",
                    {"question_id": base["id"], "version": 1},
                    {**question, "status": "published", "published_at": now()},
                    qcode + "/v1",
                )
                if not created and any(
                    version[key] != question[key]
                    for key in ("content", "grading", "explanation", "question_type", "difficulty")
                ):
                    raise RuntimeError(f"Seed conflict {qcode}: không sửa version đã xuất bản")
                versions.append(version)
                ensure(
                    conn,
                    "question_version_access_policies",
                    {"question_version_id": version["id"]},
                    {"minimum_plan_code": minimum_plan},
                    qcode + "/access",
                )
                ensure(
                    conn,
                    "question_skills",
                    {"question_version_id": version["id"], "skill_id": skill},
                    {"is_primary": True, "weight": 1},
                    qcode + "/skill",
                )
                ensure(
                    conn,
                    "lesson_questions",
                    {"question_version_id": version["id"], "lesson_id": item["id"]},
                    {"sort_order": position},
                    qcode + "/lesson",
                )
            assessment, created = ensure(
                conn,
                "assessments",
                {"code": code + "-practice"},
                {
                    "subject_id": subject_id,
                    "topic_id": topic["id"],
                    "lesson_id": item["id"],
                    "grade": 4,
                    "title": ("Thử thách: " if minimum_plan == "vip" else "Luyện tập: ")
                    + source["title"],
                    "description": f"{len(versions)} câu vận dụng. Đọc kỹ dữ kiện và xem lời giải sau khi nộp bài.",
                    "assessment_type": "quiz" if minimum_plan == "vip" else "practice",
                    "status": "published",
                    "max_attempts": 5,
                    "published_at": now(),
                },
                code + "/assessment",
            )
            if created:
                for position, version in enumerate(versions, 1):
                    ensure(
                        conn,
                        "assessment_items",
                        {"assessment_id": assessment["id"], "position": position},
                        {"question_version_id": version["id"], "points": 1},
                        code + f"/item/{position}",
                    )
            else:
                items = db.table("assessment_items")
                actual = list(
                    conn.execute(
                        select(items.c.question_version_id)
                        .where(items.c.assessment_id == assessment["id"])
                        .order_by(items.c.position)
                    ).scalars()
                )
                if actual != [version["id"] for version in versions]:
                    raise RuntimeError(f"Seed conflict {code}: không sửa đề đã tồn tại")
            for kind, target in (("lesson", item), ("assessment", assessment)):
                ensure(
                    conn,
                    "content_access_policies",
                    {f"{kind}_id": target["id"]},
                    {
                        "minimum_plan_code": minimum_plan,
                        "learning_level": source.get(
                            "learning_level",
                            "advanced" if minimum_plan == "vip" else "reinforcement",
                        ),
                        "preview": {
                            "summary": "Cùng vận dụng kiến thức đã học vào tình huống mới.",
                            "goals": [source["title"], "Tìm bằng chứng và kiểm tra kết quả."],
                        },
                    },
                    code + f"/policy/{kind}",
                )


def seed_grade4_content(conn):
    """Content only: caller owns transaction; serialized with other seed commands."""
    conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
    for subject_code, sources in NEW_TOPICS.items():
        subject_id = conn.execute(
            select(db.table("subjects").c.id).where(db.table("subjects").c.code == subject_code)
        ).scalar_one()
        for index, (key, title) in enumerate(sources.items(), 10):
            code = f"VT4-{subject_code}-{key}"
            topic, _ = ensure(
                conn,
                "topics",
                {"subject_id": subject_id, "grade": 4, "code": code},
                {"title": title, "sort_order": index},
                code,
            )
            ensure(
                conn,
                "skills",
                {"code": code + "-skill"},
                {
                    "subject_id": subject_id,
                    "topic_id": topic["id"],
                    "grade": 4,
                    "name": title,
                    "sort_order": index,
                },
                code + "/skill",
            )
    seed_advanced_content(conn, GRADE4)


def verify_seed(conn):
    report = {}
    for subject_code in CURRICULUM:
        subject_id = conn.execute(
            select(db.table("subjects").c.id).where(db.table("subjects").c.code == subject_code)
        ).scalar_one()
        counts = {}
        for name in ("topics", "lessons", "questions", "assessments"):
            table = db.table(name)
            if name == "lessons":
                topics = db.table("topics")
                statement = (
                    select(func.count())
                    .select_from(table.join(topics))
                    .where(
                        topics.c.subject_id == subject_id,
                        topics.c.grade == 4,
                        table.c.status == "published",
                    )
                )
            else:
                statement = (
                    select(func.count())
                    .select_from(table)
                    .where(table.c.subject_id == subject_id, table.c.grade == 4)
                )
                if name == "questions":
                    versions = db.table("question_versions")
                    statement = statement.join(versions).where(versions.c.status == "published")
                elif name == "assessments":
                    statement = statement.where(table.c.status == "published")
            counts[name] = conn.execute(statement).scalar_one()
        assert (
            counts["topics"] >= 4
            and counts["lessons"] >= 8
            and counts["questions"] >= 30
            and counts["assessments"] >= 3
        )
        report[subject_code] = counts
    return report

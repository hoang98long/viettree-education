from copy import deepcopy
from uuid import UUID, uuid4
from xml.etree import ElementTree as ET

import pytest
from sqlalchemy import select

from app.academy import baseline_upgrade
from app.academy.curriculum import content, records
from app.academy.media import svg, uid
from app.academy.visual_art import example_art, icon_for, labelled_picture
from app.curriculum.quality import audit_sources, sources
from app.db import db
from app.schemas.lessons import LessonContent
from app.services.content_review import CATALOG, fingerprint, review_learning_content


def test_review_covers_both_plans_all_grades_and_all_registered_packs():
    audit = audit_sources()
    assert not audit["issues"]
    assert sum(r["lessons"] for r in audit["matrix"]) == 445
    assert sum(r["questions"] for r in audit["matrix"]) == 2370
    assert {r["grade"] for r in CATALOG["lessons"]} == set(range(1, 6))
    originals = {}
    for _, _, _, prefix, lessons, _ in sources(True):
        for index, lesson in enumerate(lessons, 1):
            code = prefix + (f"-lesson-{index}" if len(lessons) > 1 else "-lesson")
            originals[code] = lesson["content"]
    assert len(CATALOG["lessons"]) == 232
    for entry in CATALOG["lessons"]:
        original = originals[entry["code"]]
        assert fingerprint(original) == entry["before_sha256"]
        updated = {**original, **entry["patch"]}
        LessonContent.model_validate(updated)
        assert fingerprint(updated) == entry["after_sha256"]
        assert updated.get("free_hint_count") == original.get("free_hint_count")
        assert updated["illustration"]


def test_mass_and_time_support_does_not_teach_perimeter_or_area():
    patch = next(
        r["patch"] for r in CATALOG["lessons"] if r["code"] == "VT4-MATH-measurement-lesson-1"
    )
    assert not any("chu vi" in value or "diện tích" in value for value in patch["hints"])
    assert patch["illustration"]["hour"] == 9 and patch["illustration"]["minute"] == 30


@pytest.mark.parametrize(
    "grade,number,labels",
    [
        (1, 26, ["Mèo: cat", "Chó: cat"]),
        (1, 27, ["Táo đỏ: red", "Cặp xanh dương: red"]),
        (2, 26, ["Táo: apple", "Cam: orange", "Chuối: cat"]),
        (2, 27, ["Sách: book", "Bút chì: pencil", "Cặp: cat"]),
        (3, 26, ["Mèo: cat", "Chó: dog", "Chim: cat"]),
    ],
)
def test_named_english_lessons_use_the_right_vocabulary_group(grade, number, labels):
    row = next(r for r in records() if r["code"] == f"AI{grade}-{number}")
    assert [item["text"] for item in row["activity"]["items"]] == labels


@pytest.mark.parametrize(
    "text,count",
    [
        ("Hai nhóm, mỗi nhóm hai: 4", 4),
        ("Hai nhóm, mỗi nhóm hai: 3", 4),
        ("Ba nhóm hai chấm: 6", 6),
        ("Ba nhóm bốn là 12", 12),
    ],
)
def test_count_pictures_show_given_groups_even_if_a_claim_is_wrong(text, count):
    root = ET.fromstring(svg(example_art(text)))
    assert len(root.findall(".//{http://www.w3.org/2000/svg}circle")) == count


def test_fraction_picture_and_sample_evidence_are_not_replaced_by_the_wrong_claim():
    root = ET.fromstring(svg(example_art("Bánh 8 phần bằng nhau, chọn 3")))
    cells = root.findall(".//{http://www.w3.org/2000/svg}rect")
    assert len(cells) == 8 and sum(c.attrib["fill"] == "#38a99a" for c in cells) == 3
    correct = example_art("Mẫu: two books on desk. There are two books.")
    wrong = example_art("Mẫu: two books on desk. There is one book.")
    assert correct == wrong
    assert len(ET.fromstring(svg(correct)).findall("{http://www.w3.org/2000/svg}g")) == 2
    assert icon_for("Tiếng chim trong bản ghi mẫu") == "sound"
    assert icon_for("Chim: cat") == "bird"
    assert icon_for("Ai phát hiện vòi còn chảy?") == "question"
    assert icon_for("AI hỗ trợ") == "robot"
    counting = ET.fromstring(svg(labelled_picture("Đếm mỗi quả một lần")))
    assert len(counting.findall(".//{http://www.w3.org/2000/svg}circle")) == 3
    fractions = ET.fromstring(svg(example_art("1/2 + 1/4 = 2/6")))
    assert len(fractions.findall(".//{http://www.w3.org/2000/svg}rect")) == 12
    assert len(fractions.findall(".//{http://www.w3.org/2000/svg}circle")) == 0


@pytest.mark.integration
def test_lesson_review_is_explicit_idempotent_and_preserves_learning_data(conn, logged_student):
    lessons, versions, policies = (
        db.table(n) for n in ("lessons", "question_versions", "content_access_policies")
    )
    identifier = conn.execute(
        select(lessons.c.id).where(lessons.c.code == "VT4-MATH-measurement-lesson-1")
    ).scalar_one()
    assert logged_student.post(f"/api/v1/lessons/{identifier}/visit").status_code == 200
    before = dict(conn.execute(select(lessons).where(lessons.c.id == identifier)).mappings().one())
    protected = {
        name: list(conn.execute(select(db.table(name))).mappings())
        for name in (
            "question_versions",
            "content_access_policies",
            "student_lesson_progress",
            "student_memberships",
        )
    }
    dry = review_learning_content(conn)
    assert dry["counts"]["eligible"] > 0
    assert (
        conn.execute(select(lessons.c.content).where(lessons.c.id == identifier)).scalar_one()
        == before["content"]
    )
    applied = review_learning_content(conn, apply=True)
    assert applied["counts"]["updated"] == dry["counts"]["eligible"]
    response = logged_student.get(f"/api/v1/lessons/{identifier}")
    assert response.status_code == 200
    assert response.json()["content"]["illustration"]["kind"] == "clock"
    assert response.json()["progress_status"] == "in_progress"
    for name, rows in protected.items():
        assert list(conn.execute(select(db.table(name))).mappings()) == rows
    assert review_learning_content(conn, apply=True)["counts"]["updated"] == 0
    log = db.table("audit_logs")
    history = conn.execute(
        select(log.c.old_values).where(
            log.c.entity_id == identifier, log.c.action == "authoring.lesson.editorial_review"
        )
    ).scalar_one()
    assert history["content"] == before["content"]


@pytest.mark.integration
def test_lesson_review_skips_teacher_content_and_drafts(conn):
    table, drafts = db.table("lessons"), db.table("lesson_drafts")
    rows = list(
        conn.execute(
            select(table)
            .where(
                table.c.code.in_(["VT4-MATH-measurement-lesson-1", "VT4-MATH-fractions-lesson-1"])
            )
            .order_by(table.c.code)
        ).mappings()
    )
    body = {**rows[0]["content"], "goals": ["Nội dung riêng của giáo viên"]}
    conn.execute(table.update().where(table.c.id == rows[0]["id"]).values(content=body))
    admin = conn.execute(
        select(db.table("users").c.id).where(db.table("users").c.username == "admin")
    ).scalar_one()
    conn.execute(
        drafts.insert().values(
            lesson_id=rows[1]["id"],
            payload={},
            source_fingerprint="0" * 64,
            updated_by=admin,
        )
    )
    result = review_learning_content(conn, apply=True)
    states = {item["code"]: item["status"] for item in result["items"]}
    assert all(states[row["code"]] == "customized" for row in rows)
    assert (
        conn.execute(select(table.c.content).where(table.c.id == rows[0]["id"])).scalar_one()
        == body
    )


@pytest.mark.integration
@pytest.mark.parametrize("media_only", [False, True])
def test_academy_revision_preserves_pinned_version_and_custom_access(
    conn, logged_student, monkeypatch, media_only
):
    source = next(r for r in records() if r["code"] == "AI2-26")
    row = {**source, "code": "revision-" + uuid4().hex, "position": 900}
    lessons, versions, progress = (
        db.table(n) for n in ("ai_lessons", "ai_lesson_versions", "ai_progress")
    )
    identifier, previous = uid(row["code"]), uuid4()
    original = deepcopy(content(source))
    original["steps"][0]["text"] = "Đây là bản cũ mà học sinh đang đọc."
    if media_only:
        original["estimated_minutes"] = 35
        original["hero"] = "AI2-26-v2-hero"
    conn.execute(
        lessons.insert().values(
            id=identifier,
            code=row["code"],
            title=row["title"],
            unit_id=uid(row["unit_code"]),
            position=900,
            minimum_plan_code="free",
        )
    )
    conn.execute(
        versions.insert().values(
            id=previous, lesson_id=identifier, version=1, status="published", payload=original
        )
    )
    user = UUID(logged_student.get("/api/v1/auth/me").json()["id"])
    conn.execute(
        progress.insert().values(
            student_id=user, lesson_id=identifier, version_id=previous, next_step=1
        )
    )
    monkeypatch.setitem(
        baseline_upgrade.EDITORIAL_BASELINE,
        row["code"],
        {
            "sha256": "0" * 64 if media_only else baseline_upgrade.fingerprint(original),
            "media_only_sha256": baseline_upgrade.fingerprint(original) if media_only else None,
            "title": row["title"],
            "position": 900,
            "unit_code": row["unit_code"],
        },
    )
    revised = baseline_upgrade.publish_editorial_revision(conn, row, content(source))
    assert (
        revised and baseline_upgrade.publish_editorial_revision(conn, row, content(source)) is None
    )
    stored = conn.execute(select(versions).where(versions.c.id == previous)).mappings().one()
    assert stored["payload"] == original and stored["status"] == "archived"
    assert (
        conn.execute(
            select(progress.c.version_id).where(progress.c.lesson_id == identifier)
        ).scalar_one()
        == previous
    )
    assert (
        conn.execute(
            select(lessons.c.minimum_plan_code).where(lessons.c.id == identifier)
        ).scalar_one()
        == "free"
    )
    fresh = conn.execute(select(versions.c.payload).where(versions.c.id == revised)).scalar_one()
    if media_only:
        assert fresh["estimated_minutes"] == 35
        assert fresh["steps"][0]["text"] == original["steps"][0]["text"]
    assert fresh["hero"] == content(source)["hero"]


def test_academy_draft_or_teacher_edit_is_never_replaced():
    row = records()[0]
    current = dict(
        created_by=None, title=row["title"], position=row["position"], unit_id=uid(row["unit_code"])
    )
    original = baseline_upgrade.EDITORIAL_BASELINE[row["code"]]
    version = dict(
        payload={"custom": "teacher text"}, created_by=None, reviewed_by=None, status="published"
    )
    assert baseline_upgrade.editorial_candidate(current, [version], row, content(row)) is None
    assert original["sha256"] != baseline_upgrade.fingerprint(version["payload"])


def test_known_legacy_unit_can_keep_its_position_without_accepting_an_arbitrary_move(monkeypatch):
    row = next(r for r in records() if r["code"] == "AI3-01")
    payload = {"legacy": "bundled payload"}
    old = baseline_upgrade.EDITORIAL_BASELINE[row["code"]]
    monkeypatch.setitem(
        baseline_upgrade.EDITORIAL_BASELINE,
        row["code"],
        {**old, "sha256": baseline_upgrade.fingerprint(payload)},
    )
    current = dict(
        created_by=None,
        title=old["title"],
        position=old["position"],
        unit_id=uid(baseline_upgrade.BASELINE[row["code"]]["unit_code"]),
    )
    version = dict(payload=payload, created_by=None, reviewed_by=None, status="published")
    assert baseline_upgrade.editorial_candidate(current, [version], row, content(row)) == version
    current["unit_id"] = uuid4()
    assert baseline_upgrade.editorial_candidate(current, [version], row, content(row)) is None

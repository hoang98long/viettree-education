from copy import deepcopy
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.db import db
from app.lesson_schemas import Illustration, LessonContent
from app.lesson_support import enrich
from tests.test_authoring import question_payload, restore_student
from tests.test_memberships import admin_login, identities, membership

BASE = "/api/v1/admin/lessons"


def payload(client, plan="free"):
    question = question_payload(client)
    return {
        "code": "lesson-test-" + str(uuid4()),
        "grade": 4,
        "subject_id": question["subject_id"],
        "topic_id": question["topic_id"],
        "skill_ids": question["skill_ids"],
        "title": "Bài học kiểm tra minh họa",
        "estimated_minutes": 12,
        "minimum_plan_code": plan,
        "preview": {"summary": "Giới thiệu mục tiêu bài học", "goals": ["Hiểu ví dụ minh họa"]},
        "content": {
            "blocks": [
                {
                    "type": "text",
                    "title": "Cùng khám phá",
                    "text": "Đọc và giải thích kiến thức bằng lời của em.",
                },
                {
                    "type": "example",
                    "title": "Thử với ví dụ",
                    "text": "Ba trong tám phần bằng nhau là ba phần tám.",
                },
                {
                    "type": "remember",
                    "title": "Em ghi nhớ",
                    "text": "Các phần của một đơn vị có kích thước bằng nhau.",
                },
            ],
            "goals": ["Giải thích ví dụ bằng lời"],
            "hints": ["Chọn một đơn vị trước", "Đếm các phần bằng nhau"],
            "reflection": ["Em có thể vẽ lại không?"],
            "illustration": {
                "kind": "fraction",
                "caption": "Ba trong tám phần bằng nhau",
                "numerator": 3,
                "denominator": 8,
            },
        },
    }


def save(client, data, changes=None):
    body = {
        **data["payload"],
        **(changes or {}),
        "expected_revision": data["edit_revision"],
        "source_fingerprint": data["source_fingerprint"],
    }
    return client.put(f"{BASE}/{data['id']}", json=body)


def act(client, data, operation):
    return client.post(
        f"{BASE}/{data['id']}/{operation}",
        json={
            "expected_revision": data["edit_revision"],
            "reason": "Đã kiểm tra ví dụ và chú thích",
        },
    )


@pytest.mark.integration
def test_create_review_publish_then_edit_keeps_live_content_until_publish(logged_student, conn):
    client = logged_student
    student, _ = identities(client, conn)
    cookies = dict(client.cookies)
    admin_login(client)
    body = payload(client)
    created = client.post(BASE, json=body)
    assert created.status_code == 200, created.text
    data = created.json()
    restore_student(client, cookies)
    assert client.get(f"/api/v1/lessons/{data['id']}").status_code == 404
    assert client.get(f"{BASE}/{data['id']}").status_code == 403
    admin_login(client)
    assert act(client, data, "publish").status_code == 409
    reviewed = act(client, data, "review").json()
    # A save invalidates approval, and an older revision cannot publish or overwrite.
    edited = save(client, reviewed, {"title": "Bài đã sửa sau khi duyệt"}).json()
    assert edited["draft_status"] == "draft"
    assert act(client, reviewed, "publish").status_code == 409
    assert save(client, reviewed).status_code == 409
    assert act(client, edited, "publish").status_code == 409
    edited = act(client, edited, "review").json()
    live = act(client, edited, "publish").json()
    assert live["lesson_status"] == "published"
    assert live["source_changed"] is False
    working = save(client, live, {"title": "Bản nháp thứ hai chưa xuất bản"}).json()
    assert working["draft_status"] == "draft"
    restore_student(client, cookies)
    viewed = client.get(f"/api/v1/lessons/{live['id']}").json()
    assert viewed["title"] == "Bài đã sửa sau khi duyệt"
    assert viewed["content"]["hints"] == body["content"]["hints"]
    assert viewed["content"]["illustration"]["denominator"] == 8
    assert "payload" not in viewed and "history" not in viewed
    admin_login(client)
    reset = act(client, working, "reset").json()
    assert reset["payload"]["title"] == viewed["title"]
    assert reset["edit_revision"] > working["edit_revision"]
    assert any(item["action"] == "authoring.lesson.publish" for item in reset["history"])
    assert client.get(BASE + "?status=pending").json()["total"] >= 1
    assert client.get(BASE + "?search=" + body["code"]).json()["items"][0]["id"] == live["id"]
    assert client.get(BASE + "?search=%25").json()["total"] == 0
    assert client.get(BASE + "?page=100").json()["items"] == []
    assert client.post(BASE, json=body).status_code == 409
    assert save(client, reset, {"code": "changed-code"}).status_code == 422
    assert save(client, reset, {"skill_ids": []}).status_code == 422
    attempts = db.table("attempts")
    assert (
        conn.execute(select(attempts.c.id).where(attempts.c.student_id == student)).first() is None
    )


@pytest.mark.integration
def test_policy_change_blocks_stale_draft_then_reset_rebases(logged_student, conn):
    client = logged_student
    student, admin = identities(client, conn)
    cookies = dict(client.cookies)
    admin_login(client)
    data = client.post(BASE, json=payload(client)).json()
    data = act(client, act(client, data, "review").json(), "publish").json()
    draft = save(client, data).json()
    changed = client.put(
        f"/api/v1/admin/content/lesson/{data['id']}/policy",
        json={
            "minimum_plan_code": "vip",
            "learning_level": "advanced",
            "preview": {"summary": "Bài nâng cao cần gói VIP"},
            "reason": "Kiểm tra thay đổi chính sách khi có nháp",
        },
    )
    assert changed.status_code == 200
    assert save(client, draft).status_code == 409
    assert act(client, draft, "review").status_code == 409
    latest = client.get(f"{BASE}/{data['id']}").json()
    assert latest["source_changed"] is True
    reset = act(client, latest, "reset").json()
    assert reset["source_changed"] is False
    assert reset["payload"]["minimum_plan_code"] == "vip"
    restore_student(client, cookies)
    denied = client.get(f"/api/v1/lessons/{data['id']}")
    assert denied.status_code == 403
    assert "content" not in denied.json()
    membership(conn, student, admin)
    assert client.get(f"/api/v1/lessons/{data['id']}").status_code == 200
    client.headers.pop("X-CSRF-Token")
    assert client.post(BASE, json={}).status_code == 403


@pytest.mark.integration
def test_all_seeded_lessons_have_valid_support_and_followups_are_eligible(logged_student, conn):
    client = logged_student
    lessons, topics = db.table("lessons"), db.table("topics")
    records = (
        conn.execute(
            select(
                lessons.c.id, lessons.c.content, topics.c.code, lessons.c.code.label("lesson_code")
            )
            .select_from(lessons.join(topics))
            .where(lessons.c.code.like("VT4-%"), lessons.c.status == "published")
        )
        .mappings()
        .all()
    )
    original = deepcopy(records[0]["content"])
    for item in records:
        content = LessonContent.model_validate(enrich(item["content"], item["code"]))
        assert len(content.hints) == 3
        if "-g4-" not in item["lesson_code"]:
            assert content.illustration is not None
    assert records[0]["content"] == original
    first = client.get("/api/v1/topics?grade=4&subject_code=MATH").json()[0]
    free = next(
        item
        for item in client.get(f"/api/v1/lessons?topic_id={first['id']}").json()
        if not item["locked"]
    )
    result = client.get(f"/api/v1/lessons/{free['id']}").json()
    assert result["next_lessons"]
    for item in result["next_lessons"]:
        opened = client.get(f"/api/v1/lessons/{item['id']}")
        assert opened.status_code == 200
        assert opened.json()["minimum_plan_code"] == "free"
        assert item["id"] != free["id"]
    completed_id = result["next_lessons"][0]["id"]
    client.post(f"/api/v1/lessons/{completed_id}/complete")
    assert completed_id not in [
        item["id"] for item in client.get(f"/api/v1/lessons/{free['id']}").json()["next_lessons"]
    ]
    uuid = UUID(free["id"])
    assert conn.execute(select(lessons.c.content).where(lessons.c.id == uuid)).scalar_one() == next(
        item["content"] for item in records if item["id"] == uuid
    )


@pytest.mark.parametrize(
    "change",
    [
        {"kind": "javascript"},
        {"denominator": 0},
        {"numerator": 9, "denominator": 8},
        {"hour": 24},
        {"rows": 9},
        {"caption": "x"},
        {"url": "https://example.org/image.svg"},
    ],
)
def test_invalid_illustration_is_rejected(change):
    with pytest.raises(ValidationError):
        Illustration.model_validate(
            {"kind": "fraction", "caption": "Hình minh họa phân số", **change}
        )


@pytest.mark.integration
@pytest.mark.parametrize(
    "method,path",
    [
        ("get", ""),
        ("post", ""),
        ("put", "/00000000-0000-0000-0000-000000000000"),
        ("post", "/00000000-0000-0000-0000-000000000000/review"),
    ],
)
def test_student_cannot_use_lesson_studio(logged_student, method, path):
    kwargs = {} if method == "get" else {"json": {}}
    assert getattr(logged_student, method)(BASE + path, **kwargs).status_code == 403


@pytest.mark.integration
def test_concurrent_saves_cannot_overwrite_each_other(test_engine):
    from concurrent.futures import ThreadPoolExecutor
    from threading import Barrier

    from fastapi import HTTPException

    from app.lesson_schemas import LessonInput
    from app.seed import seed
    from app.services import lesson_studio

    with test_engine.begin() as connection:
        db.load(connection)
        seed(connection)
        users, topics, skills = db.table("users"), db.table("topics"), db.table("skills")
        admin = connection.execute(
            select(users.c.id).where(users.c.username == "admin")
        ).scalar_one()
        topic = (
            connection.execute(select(topics).where(topics.c.code == "VT4-MATH-fractions"))
            .mappings()
            .one()
        )
        skill = connection.execute(
            select(skills.c.id).where(skills.c.topic_id == topic["id"])
        ).scalar_one()
        data = LessonInput.model_validate(
            {
                "code": "concurrent-lesson-" + str(uuid4()),
                "title": "Bài nháp thử lưu đồng thời",
                "grade": 4,
                "subject_id": topic["subject_id"],
                "topic_id": topic["id"],
                "skill_ids": [skill],
                "content": enrich(
                    {
                        "blocks": [
                            {
                                "type": "text",
                                "title": "Khám phá",
                                "text": "Các phần bằng nhau trong một đơn vị.",
                            },
                            {
                                "type": "example",
                                "title": "Ví dụ",
                                "text": "Ba trong tám phần bằng nhau là ba phần tám.",
                            },
                            {
                                "type": "remember",
                                "title": "Ghi nhớ",
                                "text": "Đếm tổng số phần bằng nhau trước.",
                            },
                        ]
                    },
                    topic["code"],
                ),
            }
        )
        draft = lesson_studio.save(connection, admin, data)
    barrier = Barrier(2)

    def write(index):
        body = LessonInput.model_validate(
            {
                **draft["payload"],
                "title": f"Bản nháp của người sửa {index}",
                "expected_revision": draft["edit_revision"],
                "source_fingerprint": draft["source_fingerprint"],
            }
        )
        barrier.wait(timeout=10)
        try:
            with test_engine.begin() as connection:
                return lesson_studio.save(connection, admin, body, draft["id"])["edit_revision"]
        except HTTPException as error:
            assert error.status_code == 409
            return "conflict"

    with ThreadPoolExecutor(max_workers=2) as pool:
        outcomes = list(pool.map(write, [1, 2]))
    assert sorted(map(str, outcomes)) == ["2", "conflict"]
    with test_engine.connect() as connection:
        result = lesson_studio.detail(connection, draft["id"])
        assert result["edit_revision"] == 2
        assert result["lesson_status"] == "draft"

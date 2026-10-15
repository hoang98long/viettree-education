"""Grade-five editorial validation and journeys on a separate PostgreSQL database."""

from copy import deepcopy
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import select

from app.curriculum.grades.grade_05.pack import ALL, EXPECTED, TOPICS
from app.curriculum.grades.grade_05.readings import PERSON, POEM, RAIN, SCENERY, SEEDLING, UMBRELLA
from app.curriculum.seeding import seed_grade_content, verify_seed
from app.db import db
from app.schemas.authoring import QuestionInput
from app.schemas.lessons import Illustration, LessonContent
from app.services.grading import grade_answer, validate_answer
from tests.test_grading import correct_answer
from tests.test_memberships import admin_login, identities, membership

UNITS = [(s, u) for s, units in ALL.items() for u in units]
# Golden answers calculated independently from the exercise statements.
MATH_SHEET = """natural-review|152|90|60|4
fraction-review|4/5|3/5|8/15|3/2
decimal-place|0.1|0.2|0.3|0.4
decimal-order|1|2.5|3|4.5
decimal-add-subtract|4.75|5.25|6.75|7.25
decimal-multiply-divide|5|10|9|14
percent-basics|5|4|15|8
sum-difference-ratio|3|6|9|12
area-units|15000|2000000|3|45000|5000000|6
volume-units|1000|2|3000|4|5000|6
triangle-area|12|21|16|27|20|33
trapezoid-area|18|21|24|27|30|33
circle-measures|12.56|28.26|4|31.4|113.04|7
solid-nets|6|12|8|96|2|3
surface-area|60|122|72|150|84|178
solid-volume|72|27|96|125|120|343
steady-motion|20|90|8|50|180|14
statistics-basics|20|9|2/5|50|18|2/5
map-scale|15|4|35|8|55|12|75|16
discount-budget|34000|68000|102000|136000|170000|204000|238000|272000
pie-reasoning|8|12|16|20|24|28|32|36
observed-ratios|3/10|3/10|3/10|3/10|3/10|3/10|3/10|3/10
composite-area|15|21|27|33|39|45
motion-with-rest|2.5|4.5|6.5|8.5|10.5|12.5
four-step-budget|4000|8000|12000|16000|20000|24000"""
MATH_ANSWERS = {p[0]: p[1:] for line in MATH_SHEET.splitlines() if (p := line.split("|"))}


@pytest.mark.parametrize("subject,unit", UNITS, ids=[s + "-" + u["code"] for s, u in UNITS])
def test_source_content_schema_support_and_answers(subject, unit):
    content = LessonContent.model_validate(unit["lesson"]["content"])
    assert len(content.hints) == 3 and content.free_hint_count == 1
    assert unit["topic"] in TOPICS[subject]
    assert unit["lesson"]["estimated_minutes"] in (12, 15)
    if subject == "MATH":
        solutions = MATH_ANSWERS[unit["code"].removeprefix("g5-")]
        assert len(unit["questions"]) == len(solutions)
    elif subject == "ENGLISH":
        assert 60 <= len(content.blocks[1].text.split()) <= 80
    for i, q in enumerate(unit["questions"]):
        QuestionInput.model_validate(
            dict(
                q,
                code="G5-TEST",
                grade=5,
                topic_id=uuid4(),
                subject_id=uuid4(),
                skill_ids=[uuid4()],
                explanation=q["explanation"]["text"],
            )
        )
        answer = correct_answer(q)
        if subject == "MATH":
            solution = solutions[i]
            answer = (
                {"text": solution}
                if q["question_type"] == "fill_blank"
                else {
                    "option_id": next(
                        o["id"]
                        for o in q["content"]["options"]
                        if o["text"].replace(",", ".") == solution
                    )
                }
            )
        else:
            assert content.blocks[1].text in q["content"]["prompt"]
        validate_answer(q["question_type"], q["content"], answer)
        assert grade_answer(q["question_type"], q["grading"], answer)
        assert not grade_answer(q["question_type"], q["grading"], None)
        if q["question_type"] == "single_choice":
            options = q["content"]["options"]
            assert len({o["text"] for o in options}) == len(options)
            assert (
                sum(
                    grade_answer("single_choice", q["grading"], {"option_id": o["id"]})
                    for o in options
                )
                == 1
            )
        else:
            assert grade_answer(
                "fill_blank", q["grading"], {"text": solutions[i].replace(".", ",")}
            )


def test_original_reading_lengths_and_plan_inventory():
    for text in (UMBRELLA, SEEDLING):
        assert 300 <= len(text.split()) <= 350
    for text in (SCENERY, PERSON):
        assert 200 <= len(text.split()) <= 250
    assert len(RAIN.split()) == 230
    assert 110 <= len(POEM.split()) <= 130
    assert len(UNITS) == 68
    assert sum(len(u["questions"]) for _, u in UNITS) == 384
    assert sum(u["minimum_plan_code"] == "vip" for _, u in UNITS) == 22
    assert sum(len(u["questions"]) for _, u in UNITS if u["minimum_plan_code"] == "vip") == 156


@pytest.mark.parametrize(
    "patch",
    [
        {"kind": "pie", "values": [50, 30, 10]},
        {"kind": "pie", "values": [100], "labels": ["A", "B"]},
        {"kind": "triangle", "base": 0},
        {"kind": "box", "width": -1},
        {"kind": "circle", "radius": float("inf")},
        {"kind": "trapezoid", "height": float("nan")},
    ],
)
def test_invalid_figures_cannot_be_saved(patch):
    with pytest.raises(ValidationError):
        Illustration.model_validate({"caption": "Minh họa số liệu bài học", **patch})


def grade5_student(client, conn):
    student, admin = identities(client, conn)
    profiles = db.table("student_profiles")
    conn.execute(profiles.update().where(profiles.c.student_id == student).values(current_grade=5))
    return student, admin


@pytest.mark.integration
def test_seed_inventory_idempotent_and_preserves_editor_revision(conn):
    assert verify_seed(conn, 5) == EXPECTED
    lessons, topics = db.table("lessons"), db.table("topics")
    original = dict(
        conn.execute(select(lessons).join(topics).where(topics.c.grade == 5).limit(1))
        .mappings()
        .one()
    )
    changed = deepcopy(original["content"])
    changed["blocks"][0]["text"] = "Nội dung giáo viên đã điều chỉnh, cần giữ lại."
    conn.execute(lessons.update().where(lessons.c.id == original["id"]).values(content=changed))
    grade4_before = verify_seed(conn, 4)
    seed_grade_content(conn, 5)
    assert verify_seed(conn, 5) == EXPECTED
    assert verify_seed(conn, 4) == grade4_before
    assert (
        conn.execute(select(lessons.c.content).where(lessons.c.id == original["id"])).scalar_one()
        == changed
    )


@pytest.mark.integration
@pytest.mark.parametrize("subject", ["MATH", "VIETNAMESE", "ENGLISH"])
def test_every_assessment_save_resume_submit_and_history(logged_student, conn, subject):
    client = logged_student
    student, admin = grade5_student(client, conn)
    membership(conn, student, admin)
    assessments = client.get(f"/api/v1/assessments?grade=5&subject_code={subject}").json()
    assert len(assessments) == EXPECTED[subject]["assessments"]
    versions = db.table("question_versions")
    for assessment in assessments:
        assigned = client.post(f"/api/v1/students/me/assessments/{assessment['id']}/assign-self")
        assert assigned.status_code == 200, assigned.text
        started = client.post("/api/v1/attempts", json={"assignment_id": assigned.json()["id"]})
        assert started.status_code == 200, started.text
        identifier = started.json()["id"]
        body = client.get(f"/api/v1/attempts/{identifier}")
        assert all(
            s not in body.text
            for s in ["correct_option_id", "accepted_answers", "grading", "explanation"]
        )
        for item in body.json()["items"]:
            q = dict(
                conn.execute(
                    select(versions).where(versions.c.id == UUID(item["question_version_id"]))
                )
                .mappings()
                .one()
            )
            response = client.put(
                f"/api/v1/attempts/{identifier}/answers/{item['id']}",
                json={"answer": correct_answer(q)},
            )
            assert response.status_code == 200, response.text
        resumed = client.get(f"/api/v1/attempts/{identifier}").json()
        assert all(item["answer"] is not None for item in resumed["items"])
        assert client.post(f"/api/v1/attempts/{identifier}/submit").status_code == 200
        result = client.get(f"/api/v1/attempts/{identifier}/result").json()
        assert result["total_score"] == result["max_score"] > 0
    membership(conn, student, admin, "revoke")
    assert client.get(f"/api/v1/attempts/{identifier}/result").status_code == 200


@pytest.mark.integration
def test_library_own_grade_pagination_filters_hints_live_membership(logged_student, conn):
    client = logged_student
    student, admin = grade5_student(client, conn)
    base = "/api/v1/students/me/lesson-library"
    first = client.get(base)
    assert first.status_code == 200, first.text
    assert "no-store" in first.headers["cache-control"]
    data = first.json()
    assert data["grade"] == 5 and data["summary"] == dict(
        total=68, completed=0, in_progress=0, free=46, vip=22, bookmarked=0
    )
    assert len(data["items"]) == 12
    seen = []
    for page in range(1, 7):
        response = client.get(base, params={"page": page})
        assert all(s not in response.text for s in ["grading", "blocks", "hints", "explanation"])
        seen.extend(item["id"] for item in response.json()["items"])
    assert len(seen) == len(set(seen)) == 68
    assert client.get(base, params={"page": 7}).json()["items"] == []
    for subject, count in [("MATH", 25), ("VIETNAMESE", 23), ("ENGLISH", 20)]:
        assert (
            client.get(base, params={"subject_code": subject}).json()["summary"]["total"] == count
        )
    assert client.get(base, params={"plan": "free"}).json()["summary"]["total"] == 46
    assert client.get(base, params={"category": "thinking"}).json()["summary"]["total"] == 22
    for word in ["bieu do", "BIỂU ĐỒ", "  biểu đồ  "]:
        result = client.get(base, params={"search": word}).json()
        assert result["summary"]["total"] == 3
    for word in ["%", "_", "\\", "' OR 1=1 --"]:
        assert client.get(base, params={"search": word}).json()["summary"]["total"] == 0
    for params in [
        {"page": 0},
        {"plan": "admin"},
        {"search": "x" * 81},
        {"subject_code": "MISSING"},
    ]:
        assert client.get(base, params=params).status_code == 422
    free = data["items"][0]
    vip = client.get(base, params={"plan": "vip"}).json()["items"][0]
    path = f"/api/v1/lessons/{free['id']}"
    assert len(client.get(path).json()["content"]["hints"]) == 1
    assert vip["locked"] and client.get(f"/api/v1/lessons/{vip['id']}").status_code == 403
    assert client.post(path + "/visit").status_code == 200
    assert client.get(base, params={"progress": "in_progress"}).json()["summary"]["total"] == 1
    assert client.post(path + "/complete").status_code == 200
    assert client.get(base, params={"progress": "completed"}).json()["items"][0]["id"] == free["id"]
    membership(conn, student, admin)
    vip_library = client.get("/api/v1/students/me/vip/library").json()
    assert vip_library["grade"] == 5 and len(vip_library["lessons"]) == 22
    adaptive = client.post(
        "/api/v1/students/me/learning-plans", json={"subject_code": "MATH", "mode": "adaptive"}
    )
    assert adaptive.status_code == 200, adaptive.text
    assert adaptive.json()["mode"] == "adaptive" and adaptive.json()["items"]
    assert len(client.get(path).json()["content"]["hints"]) == 3
    assert all(
        not row["locked"] for row in client.get(base, params={"plan": "vip"}).json()["items"]
    )
    assert client.get(f"/api/v1/lessons/{vip['id']}").status_code == 200
    membership(conn, student, admin, "revoke")
    assert all(row["locked"] for row in client.get(base, params={"plan": "vip"}).json()["items"])
    assert len(client.get(path).json()["content"]["hints"]) == 1
    assert client.get(f"/api/v1/lessons/{vip['id']}").status_code == 403
    admin_login(client)
    assert client.get(base).status_code == 403
    mapping = client.get("/api/v1/admin/curriculum-map?grade=5").json()
    assert len(mapping["rows"]) == 22
    assert sum(row["questions"] for row in mapping["rows"]) == 384
    assert client.get("/api/v1/admin/curriculum-map?grade=6").status_code == 422
    client.cookies.clear()
    assert client.get(base).status_code == 401


@pytest.mark.integration
def test_library_hides_unpublished_inactive_and_other_student_progress(logged_student, conn):
    client = logged_student
    student, _ = grade5_student(client, conn)
    base = "/api/v1/students/me/lesson-library"
    lessons, topics, progress = (
        db.table(n) for n in ("lessons", "topics", "student_lesson_progress")
    )
    rows = client.get(base).json()["items"]
    identifier = UUID(rows[0]["id"])
    other = conn.execute(
        select(db.table("users").c.id).where(db.table("users").c.username == "longnh")
    ).scalar_one()
    conn.execute(
        progress.insert().values(student_id=other, lesson_id=identifier, status="completed")
    )
    assert client.get(base, params={"progress": "completed"}).json()["items"] == []
    conn.execute(lessons.update().where(lessons.c.id == identifier).values(status="draft"))
    assert client.get(base).json()["summary"]["total"] == 67
    topic = conn.execute(select(lessons.c.topic_id).where(lessons.c.id == identifier)).scalar_one()
    conn.execute(topics.update().where(topics.c.id == topic).values(is_active=False))
    active = client.get(base).json()
    assert active["summary"]["total"] < 67
    profiles = db.table("student_profiles")
    conn.execute(profiles.update().where(profiles.c.student_id == student).values(current_grade=1))
    assert client.get(base).json()["summary"]["total"] == 68
    assert client.get(f"/api/v1/lessons/{rows[2]['id']}").status_code == 403

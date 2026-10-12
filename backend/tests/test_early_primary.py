import json
from copy import deepcopy
from uuid import UUID, uuid4

import pytest
from sqlalchemy import func, select

from app.authoring_schemas import QuestionInput
from app.db import db
from app.early_primary_curriculum import PACKS, TOPICS
from app.early_primary_support import EXPECTED
from app.lesson_schemas import LessonContent
from app.seed import seed_early_primary_content, verify_seed
from app.services.grading import grade_answer
from tests.test_grading import correct_answer
from tests.test_memberships import admin_login, identities, membership

UNITS = [(g, s, u) for g, p in PACKS.items() for s, units in p["all"].items() for u in units]
# Independently checked arithmetic, quantities and shape/time answers, in exercise order.
MATH_SHEETS = {
    1: """count-five|2|4|1|5
zero-ten|0|6|8|10
add-ten|3|4|5|6
subtract-ten|3|3|3|6
flat-shapes|Hình tròn|Hình tam giác|Hình vuông|Hình chữ nhật
solid-shapes|Khối lập phương|Khối hộp chữ nhật|Hình phẳng|Xúc xắc
long-short|A|A|Chung một đầu|Dài bằng nhau
centimetres|3|5|8|10
eleven-twenty|11|12|14|15|17|19
tens-units|21|34|42|56|60|87
compare|14|31|43|50|68|91
round-tens|20|30|50|50|70|90
add-hundred|25|37|46|65|67|80
subtract-hundred|13|22|25|33|64|50
whole-hours|2|4|6|8|10|11
week|Thứ ba|Thứ tư|Thứ năm|Thứ sáu|Thứ bảy|Chủ nhật
more|3|5|7|7|9|8
left|3|3|4|4|4|7
number-gaps|3|5|7|13|15|23|34|48
hidden-add|2|3|4|2|4|2|6|3
relevant|3|4|4|6|7|7|8|9
repeat|Hình tam giác|Hình tròn|Hình tròn|Hình tam giác|Hình tam giác|Hình tròn|Hình tam giác|Hình tròn
different|Hình tam giác|Hình tròn|Hình tròn|Hình vuông|Hình vuông|Hình tam giác
shape-objects|Hình tròn|Hình chữ nhật|Hình vuông|Hình tam giác|Hình tròn|Hình vuông
before-after|7|8|6|9|8|10""",
    2: """read-tens|32|46|50|78
compare-tens|32|59|70|91
carry-hundred|25|41|61|64
borrow-hundred|17|17|26|44
times-2|4|6|8|12
times-5|10|15|20|30
length-units|10|20|40|60
mass-volume|5|6|3|8
read-thousand|123|205|340|416|608|999
hundreds|200|400|500|600|700|800
number-line|200|299|409|619|900|999
add-thousand|337|337|467|570|815|870
subtract-thousand|222|333|333|603|440|433
single-carry|263|363|563|583|763|861
lines|5|9|8|11|13|15
four-sides|4|Khối cầu|Khối trụ|Có|Không|Các đoạn nối tiếp
quarter-half|60|24|15|30|31|19
picture-count|2|4|5|3|6|8
more-than|15|19|27|33|39|51|60|74
less-than|14|18|27|38|48|58|64|77
share|3|5|7|9|2|4|6|8
missing|9|13|23|33|37|46|49|49
chance|Chắc chắn|Không thể|Có thể|Chắc chắn|Không thể|Có thể
schedule|8|10|21|14|30|15
line-check|7|11|15|13|17|22""",
}
MATH_ANSWERS = {
    g: {p[0]: p[1:] for line in sheet.splitlines() if (p := line.split("|"))}
    for g, sheet in MATH_SHEETS.items()
}


@pytest.mark.parametrize(
    "grade,subject,unit", UNITS, ids=[f"g{g}-{s}-{u['code']}" for g, s, u in UNITS]
)
def test_all_lessons_have_valid_support_and_unambiguous_grading(grade, subject, unit):
    content = LessonContent.model_validate(unit["lesson"]["content"])
    assert len(content.hints) == 3 and content.free_hint_count == 1
    assert unit["lesson"]["estimated_minutes"] == (6 if grade == 1 else 8)
    assert unit["topic"] in TOPICS[grade][subject]
    assert len(
        {
            json.dumps(
                {
                    "prompt": q["content"]["prompt"],
                    "options": sorted(o["text"] for o in q["content"].get("options", [])),
                },
                ensure_ascii=False,
                sort_keys=True,
            )
            for q in unit["questions"]
        }
    ) == len(unit["questions"])
    for i, q in enumerate(unit["questions"]):
        QuestionInput.model_validate(
            dict(
                q,
                code="EARLY-TEST",
                grade=grade,
                topic_id=uuid4(),
                subject_id=uuid4(),
                skill_ids=[uuid4()],
                explanation=q["explanation"]["text"],
            )
        )
        assert not grade_answer(q["question_type"], q["grading"], None)
        if q["question_type"] == "single_choice":
            choices = q["content"]["options"]
            assert len(choices) in (2, 3)
            assert len({o["text"] for o in choices}) == len(choices)
            assert (
                sum(
                    grade_answer("single_choice", q["grading"], {"option_id": o["id"]})
                    for o in choices
                )
                == 1
            )
        if subject == "MATH":
            solution = MATH_ANSWERS[grade][unit["code"].split("-", 1)[1]][i]
            answer = (
                {"text": solution}
                if q["question_type"] == "fill_blank"
                else {
                    "option_id": next(
                        o["id"] for o in q["content"]["options"] if o["text"] == solution
                    )
                }
            )
            assert grade_answer(q["question_type"], q["grading"], answer), (unit["code"], i)
        else:
            assert content.blocks[1].text in q["content"]["prompt"]


@pytest.mark.parametrize("grade", [1, 2])
@pytest.mark.integration
def test_inventory_plans_short_lessons_and_repeat_seed_preserves_edits(conn, grade):
    assert verify_seed(conn, grade) == EXPECTED
    lessons, topics, policies = (
        db.table(n) for n in ("lessons", "topics", "content_access_policies")
    )
    for kind, expected in [
        ("lesson", {"free": 46, "vip": 22}),
        ("assessment", {"free": 34, "vip": 22}),
    ]:
        table = lessons if kind == "lesson" else db.table("assessments")
        actual = conn.execute(
            select(policies.c.minimum_plan_code, func.count())
            .select_from(table.join(policies, policies.c[f"{kind}_id"] == table.c.id))
            .where(table.c.code.like(f"VT{grade}-%"))
            .group_by(policies.c.minimum_plan_code)
        ).all()
        assert dict(actual) == expected
    identifier = conn.execute(
        select(lessons.c.id).join(topics).where(topics.c.grade == grade).limit(1)
    ).scalar_one()
    content = deepcopy(
        conn.execute(select(lessons.c.content).where(lessons.c.id == identifier)).scalar_one()
    )
    content["goals"] = ["Mục tiêu đã được giáo viên điều chỉnh"]
    conn.execute(lessons.update().where(lessons.c.id == identifier).values(content=content))
    names = [
        "users",
        "student_profiles",
        "student_memberships",
        "auth_sessions",
        "lessons",
        "question_versions",
        "assessments",
        "assessment_items",
        "content_access_policies",
        "attempts",
        "student_lesson_progress",
    ]
    before = {
        n: [
            dict(r)
            for r in conn.execute(
                select(db.table(n)).order_by(*db.table(n).primary_key.columns)
            ).mappings()
        ]
        for n in names
    }
    seed_early_primary_content(conn, grade)
    after = {
        n: [
            dict(r)
            for r in conn.execute(
                select(db.table(n)).order_by(*db.table(n).primary_key.columns)
            ).mappings()
        ]
        for n in names
    }
    assert before == after


@pytest.mark.parametrize("grade", [1, 2])
@pytest.mark.integration
def test_free_vip_hints_expiry_revocation_grade_scope_and_admin_map(logged_student, conn, grade):
    client = logged_student
    student, admin = identities(client, conn)
    profiles = db.table("student_profiles")
    conn.execute(
        profiles.update().where(profiles.c.student_id == student).values(current_grade=grade)
    )
    lessons = db.table("lessons")
    free = (
        conn.execute(
            select(lessons.c.id, lessons.c.content).where(
                lessons.c.code == f"VT{grade}-MATH-numbers-lesson-1"
            )
        )
        .mappings()
        .one()
    )
    path = f"/api/v1/lessons/{free['id']}"
    response = client.get(path)
    assert response.status_code == 200 and len(response.json()["content"]["hints"]) == 1
    assert all(h not in response.text for h in free["content"]["hints"][1:])
    catalog = client.get(f"/api/v1/assessments?grade={grade}").json()
    vip = next(a for a in catalog if a["minimum_plan_code"] == "vip")
    assert (
        client.post(f"/api/v1/students/me/assessments/{vip['id']}/assign-self").status_code == 403
    )
    wrong = conn.execute(
        select(lessons.c.id).where(lessons.c.code == "VT4-MATH-numbers-lesson-1")
    ).scalar_one()
    assert client.get(f"/api/v1/lessons/{wrong}").status_code == 403
    plan = client.post("/api/v1/students/me/learning-plans", json={"subject_code": "MATH"})
    assert plan.status_code == 200, plan.text
    assigned_lessons = [step["lesson_id"] for step in plan.json()["items"] if step["lesson_id"]]
    assert len(assigned_lessons) == 3
    assert all(
        client.get(f"/api/v1/lessons/{identifier}").json()["grade"] == grade
        for identifier in assigned_lessons
    )
    membership(conn, student, admin)
    assert len(client.get(path).json()["content"]["hints"]) == 3
    membership(conn, student, admin, "revoke")
    assert len(client.get(path).json()["content"]["hints"]) == 1
    assert client.get("/api/v1/students/me/thinking").json()["grade"] == grade
    admin_login(client)
    report = client.get(f"/api/v1/admin/curriculum-map?grade={grade}").json()
    assert len(report["rows"]) == 21
    assert sum(r["free_lessons"] for r in report["rows"]) == 46
    assert sum(r["vip_lessons"] for r in report["rows"]) == 22
    assert sum(r["questions"] for r in report["rows"]) == 384


@pytest.mark.parametrize("grade", [1, 2])
@pytest.mark.parametrize("subject", ["MATH", "VIETNAMESE", "ENGLISH"])
@pytest.mark.integration
def test_every_assessment_can_save_resume_submit_and_keep_result(
    logged_student, conn, grade, subject
):
    client = logged_student
    student, admin = identities(client, conn)
    conn.execute(
        db.table("student_profiles")
        .update()
        .where(db.table("student_profiles").c.student_id == student)
        .values(current_grade=grade)
    )
    membership(conn, student, admin)
    assessments = client.get(f"/api/v1/assessments?grade={grade}&subject_code={subject}").json()
    assert len(assessments) == EXPECTED[subject]["assessments"]
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
            versions = db.table("question_versions")
            q = dict(
                conn.execute(
                    select(versions).where(versions.c.id == UUID(item["question_version_id"]))
                )
                .mappings()
                .one()
            )
            assert (
                client.put(
                    f"/api/v1/attempts/{identifier}/answers/{item['id']}",
                    json={"answer": correct_answer(q)},
                ).status_code
                == 200
            )
        resumed = client.get(f"/api/v1/attempts/{identifier}").json()
        assert all(item["answer"] is not None for item in resumed["items"])
        assert client.post(f"/api/v1/attempts/{identifier}/submit").status_code == 200
        result = client.get(f"/api/v1/attempts/{identifier}/result").json()
        assert result["total_score"] == result["max_score"] > 0
    membership(conn, student, admin, "revoke")
    assert client.get(f"/api/v1/attempts/{identifier}/result").status_code == 200

from copy import deepcopy
from datetime import timedelta
from uuid import UUID, uuid4

import pytest
from pydantic import ValidationError
from sqlalchemy import func, select

from app.authoring_schemas import QuestionInput
from app.core.security import now
from app.db import db
from app.grade3_curriculum import ALL, EXPECTED
from app.lesson_schemas import LessonContent
from app.seed import seed_grade3_content, verify_seed
from app.services.grading import grade_answer, validate_answer
from tests.test_grading import correct_answer
from tests.test_memberships import admin_login, identities, membership

# Answer texts checked against the arithmetic and the original reading passages.
# Selection ids are resolved from these texts, never copied from grading keys.
SHEETS = {
    "MATH": """
read-four|2703|500|6248|4000
compare-four|5012|8910|6999|9999
multiply-tables|42|72|45|56
division-tables|9|9|4|8
equal-parts|2|3|4|7
part-of-group|9|8|7|6
length|40|28|7|55
mass-volume|1000|2000|350|380
five-digits|35204|60000|100000|500|70009|82307
rounding|4260|4270|7500|12000|30000|17000
roman|4|6|9|12|18|20
add-subtract|3825|5544|37875|31275|7000|52220
one-digit|492|618|212|312|6025|1008
expressions|40|64|81|9|44|23
clock-calendar|60|30|20|120|30|6
perimeter|20|26|48|40|7|18
area|24|9|28|18|64|7
tables|30|4|36|24|21|8
two-steps|19|34|10|8|21|43
remainders|1|7|5|59|8|8|1|76
enough-boxes|4|4|5|7|6|6|6|6
shopping|12000|6000|35000|6|11000|10000|16000|3000
same-perimeter|16|12|16|15|3|16|7|21
intervals|5|12|5|14|18|7
possible|2|0|8|2|9|3
""",
    "VIETNAMESE": """
garden-story|Mai|Mỗi sáng|Để cây nhận ánh sáng|Mầm xanh
library-story|Bìa bị bong|Cô thủ thư|Khi keo khô|Biết giữ gìn sách chung
school-words|Thước kẻ|Đọc|Thủ thư|Rộng
community-words|Cảm ơn bạn|Yêu thương|Quét nhà|Xin lỗi bạn
sentence-patterns|Anh em là sinh viên.|Lan vẽ tranh.|Bông hoa thơm.|Bé
punctuation|Dấu hỏi|Dấu chấm|Dấu chấm than|Viết hoa chữ cái đầu
proper-names|Nguyễn Văn An|Hà Nội|Lan|Em yêu trường em.
context-spelling|Chân trời|Tổ chim|Nụ cười|Rửa
poem|Ô cửa|Gió|Tiếng cười|Bốn dòng|Vui tươi|Nhành lá xanh
instructions|Sạch|Người lớn|Bên ngoài hộp|Khi hồ dán khô|Hồ dán|Dán giấy màu~Chờ hồ khô~Đặt bút vào hộp
comparison|Chiếc đĩa|Dáng tròn|Như|Suối trong như gương.|Màu trắng|Lá bàng như chiếc quạt.
dialogue|Dấu hai chấm|Đánh dấu lời nhân vật|Mẹ|Con chuẩn bị rồi ạ.|Sự lễ phép|Dấu hỏi
short-paragraph|Chiếc cặp|Cặp có hai ngăn.|Quai cặp giúp em đeo thoải mái.|Em lau cặp mỗi tối.|Quan sát đồ vật|Quan sát, lập ý~Viết thành câu~Đọc và sửa
message|Mẹ|An|Nhà bà|Bố|5 giờ chiều|Việc chính và người gửi
listen-retell|Bình|Sân|Phân loại lá khô|Rửa tay|Nhờ người nói nhắc lại|Nhặt lá~Phân loại lá~Rửa tay
evidence|Mây xám|Mẹ|Em mặc áo mưa|Hòa biết chuẩn bị trước.|Màu áo mưa|Khi mưa bắt đầu rơi|Có mây xám~Hòa đi cùng mẹ|Tìm chi tiết làm bằng chứng
logic-books|Thơ|Truyện|Sách cây|Truyện|Không, vì mỗi cuốn một bạn|Lập bảng và loại trừ|An chọn thơ|Chưa đủ thông tin
meaning-context|Cách nói dịu dàng|Khối lượng cặp nhỏ|Mây trắng như bông.|Sự ấm áp|Chăm chú|Đọc câu và đoạn quanh từ
repair-sentences|Lan đang đọc sách.|Bạn đọc sách gì?|Em thích vẽ.|Ôi, hoa đẹp quá!|Dấu hai chấm|Giữ ý chính và làm câu rõ hơn
edit-notice|Lớp 3B|Thư viện|15 giờ thứ sáu|Một truyện sạch, đủ trang|Cô Hoa|Hỏi người phụ trách|Thời gian~Địa điểm|Để giữ đúng thông tin ban đầu
recount|Nhặt và trả sách|Bạn đánh rơi sách|Em vui vì đã giúp bạn.|Bạn đánh rơi sách~Em trả sách~Bạn cảm ơn|Cá vàng bơi trong bể.|Kể việc thật bằng lời của mình|Cảm xúc hoặc điều em học được|Trình tự, ý câu và dấu câu
letter|Bà|Mai|Dạo này bà có khỏe không ạ?|Biết tự chuẩn bị cặp|Cháu chúc bà khỏe.|Tên người gửi
discussion|Nơi đặt góc đọc|Đủ ánh sáng|Tránh lối đi để an toàn|Lắng nghe hết lượt|Mình đề xuất cách khác vì...|Đủ sáng và tránh lối đi
""",
    "ENGLISH": """
greetings|Hello!|What is your name?|My|Ben
age|Nine|Eight|How old are you?|am
supplies|Ruler|Blue|This is a book.|pen
classroom|Đứng lên|Ngồi xuống|Please|Mở sách
members|Linh|Minh|Sister|mother
pronouns|Ten|Seven|is|Brother
rooms|Bedroom|Kitchen|Living room|Where is the book?
positions|Under the table|On the desk|in|Trong túi
toys|Two|Kite|On the chair|are|There is a kite.|Cất đồ chơi
colours|Yellow|Red|Blue|What colour is it?|Green|red
pet-words|Cat|White|Dog|Black|Bird|Water
likes|Drawing|Reading|A flower|A cat|Do you like drawing?|do
can|Sing|Swim|Swim|Sing|Can you sing?|can
friend-cards|Ben|Mai|Lucy|Tuổi|Reading|Lucy|Mai~Lucy|How old are you?
polite-help|Ruler|Mai|May I come in?|Thank you.|You are welcome.|Trả lại Mai
room-reading|Two|Red ball|In the bag|On the bed|Books|under|The pen is blue.|Books
lost-toy|Ball|Ball|Kite|Car|Red|Yellow|Ben wants the blue toy.~Each child takes one toy.|No, not enough information.
pet-cards|White cat|On the chair|Black dog|Under the table|Bird|cannot|Big|Tên của con chó
actions-now|Reading|Drawing a flower|In the garden|am|She is singing.|What are you doing?
mixed-review|Nine|Seven|Dolls|Cars|Living room|Reading
""",
}
ANSWERS = {
    subject: {
        parts[0]: parts[1:] for line in sheet.strip().splitlines() if (parts := line.split("|"))
    }
    for subject, sheet in SHEETS.items()
}
PACK = [(subject, unit) for subject, units in ALL.items() for unit in units]


@pytest.mark.parametrize("subject,unit", PACK, ids=[s + "-" + u["code"] for s, u in PACK])
def test_all_384_questions_support_and_answers(subject, unit):
    content = LessonContent.model_validate(unit["lesson"]["content"])
    assert len(content.hints) == 3 and content.free_hint_count == 1
    expected = ANSWERS[subject][unit["code"].removeprefix("g3-")]
    assert len(unit["questions"]) == len(expected)
    for question, solution in zip(unit["questions"], expected, strict=True):
        QuestionInput.model_validate(
            {
                **question,
                "explanation": question["explanation"]["text"],
                "code": "TEST-G3",
                "grade": 3,
                "subject_id": uuid4(),
                "topic_id": uuid4(),
                "skill_ids": [uuid4()],
            }
        )
        kind = question["question_type"]
        options = {o["text"]: o["id"] for o in question["content"].get("options", [])}
        answer = (
            {"text": solution}
            if kind == "fill_blank"
            else (
                {"option_id": options[solution]}
                if kind == "single_choice"
                else {
                    "ordered_ids" if kind == "ordering" else "option_ids": [
                        options[s] for s in solution.split("~")
                    ]
                }
            )
        )
        validate_answer(kind, question["content"], answer)
        assert grade_answer(kind, question["grading"], answer)
        assert not grade_answer(kind, question["grading"], None)
        if kind == "single_choice":
            assert (
                sum(
                    grade_answer(kind, question["grading"], {"option_id": option_id})
                    for option_id in options.values()
                )
                == 1
            )
        assert len(question["explanation"]["text"]) >= 5
        if subject != "MATH":
            assert unit["lesson"]["content"]["blocks"][1]["text"] in question["content"]["prompt"]


@pytest.mark.parametrize("free_count", [0, 4, 6])
def test_invalid_hint_allocation_cannot_be_saved(free_count):
    content = deepcopy(ALL["MATH"][0]["lesson"]["content"])
    content["free_hint_count"] = free_count
    with pytest.raises(ValidationError):
        LessonContent.model_validate(content)


def grade3_student(client, conn):
    student, admin = identities(client, conn)
    table = db.table("student_profiles")
    conn.execute(table.update().where(table.c.student_id == student).values(current_grade=3))
    return student, admin


@pytest.mark.integration
def test_inventory_matches_grade4_and_seed_preserves_edits_and_history(conn):
    assert verify_seed(conn, grade=3) == EXPECTED
    versions, questions = db.table("question_versions"), db.table("questions")
    version = dict(
        conn.execute(select(versions).join(questions).where(questions.c.grade == 3).limit(1))
        .mappings()
        .one()
    )
    for key in ("id", "created_at"):
        version.pop(key)
    version["version"] = 2
    version["status"] = "draft"
    conn.execute(versions.insert().values(**version))
    # A draft revision does not increase the published-question inventory.
    assert verify_seed(conn, grade=3) == EXPECTED
    grade4 = verify_seed(conn, grade=4)
    assert all(
        grade4[s][key] >= count for s, counts in EXPECTED.items() for key, count in counts.items()
    )
    lessons, policies, topics = (
        db.table(n) for n in ("lessons", "content_access_policies", "topics")
    )
    for kind, expected in (
        ("lesson", {"free": 46, "vip": 22}),
        ("assessment", {"free": 34, "vip": 22}),
    ):
        table = lessons if kind == "lesson" else db.table("assessments")
        query = (
            select(policies.c.minimum_plan_code, func.count())
            .select_from(table.join(policies, policies.c[f"{kind}_id"] == table.c.id))
            .where(table.c.code.like("VT3-%"))
            .group_by(policies.c.minimum_plan_code)
        )
        assert dict(conn.execute(query).all()) == expected
    questions, qpolicies, versions = (
        db.table(n) for n in ("questions", "question_version_access_policies", "question_versions")
    )
    assert dict(
        conn.execute(
            select(qpolicies.c.minimum_plan_code, func.count())
            .select_from(questions.join(versions).join(qpolicies))
            .where(questions.c.grade == 3)
            .group_by(qpolicies.c.minimum_plan_code)
        ).all()
    ) == {"free": 228, "vip": 156}
    identifier = conn.execute(
        select(lessons.c.id).where(lessons.c.code == "VT3-MATH-numbers-lesson-1")
    ).scalar_one()
    content = conn.execute(select(lessons.c.content).where(lessons.c.id == identifier)).scalar_one()
    content["goals"] = ["Mục tiêu lớp 3 đã được giáo viên điều chỉnh"]
    conn.execute(lessons.update().where(lessons.c.id == identifier).values(content=content))
    names = [
        "users",
        "student_profiles",
        "auth_sessions",
        "student_memberships",
        "lessons",
        "question_versions",
        "assessments",
        "assessment_items",
        "content_access_policies",
        "attempts",
        "attempt_answers",
        "student_lesson_progress",
    ]
    before = {
        name: [dict(r) for r in conn.execute(select(db.table(name))).mappings()] for name in names
    }
    for _ in range(2):
        seed_grade3_content(conn)
    after = {
        name: [dict(r) for r in conn.execute(select(db.table(name))).mappings()] for name in names
    }
    assert before == after


@pytest.mark.integration
def test_grade3_hints_live_membership_expiry_revocation_and_no_leak(logged_student, conn):
    client = logged_student
    student, admin = grade3_student(client, conn)
    lessons, topics = db.table("lessons"), db.table("topics")
    rows = (
        conn.execute(
            select(lessons.c.id, lessons.c.content).join(topics).where(topics.c.grade == 3)
        )
        .mappings()
        .all()
    )
    free = next(r for r in rows if r["content"]["blocks"][0]["text"].startswith("Số có bốn chữ số"))
    identifier = str(free["id"])
    path = f"/api/v1/lessons/{identifier}"
    response = client.get(path)
    assert response.status_code == 200 and response.headers["cache-control"] == "no-store"
    assert response.json()["hint_access"] == {"available": 1, "total": 3, "vip_locked": 2}
    assert response.json()["content"]["hints"] == free["content"]["hints"][:1]
    assert all(text not in response.text for text in free["content"]["hints"][1:])
    assert "free_hint_count" not in response.json()["content"]
    membership(conn, student, admin)
    assert client.get(path).json()["content"]["hints"] == free["content"]["hints"]
    features = db.table("membership_plan_features")
    conn.execute(features.delete().where(features.c.feature_code == "learning.guided_hints"))
    assert len(client.get(path).json()["content"]["hints"]) == 1
    conn.execute(features.insert().values(plan_code="vip", feature_code="learning.guided_hints"))
    members = db.table("student_memberships")
    conn.execute(
        members.update()
        .where(members.c.student_id == student)
        .values(starts_at=now() - timedelta(days=2), ends_at=now() - timedelta(seconds=1))
    )
    assert len(client.get(path).json()["content"]["hints"]) == 1
    membership(conn, student, admin)
    assert len(client.get(path).json()["content"]["hints"]) == 3
    membership(conn, student, admin, "revoke")
    assert len(client.get(path).json()["content"]["hints"]) == 1
    admin_login(client)
    assert len(client.get(path).json()["content"]["hints"]) == 3


@pytest.mark.integration
def test_grade3_catalogues_current_grade_and_admin_filters(logged_student, conn):
    client = logged_student
    grade3_student(client, conn)
    available = client.get("/api/v1/grades").json()
    assert [r["grade"] for r in available if r["status"] == "available"] == [1, 2, 3, 4]
    assert client.get("/api/v1/admin/curriculum-map?grade=3").status_code == 403
    lessons = db.table("lessons")
    grade4_id = conn.execute(
        select(lessons.c.id).where(lessons.c.code == "VT4-MATH-numbers-lesson-1")
    ).scalar_one()
    assert client.get(f"/api/v1/lessons/{grade4_id}").json()["detail"]["code"] == "GRADE_REQUIRED"
    thinking = client.get("/api/v1/students/me/thinking").json()
    assert thinking["grade"] == 3 and thinking["total"] >= 6
    for item in thinking["items"]:
        assert item["minimum_plan_code"] == "vip" and item["locked"]
        assert client.get(f"/api/v1/lessons/{item['id']}").status_code == 403
    admin_login(client)
    report = client.get("/api/v1/admin/curriculum-map?grade=3").json()
    assert report["grade"] == 3 and len(report["rows"]) == 21
    assert sum(r["free_lessons"] for r in report["rows"]) == 46
    assert sum(r["vip_lessons"] for r in report["rows"]) == 22
    assert sum(r["questions"] for r in report["rows"]) == 384
    assert sum(r["assessments"] for r in report["rows"]) == 56
    assert len(client.get("/api/v1/admin/curriculum-map?grade=2").json()["rows"]) == 21
    assert client.get("/api/v1/admin/questions?grade=3").json()["total"] == 384
    assert client.get("/api/v1/admin/lessons?grade=3").json()["total"] == 68


@pytest.mark.integration
@pytest.mark.parametrize(
    "subject,vip", [("MATH", False), ("VIETNAMESE", False), ("ENGLISH", False), ("MATH", True)]
)
def test_grade3_real_attempt_grading_and_learning_plan(logged_student, conn, subject, vip):
    client = logged_student
    student, admin = grade3_student(client, conn)
    catalogue = client.get(f"/api/v1/assessments?grade=3&subject_code={subject}").json()
    assessment = next(a for a in catalogue if (a["minimum_plan_code"] == "vip") == vip)
    path = f"/api/v1/students/me/assessments/{assessment['id']}/assign-self"
    if vip:
        assert client.post(path).status_code == 403
        membership(conn, student, admin)
    assigned = client.post(path)
    assert assigned.status_code == 200, assigned.text
    started = client.post("/api/v1/attempts", json={"assignment_id": assigned.json()["id"]})
    assert started.status_code == 200, started.text
    identifier = started.json()["id"]
    response = client.get(f"/api/v1/attempts/{identifier}")
    assert all(
        secret not in response.text
        for secret in ("grading", "accepted_answers", "correct_option", "explanation")
    )
    for item in response.json()["items"]:
        table = db.table("question_versions")
        question = dict(
            conn.execute(select(table).where(table.c.id == UUID(item["question_version_id"])))
            .mappings()
            .one()
        )
        saved = client.put(
            f"/api/v1/attempts/{identifier}/answers/{item['id']}",
            json={"answer": correct_answer(question)},
        )
        assert saved.status_code == 200, saved.text
    assert client.post(f"/api/v1/attempts/{identifier}/submit").status_code == 200
    result = client.get(f"/api/v1/attempts/{identifier}/result").json()
    assert result["total_score"] == result["max_score"] > 0
    assert result["correct_count"] == assessment["item_count"]
    plan = client.post("/api/v1/students/me/learning-plans", json={"subject_code": subject})
    assert plan.status_code == 200, plan.text
    for step in plan.json()["items"]:
        if step["lesson_id"]:
            assert client.get(f"/api/v1/lessons/{step['lesson_id']}").json()["grade"] == 3

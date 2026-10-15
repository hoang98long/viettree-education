"""Shared additive publishing for named releases, separate from baseline inventory."""

from dataclasses import dataclass
from typing import Callable

from sqlalchemy import func, select, text

from app.curriculum.registry import SUPPORTED_GRADES, get_pack
from app.curriculum.seeding import seed_advanced_content
from app.db import db


@dataclass(frozen=True)
class SupplementPack:
    code: str
    title: str
    content: Callable[[int], dict]

    def inventory(self, grades=SUPPORTED_GRADES):
        return {
            "release": self.code,
            "grades": {
                str(grade): {
                    subject: {
                        "lessons": len(units),
                        "questions": sum(len(unit["questions"]) for unit in units),
                        "assessments": len(units),
                        "free_lessons": sum(unit["minimum_plan_code"] == "free" for unit in units),
                        "vip_lessons": sum(unit["minimum_plan_code"] == "vip" for unit in units),
                    }
                    for subject, units in self.content(grade).items()
                }
                for grade in dict.fromkeys(grades)
            },
        }

    def expected(self, grade):
        rows = self.inventory([grade])["grades"][str(grade)].values()
        return {
            key: sum(row[key] for row in rows) for key in ("lessons", "questions", "assessments")
        }

    def published_counts(self, conn, grade):
        source = self.content(grade)
        codes = [
            f"VT{grade}-{subject}-{unit['code']}"
            for subject, units in source.items()
            for unit in units
        ]
        counts = {}
        for name, suffix in (("lessons", "-lesson"), ("assessments", "-practice")):
            table = db.table(name)
            counts[name] = conn.execute(
                select(func.count())
                .select_from(table)
                .where(
                    table.c.code.in_([code + suffix for code in codes]),
                    table.c.status == "published",
                )
            ).scalar_one()
        questions, versions = db.table("questions"), db.table("question_versions")
        question_codes = [
            f"VT{grade}-{subject}-{unit['code']}-q-{index:02d}"
            for subject, units in source.items()
            for unit in units
            for index in range(1, len(unit["questions"]) + 1)
        ]
        counts["questions"] = conn.execute(
            select(func.count(func.distinct(questions.c.id)))
            .select_from(questions.join(versions))
            .where(
                questions.c.code.in_(question_codes),
                questions.c.is_active.is_(True),
                versions.c.status == "published",
            )
        ).scalar_one()
        return counts

    def verify(self, conn, grades=SUPPORTED_GRADES):
        report = {"release": self.code, "grades": {}}
        for grade in dict.fromkeys(grades):
            counts = self.published_counts(conn, grade)
            if counts != self.expected(grade):
                raise ValueError(f"Bộ {self.code} lớp {grade} chưa đủ bài đã xuất bản")
            report["grades"][str(grade)] = counts
        return report

    def seed(self, conn, grades=SUPPORTED_GRADES):
        grades = tuple(dict.fromkeys(grades))
        conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
        topics = db.table("topics")
        expected = set()
        for grade in grades:
            for subject, units in self.content(grade).items():
                for unit in units:
                    if unit["topic"] not in get_pack(grade).topics[subject]:
                        raise ValueError("Chủ đề bổ sung không thuộc chương trình của khối")
                    expected.add(f"VT{grade}-{subject}-{unit['topic']}")
        present = set(
            conn.execute(select(topics.c.code).where(topics.c.code.in_(expected))).scalars()
        )
        if present != expected:
            raise ValueError(
                "Thiếu chủ đề nền tảng. Chạy seed-grade-content --grade N cho các khối đã chọn trước."
            )
        for grade in grades:
            seed_advanced_content(conn, self.content(grade), grade=grade)
        return self.verify(conn, grades)

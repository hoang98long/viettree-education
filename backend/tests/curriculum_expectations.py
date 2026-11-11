"""Independent source contracts for baseline tests with optional packs installed.

Presence selects complete named packs; counts and policies come from the source,
not from the API under test or a COUNT query copied from its implementation.
"""

from collections import Counter

from sqlalchemy import select

from app.curriculum.registry import SUBJECT_CODES, get_pack
from app.curriculum.supplements.registry import releases
from app.db import db


def source_catalog(grade, release_codes=()):
    pack = get_pack(grade)
    catalog = {kind: {} for kind in ("topics", "lessons", "questions", "assessments")}

    def unit(subject, source, *, core):
        prefix = f"VT{grade}-{subject}-{source['code']}"
        topic = source["code"] if core else source["topic"]
        topic_code = f"VT{grade}-{subject}-{topic}"
        common = {
            "subject": subject,
            "plan": "free" if core else source.get("minimum_plan_code", "vip"),
            "topic_code": topic_code,
            "topic_title": pack.topics[subject][topic],
        }
        catalog["topics"][topic_code] = {"subject": subject, "title": common["topic_title"]}
        lesson_sources = source["lessons"] if core else [source["lesson"]]
        for index, lesson in enumerate(lesson_sources, 1):
            code = prefix + (f"-lesson-{index}" if core else "-lesson")
            assert code not in catalog["lessons"], code
            catalog["lessons"][code] = {
                **common,
                "title": lesson["title"],
                "category": lesson["content"].get("category", "core"),
            }
        for index in range(1, len(source["questions"]) + 1):
            code = prefix + f"-q-{index:02d}"
            assert code not in catalog["questions"], code
            catalog["questions"][code] = common
        catalog["assessments"][prefix + "-practice"] = common

    for subject in SUBJECT_CODES:
        for source in pack.core[subject]:
            unit(subject, source, core=True)
        for extension in pack.extensions:
            for source in extension[subject]:
                unit(subject, source, core=False)
    for code in release_codes:
        for subject, sources in releases()[code].content(grade).items():
            for source in sources:
                unit(subject, source, core=False)
    return catalog


def baseline_codes(grade, kind, subject=None):
    return {
        code
        for code, row in source_catalog(grade)[kind].items()
        if subject is None or row["subject"] == subject
    }


def installed_catalog(conn, grade):
    """Require every baseline code and every entity of any present optional pack."""
    baseline = source_catalog(grade)
    complete = source_catalog(grade, releases())
    kinds = ("lessons", "questions", "assessments")
    present = {
        kind: set(
            conn.execute(
                select(db.table(kind).c.code).where(db.table(kind).c.code.in_(complete[kind]))
            ).scalars()
        )
        for kind in kinds
    }
    for kind in kinds:
        assert set(baseline[kind]) <= present[kind], (grade, kind, "baseline missing")
    installed = []
    for release in releases():
        source = source_catalog(grade, [release])
        extra = {kind: set(source[kind]) - set(baseline[kind]) for kind in kinds}
        if any(extra[kind] & present[kind] for kind in kinds):
            assert all(extra[kind] <= present[kind] for kind in kinds), (
                grade,
                release,
                "partially installed pack",
            )
            installed.append(release)
    return source_catalog(grade, installed)


def catalog_inventory(catalog):
    return {
        subject: {
            kind: sum(row["subject"] == subject for row in rows.values())
            for kind, rows in catalog.items()
        }
        for subject in SUBJECT_CODES
    }


def plan_counts(catalog, kind):
    return dict(Counter(row["plan"] for row in catalog[kind].values()))


def library_summary(catalog):
    plans = plan_counts(catalog, "lessons")
    return dict(
        total=len(catalog["lessons"]),
        completed=0,
        in_progress=0,
        free=plans.get("free", 0),
        vip=plans.get("vip", 0),
        bookmarked=0,
    )

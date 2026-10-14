"""Audit bundled content; optionally inspect published assessment questions read-only."""

import argparse
import json
from pathlib import Path

from sqlalchemy import select

from app.curriculum.quality import audit_sources
from app.db import db, engine
from app.schemas.authoring import QuestionInput


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--database",
        action="store_true",
        help="Read published exercises from configured DB; no writes",
    )
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = audit_sources()
    if args.database:
        with engine().connect() as conn:
            db.load(conn)
            q, v, items, a = (
                db.table(name)
                for name in ("questions", "question_versions", "assessment_items", "assessments")
            )
            rows = (
                conn.execute(
                    select(v, q.c.code, q.c.grade, q.c.subject_id, q.c.topic_id)
                    .select_from(v.join(q))
                    .where(
                        select(items.c.id)
                        .join(a)
                        .where(items.c.question_version_id == v.c.id, a.c.status == "published")
                        .exists()
                    )
                )
                .mappings()
                .all()
            )
            report["database"] = {"published_assessment_versions": len(rows), "issues": []}
            for row in rows:
                try:
                    QuestionInput.model_validate(
                        {
                            "code": row["code"],
                            "grade": row["grade"],
                            "subject_id": row["subject_id"],
                            "topic_id": row["topic_id"],
                            "skill_ids": [row["question_id"]],
                            "question_type": row["question_type"],
                            "difficulty": row["difficulty"],
                            "content": row["content"],
                            "grading": row["grading"],
                            "explanation": row["explanation"]["text"],
                        }
                    )
                except (ValueError, KeyError) as error:
                    report["database"]["issues"].append(
                        {
                            "code": row["code"],
                            "version": row["version"],
                            "kind": type(error).__name__,
                        }
                    )
    payload = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            {
                "source_issues": len(report["issues"]),
                "source_questions": sum(row["questions"] for row in report["matrix"]),
                "database": report.get("database"),
            },
            ensure_ascii=False,
        )
    )
    if report["issues"] or report.get("database", {}).get("issues"):
        raise SystemExit(1)


if __name__ == "__main__":
    main()

"""Full development fixtures. Content-only production commands live in curriculum."""

from sqlalchemy import text

from app.curriculum.seeding import seed_grade_content, verify_seed
from app.db import db
from app.fixtures.base_accounts import seed_accounts


def seed(conn, reset=False):
    conn.execute(text("SELECT pg_advisory_xact_lock(78249100)"))
    db.load(conn)
    seed_accounts(conn, reset)
    for grade in (4, 3, 1, 2, 5):
        seed_grade_content(conn, grade)
    return verify_seed(conn)

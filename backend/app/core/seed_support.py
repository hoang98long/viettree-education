from uuid import NAMESPACE_URL, uuid5

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

from app.db import db


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

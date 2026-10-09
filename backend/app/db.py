import re
from functools import lru_cache
from threading import Lock

from sqlalchemy import MetaData, create_engine, inspect
from sqlalchemy.engine import Connection

from app.core.config import ROOT, settings

SCHEMA = ROOT / "database/viettree_education_schema.sql"
TABLE_NAMES = re.findall(r"CREATE TABLE IF NOT EXISTS (\w+)", SCHEMA.read_text(encoding="utf-8"))
AUTH_TABLES = ["auth_sessions", "auth_login_limits"]


@lru_cache
def engine():
    return create_engine(settings().database_url, pool_pre_ping=True, hide_parameters=True)


class Database:
    def __init__(self):
        self.metadata = MetaData()
        self._lock = Lock()

    def validate(self, connection: Connection, include_auth=True):
        inspector = inspect(connection)
        needed = TABLE_NAMES + (AUTH_TABLES if include_auth else [])
        missing = sorted(set(needed) - set(inspector.get_table_names(schema="public")))
        if missing:
            raise RuntimeError(
                "Thiếu bảng: "
                + ", ".join(missing)
                + ". Import SQL gốc / chạy alembic upgrade head."
            )
        # Đối chiếu cột thật với từng CREATE TABLE của nguồn SQL.
        source = SCHEMA.read_text(encoding="utf-8")
        for name in TABLE_NAMES:
            block = source.split(f"CREATE TABLE IF NOT EXISTS {name} (", 1)[1].split("\n);", 1)[0]
            required = set(
                re.findall(
                    r"^    (\w+)\s+(?:UUID|VARCHAR|TEXT|BOOLEAN|TIMESTAMPTZ|SMALLINT|JSONB|INTEGER|NUMERIC|DATE|BIGINT|INET|CHAR)",
                    block,
                    re.M,
                )
            )
            actual = {column["name"] for column in inspector.get_columns(name, schema="public")}
            if required - actual:
                raise RuntimeError(
                    f"Schema không khớp: {name}, thiếu cột {sorted(required - actual)}"
                )

    def load(self, connection: Connection):
        with self._lock:
            if not self.metadata.tables:
                self.validate(connection)
                self.metadata.reflect(connection, only=TABLE_NAMES + AUTH_TABLES)

    def table(self, name: str):
        return self.metadata.tables[name]


db = Database()


def connection():
    with engine().begin() as conn:
        db.load(conn)
        yield conn

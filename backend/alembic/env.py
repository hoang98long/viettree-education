from alembic import context

from app.db import engine

if context.is_offline_mode():
    raise RuntimeError("Migration phải kiểm tra trực tiếp schema hiện có")
else:
    with engine().connect() as connection:
        context.configure(connection=connection, target_metadata=None)
        with context.begin_transaction():
            context.run_migrations()

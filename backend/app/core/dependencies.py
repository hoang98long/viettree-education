"""Database transactions finish before any success response reaches the client."""

from fastapi import Depends

from app.db import connection

# FastAPI's default request scope ends after response bytes are sent. A login,
# publish or grade must commit (or roll back) before the next client request.
database = Depends(connection, scope="function")

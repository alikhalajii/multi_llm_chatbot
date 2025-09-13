from sqlalchemy import text
from app.core.db import engine


def check_pgvector():
    """Check if pgvector extension is installed in Postgres."""
    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT extname FROM pg_extension WHERE extname = 'vector';")
        ).fetchone()
        if not result:
            raise RuntimeError(
                "❌ pgvector extension is not installed in the database.\n"
                "Run: CREATE EXTENSION vector; or ensure db/init.sql runs."
            )
        print("✅ pgvector extension is installed.")

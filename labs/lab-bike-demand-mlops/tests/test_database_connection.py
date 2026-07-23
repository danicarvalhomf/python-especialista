from sqlalchemy import text

from src.common.database import get_engine


def test_database_connection():
    engine = get_engine()

    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.scalar()

    assert version is not None
    assert "PostgreSQL" in version
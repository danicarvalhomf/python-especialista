from src.config import (
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
)

def test_database_config():
    assert DATABASE_HOST is not None
    assert DATABASE_PORT is not None
    assert DATABASE_NAME is not None
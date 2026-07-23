from sqlalchemy import create_engine

from src.config import(
    DATABASE_HOST,
    DATABASE_PORT,
    DATABASE_NAME,
    DATABASE_USER,
    DATABASE_PASSWORD
)

DATABASE_URL = (
    "postgresql+psycopg://"
    f"{DATABASE_USER}:{DATABASE_PASSWORD}"
    f"@{DATABASE_HOST}:{DATABASE_PORT}"
    f"/{DATABASE_NAME}"
)

def get_engine():
    return create_engine(
        DATABASE_URL,
        pool_pre_ping=True
    )
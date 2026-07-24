from sqlalchemy import text

from src.common.database import get_engine
from src.ingestion.load_raw_dataset import ingest_raw_dataset


def test_raw_dataset_is_persisted():
    inserted_rows = ingest_raw_dataset()
    engine = get_engine()

    with engine.connect() as connection:
        persisted_rows = connection.execute(
            text("SELECT COUNT(*) FROM bike_rentals_raw;")
        ).scalar_one()

    assert inserted_rows > 0
    assert persisted_rows == inserted_rows
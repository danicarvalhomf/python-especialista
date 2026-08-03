from sqlalchemy import text

from src.common.database import get_engine
from src.features.build_training_dataset import (
    build_training_dataset,
)


def test_feature_dataset_is_persisted():
    persisted_rows = build_training_dataset()
    engine = get_engine()

    with engine.connect() as connection:
        database_rows = connection.execute(
            text(
                """
                SELECT COUNT(*)
                FROM bike_rentals_features;
                """
            )
        ).scalar_one()

    assert persisted_rows > 0
    assert database_rows == persisted_rows
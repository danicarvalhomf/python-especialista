import numpy as np
import pandas as pd
from sqlalchemy import text

from src.common.database import create_database_tables, get_engine

SOURCE_TABLE = "bike_rentals_raw"
FEATURE_TABLE = "bike_rentals_features"


def load_raw_data() -> pd.DataFrame:
    """Load raw bike rental data from PostgreSQL."""

    engine = get_engine()

    query = text(
        """
        SELECT
            instant,
            date,
            season,
            holiday,
            weekday,
            working_day,
            weather_situation,
            temperature,
            apparent_temperature,
            humidity,
            wind_speed,
            total_rentals,
            hour
        FROM bike_rentals_raw
        ORDER BY date, hour;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection)

    if dataframe.empty:
        raise ValueError(
            "The raw dataset table is empty. Run the ingestion pipeline first."
        )

    return dataframe


def build_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Create calendar and cyclical features for demand forecasting."""

    features = dataframe.copy()

    features["date"] = pd.to_datetime(features["date"])

    features["timestamp"] = (
        features["date"]
        + pd.to_timedelta(features["hour"], unit="h")
    )

    features["year"] = features["timestamp"].dt.year
    features["month"] = features["timestamp"].dt.month
    features["day"] = features["timestamp"].dt.day

    # In the UCI dataset:
    # 0 = Sunday and 6 = Saturday.
    features["is_weekend"] = features["weekday"].isin([0, 6])

    # Cyclical representation prevents artificial discontinuities.
    # For example, hour 23 and hour 0 are temporally close.
    features["hour_sin"] = np.sin(
        2 * np.pi * features["hour"] / 24
    )
    features["hour_cos"] = np.cos(
        2 * np.pi * features["hour"] / 24
    )

    features["weekday_sin"] = np.sin(
        2 * np.pi * features["weekday"] / 7
    )
    features["weekday_cos"] = np.cos(
        2 * np.pi * features["weekday"] / 7
    )

    features["month_sin"] = np.sin(
        2 * np.pi * (features["month"] - 1) / 12
    )
    features["month_cos"] = np.cos(
        2 * np.pi * (features["month"] - 1) / 12
    )

    feature_columns = [
        "instant",
        "timestamp",
        "year",
        "month",
        "day",
        "hour",
        "weekday",
        "is_weekend",
        "season",
        "holiday",
        "working_day",
        "weather_situation",
        "temperature",
        "apparent_temperature",
        "humidity",
        "wind_speed",
        "hour_sin",
        "hour_cos",
        "weekday_sin",
        "weekday_cos",
        "month_sin",
        "month_cos",
        "total_rentals",
    ]

    features = features[feature_columns]
    features = features.sort_values("timestamp").reset_index(drop=True)

    if features["timestamp"].duplicated().any():
        raise ValueError("Duplicated timestamps were found.")

    if features.isna().any().any():
        columns_with_nulls = features.columns[
            features.isna().any()
        ].tolist()

        raise ValueError(
            f"Feature dataset contains null values: {columns_with_nulls}"
        )

    return features


def persist_features(dataframe: pd.DataFrame) -> int:
    """Persist the feature dataset into PostgreSQL."""

    create_database_tables()
    engine = get_engine()

    with engine.begin() as connection:
        connection.execute(
            text(f"TRUNCATE TABLE {FEATURE_TABLE};")
        )

        dataframe.to_sql(
            name=FEATURE_TABLE,
            con=connection,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1_000,
        )

    return len(dataframe)


def build_training_dataset() -> int:
    """Run the complete feature engineering pipeline."""

    raw_data = load_raw_data()
    features = build_features(raw_data)

    return persist_features(features)


if __name__ == "__main__":
    persisted_rows = build_training_dataset()
    print(f"Feature rows persisted: {persisted_rows}")
from pathlib import Path

import pandas as pd
from sqlalchemy import text

from src.common.database import create_database_tables, get_engine
from src.config import BASE_DIR

DATASET_PATH = BASE_DIR / "data" / "raw" / "hour.csv"
TABLE_NAME = "bike_rentals_raw"

EXPECTED_COLUMNS = [
    "instant",
    "dteday",
    "season",
    "yr",
    "mnth",
    "hr",
    "holiday",
    "weekday",
    "workingday",
    "weathersit",
    "temp",
    "atemp",
    "hum",
    "windspeed",
    "casual",
    "registered",
    "cnt",
]

COLUMN_MAPPING = {
    "dteday": "date",
    "yr": "year",
    "mnth": "month",
    "hr": "hour",
    "workingday": "working_day",
    "weathersit": "weather_situation",
    "temp": "temperature",
    "atemp": "apparent_temperature",
    "hum": "humidity",
    "windspeed": "wind_speed",
    "casual": "casual_rentals",
    "registered": "registered_rentals",
    "cnt": "total_rentals",
}


def load_raw_dataset(dataset_path: Path = DATASET_PATH) -> pd.DataFrame:
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found: {dataset_path}")

    dataframe = pd.read_csv(dataset_path)

    missing_columns = set(EXPECTED_COLUMNS) - set(dataframe.columns)
    if missing_columns:
        raise ValueError(
            f"Dataset is missing required columns: {sorted(missing_columns)}"
        )

    dataframe = dataframe[EXPECTED_COLUMNS].rename(columns=COLUMN_MAPPING)
    dataframe["date"] = pd.to_datetime(dataframe["date"]).dt.date

    if dataframe.empty:
        raise ValueError("Dataset is empty.")

    if dataframe["instant"].duplicated().any():
        raise ValueError("Dataset contains duplicated instant identifiers.")

    return dataframe


def ingest_raw_dataset() -> int:
    dataframe = load_raw_dataset()
    engine = get_engine()

    create_database_tables()

    with engine.begin() as connection:
        connection.execute(text(f"TRUNCATE TABLE {TABLE_NAME};"))

        dataframe.to_sql(
            name=TABLE_NAME,
            con=connection,
            if_exists="append",
            index=False,
            method="multi",
            chunksize=1_000,
        )

    return len(dataframe)


if __name__ == "__main__":
    inserted_rows = ingest_raw_dataset()
    print(f"Inserted rows: {inserted_rows}")
import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.metrics import (
    mean_absolute_error,
    r2_score,
    root_mean_squared_error,
)
from sqlalchemy import text

from src.common.database import get_engine
from src.config import BASE_DIR


FEATURE_TABLE = "bike_rentals_features"
TARGET_COLUMN = "total_rentals"

MODEL_DIR = BASE_DIR / "models"
REPORTS_DIR = BASE_DIR / "reports"

MODEL_PATH = MODEL_DIR / "bike_demand_model.joblib"
METRICS_PATH = REPORTS_DIR / "training_metrics.json"

FEATURE_COLUMNS = [
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
]


def load_training_data() -> pd.DataFrame:
    """Load the feature dataset from PostgreSQL."""

    engine = get_engine()

    query = text(
        f"""
        SELECT
            timestamp,
            {", ".join(FEATURE_COLUMNS)},
            {TARGET_COLUMN}
        FROM {FEATURE_TABLE}
        ORDER BY timestamp;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection)

    if dataframe.empty:
        raise ValueError(
            "Feature table is empty. Run the feature pipeline first."
        )

    dataframe["timestamp"] = pd.to_datetime(dataframe["timestamp"])

    return dataframe


def temporal_train_test_split(
    dataframe: pd.DataFrame,
    test_fraction: float = 0.20,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split data chronologically without shuffling."""

    if not 0 < test_fraction < 1:
        raise ValueError("test_fraction must be between 0 and 1.")

    split_index = int(len(dataframe) * (1 - test_fraction))

    train_data = dataframe.iloc[:split_index].copy()
    test_data = dataframe.iloc[split_index:].copy()

    if train_data.empty or test_data.empty:
        raise ValueError("Temporal split produced an empty dataset.")

    if train_data["timestamp"].max() >= test_data["timestamp"].min():
        raise ValueError("Temporal leakage detected between train and test.")

    return train_data, test_data


def evaluate_model(
    model: Any,
    features: pd.DataFrame,
    target: pd.Series,
) -> dict[str, float]:
    """Calculate regression metrics."""

    predictions = model.predict(features)

    return {
        "mae": float(mean_absolute_error(target, predictions)),
        "rmse": float(root_mean_squared_error(target, predictions)),
        "r2": float(r2_score(target, predictions)),
    }


def train_models() -> dict[str, Any]:
    """Train baseline and main model, evaluate and persist artifacts."""

    dataframe = load_training_data()
    train_data, test_data = temporal_train_test_split(dataframe)

    x_train = train_data[FEATURE_COLUMNS]
    y_train = train_data[TARGET_COLUMN]

    x_test = test_data[FEATURE_COLUMNS]
    y_test = test_data[TARGET_COLUMN]

    baseline_model = DummyRegressor(strategy="mean")
    baseline_model.fit(x_train, y_train)

    main_model = HistGradientBoostingRegressor(
        learning_rate=0.08,
        max_iter=250,
        max_leaf_nodes=31,
        l2_regularization=0.1,
        random_state=42,
    )
    main_model.fit(x_train, y_train)

    baseline_metrics = evaluate_model(
        baseline_model,
        x_test,
        y_test,
    )

    model_metrics = evaluate_model(
        main_model,
        x_test,
        y_test,
    )

    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    joblib.dump(main_model, MODEL_PATH)

    results = {
        "model": "HistGradientBoostingRegressor",
        "training_rows": len(train_data),
        "test_rows": len(test_data),
        "training_start": train_data["timestamp"].min().isoformat(),
        "training_end": train_data["timestamp"].max().isoformat(),
        "test_start": test_data["timestamp"].min().isoformat(),
        "test_end": test_data["timestamp"].max().isoformat(),
        "baseline_metrics": baseline_metrics,
        "model_metrics": model_metrics,
        "feature_columns": FEATURE_COLUMNS,
        "model_path": str(MODEL_PATH),
    }

    METRICS_PATH.write_text(
        json.dumps(results, indent=2),
        encoding="utf-8",
    )

    return results


if __name__ == "__main__":
    training_results = train_models()
    print(json.dumps(training_results, indent=2))
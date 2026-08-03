import pandas as pd

from src.common.database import get_engine
from src.prediction.predict import load_model, predict
from src.training.train_model import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
    load_training_data,
    temporal_train_test_split,
)

PREDICTIONS_TABLE = "bike_demand_predictions"


def generate_test_predictions() -> pd.DataFrame:
    dataframe = load_training_data()
    _, test_data = temporal_train_test_split(dataframe)

    model = load_model()

    input_data = test_data[FEATURE_COLUMNS]
    predictions = predict(model, input_data)

    results = pd.DataFrame(
        {
            "timestamp": test_data["timestamp"].values,
            "actual": test_data[TARGET_COLUMN].values,
            "predicted": predictions,
        }
    )

    results["absolute_error"] = (
        results["actual"] - results["predicted"]
    ).abs()

    return results


def persist_test_predictions(
    dataframe: pd.DataFrame,
) -> int:
    engine = get_engine()

    with engine.begin() as connection:
        dataframe.to_sql(
            name=PREDICTIONS_TABLE,
            con=connection,
            if_exists="replace",
            index=False,
            method="multi",
            chunksize=1_000,
        )

    return len(dataframe)


def generate_and_persist_predictions() -> int:
    predictions = generate_test_predictions()
    return persist_test_predictions(predictions)


if __name__ == "__main__":
    persisted_rows = generate_and_persist_predictions()
    print(f"Prediction rows persisted: {persisted_rows}")
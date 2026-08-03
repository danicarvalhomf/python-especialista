import joblib
import numpy as np
import pandas as pd

from src.training.train_model import FEATURE_COLUMNS, MODEL_PATH


def load_model():
    return joblib.load(MODEL_PATH)


def build_prediction_dataframe(data: dict) -> pd.DataFrame:
    dataframe = pd.DataFrame([data])

    dataframe["is_weekend"] = dataframe["weekday"].isin([0, 6])

    dataframe["hour_sin"] = np.sin(
        2 * np.pi * dataframe["hour"] / 24
    )
    dataframe["hour_cos"] = np.cos(
        2 * np.pi * dataframe["hour"] / 24
    )

    dataframe["weekday_sin"] = np.sin(
        2 * np.pi * dataframe["weekday"] / 7
    )
    dataframe["weekday_cos"] = np.cos(
        2 * np.pi * dataframe["weekday"] / 7
    )

    dataframe["month_sin"] = np.sin(
        2 * np.pi * (dataframe["month"] - 1) / 12
    )
    dataframe["month_cos"] = np.cos(
        2 * np.pi * (dataframe["month"] - 1) / 12
    )

    return dataframe[FEATURE_COLUMNS]


def predict(model, dataframe):
    predictions = model.predict(dataframe)

    return np.maximum(predictions, 0)
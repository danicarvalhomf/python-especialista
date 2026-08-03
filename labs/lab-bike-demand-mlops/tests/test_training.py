import json

import joblib

from src.training.train_model import (
    FEATURE_COLUMNS,
    METRICS_PATH,
    MODEL_PATH,
    load_training_data,
    temporal_train_test_split,
    train_models,
)


def test_training_data_is_loaded():
    dataframe = load_training_data()

    assert not dataframe.empty
    assert "timestamp" in dataframe.columns
    assert "total_rentals" in dataframe.columns

    for column in FEATURE_COLUMNS:
        assert column in dataframe.columns


def test_temporal_split_preserves_order():
    dataframe = load_training_data()

    train_data, test_data = temporal_train_test_split(dataframe)

    assert not train_data.empty
    assert not test_data.empty
    assert train_data["timestamp"].max() < test_data["timestamp"].min()


def test_training_creates_model_and_metrics():
    results = train_models()

    assert MODEL_PATH.exists()
    assert METRICS_PATH.exists()

    assert results["training_rows"] > 0
    assert results["test_rows"] > 0

    assert "baseline_metrics" in results
    assert "model_metrics" in results


def test_main_model_beats_baseline():
    results = train_models()

    baseline_mae = results["baseline_metrics"]["mae"]
    model_mae = results["model_metrics"]["mae"]

    assert model_mae < baseline_mae


def test_saved_model_can_be_loaded():
    train_models()

    model = joblib.load(MODEL_PATH)

    assert hasattr(model, "predict")


def test_metrics_file_contains_expected_fields():
    train_models()

    metrics = json.loads(
        METRICS_PATH.read_text(encoding="utf-8")
    )

    assert metrics["model"] == "HistGradientBoostingRegressor"
    assert "mae" in metrics["model_metrics"]
    assert "rmse" in metrics["model_metrics"]
    assert "r2" in metrics["model_metrics"]
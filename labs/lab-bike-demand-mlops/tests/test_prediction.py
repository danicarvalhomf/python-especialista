from src.prediction.predict import load_model, predict
from src.training.train_model import (
    FEATURE_COLUMNS,
    load_training_data,
)


def test_model_is_loaded():
    model = load_model()

    assert hasattr(model, "predict")


def test_prediction_returns_expected_number_of_values():
    model = load_model()
    dataframe = load_training_data()

    input_data = dataframe[FEATURE_COLUMNS].head(3)
    predictions = predict(model, input_data)

    assert len(predictions) == len(input_data)


def test_prediction_is_non_negative():
    model = load_model()
    dataframe = load_training_data()

    input_data = dataframe[FEATURE_COLUMNS].head(3)
    predictions = predict(model, input_data)

    assert (predictions >= 0).all()


def test_prediction_accepts_single_observation():
    model = load_model()
    dataframe = load_training_data()

    input_data = dataframe[FEATURE_COLUMNS].iloc[[0]]
    predictions = predict(model, input_data)

    assert len(predictions) == 1
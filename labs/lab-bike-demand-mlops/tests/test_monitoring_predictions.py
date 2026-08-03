from src.monitoring.generate_predictions import (
    generate_test_predictions,
)


def test_predictions_dataset_is_created():
    dataframe = generate_test_predictions()

    assert not dataframe.empty


def test_predictions_dataset_has_expected_columns():
    dataframe = generate_test_predictions()

    expected_columns = {
        "timestamp",
        "actual",
        "predicted",
        "absolute_error",
    }

    assert expected_columns.issubset(dataframe.columns)


def test_predictions_are_non_negative():
    dataframe = generate_test_predictions()

    assert (dataframe["predicted"] >= 0).all()


def test_absolute_error_is_non_negative():
    dataframe = generate_test_predictions()

    assert (dataframe["absolute_error"] >= 0).all()
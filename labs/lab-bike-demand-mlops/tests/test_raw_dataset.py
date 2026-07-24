from src.ingestion.load_raw_dataset import (
    EXPECTED_COLUMNS,
    load_raw_dataset,
)


def test_raw_dataset_is_loaded():
    dataframe = load_raw_dataset()

    assert not dataframe.empty
    assert len(dataframe) > 0


def test_raw_dataset_has_expected_number_of_source_columns():
    dataframe = load_raw_dataset()

    assert len(dataframe.columns) == len(EXPECTED_COLUMNS)


def test_raw_dataset_has_unique_instant():
    dataframe = load_raw_dataset()

    assert dataframe["instant"].is_unique


def test_total_rentals_matches_components():
    dataframe = load_raw_dataset()

    expected_total = (
        dataframe["casual_rentals"]
        + dataframe["registered_rentals"]
    )

    assert (dataframe["total_rentals"] == expected_total).all()
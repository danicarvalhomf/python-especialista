from src.features.build_training_dataset import (
    build_features,
    load_raw_data,
)


def test_feature_dataset_is_created():
    raw_data = load_raw_data()
    features = build_features(raw_data)

    assert not features.empty
    assert len(features) == len(raw_data)


def test_feature_dataset_has_unique_timestamps():
    raw_data = load_raw_data()
    features = build_features(raw_data)

    assert features["timestamp"].is_unique


def test_feature_dataset_is_sorted_by_timestamp():
    raw_data = load_raw_data()
    features = build_features(raw_data)

    assert features["timestamp"].is_monotonic_increasing


def test_cyclical_features_are_within_expected_range():
    raw_data = load_raw_data()
    features = build_features(raw_data)

    cyclical_columns = [
        "hour_sin",
        "hour_cos",
        "weekday_sin",
        "weekday_cos",
        "month_sin",
        "month_cos",
    ]

    for column in cyclical_columns:
        assert features[column].between(-1, 1).all()


def test_feature_dataset_does_not_include_target_components():
    raw_data = load_raw_data()
    features = build_features(raw_data)

    assert "casual_rentals" not in features.columns
    assert "registered_rentals" not in features.columns
    assert "total_rentals" in features.columns


def test_feature_dataset_has_no_missing_values():
    raw_data = load_raw_data()
    features = build_features(raw_data)

    assert not features.isna().any().any()
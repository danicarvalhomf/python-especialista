from typing import Any

import pandas as pd
import requests

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

def load_weather_data(
    latitude: float,
    longitude: float,
    timezone: str,
    forecast_days: int = 7,
) -> pd.DataFrame:
    """ Load hourly weather forecast data from Open-Meteo. """

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "timezone": timezone,
        "forecast_days": forecast_days,
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation_probability",
            "precipitation",
            "wind_speed_10m",
            "wind_gusts_10m",
            "relative_humidity_2m",
            "uv_index",
        ],
    }

    response = requests.get(
        FORECAST_URL,
        params=params,
        timeout=20,
    )

    response.raise_for_status()

    hourly_data = response.json()["hourly"]
    dataframe = pd.DataFrame(hourly_data)

    dataframe["time"] = pd.to_datetime(dataframe["time"])
    return dataframe

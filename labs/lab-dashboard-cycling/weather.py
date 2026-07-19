import time

import pandas as pd
import requests

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"

MAX_RETRIES = 2
INITIAL_RETRY_DELAY_SECONDS = 3


def load_weather_data(
    latitude: float,
    longitude: float,
    timezone: str,
    forecast_days: int = 7,
) -> pd.DataFrame:
    """Load hourly weather forecast data from Open-Meteo."""

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

    headers = {
        "User-Agent": (
            "cycling-weather-dashboard/1.0 "
            "(weather dashboard for educational purposes)"
        )
    }

    retry_delay = INITIAL_RETRY_DELAY_SECONDS

    for attempt in range(1, MAX_RETRIES + 1):
        response = requests.get(
            FORECAST_URL,
            params=params,
            headers=headers,
            timeout=30,
        )

        if response.status_code == 429:
            if attempt == MAX_RETRIES:
                response.raise_for_status()

            retry_after = response.headers.get("Retry-After")

            if retry_after and retry_after.isdigit():
                wait_seconds = int(retry_after)
            else:
                wait_seconds = retry_delay

            print(
                "Open-Meteo rate limit reached. "
                f"Retrying in {wait_seconds} seconds "
                f"({attempt}/{MAX_RETRIES})."
            )

            time.sleep(wait_seconds)
            retry_delay *= 2
            continue

        response.raise_for_status()

        hourly_data = response.json()["hourly"]
        dataframe = pd.DataFrame(hourly_data)
        dataframe["time"] = pd.to_datetime(dataframe["time"])

        return dataframe

    raise RuntimeError("Unable to load weather data from Open-Meteo.")
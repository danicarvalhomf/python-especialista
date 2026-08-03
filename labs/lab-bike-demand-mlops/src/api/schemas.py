from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    year: int = Field(ge=2011)
    month: int = Field(ge=1, le=12)
    day: int = Field(ge=1, le=31)
    hour: int = Field(ge=0, le=23)
    weekday: int = Field(ge=0, le=6)

    season: int = Field(ge=1, le=4)
    holiday: int = Field(ge=0, le=1)
    working_day: int = Field(ge=0, le=1)
    weather_situation: int = Field(ge=1, le=4)

    temperature: float
    apparent_temperature: float
    humidity: float
    wind_speed: float


class PredictionResponse(BaseModel):
    predicted_total_rentals: float
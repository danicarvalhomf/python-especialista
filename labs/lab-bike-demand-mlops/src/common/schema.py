from sqlalchemy import (
    Column,
    Date,
    Float,
    Integer,
    MetaData,
    Table,
)

metadata = MetaData()

bike_rentals_raw = Table(
    "bike_rentals_raw",
    metadata,
    Column("instant", Integer, primary_key=True),
    Column("date", Date, nullable=False),
    Column("season", Integer, nullable=False),
    Column("year", Integer, nullable=False),
    Column("month", Integer, nullable=False),
    Column("hour", Integer, nullable=False),
    Column("holiday", Integer, nullable=False),
    Column("weekday", Integer, nullable=False),
    Column("working_day", Integer, nullable=False),
    Column("weather_situation", Integer, nullable=False),
    Column("temperature", Float, nullable=False),
    Column("apparent_temperature", Float, nullable=False),
    Column("humidity", Float, nullable=False),
    Column("wind_speed", Float, nullable=False),
    Column("casual_rentals", Integer, nullable=False),
    Column("registered_rentals", Integer, nullable=False),
    Column("total_rentals", Integer, nullable=False),
)
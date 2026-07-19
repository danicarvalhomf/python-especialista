import pandas as pd
import vizro.models as vm
import vizro.plotly.express as px
from vizro import Vizro

from weather import load_weather_data

LOCATIONS = {
    "Uberlândia - MG": {
        "latitude": -18.9186,
        "longitude": -48.2772,
        "timezone": "America/Sao_Paulo",
    },
    "Aracaju - SE": {
        "latitude": -10.9472,
        "longitude": -37.0731,
        "timezone": "America/Maceio",
    }
}


def load_all_locations() -> pd.DataFrame:
    dataframes: list[pd.DataFrame] = []

    for city_name, location in LOCATIONS.items():
        city_data = load_weather_data(
            latitude=location["latitude"],
            longitude=location["longitude"],
            timezone=location["timezone"],
        )

        city_data["Cidade"] = city_name
        city_data["Data"] = city_data["time"].dt.normalize()
        dataframes.append(city_data)

    return pd.concat(dataframes, ignore_index=True)


weather_data = load_all_locations()


page = vm.Page(
    title="Condições para ciclismo",
    components=[
        vm.Graph(
            title="Temperatura e sensação térmica",
            figure=px.line(
                weather_data,
                x='time',
                y=["temperature_2m", "apparent_temperature"],
                labels={
                    "time": "Data e horário",
                    "value": "Temperatura (°C)",
                    "variable": "Indicador",
                },
            )
        ),
        vm.Graph(
            title="Probabilidade de chuva",
            figure=px.bar(
                weather_data,
                x='time',
                y="precipitation_probability",
                labels={
                    "time": "Data e horário",
                    "precipitation_probability": "Probab. de chuva (%)",
                },
            )
        ),
        vm.Graph(
            title="Velocidade do vento",
            figure=px.line(
                weather_data,
                x='time',
                y="wind_speed_10m",
                labels={
                    "time": "Data e horário",
                    "wind_speed_10m": "Veloc. do vento (Km/h)",
                },
            )
        ),
    ],
    controls=[
        vm.Filter(
            column="Cidade",
            selector=vm.Dropdown(
                title="Cidade",
                description="Fonte dos dados meteorológicos: **Open-Meteo**.",
                multi=False,
                value="Aracaju - SE",
            ),
        ),
        vm.Filter(
            column="Data",
            selector=vm.DatePicker(
                range=False,
            ),
        ),
    ]
)

dashboard = vm.Dashboard(
    pages=[page],
    theme="vizro_light",
)

app = Vizro().build(dashboard)

if __name__ == "__main__":
    app.run(debug=True)
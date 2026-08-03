import json

import pandas as pd
import vizro.models as vm
import vizro.plotly.express as px
from sqlalchemy import text
from vizro import Vizro

from src.common.database import get_engine
from src.config import BASE_DIR


METRICS_PATH = BASE_DIR / "reports" / "training_metrics.json"


def load_predictions() -> pd.DataFrame:
    """Load model predictions persisted in PostgreSQL."""

    engine = get_engine()

    query = text(
        """
        SELECT
            timestamp,
            actual,
            predicted,
            absolute_error
        FROM bike_demand_predictions
        ORDER BY timestamp;
        """
    )

    with engine.connect() as connection:
        dataframe = pd.read_sql(query, connection)

    if dataframe.empty:
        raise ValueError(
            "Prediction table is empty. "
            "Run the prediction generation pipeline first."
        )

    dataframe["timestamp"] = pd.to_datetime(
        dataframe["timestamp"]
    )

    # Mantém a coluna como datetime64 para uso no DatePicker.
    dataframe["date"] = (
        dataframe["timestamp"]
        .dt.normalize()
    )

    return dataframe


def load_metrics() -> dict:
    """Load metrics generated during model training."""

    if not METRICS_PATH.exists():
        raise FileNotFoundError(
            f"Training metrics file not found: {METRICS_PATH}"
        )

    return json.loads(
        METRICS_PATH.read_text(encoding="utf-8")
    )


def format_decimal_pt_br(
    value: float,
    decimal_places: int = 2,
) -> str:
    """Format a number using a comma as decimal separator."""

    formatted_value = f"{value:,.{decimal_places}f}"

    return (
        formatted_value
        .replace(",", "#")
        .replace(".", ",")
        .replace("#", ".")
    )


predictions = load_predictions()
metrics = load_metrics()

model_metrics = metrics["model_metrics"]

mae_value = format_decimal_pt_br(
    model_metrics["mae"],
    decimal_places=2,
)

rmse_value = format_decimal_pt_br(
    model_metrics["rmse"],
    decimal_places=2,
)

r2_percentage = format_decimal_pt_br(
    model_metrics["r2"] * 100,
    decimal_places=2,
)


page = vm.Page(
    title="Monitoramento do Modelo de Demanda",

    layout=vm.Grid(
        grid=[
            [0, 1, 2],
            [3, 3, 3],
            [3, 3, 3],
            [4, 4, 4],
            [4, 4, 4],
            [5, 5, 5],
            [5, 5, 5],
        ],
        row_min_height="100px",
    ),

    components=[
        vm.Card(
            text=f"""
### Erro Médio (MAE)

# {mae_value}

**bicicletas**
"""
        ),

        vm.Card(
            text=f"""
### Erro Quadrático (RMSE)

# {rmse_value}

**bicicletas**
"""
        ),

        vm.Card(
            text=f"""
### Precisão do Modelo (R²)

# {r2_percentage}%
"""
        ),

        vm.Graph(
            title="Demanda real e prevista",
            figure=px.line(
                predictions,
                x="timestamp",
                y=[
                    "actual",
                    "predicted",
                ],
                labels={
                    "timestamp": "Data e horário",
                    "value": "Quantidade de locações",
                    "variable": "Série",
                    "actual": "Demanda real",
                    "predicted": "Demanda prevista",
                },
            ),
        ),

        vm.Graph(
            title="Valores reais versus previstos",
            figure=px.scatter(
                predictions,
                x="actual",
                y="predicted",
                labels={
                    "actual": "Demanda real",
                    "predicted": "Demanda prevista",
                },
            ),
        ),

        vm.Graph(
            title="Erro absoluto ao longo do tempo",
            figure=px.line(
                predictions,
                x="timestamp",
                y="absolute_error",
                labels={
                    "timestamp": "Data e horário",
                    "absolute_error": "Erro absoluto",
                },
            ),
        ),
    ],

    controls=[
        vm.Filter(
            column="date",
            selector=vm.DatePicker(
                title="Data",
                range=True,
            ),
        ),
    ],
)


dashboard = vm.Dashboard(
    pages=[page],
    theme="vizro_light",
)

app = Vizro().build(dashboard)


if __name__ == "__main__":
    app.run(debug=True)
from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.api.schemas import (
    PredictionRequest,
    PredictionResponse,
)
from src.prediction.predict import (
    build_prediction_dataframe,
    load_model,
    predict,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.model = load_model()
    yield


app = FastAPI(
    title="Bike Demand Prediction API",
    description=(
        "API para previsão da demanda horária de bicicletas compartilhadas."
    ),
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "healthy"}


@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict_bike_demand(
    request: PredictionRequest,
) -> PredictionResponse:
    input_dataframe = build_prediction_dataframe(
        request.model_dump()
    )

    predictions = predict(
        app.state.model,
        input_dataframe,
    )

    return PredictionResponse(
        predicted_total_rentals=float(predictions[0])
    )
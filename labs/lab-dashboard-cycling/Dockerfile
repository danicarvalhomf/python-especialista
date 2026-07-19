FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN uv sync --frozen --no-dev --no-install-project

COPY main.py weather.py ./

EXPOSE 8050

CMD ["sh", "-c", "/app/.venv/bin/gunicorn main:app --workers 1 --bind 0.0.0.0:${PORT:-8050}"]
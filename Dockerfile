FROM ghcr.io/astral-sh/uv:0.4.18 AS uv_bin
FROM python:3.11-alpine

WORKDIR /app

RUN apk add --no-cache curl libstdc++

COPY --from=uv_bin /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.venv/bin:$PATH"

COPY pyproject.toml .
RUN uv venv /app/.venv && uv sync --no-install-project --no-dev

COPY src ./src
COPY README.md .

RUN uv sync --no-dev

EXPOSE 8000

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

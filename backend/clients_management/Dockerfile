# Stage 1 (установка зависимостей)
FROM python:3.12-slim AS builder

WORKDIR /build

ENV POETRY_VERSION=2.1.2 \
    POETRY_VIRTUALENVS_CREATE=false \
    PATH="/root/.local/bin:$PATH"

RUN apt-get update \
    && apt-get install -y curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-ansi --only main

COPY . ./app/

# Stage 2 (копирование файлов и запуск сервиса)
FROM python:3.12-slim AS runtime

WORKDIR /app

COPY --from=builder /build/app ./
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

CMD ["python", "start.py"]

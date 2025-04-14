# 1. Базовый образ с Python 3.12
FROM python:3.12-slim

# 2. Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 3. Установка poetry
ENV POETRY_VERSION=2.1.2
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && ln -s /root/.local/bin/poetry /usr/local/bin/poetry

# 4. Отключаем создание виртуального окружения (оно не нужно внутри контейнера)
ENV POETRY_VIRTUALENVS_CREATE=false

# 5. Устанавливаем рабочую директорию
WORKDIR /app

# 6. Копируем только pyproject.toml и poetry.lock (если есть)
COPY pyproject.toml poetry.lock* ./

# 7. Устанавливаем зависимости
RUN poetry install --no-interaction --no-ansi

# 8. Копируем весь проект
COPY . .

# 9. Указываем команду по умолчанию — запуск FastAPI через uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

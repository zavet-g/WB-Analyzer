# syntax=docker.io/docker/dockerfile:1
FROM python:3.13-slim AS base-image

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=1.8.3 \
    PROJECT_PATH="/app"

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN mkdir $PROJECT_PATH
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    gcc \
    libc-dev \
    libffi-dev \
    && rm -rf /var/lib/apt/lists/*

# Установка Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Очистка кэша Poetry
RUN poetry cache clear --all pypi

############################################################
# Образ для разработки
FROM base-image AS dev
ENV PRODUCTION=False
COPY pyproject.toml poetry.lock* $PROJECT_PATH/
WORKDIR $PROJECT_PATH
# Установка зависимостей
RUN poetry install --verbose || { echo "poetry install failed"; exit 1; }
# Проверка виртуальной среды
RUN ls -la /app/.venv/bin
# Проверка установки uvicorn
RUN poetry run which uvicorn || { echo "uvicorn not found"; exit 1; }
RUN poetry run uvicorn --version || { echo "uvicorn version check failed"; exit 1; }
# Копирование остального кода
COPY . $PROJECT_PATH
RUN chown -R $(whoami):$(whoami) /app
RUN chmod -R u+rwX /app/.venv
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "apps.api.v1.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]

############################################################
# Образ для production
FROM base-image AS prod
ENV PRODUCTION=True
COPY pyproject.toml poetry.lock* $PROJECT_PATH/
WORKDIR $PROJECT_PATH
# Установка зависимостей
RUN poetry install --no-dev --verbose || { echo "poetry install failed"; exit 1; }
# Проверка виртуальной среды
RUN ls -la /app/.venv/bin
# Проверка установки uvicorn
RUN poetry run which uvicorn || { echo "uvicorn not found"; exit 1; }
RUN poetry run uvicorn --version || { echo "uvicorn version check failed"; exit 1; }
# Копирование остального кода
COPY . $PROJECT_PATH
RUN chown -R $(whoami):$(whoami) /app
RUN chmod -R u+rwX /app/.venv
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "apps.api.v1.main:app", "--host", "0.0.0.0", "--port", "8000"]
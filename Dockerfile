# syntax=docker.io/docker/dockerfile:1.7-labs
FROM python:3.11-alpine AS base-image
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    POETRY_HOME="/usr/local/bin/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    POETRY_VERSION=2.0 \
    PROJECT_PATH="/src"
ENV PATH="$POETRY_HOME/bin:$PATH"
RUN mkdir $PROJECT_PATH
RUN apk --no-cache add curl gcc musl-dev libffi-dev

##############################################################
# Образ для разработки
FROM base-image AS dev
ENV PRODUCTION=False
COPY --exclude=poetry.lock --exclude=.venv ./ $PROJECT_PATH
WORKDIR $PROJECT_PATH
RUN pip install --no-cache-dir poetry=="$POETRY_VERSION" && poetry install
CMD [".venv/bin/uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "3000"]
#CMD ["sleep", "350000"]

##############################################################
# Образ для production: не ставятся dev зависимости, uvicorn запускается без hot reload
FROM base-image AS prod
ENV PRODUCTION=True
COPY --exclude=poetry.lock --exclude=.venv ./ $PROJECT_PATH
WORKDIR $PROJECT_PATH
RUN pip install --no-cache-dir poetry=="$POETRY_VERSION" && poetry install 
CMD [".venv/bin/uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "3000"]

import logging
import sys
import time

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from loguru import logger
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from apps.api import router as api_router
from apps.auth import router as auth_router
from apps.settings import SETTINGS
from apps.utils.enums.env_enum import EnvEnum


async def init_logger() -> None:
    """Метод инициализации логеров."""
    logger.remove()
    level = (
        'INFO' if SETTINGS.ENVIRONMENT in [EnvEnum.LOCAL, EnvEnum.STAGE, EnvEnum.PROD] else 'DEBUG'
    )

    logger.add(
        sys.stdout,
        format='{time:YYYY-MM-DD at HH:mm:ss} {level} {message} in {name} {line}',
        level=level,
    )
    logger.add(
        sys.stderr,
        colorize=True,
        format='<red>{time:YYYY-MM-DD at HH:mm:ss} {level} {message} in {name} {line}</red>',
        level='ERROR',
    )

    logging.getLogger('uvicorn.access').setLevel(level)


@asynccontextmanager
async def lifespan(*args, **kwargs) -> AsyncGenerator[None, None]:
    """Действия перед стартом аппа."""
    await init_logger()
    yield


def get_fastapi_app() -> FastAPI:
    """Получаем объект фастапи c прогруженными роутами.

    Returns:
        FastAPI
    """
    fast_api_app = FastAPI(
        default_response_class=ORJSONResponse,
        title=SETTINGS.PROJECT_NAME,
        openapi_url='/openapi.json',
        lifespan=lifespan,
    )
    fast_api_app.include_router(api_router)
    fast_api_app.include_router(auth_router)
    return fast_api_app


app = get_fastapi_app()


if SETTINGS.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in SETTINGS.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )


@app.middleware('http')
async def add_process_time_header(request: Request, call_next: Any) -> Response:
    """Добавление времени выполнения сервиса в ответ.

    Args:
        request (Request): Объект запроса
        call_next (Any): Функция которая получит request в качестве параметра.

    Returns:
        Response: Объект ответа приложения
    """
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers['X-Process-Time'] = str(process_time)
    return response


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)

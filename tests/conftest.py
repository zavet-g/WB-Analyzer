import asyncio
import platform
import sys

from collections.abc import AsyncGenerator
from collections.abc import Generator
from typing import Any

import pytest

from fastapi import FastAPI
from httpx import ASGITransport
from httpx import AsyncClient
from httpx import Headers
from loguru import logger
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_sessionmaker

from apps.db.base_db_class import BaseDBModel
from apps.db.enabled_migration_schemas import enabled_pg_schemas
from apps.db.session import PGEngineConnector
from apps.settings import SETTINGS
from apps.utils.enums.env_enum import EnvEnum
from tests.consts import BASE_AUTH_URL
from tests.consts import STUB_EMAIL
from tests.consts import STUB_PASS


@pytest.fixture(scope='session')
def event_loop():
    """Фикстура для получения евент лупа.

    Проверяем, закрыт ли луп, и запущен ли он на винде.
    """
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()

    yield loop
    loop.close()


@pytest.fixture(autouse=True)
def _setup_conftest() -> Generator[Any, Any, None]:
    """Подстановка тестовых конфигов."""
    SETTINGS.ENVIRONMENT = EnvEnum.PYTEST
    SETTINGS.SQLALCHEMY_DATABASE_URI = SETTINGS.TEST_SQLALCHEMY_DATABASE_URI

    logger.remove()
    logger.add(sys.stdout, format='{message} | {name} {line}', level='INFO')
    logger.add(
        sys.stderr,
        colorize=True,
        format='<red>{message} | {name} {line}</red>',
        level='ERROR',
    )
    logger.level('DEBUG', color='<yellow>')

    yield


def get_test_connector():
    """Получение тестового PG коннектора."""
    return PGEngineConnector(sql_alchemy_uri=SETTINGS.TEST_SQLALCHEMY_DATABASE_URI)


@pytest.fixture(scope='session')
async def engine() -> AsyncGenerator[Any, Any]:
    """Фикстура для получения движка алхимии.

    Используется для наката / отката состояния бд.
    """
    connector = get_test_connector()
    engine = connector.get_pg_engine(sql_alchemy_uri=SETTINGS.TEST_SQLALCHEMY_DATABASE_URI)
    yield engine
    await engine.dispose()


@pytest.fixture(scope='class')
async def db_init(engine):
    """Фикстура для скидывания состояния БД.

    Args:
        engine: AsyncEngine
    """
    meta = BaseDBModel.metadata

    async with engine.connect() as conn:
        for schema in enabled_pg_schemas:
            await conn.execute(text('SET TIME ZONE UTC;'))
            await conn.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE;'))
            await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema};'))

        await conn.run_sync(meta.create_all)
        await conn.commit()


@pytest.fixture(scope='class')
async def migrations_clean_up(engine):
    """Фикстура для тестирования миграций.

    Главное отличие от session фикстуры - нет conn.run_sync(meta.create_all).

    Args:
        engine: AsyncEngine
    """
    async with engine.begin() as conn:
        for schema in enabled_pg_schemas:
            await conn.execute(text(f'DROP SCHEMA IF EXISTS {schema} CASCADE;'))
            await conn.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema};'))


@pytest.fixture(scope='class')
async def session(engine, db_init) -> AsyncGenerator[Any, Any]:
    """Получение тестовой сессии SQLALchemy."""
    session_maker = async_sessionmaker(
        engine,
        expire_on_commit=False,
    )

    async with session_maker() as session:
        yield session


@pytest.fixture(scope='class')
async def db_init_pre_build(session, request):
    """Генерация дерева данных."""
    for stmt in request.param:
        await session.execute(stmt)

    await session.commit()


@pytest.fixture
async def client() -> AsyncGenerator[Any, Any]:
    """Тестовый клиент без авторизации."""
    from apps.db.session import connector
    from apps.main import get_fastapi_app

    main_app: FastAPI = get_fastapi_app()
    test_connector = get_test_connector()

    main_app.dependency_overrides[connector.get_pg_session] = test_connector.get_pg_session

    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        follow_redirects=True,
    ) as client:
        yield client


@pytest.fixture(scope='function')
async def auth_client() -> AsyncGenerator[Any, Any]:
    """Тестовый клиент с авторизацией."""
    from apps.db.session import connector
    from apps.main import get_fastapi_app

    main_app = get_fastapi_app()
    test_connector = get_test_connector()

    main_app.dependency_overrides[connector.get_pg_session] = test_connector.get_pg_session

    async with AsyncClient(
        transport=ASGITransport(app=main_app),
        follow_redirects=True,
    ) as client:
        res = await client.post(
            url=f'{BASE_AUTH_URL}/login/',
            json={
                'user_email': STUB_EMAIL,
                'user_password': STUB_PASS,
            },
        )
        auth_header = Headers(
            {
                'Authorization': f'Bearer {res.json()["access_token"]}',
            },
        )
        client.headers.update(auth_header)
        yield client

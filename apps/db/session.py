"""Сессия алхимии."""

import json

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import ClassVar

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine

from apps.settings import SETTINGS


class PGEngineConnector:
    """Класс постгри, отвечающий за получение сессии.

    Сохраняет Engine по ключу URI. Нужен для кросс
    БД соединения и изоляции базы от скоупа модуля.
    """

    sql_alchemy_uri: str
    engine_dict: ClassVar[dict[str, AsyncEngine]] = {}

    def __init__(self, sql_alchemy_uri: str = SETTINGS.SQLALCHEMY_DATABASE_URI):
        """Инициализируем объект коннектора.

        Args:
            sql_alchemy_uri: строка подключения пг
        """
        self.sql_alchemy_uri = sql_alchemy_uri

    @classmethod
    def get_pg_engine(cls, sql_alchemy_uri: str) -> AsyncEngine:
        """Получаем движок для алхимии. Одиночка.

        Returns:
            AsyncEngine
        """
        if engine := cls.engine_dict.get(sql_alchemy_uri):
            return engine

        engine = create_async_engine(
            sql_alchemy_uri,
            pool_size=SETTINGS.ALCHEMY_POLL_SIZE,
            max_overflow=SETTINGS.ALCHEMY_OVERFLOW_POOL_SIZE,
            pool_pre_ping=True,
            json_serializer=lambda x: json.dumps(x) if not isinstance(x, str) else x,
        )
        cls.engine_dict[sql_alchemy_uri] = engine
        return engine

    def get_session_maker(self) -> async_sessionmaker[AsyncSession]:
        """Получение объекта AsyncSessionMaker."""
        return async_sessionmaker(
            self.get_pg_engine(sql_alchemy_uri=self.sql_alchemy_uri),
            expire_on_commit=False,
        )

    async def get_pg_session(self) -> AsyncGenerator[AsyncSession, None]:
        """Получение сессии."""
        session_maker = self.get_session_maker()
        async with session_maker() as session:
            yield session

    @asynccontextmanager
    async def get_pg_session_cm(self) -> AsyncGenerator[AsyncSession, None]:
        """Получаем сессию в асинхронном менеджере контекста.

        from app.db.session import connector
        async with connector.get_pg_session_cm() as db:
            obj = await raw_history_CRUD.create(db=db, obj_in=body)
        """
        session_maker = self.get_session_maker()
        async with session_maker() as session:
            yield session

connector = PGEngineConnector()
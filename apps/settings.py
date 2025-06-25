from typing import Any

from dotenv import find_dotenv
from dotenv import load_dotenv
from pydantic import AnyHttpUrl
from pydantic import PostgresDsn
from pydantic import ValidationError
from pydantic import model_validator
from pydantic_settings import BaseSettings

from apps.utils.enums.env_enum import EnvEnum
from apps.utils.enums.log_level_enum import LogLevelEnum


class Settings(BaseSettings):
    """Класс конфигурации. Содержит все переменные, которые мы используем в проекте."""

    def __init__(self, **values: Any):
        load_dotenv(find_dotenv(), override=True)
        super().__init__(**values)

    @model_validator(mode='before')
    @classmethod
    def assemble_db_connection(cls, data: Any) -> dict:
        """Собираем PG-URI."""
        sqlalchemy_db_uri = None
        if data.get('POSTGRES_USER') and data.get('POSTGRES_HOST'):
            sqlalchemy_db_uri = str(
                PostgresDsn.build(
                    scheme='postgresql+asyncpg',
                    username=data.get('POSTGRES_USER'),
                    password=data.get('POSTGRES_PASSWORD'),
                    host=data.get('POSTGRES_HOST'),
                    port=int(data.get('POSTGRES_PORT', 5432)),
                    path=data.get('POSTGRES_DB', ''),
                )
            )

        if not sqlalchemy_db_uri:
            raise ValidationError('Please fill Postgres settings in ENV')

        sqlalchemy_db_uri = sqlalchemy_db_uri.replace('%', '%%')
        data.update({'SQLALCHEMY_DATABASE_URI': sqlalchemy_db_uri})
        return data

    @model_validator(mode='before')
    @classmethod
    def assemble_cors_origin(cls, data: Any) -> dict:
        """Валидируем корсы."""
        backend_cors_origins = data.get('BACKEND_CORS_ORIGINS')
        if backend_cors_origins:
            if isinstance(backend_cors_origins, str) and not backend_cors_origins.startswith('['):
                backend_cors_origins = [i.strip() for i in backend_cors_origins.split(',')]
            elif isinstance(backend_cors_origins, list | str):
                pass
            else:
                raise ValueError(f'BACKEND_CORS_ORIGINS={backend_cors_origins} validation error')
            data.update({'BACKEND_CORS_ORIGINS': backend_cors_origins})
        return data

    # Общие настройки
    ENVIRONMENT: EnvEnum = EnvEnum.PROD
    LOG_LEVEL: LogLevelEnum = LogLevelEnum.INFO
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []
    PROJECT_NAME: str = "wb-analyzer"

    # База данных
    POSTGRES_HOST: str = 'db'
    POSTGRES_PORT: int | str = 5432
    POSTGRES_USER: str | None = 'postgres'
    POSTGRES_PASSWORD: str | None = 'postgres'
    POSTGRES_DB: str | None = 'wb_analyzer'
    SQLALCHEMY_DATABASE_URI: str
    ALCHEMY_POLL_SIZE: int = 10
    ALCHEMY_OVERFLOW_POOL_SIZE: int = 20

SETTINGS = Settings()
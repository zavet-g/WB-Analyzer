import asyncio
import os
import sys

from logging.config import fileConfig

from alembic import context
from dotenv import find_dotenv
from dotenv import load_dotenv
from loguru import logger
from sqlalchemy import pool
from sqlalchemy import text
from sqlalchemy.ext.asyncio import async_engine_from_config

from apps.db.enabled_migration_models import BaseDBModel
from apps.db.enabled_migration_schemas import enabled_pg_schemas

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)

load_dotenv(find_dotenv(), override=True)

config = context.config
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', '')
logger.opt(colors=True).info(f'Database URI loaded <GREEN>{SQLALCHEMY_DATABASE_URI=}</GREEN>')
config.set_main_option('sqlalchemy.url', SQLALCHEMY_DATABASE_URI.replace('%', '%%'))

fileConfig(config.config_file_name if config.config_file_name else f'{BASE_DIR}/alembic.ini')

target_metadata = BaseDBModel.metadata
target_schemas = list(target_metadata._schemas)

for schema in target_schemas:
    if schema not in enabled_pg_schemas:
        raise Exception(
            'Add new schema(s) in enabled_pg_schemas or fix schema name typo in detected table(s)'
        )

def include_name(name, type_, parent_names):
    """Фильтр для включения объектов в миграции."""
    if type_ == 'schema':
        return name in enabled_pg_schemas
    return True

def process_revision_directives(context, revision, directives):
    """Манипуляция директивами миграций при автогенерации."""
    if config.cmd_opts.autogenerate:
        script = directives[0]
        for upgrade_ops in script.upgrade_ops_list:
            if upgrade_ops.is_empty():
                directives[:] = []

def run_migrations_offline() -> None:
    """Запуск миграций в оффлайн режиме."""
    url = config.get_main_option('sqlalchemy.url')
    context.configure(
        url=url,
        echo=True,
        target_metadata=target_metadata,
        literal_binds=True,
        compare_type=True,
        compare_server_default=True,
        dialect_opts={'paramstyle': 'named'},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection):
    """Запуск миграций в онлайн режиме."""
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        include_schemas=True,
        version_table_schema=enabled_pg_schemas[0],
        include_name=include_name,
        process_revision_directives=process_revision_directives,
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_migrations_online():
    """Запуск миграций в онлайн режиме."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix='sqlalchemy.',
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        for schema in enabled_pg_schemas:
            await connection.execute(text(f'CREATE SCHEMA IF NOT EXISTS {schema}'))
            await connection.commit()
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

if context.is_offline_mode():
    run_migrations_offline()
else:
    asyncio.run(run_migrations_online())
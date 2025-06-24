from fastapi import Depends
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.base_crud import BaseCrud
from apps.api.v1.models.log_entry_model import LogEntryModel
from apps.api.v1.models.server_model import ServerModel
from apps.api.v1.schemas.log_entry_schema import GetLogEntryOutSchema
from apps.api.v1.schemas.server_schema import ServerOutSchema
from apps.api.v1.schemas.server_schema import ServerWithLogsOutSchema
from apps.auth.schemas.user_schema import UserSchema
from apps.db.session import connector


class ServerCrud(BaseCrud):
    async def get_servers(
        self,
        user: UserSchema,
        db: AsyncSession = Depends(connector.get_pg_session),
    ) -> list[ServerOutSchema]:
        """Получаем все записи логов из таблицы EmailLogModel.

        Args:
            user (UserSchema): Пользователь (не используется для фильтрации).
            db (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            list[ServerOutSchema]: Список всех записей логов в формате Pydantic-схемы.
        """
        stmt = select(ServerModel)

        res = await db.execute(stmt)
        entries = res.scalars().all()

        return [ServerOutSchema.model_validate(entry) for entry in entries]

    async def get_server_by_id(
        self,
        db: AsyncSession,
        user: UserSchema,
        server_id: int,
    ) -> ServerWithLogsOutSchema:
        """Получаем сервер по ID и связанные записи логов.

        Args:
            db (AsyncSession): Асинхронная сессия SQLAlchemy.
            user (UserSchema): Аутентифицированный пользователь.
            server_id (int): ID сервера.

        Returns:
            ServerWithLogsOutSchema: Данные сервера и связанные логи.

        Raises:
            ValueError: Если сервер с указанным ID не найден.
        """

        log_json = func.json_agg(
            func.json_build_object(
                'id',
                LogEntryModel.id,
                'timestamp',
                LogEntryModel.timestamp,
                'remote_addr',
                LogEntryModel.remote_addr,
                'method',
                LogEntryModel.method,
                'uri',
                LogEntryModel.uri,
                'http_version',
                LogEntryModel.http_version,
                'status',
                LogEntryModel.status,
                'size',
                LogEntryModel.size,
                'referrer',
                LogEntryModel.referrer,
                'user_agent',
                LogEntryModel.user_agent,
            )
        ).filter(LogEntryModel.id.is_not(None))

        stmt = (
            select(ServerModel.id, ServerModel.name, ServerModel.ip_address, log_json.label('logs'))
            .outerjoin(LogEntryModel, ServerModel.id == LogEntryModel.server_id)
            .where(ServerModel.id == server_id)
            .group_by(ServerModel.id)
        )

        res = await db.execute(stmt)
        row = res.fetchone()

        if not row:
            raise ValueError(f'Server with id {server_id} not found.')

        return ServerWithLogsOutSchema(
            id=row.id,
            name=row.name,
            ip_address=row.ip_address,
            logs=[GetLogEntryOutSchema(**log) for log in row.logs or []],
        )


server_crud_obj = ServerCrud(ServerModel)

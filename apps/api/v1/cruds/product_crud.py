from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.base_crud import BaseCrud
from apps.api.v1.models.product_model import LogEntryModel
from apps.api.v1.schemas.product_schema import GetLogEntryOutSchema
from apps.auth.schemas.user_schema import UserSchema
from apps.db.session import connector


class LogEntryCrud(BaseCrud):
    async def get_entry_logs(
        self,
        user: UserSchema,
        db: AsyncSession = Depends(connector.get_pg_session),
    ) -> list[GetLogEntryOutSchema]:
        """Получаем все записи логов из таблицы EmailLogModel.

        Args:
            user (UserSchema): Пользователь (не используется для фильтрации).
            db (AsyncSession): Асинхронная сессия базы данных.

        Returns:
            list[GetLogEntryOutSchema]: Список всех записей логов в формате Pydantic-схемы.
        """
        stmt = select(LogEntryModel).order_by(LogEntryModel.timestamp)

        res = await db.execute(stmt)
        entries = res.scalars().all()

        return [GetLogEntryOutSchema.model_validate(entry) for entry in entries]


log_entry_crud_obj = LogEntryCrud(LogEntryModel)

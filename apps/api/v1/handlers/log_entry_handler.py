from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.log_entry_crud import log_entry_crud_obj
from apps.api.v1.schemas.log_entry_schema import GetLogEntryOutSchema
from apps.auth.dependencies.auth_dependency import auth_dependency
from apps.auth.schemas.user_schema import UserSchema
from apps.db.session import connector

router = APIRouter()


@router.get(
    '/get_entry_logs',
    response_model=list[GetLogEntryOutSchema],
)
async def get_entry_logs(
    user: UserSchema = Depends(auth_dependency.check_token),
    db: AsyncSession = Depends(connector.get_pg_session),
) -> list[GetLogEntryOutSchema]:
    """Получаем список сообщений.

    Args:
        user: пользователь
        db: AsyncSession

    Returns:
        list[GetLogEntryOutSchema]: Список логов
    """
    return await log_entry_crud_obj.get_entry_logs(
        db=db,
        user=user,
    )

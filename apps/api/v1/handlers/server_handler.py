from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.server_crud import server_crud_obj
from apps.api.v1.schemas.server_schema import ServerOutSchema
from apps.api.v1.schemas.server_schema import ServerWithLogsOutSchema
from apps.auth.dependencies.auth_dependency import auth_dependency
from apps.auth.schemas.user_schema import UserSchema
from apps.db.session import connector

router = APIRouter()


@router.get(
    '/get_servers',
    response_model=list[ServerOutSchema],
)
async def get_servers(
    user: UserSchema = Depends(auth_dependency.check_token),
    db: AsyncSession = Depends(connector.get_pg_session),
) -> list[ServerOutSchema]:
    """Получаем список сообщений.

    Args:
        user: пользователь
        db: AsyncSession

    Returns:
        list[ServerOutSchema]: Список логов
    """
    return await server_crud_obj.get_servers(
        db=db,
        user=user,
    )


@router.get(
    '/get-server-by-id/{server_id}',
    response_model=ServerWithLogsOutSchema,
)
async def get_server_by_id(
    server_id: int,
    user: UserSchema = Depends(auth_dependency.check_token),
    db: AsyncSession = Depends(connector.get_pg_session),
) -> ServerWithLogsOutSchema:
    """Получаем сервер по ID и связанные записи логов.

    Args:
        server_id (int): ID сервера.
        user (UserSchema): Аутентифицированный пользователь.
        db (AsyncSession): Асинхронная сессия SQLAlchemy.

    Returns:
        ServerWithLogsOutSchema: Данные сервера и связанные логи.
    """
    return await server_crud_obj.get_server_by_id(
        db=db,
        user=user,
        server_id=server_id,
    )

from fastapi import APIRouter
from starlette.responses import Response
from starlette.status import HTTP_200_OK

health_check_router = APIRouter()


@health_check_router.get(
    '/health',
    status_code=HTTP_200_OK,
)
async def default_health_check() -> Response:
    """Всегда отдает OK. Нужен, чтоб понять жив ли контейнер.

    Returns:
        Response
    """
    return Response(
        content='OK',
        status_code=HTTP_200_OK,
    )

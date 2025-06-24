from fastapi import APIRouter

from apps.api.v1.handlers import product_heandler
from apps.api.v1.handlers import server_handler
from apps.utils import health_check

router = APIRouter()

router.include_router(
    product_heandler.router,
    prefix='/api',
    tags=['api'],
)

router.include_router(
    server_handler.router,
    prefix='/api',
    tags=['api'],
)

router.include_router(health_check.health_check_router, tags=['health_check'])

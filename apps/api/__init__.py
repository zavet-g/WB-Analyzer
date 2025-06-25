from fastapi import APIRouter

from apps.api.v1.handlers import product_handler
from apps.utils import health_check

router = APIRouter()

router.include_router(
    product_handler.router,
)

router.include_router(
    health_check.health_check_router,
    tags=['health_check'],
)
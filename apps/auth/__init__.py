from fastapi import APIRouter

from apps.auth.handlers import auth_handler

router = APIRouter()

router.include_router(
    auth_handler.router,
    tags=['auth'],
    prefix='/api/auth',
)

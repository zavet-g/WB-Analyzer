import datetime

import jwt

from fastapi import Depends
from fastapi import HTTPException
from fastapi.security import APIKeyCookie
from fastapi.security import APIKeyHeader
from loguru import logger
from simple_print import sprint
from starlette.responses import Response
from starlette.status import HTTP_401_UNAUTHORIZED

from apps.auth.schemas.user_schema import AuthSchema
from apps.auth.schemas.user_schema import EncodedJWTTokenSchema
from apps.auth.schemas.user_schema import JWTTokenSchema
from apps.auth.schemas.user_schema import UserSchema
from apps.settings import SETTINGS
from apps.utils.enums.user_role_enum import UserRoleEnum

cookie_access_token = APIKeyCookie(name='access_token', auto_error=False)
header_access_token = APIKeyHeader(name='authorization', auto_error=False)

cookie_refresh_token = APIKeyCookie(name='refresh_token', auto_error=False)
header_refresh_token = APIKeyHeader(name='refresh_token', auto_error=False)


class AuthDependency:
    async def get_token(
        self,
        auth_data: AuthSchema,
    ) -> EncodedJWTTokenSchema:
        """Получение аксесс и рефреш токенов.

        Args:
            auth_data: UserLoginSchema

        Returns:
            JWTTokenResponseSchema
        """
        now = datetime.datetime.now(datetime.UTC)
        exp = now + datetime.timedelta(SETTINGS.JWT_TOKEN_TTL)
        jwt_token = JWTTokenSchema(
            iat=now,
            exp=exp,
            sub='auth',
            user_email=auth_data.user_email,
            user_roles=[UserRoleEnum.SYSTEM_ADMINISTRATOR.value],
        )
        encoded_jwt_token = jwt.encode(
            jwt_token.model_dump(),
            SETTINGS.JWT_SECRET_KEY,
            algorithm=SETTINGS.JWT_ALGORITHM,
        )
        return EncodedJWTTokenSchema(
            access_token=encoded_jwt_token,
            refresh_token=encoded_jwt_token,
        )

    async def check_token(
        self,
        cookie_token: str = Depends(cookie_access_token),
        header_token: str = Depends(header_access_token),
    ) -> UserSchema | Response:
        """Проверяем токен при запросе.

        Args:
            cookie_token: токен в куках
            header_token: токен в хедере
        """

        if header_token:
            token = header_token.split(' ')[-1]
        elif cookie_token:
            token = cookie_token
        else:
            sprint('Я тут')
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Необходимо авторизоваться',
            )

        decoded_token_data = jwt.decode(
            token,
            SETTINGS.JWT_SECRET_KEY,
            algorithms=[SETTINGS.JWT_ALGORITHM],
        )

        return UserSchema.model_validate(decoded_token_data)

    async def delete_token(
        self,
        cookie_token: str = Depends(cookie_refresh_token),
        header_token: str = Depends(header_refresh_token),
    ) -> None:
        """Выходим и удаляем токен.

        Raises:
            HTTPException: Ошибка при удалении

        Args:
            cookie_token: str - токен в куках
            header_token: str - токен в хедере
        """
        if header_token:
            token = header_token.split(' ')[-1]
        elif cookie_token:
            token = cookie_token
        else:
            raise HTTPException(
                status_code=HTTP_401_UNAUTHORIZED,
                detail='Невозможно удалить токен, вы не авторизованы',
            )

        logger.info(token)
        logger.info(header_token)


auth_dependency = AuthDependency()

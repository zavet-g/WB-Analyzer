from datetime import datetime

from pydantic import EmailStr
from pydantic import SecretStr

from apps.api.v1.schemas.base_schema import BaseSchema
from apps.utils.enums.user_role_enum import UserRoleEnum


class AuthSchema(BaseSchema):
    user_email: EmailStr
    user_password: SecretStr


class UserSchema(BaseSchema):
    user_email: EmailStr
    user_roles: list[UserRoleEnum]

    @property
    def get_roles(self) -> list[UserRoleEnum]:
        """Получаем роли пользователя.

        Returns:
            list[UserRoleEnum]: роли пользователя
        """
        return [UserRoleEnum(role) for role in self.user_roles]


class JWTTokenSchema(BaseSchema):
    iat: datetime
    exp: datetime
    sub: str
    user_email: str
    user_roles: list[str]


class EncodedJWTTokenSchema(BaseSchema):
    access_token: str
    refresh_token: str

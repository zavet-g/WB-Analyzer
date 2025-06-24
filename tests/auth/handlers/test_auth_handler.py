from starlette.status import HTTP_200_OK
from starlette.status import HTTP_204_NO_CONTENT
from starlette.status import HTTP_401_UNAUTHORIZED

from tests.consts import BASE_AUTH_URL
from tests.consts import STUB_EMAIL
from tests.consts import STUB_PASS


class TestAuthHandler:
    """TestAuthHandler.

    Запуск:
        pytest tests/auth/handlers/test_auth_handler.py -s
    """

    async def test_login(self, client):
        """Тестирование логина пользователя.

        Args:
            client (AsyncClient): асинхронный клиент httpx
        """
        response = await client.post(
            f'{BASE_AUTH_URL}/login',
            json={
                'user_email': STUB_EMAIL,
                'user_password': STUB_PASS,
            },
        )
        assert response.status_code == HTTP_200_OK
        assert 'access_token' in response.headers['set-cookie']

    async def test_logout(self, client):
        """Тестирование логаута пользователя.

        Args:
            client (AsyncClient): асинхронный клиент httpx
        """

        # Не авторизованы
        response = await client.delete(
            f'{BASE_AUTH_URL}/logout',
        )
        data = response.json()

        assert data == {'detail': 'Невозможно удалить токен, вы не авторизованы'}
        assert response.status_code == HTTP_401_UNAUTHORIZED

        # Передали токен в хедере
        response = await client.delete(
            f'{BASE_AUTH_URL}/logout',
            headers={'refresh_token': 'SomeFakeToken'},
        )

        assert response.status_code == HTTP_204_NO_CONTENT
        assert response.text == ''

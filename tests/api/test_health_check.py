import pytest

from starlette.status import HTTP_200_OK
from starlette.status import HTTP_405_METHOD_NOT_ALLOWED

from tests.consts import BASE_URL


@pytest.mark.parametrize('url', ['health'])
class TestHealthCheck:
    """Тестирование хелсчека.

    Запуск:
        pytest tests/api/test_health_check.py -s
    """

    async def test_health_check(self, client, url):
        """Тестирование HealthCheck метода."""
        response = await client.get(f'{BASE_URL}/{url}')

        assert response.status_code == HTTP_200_OK
        assert response.text == 'OK'

    async def test_health_check_fail(self, client, url):
        """Негативное тестирование HealthCheck метода (только GET)."""
        for method in ['POST', 'PUT', 'DELETE']:
            response = await client.request(url=f'{BASE_URL}/{url}', method=method)

            assert response.status_code == HTTP_405_METHOD_NOT_ALLOWED
            assert response.json()['detail'] == 'Method Not Allowed'

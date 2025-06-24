import pytest

from starlette.status import HTTP_200_OK

from tests.consts import BASE_API_URL
from tests.sql_init_data.base_data_tree import base_parser_tree


@pytest.mark.handlers
@pytest.mark.parametrize(
    'db_init_pre_build',
    [base_parser_tree],
    indirect=True,
)
class TestGetServers:
    """Набор тестов для TestGetServers.

    Запуск:
        pytest tests/api/handlers/test_server_handler.py::TestGetServers -s

    """

    async def test_get_servers(
        self,
        auth_client,
        db_init_pre_build,
    ):
        response = await auth_client.get(
            f'{BASE_API_URL}/get_servers',
        )
        assert response.status_code == HTTP_200_OK


@pytest.mark.handlers
@pytest.mark.parametrize(
    'db_init_pre_build',
    [base_parser_tree],
    indirect=True,
)
class TestGetServerById:
    """Набор тестов для TestGetServerById.

    Запуск:
        pytest tests/api/handlers/test_server_handler.py::TestGetServerById -s

    """

    async def test_get_servers(
        self,
        auth_client,
        db_init_pre_build,
    ):
        response = await auth_client.get(
            f'{BASE_API_URL}/get-server-by-id/2',
        )
        assert response.status_code == HTTP_200_OK

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
class TestGetEntryLogs:
    """Набор тестов для TestGetEntryLogs.

    Запуск:
        pytest tests/api/handlers/test_log_entry_handler.py::TestGetEntryLogs -s
    """

    async def test_get_entry_logs(
        self,
        auth_client,
        db_init_pre_build,
    ):
        response = await auth_client.get(
            f'{BASE_API_URL}/get_entry_logs',
        )

        assert response.status_code == HTTP_200_OK

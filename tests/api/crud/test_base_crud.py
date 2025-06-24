import pytest

from apps.api.v1.cruds.base_crud import BaseCrud
from apps.api.v1.models.product_model import LogEntryModel
from tests.sql_init_data.base_data_tree import base_parser_tree


@pytest.mark.parametrize(
    'db_init_pre_build',
    [base_parser_tree],
    indirect=True,
)
class TestBaseCrud:
    """Тестируем базовый круд.

    Запуск:
        pytest tests/api/crud/test_base_crud.py -s
    """

    CRUD = BaseCrud(LogEntryModel)

    async def test_get(
        self,
        session,
        db_init_pre_build,
    ):
        obj = await self.CRUD.get(db=session, _id=1)
        assert obj

    async def test_get_list(
        self,
        session,
        db_init_pre_build,
    ):
        objs = await self.CRUD.get_list(db=session)
        assert len(list(objs)) > 0

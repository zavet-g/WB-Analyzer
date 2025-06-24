import pytest

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.base_crud import BaseCrud
from apps.api.v1.models.product_model import ProductModel
from apps.db.session import PGEngineConnector


@pytest.fixture
async def db_session():
    """Фикстура для создания тестовой сессии."""
    connector = PGEngineConnector()
    async with connector.get_pg_session() as session:
        yield session

@pytest.fixture
async def db_init_pre_build(db_session: AsyncSession):
    """Фикстура для инициализации тестовых данных."""
    test_data = [
        {
            "id": 1,
            "name": "Test Product 1",
            "price": 10000,
            "discount_price": 9000,
            "rating": 4.5,
            "reviews_count": 100,
            "category": "ноутбуки"
        },
        {
            "id": 2,
            "name": "Test Product 2",
            "price": 20000,
            "discount_price": 18000,
            "rating": 4.0,
            "reviews_count": 50,
            "category": "ноутбуки"
        }
    ]
    await db_session.execute(insert(ProductModel), test_data)
    await db_session.commit()

@pytest.mark.asyncio
class TestBaseCrud:
    """Тестируем базовый CRUD."""

    CRUD = BaseCrud(ProductModel)

    async def test_get(
        self,
        db_session: AsyncSession,
        db_init_pre_build
    ):
        """Тестируем получение одной записи."""
        obj = await self.CRUD.get(db=db_session, _id=1)
        assert obj is not None
        assert obj.id == 1
        assert obj.name == "Test Product 1"

    async def test_get_list(
        self,
        db_session: AsyncSession,
        db_init_pre_build
    ):
        """Тестируем получение списка записей."""
        objs = await self.CRUD.get_list(db=db_session)
        assert len(list(objs)) == 2
import pytest

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.models.product_model import ProductModel


@pytest.fixture
async def base_data_tree(session: AsyncSession):
    """Фикстура для инициализации тестовых данных для ProductModel.

    Запуск:
        pytest tests/sql_init_data/base_data_tree.py::base_data_tree -s
    """
    test_data = [
        {
            "id": 1,
            "name": "Test Laptop 1",
            "price": 50000,
            "discount_price": 45000,
            "rating": 4.5,
            "reviews_count": 100,
            "category": "ноутбуки"
        },
        {
            "id": 2,
            "name": "Test Laptop 2",
            "price": 60000,
            "discount_price": 55000,
            "rating": 4.0,
            "reviews_count": 50,
            "category": "ноутбуки"
        }
    ]
    await session.execute(insert(ProductModel), test_data)
    await session.commit()

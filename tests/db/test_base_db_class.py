import pytest

from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.models.product_model import ProductModel


@pytest.mark.asyncio
class TestBaseDBClass:
    """Тестирование базового класса БД.

    Запуск всех тестов:
        pytest tests/db/test_base_db_class.py -s
    """

    async def test_group_by_fields(self, session: AsyncSession, base_data_tree):
        """Тестируем метод group_by_fields для ProductModel.

        Запуск:
            pytest tests/db/test_base_db_class.py::TestBaseDBClass::test_group_by_fields -s
        """
        result = ProductModel.group_by_fields()
        assert len(result) == 6  # Поля: id, name, price, discount_price, rating, reviews_count
        assert str(result[0]) == 'products.id'  # Проверяем первое поле

    async def test_jsonb_build_object(self, session: AsyncSession, base_data_tree):
        """Тестируем метод jsonb_build_object для ProductModel.

        Запуск:
            pytest tests/db/test_base_db_class.py::TestBaseDBClass::test_jsonb_build_object -s
        """
        result = ProductModel.jsonb_build_object()
        assert len(result) == 12  # 6 полей * 2 (ключ + значение в JSONB)
        assert str(result[0]) == "'id'"  # Проверяем первый ключ
        assert str(result[1]) == 'products.id'  # Проверяем первое значение

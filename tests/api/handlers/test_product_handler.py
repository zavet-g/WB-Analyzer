import pytest

from fastapi.testclient import TestClient
from sqlalchemy import delete
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.models.product_model import ProductModel
from apps.db.session import PGEngineConnector
from apps.main import app


@pytest.fixture
async def db_session():
    """Фикстура для создания тестовой сессии."""
    connector = PGEngineConnector()
    async with connector.get_pg_session() as session:
        yield session
        # Очистка данных после теста
        await session.execute(delete(ProductModel))
        await session.commit()

@pytest.fixture
async def db_init_pre_build(db_session: AsyncSession):
    """Фикстура для инициализации тестовых данных."""
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
    await db_session.execute(insert(ProductModel), test_data)
    await db_session.commit()

@pytest.mark.asyncio
class TestProductHandler:
    """Тестируем обработчик получения товаров.

    Запуск всех тестов класса:
        pytest tests/api/handlers/test_product_handler.py -s
    """

    @pytest.fixture
    def client(self):
        """Фикстура для FastAPI TestClient."""
        return TestClient(app)

    async def test_get_products(
        self,
        client: TestClient,
        db_init_pre_build
    ):
        """Тестируем endpoint /api/products.

        Запуск:
            pytest tests/api/handlers/test_product_handler.py::TestProductHandler::test_get_products -s
        """
        response = client.get("/api/products")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        assert data[0]["id"] == 1
        assert data[0]["name"] == "Test Laptop 1"
        assert data[0]["category"] == "ноутбуки"

    async def test_get_products_with_filters(
        self,
        client: TestClient,
        db_init_pre_build
    ):
        """Тестируем endpoint /api/products с фильтрами.

        Запуск:
            pytest tests/api/handlers/test_product_handler.py::TestProductHandler::test_get_products_with_filters -s
        """
        response = client.get("/api/products?min_price=55000&min_rating=4.2")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["id"] == 1
        assert data[0]["name"] == "Test Laptop 1"

    async def test_parse_products(
        self,
        client: TestClient,
        mocker
    ):
        """Тестируем endpoint /api/parse.

        Запуск:
            pytest tests/api/handlers/test_product_handler.py::TestProductHandler::test_parse_products -s
        """
        mocker.patch("apps.api.v1.wildberries_parser.WildberriesParser.parse_products")
        response = client.post("/api/parse?category=ноутбуки")
        assert response.status_code == 200
        assert response.json() == {"message": "Parsing started for category: ноутбуки"}

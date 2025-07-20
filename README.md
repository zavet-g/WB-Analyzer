# WB-Analyzer

Сервис аналитики товаров с парсингом данных с Wildberries и визуализацией на фронтенде.

## Описание

Проект представляет собой backend-сервис для парсинга товаров с сайта Wildberries с возможностью фильтрации и анализа данных.

## Технологии

- **Python 3.13**
- **FastAPI** - веб-фреймворк
- **SQLAlchemy 2.0** - ORM
- **PostgreSQL** - база данных
- **Alembic** - миграции
- **Poetry** - управление зависимостями
- **Docker** - контейнеризация
- **BeautifulSoup4** - парсинг HTML
- **aiohttp** - асинхронные HTTP запросы

## Структура проекта

```
WB-Analyzer/
├── apps/
│   ├── api/v1/
│   │   ├── models/          # SQLAlchemy модели
│   │   ├── schemas/         # Pydantic схемы
│   │   ├── handlers/        # FastAPI обработчики
│   │   ├── cruds/          # CRUD операции
│   │   └── wildberries_parser.py  # Парсер Wildberries
│   ├── db/                 # Настройки базы данных
│   ├── utils/              # Утилиты
│   └── main.py             # Точка входа приложения
├── migrations/             # Миграции Alembic
├── tests/                  # Тесты
└── docker-compose.yml      # Docker конфигурация
```

## Установка и запуск

### Локальная разработка

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd WB-Analyzer
```

2. Установите зависимости:
```bash
poetry install
```

3. Создайте файл .env на основе env.example:
```bash
cp env.example .env
```

4. Запустите PostgreSQL (через Docker):
```bash
docker-compose up db -d
```

5. Примените миграции:
```bash
poetry run alembic upgrade head
```

6. Запустите приложение:
```bash
poetry run uvicorn apps.main:app --reload
```

### Docker

```bash
docker-compose up -d
```

## API Endpoints

### GET /api/products
Получение списка товаров с фильтрацией.

**Параметры:**
- `min_price` (float) - минимальная цена
- `min_rating` (float) - минимальный рейтинг
- `min_reviews` (int) - минимальное количество отзывов
- `category` (str) - категория товаров

**Пример:**
```
GET /api/products/?min_price=5000&min_rating=4.0
```

### POST /api/parse
Запуск парсинга товаров по категории.

**Параметры:**
- `category` (str) - категория для парсинга

**Пример:**
```
POST /api/parse
{
    "category": "ноутбуки"
}
```

## Модель данных

### Product
- `id` (int) - уникальный идентификатор
- `name` (str) - название товара
- `price` (int) - цена
- `discount_price` (int, optional) - цена со скидкой
- `rating` (float, optional) - рейтинг
- `reviews_count` (int, optional) - количество отзывов
- `category` (str) - категория

## Тестирование

```bash
# Запуск всех тестов
poetry run pytest

# Запуск тестов с покрытием
poetry run pytest --cov=apps

# Запуск конкретного теста
poetry run pytest tests/api/handlers/test_product_handler.py -v
```

## Разработка

### Создание миграций
```bash
poetry run alembic revision --autogenerate -m "Description"
poetry run alembic upgrade head
```

### Линтинг и форматирование
```bash
poetry run ruff check .
poetry run ruff format .
```

## Лицензия

MIT
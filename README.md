# 🛍️ WB-Analyzer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.13-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15.1-blue?style=for-the-badge&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Enabled-blue?style=for-the-badge&logo=docker)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**Сервис аналитики товаров с парсингом данных с Wildberries и визуализацией на фронтенде**

[🚀 Быстрый старт](#быстрый-старт) • [📖 Документация](#документация) • [🔧 API](#api-endpoints) • [🧪 Тестирование](#тестирование)

</div>

---

## 📋 Описание

**WB-Analyzer** — это современный backend-сервис для парсинга и анализа товаров с сайта Wildberries. Проект предоставляет RESTful API для получения данных о товарах с возможностью фильтрации по различным параметрам.

### ✨ Основные возможности

- 🔍 **Парсинг товаров** с Wildberries по категориям
- 📊 **Фильтрация данных** по цене, рейтингу, количеству отзывов
- 🚀 **Асинхронная архитектура** для высокой производительности
- 🐳 **Docker контейнеризация** для простого развертывания
- 📈 **Автоматическая документация** API (Swagger/OpenAPI)
- 🧪 **Полное покрытие тестами**

---

## 🛠️ Технологический стек

| Компонент | Технология | Версия |
|-----------|------------|--------|
| **Язык программирования** | Python | 3.13 |
| **Веб-фреймворк** | FastAPI | 0.115.6 |
| **ORM** | SQLAlchemy | 2.0.36 |
| **База данных** | PostgreSQL | 15.1 |
| **Миграции** | Alembic | 1.13.3 |
| **Парсинг** | BeautifulSoup4 | 4.12.3 |
| **HTTP клиент** | aiohttp | 3.9.5 |
| **Контейнеризация** | Docker | Latest |
| **Управление зависимостями** | Poetry | 1.8.3 |
| **Линтинг** | Ruff | 0.8.4 |
| **Тестирование** | pytest | 8.3.4 |

---

## 🏗️ Архитектура проекта

```
WB-Analyzer/
├── 📁 apps/
│   ├── 📁 api/v1/
│   │   ├── 📁 models/          # SQLAlchemy модели
│   │   ├── 📁 schemas/         # Pydantic схемы
│   │   ├── 📁 handlers/        # FastAPI обработчики
│   │   ├── 📁 cruds/          # CRUD операции
│   │   └── 🕷️ wildberries_parser.py  # Парсер Wildberries
│   ├── 📁 db/                 # Настройки базы данных
│   ├── 📁 utils/              # Утилиты и перечисления
│   └── 🚀 main.py             # Точка входа приложения
├── 📁 migrations/             # Миграции Alembic
├── 📁 tests/                  # Тесты (pytest)
├── 🐳 docker-compose.yml      # Docker конфигурация
├── 🐳 Dockerfile              # Docker образ
└── 📄 pyproject.toml          # Конфигурация Poetry
```

---

## 🚀 Быстрый старт

### Предварительные требования

- Python 3.13+
- Docker и Docker Compose
- Poetry (для управления зависимостями)

### Локальная разработка

1. **Клонируйте репозиторий**
```bash
git clone https://github.com/zavet-g/WB-Analyzer.git
cd WB-Analyzer
```

2. **Установите зависимости**
```bash
poetry install
```

3. **Настройте переменные окружения**
```bash
cp env.example .env
# Отредактируйте .env файл при необходимости
```

4. **Запустите базу данных**
```bash
docker-compose up db -d
```

5. **Примените миграции**
```bash
poetry run alembic upgrade head
```

6. **Запустите приложение**
```bash
poetry run uvicorn apps.main:app --reload --host 0.0.0.0 --port 8000
```

### Docker (рекомендуется)

```bash
# Запуск всех сервисов
docker-compose up -d

# Просмотр логов
docker-compose logs -f app
```

---

## 📖 Документация

### Доступ к документации

После запуска приложения документация доступна по адресам:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

---

## 🔧 API Endpoints

### 📋 Получение товаров

**GET** `/api/products`

Получение списка товаров с возможностью фильтрации.

#### Параметры запроса

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `min_price` | `float` | Минимальная цена | `5000` |
| `min_rating` | `float` | Минимальный рейтинг | `4.0` |
| `min_reviews` | `int` | Минимальное количество отзывов | `100` |
| `category` | `string` | Категория товаров | `"ноутбуки"` |

#### Примеры запросов

```bash
# Получить все товары
curl http://localhost:8000/api/products

# Фильтр по цене и рейтингу
curl "http://localhost:8000/api/products?min_price=5000&min_rating=4.0"

# Фильтр по категории
curl "http://localhost:8000/api/products?category=ноутбуки"
```

#### Пример ответа

```json
[
  {
    "id": 1,
    "name": "Ноутбук ASUS VivoBook",
    "price": 45000,
    "discount_price": 42000,
    "rating": 4.5,
    "reviews_count": 150,
    "category": "ноутбуки"
  }
]
```

### 🕷️ Запуск парсинга

**POST** `/api/parse`

Запуск парсинга товаров по указанной категории.

#### Параметры запроса

| Параметр | Тип | Описание | Пример |
|----------|-----|----------|--------|
| `category` | `string` | Категория для парсинга | `"ноутбуки"` |

#### Пример запроса

```bash
curl -X POST "http://localhost:8000/api/parse?category=ноутбуки"
```

#### Пример ответа

```json
{
  "message": "Parsing started for category: ноутбуки"
}
```

### 💚 Проверка здоровья

**GET** `/health`

Проверка состояния сервиса.

```bash
curl http://localhost:8000/health
```

---

## 📊 Модель данных

### Product

| Поле | Тип | Обязательное | Описание |
|------|-----|--------------|----------|
| `id` | `int` | ✅ | Уникальный идентификатор |
| `name` | `string` | ✅ | Название товара |
| `price` | `int` | ✅ | Цена в рублях |
| `discount_price` | `int` | ❌ | Цена со скидкой |
| `rating` | `float` | ❌ | Рейтинг (0.0 - 5.0) |
| `reviews_count` | `int` | ❌ | Количество отзывов |
| `category` | `string` | ✅ | Категория товара |

---

## 🧪 Тестирование

### Запуск тестов

```bash
# Все тесты
poetry run pytest

# С покрытием кода
poetry run pytest --cov=apps --cov-report=html

# Конкретный тест
poetry run pytest tests/api/handlers/test_product_handler.py -v

# Только быстрые тесты
poetry run pytest -m "not slow"
```

### Покрытие кода

После запуска тестов с покрытием, отчет будет доступен в `htmlcov/index.html`.

---

## 🔧 Разработка

### Создание миграций

```bash
# Автогенерация миграции
poetry run alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
poetry run alembic upgrade head

# Откат миграции
poetry run alembic downgrade -1
```

### Линтинг и форматирование

```bash
# Проверка кода
poetry run ruff check .

# Автоисправление
poetry run ruff check . --fix

# Форматирование
poetry run ruff format .

# Проверка типов
poetry run mypy apps/
```

### Pre-commit хуки

```bash
# Установка хуков
poetry run pre-commit install

# Запуск всех хуков
poetry run pre-commit run --all-files
```

---

## 🐳 Docker

### Сборка образа

```bash
# Сборка для разработки
docker build --target dev -t wb-analyzer:dev .

# Сборка для продакшена
docker build --target prod -t wb-analyzer:prod .
```

### Запуск с Docker Compose

```bash
# Запуск всех сервисов
docker-compose up -d

# Остановка
docker-compose down

# Просмотр логов
docker-compose logs -f app
```

---

## 📈 Мониторинг и логи

### Логирование

Приложение использует `loguru` для структурированного логирования:

- **INFO**: Общая информация о работе приложения
- **ERROR**: Ошибки и исключения
- **DEBUG**: Детальная отладочная информация

### Метрики

- Время выполнения запросов (X-Process-Time header)
- Количество обработанных товаров
- Статистика парсинга

---

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции (`git checkout -b feature/amazing-feature`)
3. Закоммитьте изменения (`git commit -m 'Add amazing feature'`)
4. Отправьте в ветку (`git push origin feature/amazing-feature`)
5. Откройте Pull Request

---

## 📄 Лицензия

Этот проект распространяется под лицензией MIT. См. файл [LICENSE](LICENSE) для получения дополнительной информации.

---

## 👨‍💻 Автор

**Артем Букарев** - [jollysjam@gmail.com](mailto:jollysjam@gmail.com)

---

<div align="center">

⭐ **Если проект вам понравился, поставьте звездочку!** ⭐

</div>
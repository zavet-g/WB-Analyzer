import pytest

from pytest_alembic import create_alembic_fixture
from pytest_alembic import tests

history = create_alembic_fixture({'file': 'alembic.ini'})


@pytest.mark.usefixtures('migrations_clean_up')
class TestMigrations:
    """Тестирование миграций.

    Запуск:
        pytest tests/api/test_migrations.py -s
    """

    async def test_single_head_revision(self, history):
        """Тестирование head миграции."""
        tests.test_single_head_revision(history)

    def test_upgrade(self, history):
        """Тест tear up (поднятия миграций)."""
        tests.test_upgrade(history)

    def test_model_definitions_match_ddl(self, history):
        """Тест на соотвествие моделям."""
        tests.test_model_definitions_match_ddl(history)

    @pytest.mark.slow
    def test_up_down_consistency(self, history):
        """Тест консинсетности миграций."""
        tests.test_up_down_consistency(history)

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from apps.db.annotated_fields import dt_utcnow
from apps.db.annotated_fields import dt_with_tz
from apps.db.base_db_class import BaseDBModel


class TestGroupByFields:
    """Тестирование базового класса БД.

    Запуск:
        pytest tests/db/test_base_db_class.py -s
    """

    def test_group_by_fields(self):
        class TestModel1(BaseDBModel):
            __tablename__ = 'test_1'
            __table_args__: dict[str, str] | tuple = ({'schema': 'nginx_parser_schema'},)
            id: Mapped[int] = mapped_column(
                primary_key=True,
            )
            create_date: Mapped[dt_with_tz] = mapped_column()

        result = TestModel1.group_by_fields()

        assert len(result) == 2

    def test_json_build_object(self):
        class TestModel2(BaseDBModel):
            __tablename__ = 'test_2'
            __table_args__: dict[str, str] | tuple = ({'schema': 'nginx_parser_schema'},)
            id: Mapped[int] = mapped_column(
                primary_key=True,
            )
            create_date: Mapped[dt_utcnow] = mapped_column()

        result = TestModel2.jsonb_build_object()

        assert len(result) == 4

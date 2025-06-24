from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from apps.db.base_db_class import BaseDBModel


class ServerModel(BaseDBModel):
    __tablename__ = 'server_model'
    __table_args__: dict[str, str] | tuple = ({'schema': 'nginx_parser_schema'},)

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    ip_address: Mapped[str] = mapped_column(String(45), nullable=False)

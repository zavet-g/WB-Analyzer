from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from apps.db.base_db_class import BaseDBModel


class LogEntryModel(BaseDBModel):
    __tablename__ = 'log_entry_model'
    __table_args__: dict[str, str] | tuple = ({'schema': 'nginx_parser_schema'},)

    id: Mapped[int] = mapped_column(primary_key=True)

    server_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            column='nginx_parser_schema.server_model.id',
            ondelete='CASCADE',
        ),
    )

    timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )
    remote_addr: Mapped[str] = mapped_column(String(45))
    method: Mapped[str] = mapped_column(String(10))
    uri: Mapped[str] = mapped_column(String(2048))
    http_version: Mapped[str] = mapped_column(String(10))
    status: Mapped[int] = mapped_column(Integer)
    size: Mapped[int] = mapped_column(Integer)
    referrer: Mapped[str | None] = mapped_column(
        String(2048),
        nullable=True,
    )
    user_agent: Mapped[str | None] = mapped_column(
        String(1024),
        nullable=True,
    )

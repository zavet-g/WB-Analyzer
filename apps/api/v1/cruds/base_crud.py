from typing import Any
from typing import Generic
from typing import TypeVar

from asyncpg import ForeignKeyViolationError
from asyncpg import UniqueViolationError
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import ScalarResult
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.exceptions import HTTPException
from starlette.status import HTTP_404_NOT_FOUND
from starlette.status import HTTP_409_CONFLICT
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from apps.db.base_db_class import BaseDBModel

ModelType = TypeVar('ModelType', bound=BaseDBModel)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class BaseCrud(Generic[ModelType]):
    def __init__(self, model: type[ModelType]) -> None:
        self.model = model

    async def get(
        self,
        db: AsyncSession,
        _id: Any,
    ) -> ModelType:
        """Получение единичной записи."""
        stmt = select(self.model).where(self.model.id == _id)  # type: ignore
        data = await db.scalar(stmt)

        if not data:
            raise HTTPException(
                status_code=HTTP_404_NOT_FOUND,
                detail=f'Запись {self.model.__tablename__} не найдена',
            )

        return data

    async def get_list(
        self,
        db: AsyncSession,
        *,
        skip: int | None = None,
        limit: int | None = None,
    ) -> ScalarResult[ModelType] | None:
        """Получение списка записей."""
        stmt = select(self.model).order_by(self.model.id)  # type: ignore

        if limit:
            stmt = stmt.limit(limit)
        if skip:
            stmt = stmt.offset(skip)

        return await db.scalars(stmt)

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: CreateSchemaType,
        exclude: set | None = None,
    ) -> ModelType:
        """Создание записи."""
        insert_values = obj_in.model_dump(exclude_none=True, exclude=exclude)

        if 'id' in insert_values:
            raise HTTPException(
                status_code=HTTP_409_CONFLICT,
                detail=f'Пытаемся создать запись в {self.model.__tablename__}, '
                f'передавая ID в бади. {insert_values=}',
            )

        try:
            stmt = await db.execute(
                pg_insert(self.model).values(**insert_values).returning(self.model)
            )
            await db.commit()

            return stmt.scalars().one()

        except IntegrityError as e:
            logger.error(str(e.orig))

            match e.orig.sqlstate:  # type: ignore
                case UniqueViolationError.sqlstate:
                    await db.rollback()

                    raise HTTPException(
                        status_code=HTTP_409_CONFLICT,
                        detail=(
                            f'Поля переданные в модель {self.model} содержат '
                            f'неуникальные значения. {e.orig!s}'
                        ),
                    ) from e
                case ForeignKeyViolationError.sqlstate:
                    await db.rollback()
                    raise HTTPException(
                        status_code=HTTP_409_CONFLICT,
                        detail=f'Вы пытаетесь связать поля с несуществующими значениями FK.'
                        f'{e.orig!s}',
                    ) from e
                case _:
                    await db.rollback()
                    raise HTTPException(
                        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=str(e.orig),
                    ) from e

    async def update(
        self,
        db: AsyncSession,
        *,
        _id: int,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        """Обновляем запись."""
        db_obj = await self.get(db=db, _id=_id)

        update_data = obj_in if isinstance(obj_in, dict) else obj_in.model_dump(exclude_none=True)

        try:
            for field in update_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            await db.commit()

        except IntegrityError as e:
            match e.orig.sqlstate:  # type: ignore
                case ForeignKeyViolationError.sqlstate:
                    raise HTTPException(
                        status_code=HTTP_404_NOT_FOUND,
                        detail=(
                            'Вы пытаетесь прикрепить foreign key к таблице в которой нет такого id'
                        ),
                    ) from e

                case UniqueViolationError.sqlstate:
                    raise HTTPException(
                        status_code=HTTP_409_CONFLICT,
                        detail=(
                            f'Поля переданные в модель {self.model} содержат неуникальные значения'
                        ),
                    ) from e

                case _ as e:
                    raise HTTPException(
                        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=e.detail,
                    ) from e

        return db_obj

    async def delete(self, db: AsyncSession, *, _id: int) -> None:
        """Удаляем запись."""
        db_object = await db.get(self.model, _id)

        await db.delete(db_object)
        await db.commit()

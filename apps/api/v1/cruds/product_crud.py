
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.base_crud import BaseCrud
from apps.api.v1.models.product_model import ProductModel
from apps.api.v1.schemas.product_schema import ProductOutSchema
from apps.db.session import connector


class ProductCrud(BaseCrud):
    async def get_products(
        self,
        min_price: int | None = None,
        min_rating: float | None = None,
        min_reviews: int | None = None,
        category: str | None = None,
        db: AsyncSession = Depends(connector.get_pg_session),
    ) -> list[ProductOutSchema]:
        """Получает список товаров с фильтрацией."""
        query = select(ProductModel).order_by(ProductModel.id)
        if min_price is not None:
            query = query.where(ProductModel.price >= min_price)
        if min_rating is not None:
            query = query.where(ProductModel.rating >= min_rating)
        if min_reviews is not None:
            query = query.where(ProductModel.reviews_count >= min_reviews)
        if category is not None:
            query = query.where(ProductModel.category == category)

        result = await db.execute(query)
        entries = result.scalars().all()
        return [ProductOutSchema.model_validate(entry) for entry in entries]

    async def add_product(
        self,
        product_data: dict,
        db: AsyncSession = Depends(connector.get_pg_session),
    ) -> ProductOutSchema:
        """Добавляет товар в базу."""
        db_product = ProductModel(**product_data)
        db.add(db_product)
        await db.commit()
        await db.refresh(db_product)
        return ProductOutSchema.model_validate(db_product)

product_crud_obj = ProductCrud(ProductModel)

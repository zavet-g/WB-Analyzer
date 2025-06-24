from fastapi import APIRouter, Depends, Query
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from apps.api.v1.cruds.product_crud import product_crud_obj
from apps.api.v1.schemas.product_schema import ProductOutSchema
from apps.db.session import connector

router = APIRouter()

@router.get(
    "/get_products",
    response_model=list[ProductOutSchema],
)
async def get_products(
    min_price: Optional[int] = Query(None, description="Минимальная цена"),
    min_rating: Optional[float] = Query(None, description="Минимальный рейтинг"),
    min_reviews: Optional[int] = Query(None, description="Минимальное количество отзывов"),
    category: Optional[str] = Query(None, description="Категория товаров"),
    db: AsyncSession = Depends(connector.get_pg_session),
) -> list[ProductOutSchema]:
    """Получает список товаров с фильтрацией."""
    return await product_crud_obj.get_products(
        min_price=min_price,
        min_rating=min_rating,
        min_reviews=min_reviews,
        category=category,
        db=db,
    )
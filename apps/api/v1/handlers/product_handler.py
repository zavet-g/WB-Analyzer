from typing import Optional

from fastapi import APIRouter
from fastapi import BackgroundTasks
from fastapi import Depends
from fastapi import Query
from sqlalchemy.ext.asyncio import AsyncSession

from apps.api.v1.cruds.product_crud import product_crud_obj
from apps.api.v1.schemas.product_schema import ProductOutSchema
from apps.api.v1.wildberries_parser import WildberriesParser
from apps.db.session import connector

router = APIRouter(prefix="/api", tags=["products"])

@router.get(
    "/products",
    response_model=list[ProductOutSchema],
)
async def get_products(
    min_price: Optional[float] = Query(None, description="Минимальная цена"),
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

@router.post("/parse", response_model=dict[str, str])
async def parse_products(
    category: str,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(connector.get_pg_session),
) -> dict[str, str]:
    """Запускает парсинг товаров по категории."""
    background_tasks.add_task(WildberriesParser.parse_products, category, db)
    return {"message": f"Parsing started for category: {category}"}
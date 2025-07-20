
from apps.api.v1.schemas.base_schema import BaseSchema


class ProductOutSchema(BaseSchema):
    id: int
    name: str
    price: int
    discount_price: int | None = None
    rating: float | None = None
    reviews_count: int | None = None
    category: str

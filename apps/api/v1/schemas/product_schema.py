from typing import Optional
from pydantic import BaseModel
from apps.api.v1.schemas.base_schema import BaseSchema

class ProductOutSchema(BaseSchema):
    id: int
    name: str
    price: int
    discount_price: Optional[int] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    category: str

    model_config = {'from_attributes': True}
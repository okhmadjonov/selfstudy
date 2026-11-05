from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class ProductDetailsVm(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    category_name: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
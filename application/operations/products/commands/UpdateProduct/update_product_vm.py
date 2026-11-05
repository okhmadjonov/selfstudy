from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UpdateProductVm(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    is_active: bool
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
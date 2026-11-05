from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CreateProductVm(BaseModel):
    """
    .NET: CreateProductVm
    """
    id: int
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int
    category_id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
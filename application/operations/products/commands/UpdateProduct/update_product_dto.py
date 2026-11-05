from typing import Optional
from pydantic import BaseModel, Field


class UpdateProductDto(BaseModel):
    name: str = Field(..., min_length=1, max_length=150, description="Mahsulot nomi")
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., ge=0)
    stock_quantity: int = Field(..., ge=0)
    category_id: int = Field(..., gt=0)
    is_active: Optional[bool] = Field(None)
from typing import Optional
from pydantic import BaseModel, Field


class CreateProductDto(BaseModel):
    """
    .NET: CreateProductDto
    """
    name: str = Field(..., min_length=1, max_length=150, description="Mahsulot nomi")
    description: Optional[str] = Field(None, max_length=500, description="Tavsif")
    price: float = Field(..., ge=0, description="Narxi (0 dan kam bo'lmasligi kerak)")
    stock_quantity: int = Field(0, ge=0, description="Ombordagi soni")
    category_id: int = Field(..., gt=0, description="Tegishli kategoriya IDsi")
    is_active: bool = Field(True, description="Faollik holati")
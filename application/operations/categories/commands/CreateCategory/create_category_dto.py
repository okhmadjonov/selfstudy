from typing import Optional
from pydantic import BaseModel, Field


class CreateCategoryDto(BaseModel):
    """
    .NET'dagi `CreateProductCategoryDto` ekvivalenti.
    Front-end'dan qabul qilib olinadigan forma / body ma'lumotlari.
    Validatsiya qoidalari (xuddi FluentValidation kabi) avtomatik ishlaydi.
    """
    name: str = Field(..., min_length=1, max_length=250, description="Kategoriya nomi")
    description: Optional[str] = Field(None, max_length=500, description="Kategoriya tavsifi")
    is_active: bool = Field(True, description="Kategoriya faolligi")


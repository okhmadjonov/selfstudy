from typing import Optional
from pydantic import BaseModel, Field


class UpdateCategoryDto(BaseModel):
    """
    .NET'dagi `UpdateProductCategoryDto` ekvivalenti.
    """
    name: str = Field(..., min_length=1, max_length=250, description="Kategoriya nomi")
    description: Optional[str] = Field(None, max_length=500, description="Kategoriya tavsifi")
    is_active: Optional[bool] = Field(None, description="Kategoriya faolligi")


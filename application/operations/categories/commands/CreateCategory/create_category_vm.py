from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CreateCategoryVm(BaseModel):
    """
    .NET'dagi `CreateProductCategoryVm` ekvivalenti.
    Mijozga (front-end) qaytariladigan ViewModel.
    """
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime

    # EF Core / SQLAlchemy modelini avtomatik DTO/VM ga o'girish (xuddi AutoMapper kabi)
    model_config = ConfigDict(from_attributes=True)


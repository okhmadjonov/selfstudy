from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryDetailsVm(BaseModel):
    """
    .NET'dagi `ProductCategoryDetailsVm` ekvivalenti.
    Bitta kategoriyaning barcha tafsilotlari.
    """
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


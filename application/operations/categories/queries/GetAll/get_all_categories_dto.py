from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CategoryLookupDto(BaseModel):
    """
    .NET'dagi `ProductCategoriesAllDto` ekvivalenti.
    """
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


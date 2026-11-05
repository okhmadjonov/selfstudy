from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UpdateCategoryVm(BaseModel):
    """
    .NET'dagi `UpdateProductCategoryVm` ekvivalenti.
    """
    id: int
    name: str
    description: Optional[str] = None
    is_active: bool
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


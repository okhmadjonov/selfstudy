from dataclasses import dataclass
from typing import Optional
from domain.entities.base_entity import BaseEntity


@dataclass(kw_only=True)
class Category(BaseEntity):
    """
    .NET'dagi `public class Category : BaseEntity` ekvivalenti.
    
    id, created_at, updated_at maydonlari BaseEntity'dan meros olinadi.
    """
    name: str
    description: Optional[str] = None
    is_active: bool = True

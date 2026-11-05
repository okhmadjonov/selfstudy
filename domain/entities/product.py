from dataclasses import dataclass
from typing import Optional
from domain.entities.base_entity import BaseEntity


@dataclass(kw_only=True)
class Product(BaseEntity):
    """
    .NET: public class Product : BaseEntity
    
    id, created_at, updated_at, is_deleted maydonlari BaseEntity'dan meros o'tadi.
    """
    name: str
    description: Optional[str] = None
    price: float = 0.0
    stock_quantity: int = 0
    category_id: int
    is_active: bool = True
from dataclasses import dataclass
from typing import Optional
from .update_product_dto import UpdateProductDto


@dataclass
class UpdateProductCommand:
    id: int
    name: str
    price: float
    stock_quantity: int
    category_id: int
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def from_dto(cls, id: int, dto: UpdateProductDto) -> "UpdateProductCommand":
        return cls(
            id=id,
            name=dto.name,
            description=dto.description,
            price=dto.price,
            stock_quantity=dto.stock_quantity,
            category_id=dto.category_id,
            is_active=dto.is_active,
        )
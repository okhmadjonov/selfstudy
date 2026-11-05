from dataclasses import dataclass
from typing import Optional
from .create_product_dto import CreateProductDto


@dataclass
class CreateProductCommand:
    """
    .NET: public class CreateProductCommand : IRequest<CreateProductVm>
    """
    name: str
    price: float
    stock_quantity: int
    category_id: int
    description: Optional[str] = None
    is_active: bool = True

    @classmethod
    def from_dto(cls, dto: CreateProductDto) -> "CreateProductCommand":
        return cls(
            name=dto.name,
            description=dto.description,
            price=dto.price,
            stock_quantity=dto.stock_quantity,
            category_id=dto.category_id,
            is_active=dto.is_active,
        )
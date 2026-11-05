from dataclasses import dataclass
from typing import Optional
from application.operations.categories.commands.UpdateCategory.update_category_dto import UpdateCategoryDto


@dataclass
class UpdateCategoryCommand:
    """
    .NET'dagi `UpdateProductCategoryCommand : IRequest<UpdateProductCategoryVm>` ekvivalenti.
    """
    id: int
    name: str
    description: Optional[str] = None
    is_active: Optional[bool] = None

    @classmethod
    def from_dto(cls, id: int, dto: UpdateCategoryDto) -> "UpdateCategoryCommand":
        return cls(
            id=id,
            name=dto.name,
            description=dto.description,
            is_active=dto.is_active,
        )


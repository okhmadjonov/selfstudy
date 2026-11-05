from dataclasses import dataclass
from typing import Optional
from application.operations.categories.commands.CreateCategory.create_category_dto import CreateCategoryDto


@dataclass
class CreateCategoryCommand:
    """
    .NET'dagi `public class CreateProductCategoryCommand : IRequest<CreateProductCategoryVm>` ekvivalenti.
    Biznes operatsiyasi uchun kerak bo'ladigan to'liq buyruq parametri.
    """
    name: str
    description: Optional[str] = None
    is_active: bool = True

    @classmethod
    def from_dto(cls, dto: CreateCategoryDto) -> "CreateCategoryCommand":
        """
        AutoMapper ekvivalenti: DTO'dan Command'ga map qilish.
        """
        return cls(
            name=dto.name,
            description=dto.description,
            is_active=dto.is_active,
        )


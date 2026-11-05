from datetime import datetime
from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import IBBDbContext
from application.operations.categories.commands.UpdateCategory.update_category_command import UpdateCategoryCommand
from application.operations.categories.commands.UpdateCategory.update_category_vm import UpdateCategoryVm
from persistence.database.models.category_model import CategoryModel


class UpdateCategoryHandler:
    """
    .NET'dagi `UpdateProductCategoryHandler : IRequestHandler<UpdateProductCategoryCommand, UpdateProductCategoryVm>` ekvivalenti.
    """

    def __init__(self, context: IBBDbContext) -> None:
        self._context = context

    async def handle(self, request: UpdateCategoryCommand) -> UpdateCategoryVm:
        # 1. Bazadan ID bo'yicha qidirish (FirstOrDefaultAsync)
        stmt = select(CategoryModel).where(CategoryModel.id == request.id)
        result = await self._context.session.execute(stmt)
        entity = result.scalar_one_or_none()

        # 2. Agar topilmasa NotFoundException
        if entity is None:
            raise NotFoundException("Category", request.id)

        # 3. Maydonlarni yangilash
        entity.name = request.name
        entity.description = request.description
        if request.is_active is not None:
            entity.is_active = request.is_active
        entity.updated_at = datetime.utcnow()

        # 4. Saqlash
        await self._context.save_changes_async()
        await self._context.session.refresh(entity)

        # 5. ViewModel qaytarish
        return UpdateCategoryVm.model_validate(entity)


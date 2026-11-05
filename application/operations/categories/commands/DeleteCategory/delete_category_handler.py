from datetime import datetime
from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import ISSDbContext
from application.operations.categories.commands.DeleteCategory.delete_category_command import DeleteCategoryCommand
from persistence.database.models.category_model import CategoryModel


class DeleteCategoryHandler:
    """
    .NET'dagi `DeleteProductCategoryCommandHandler` ekvivalenti.
    Soft Delete: bazadan o'chirib tashlamaydi, is_deleted=True qilib qo'yadi.
    """

    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: DeleteCategoryCommand) -> None:
        # Faqat o'chirilmaganlarni topish
        stmt = select(CategoryModel).where(
            CategoryModel.id == request.id,
            CategoryModel.is_deleted == False,
        )
        result = await self._context.session.execute(stmt)
        entity = result.scalar_one_or_none()

        if entity is None:
            raise NotFoundException("Category", request.id)

        # Soft Delete qilish (.NET dagi: entity.IsDeleted = true)
        entity.is_deleted = True
        entity.updated_at = datetime.utcnow()

        await self._context.save_changes_async()


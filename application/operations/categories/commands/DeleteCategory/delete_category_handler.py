from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import IBBDbContext
from application.operations.categories.commands.DeleteCategory.delete_category_command import DeleteCategoryCommand
from persistence.database.models.category_model import CategoryModel


class DeleteCategoryHandler:
    """
    .NET'dagi `DeleteProductCategoryCommandHandler : IRequestHandler<DeleteProductCategoryCommand>` ekvivalenti.
    """

    def __init__(self, context: IBBDbContext) -> None:
        self._context = context

    async def handle(self, request: DeleteCategoryCommand) -> None:
        stmt = select(CategoryModel).where(CategoryModel.id == request.id)
        result = await self._context.session.execute(stmt)
        entity = result.scalar_one_or_none()

        if entity is None:
            raise NotFoundException("Category", request.id)

        # Bazadan o'chirish (yoki soft-delete)
        await self._context.session.delete(entity)
        await self._context.save_changes_async()


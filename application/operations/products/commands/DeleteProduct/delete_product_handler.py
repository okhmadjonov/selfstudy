from datetime import datetime
from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import ISSDbContext
from persistence.database.models.product_model import ProductModel
from .delete_product_command import DeleteProductCommand


class DeleteProductHandler:
    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: DeleteProductCommand) -> None:
        stmt = select(ProductModel).where(
            ProductModel.id == request.id,
            ProductModel.is_deleted == False,
        )
        result = await self._context.session.execute(stmt)
        product = result.scalar_one_or_none()

        if product is None:
            raise NotFoundException("Product", request.id)

        # Soft delete
        product.is_deleted = True
        product.updated_at = datetime.utcnow()
        await self._context.save_changes_async()

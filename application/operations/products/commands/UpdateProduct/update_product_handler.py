from datetime import datetime
from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import ISSDbContext
from persistence.database.models.category_model import CategoryModel
from persistence.database.models.product_model import ProductModel
from .update_product_command import UpdateProductCommand
from .update_product_vm import UpdateProductVm


class UpdateProductHandler:
    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: UpdateProductCommand) -> UpdateProductVm:
        # 1. Mahsulotni topish (o'chirilmagan bo'lishi shart)
        stmt = select(ProductModel).where(
            ProductModel.id == request.id,
            ProductModel.is_deleted == False,
        )
        result = await self._context.session.execute(stmt)
        product = result.scalar_one_or_none()

        if product is None:
            raise NotFoundException("Product", request.id)

        # 2. Yangi berilgan kategoriya mavjudligini tekshirish
        cat_stmt = select(CategoryModel).where(
            CategoryModel.id == request.category_id,
            CategoryModel.is_deleted == False,
        )
        cat_result = await self._context.session.execute(cat_stmt)
        if cat_result.scalar_one_or_none() is None:
            raise NotFoundException("Category", request.category_id)

        # 3. Maydonlarni yangilash
        product.name = request.name
        product.description = request.description
        product.price = request.price
        product.stock_quantity = request.stock_quantity
        product.category_id = request.category_id
        if request.is_active is not None:
            product.is_active = request.is_active
        product.updated_at = datetime.utcnow()

        # 4. Saqlash
        await self._context.save_changes_async()
        await self._context.session.refresh(product)

        return UpdateProductVm.model_validate(product)

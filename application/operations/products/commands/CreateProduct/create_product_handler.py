from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import ISSDbContext
from persistence.database.models.category_model import CategoryModel
from persistence.database.models.product_model import ProductModel
from .create_product_command import CreateProductCommand
from .create_product_vm import CreateProductVm


class CreateProductHandler:
    """
    .NET: CreateProductCommandHandler : IRequestHandler<CreateProductCommand, CreateProductVm>
    """

    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: CreateProductCommand) -> CreateProductVm:
        # 1. Biznes tekshiruv: Kategoriya bazada bormi va o'chirilmaganmi?
        cat_stmt = select(CategoryModel).where(
            CategoryModel.id == request.category_id,
            CategoryModel.is_deleted == False,
        )
        cat_result = await self._context.session.execute(cat_stmt)
        category = cat_result.scalar_one_or_none()

        if category is None:
            raise NotFoundException("Category", request.category_id)

        # 2. Yangi mahsulot entitysini yaratish
        product = ProductModel(
            name=request.name,
            description=request.description,
            price=request.price,
            stock_quantity=request.stock_quantity,
            category_id=request.category_id,
            is_active=request.is_active,
        )

        # 3. Bazaga qo'shish va saqlash
        self._context.session.add(product)
        await self._context.save_changes_async()
        await self._context.session.refresh(product)

        # 4. ViewModel qaytarish
        return CreateProductVm.model_validate(product)

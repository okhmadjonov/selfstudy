from sqlalchemy import select
from sqlalchemy.orm import joinedload

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import ISSDbContext
from persistence.database.models.product_model import ProductModel
from .get_product_details_query import GetProductDetailsQuery
from .get_product_details_vm import ProductDetailsVm


class GetProductDetailsHandler:
    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: GetProductDetailsQuery) -> ProductDetailsVm:
        # .NET: _context.Products.Include(x => x.Category).FirstOrDefaultAsync(...)
        stmt = (
            select(ProductModel)
            .options(joinedload(ProductModel.category))
            .where(
                ProductModel.id == request.id,
                ProductModel.is_deleted == False,
            )
        )
        result = await self._context.session.execute(stmt)
        product = result.scalar_one_or_none()

        if product is None:
            raise NotFoundException("Product", request.id)

        vm = ProductDetailsVm.model_validate(product)
        if product.category:
            vm.category_name = product.category.name
        return vm

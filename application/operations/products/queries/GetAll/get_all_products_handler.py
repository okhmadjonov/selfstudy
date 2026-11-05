from sqlalchemy import or_, select

from application.interfaces.dbcontextinterface import ISSDbContext
from persistence.database.models.product_model import ProductModel
from .get_all_products_dto import ProductLookupDto
from .get_all_products_query import GetAllProductsQuery
from .get_all_products_vm import GetAllProductsVm


class GetAllProductsHandler:
    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: GetAllProductsQuery) -> GetAllProductsVm:
        stmt = select(ProductModel).where(ProductModel.is_deleted == False)

        # Kategoriya bo'yicha filter
        if request.category_id:
            stmt = stmt.where(ProductModel.category_id == request.category_id)

        # Qidiruv
        if request.search:
            pattern = f"%{request.search}%"
            stmt = stmt.where(
                or_(
                    ProductModel.name.ilike(pattern),
                    ProductModel.description.ilike(pattern),
                )
            )

        result = await self._context.session.execute(stmt)
        products = result.scalars().all()

        items = [ProductLookupDto.model_validate(p) for p in products]
        return GetAllProductsVm(items=items)

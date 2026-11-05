import math
from sqlalchemy import asc, desc, func, or_, select

from application.interfaces.dbcontextinterface import ISSDbContext
from persistence.database.models.product_model import ProductModel
from .get_products_list_dto import ProductListItemDto
from .get_products_list_query import GetProductsListQuery
from .get_products_list_vm import ProductsListVm


class GetProductsListHandler:
    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: GetProductsListQuery) -> ProductsListVm:
        stmt = select(ProductModel).where(ProductModel.is_deleted == False)

        # Kategoriya filtri
        if request.category_id:
            stmt = stmt.where(ProductModel.category_id == request.category_id)

        # Qidiruv filtri
        if request.search:
            pattern = f"%{request.search}%"
            stmt = stmt.where(
                or_(
                    ProductModel.name.ilike(pattern),
                    ProductModel.description.ilike(pattern),
                )
            )

        # Umumiy sonini olish
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_items = await self._context.session.scalar(count_stmt) or 0

        # Saralash
        sort_col = getattr(ProductModel, request.order_column, ProductModel.created_at)
        if request.order_type.lower() == "asc":
            stmt = stmt.order_by(asc(sort_col))
        else:
            stmt = stmt.order_by(desc(sort_col))

        # Sahifalash (Skip / Take)
        page_size = max(1, min(request.page_size, 100))
        page_index = max(1, request.page_index)
        offset = (page_index - 1) * page_size

        stmt = stmt.offset(offset).limit(page_size)

        result = await self._context.session.execute(stmt)
        products = result.scalars().all()

        total_pages = math.ceil(total_items / page_size) if page_size > 0 else 0
        items = [ProductListItemDto.model_validate(p) for p in products]

        return ProductsListVm(
            current_page=page_index,
            total_pages=total_pages,
            page_size=page_size,
            total_items=total_items,
            items=items,
        )

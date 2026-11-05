import math
from sqlalchemy import asc, desc, func, or_, select

from application.interfaces.dbcontextinterface import IBBDbContext
from application.operations.categories.queries.GetList.get_categories_list_dto import CategoryListItemDto
from application.operations.categories.queries.GetList.get_categories_list_query import GetCategoriesListQuery
from application.operations.categories.queries.GetList.get_categories_list_vm import CategoriesListVm
from persistence.database.models.category_model import CategoryModel


class GetCategoriesListHandler:
    """
    .NET'dagi `ProductCategoriesListQueryHandler` ekvivalenti.
    Pagination (Skip/Take), Search va Order by bilan ishlaydi.
    """

    def __init__(self, context: IBBDbContext) -> None:
        self._context = context

    async def handle(self, request: GetCategoriesListQuery) -> CategoriesListVm:
        stmt = select(CategoryModel)

        # 1. Search filtri (nomi yoki tavsifida)
        if request.search:
            pattern = f"%{request.search}%"
            stmt = stmt.where(
                or_(
                    CategoryModel.name.ilike(pattern),
                    CategoryModel.description.ilike(pattern),
                )
            )

        # 2. Total items hisoblash (CountAsync)
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_items = await self._context.session.scalar(count_stmt) or 0

        # 3. Saralash (OrderBy)
        sort_col = getattr(CategoryModel, request.order_column, CategoryModel.created_at)
        if request.order_type.lower() == "desc":
            stmt = stmt.order_by(desc(sort_col))
        else:
            stmt = stmt.order_by(asc(sort_col))

        # 4. Sahifalash (Skip(pi-1 * ps).Take(ps))
        page_size = max(1, min(request.page_size, 100))
        page_index = max(1, request.page_index)
        offset = (page_index - 1) * page_size

        stmt = stmt.offset(offset).limit(page_size)

        result = await self._context.session.execute(stmt)
        categories = result.scalars().all()

        total_pages = math.ceil(total_items / page_size) if page_size > 0 else 0
        items = [CategoryListItemDto.model_validate(c) for c in categories]

        return CategoriesListVm(
            current_page=page_index,
            total_pages=total_pages,
            page_size=page_size,
            total_items=total_items,
            items=items,
        )


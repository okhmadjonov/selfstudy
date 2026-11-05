from sqlalchemy import or_, select

from application.interfaces.dbcontextinterface import IBBDbContext
from application.operations.categories.queries.GetAll.get_all_categories_dto import CategoryLookupDto
from application.operations.categories.queries.GetAll.get_all_categories_query import GetAllCategoriesQuery
from application.operations.categories.queries.GetAll.get_all_categories_vm import GetAllCategoriesVm
from persistence.database.models.category_model import CategoryModel


class GetAllCategoriesHandler:
    """
    .NET'dagi `ProductCategoriesAllQueryHandler : IRequestHandler<ProductCategoriesAllQuery, ProductCategoriesAllVm>` ekvivalenti.
    """

    def __init__(self, context: IBBDbContext) -> None:
        self._context = context

    async def handle(self, request: GetAllCategoriesQuery) -> GetAllCategoriesVm:
        stmt = select(CategoryModel)

        # Qidiruv bo'lsa (Search filter)
        if request.search:
            search_pattern = f"%{request.search}%"
            stmt = stmt.where(
                or_(
                    CategoryModel.name.ilike(search_pattern),
                    CategoryModel.description.ilike(search_pattern),
                )
            )

        result = await self._context.session.execute(stmt)
        categories = result.scalars().all()

        items = [CategoryLookupDto.model_validate(c) for c in categories]
        return GetAllCategoriesVm(items=items)


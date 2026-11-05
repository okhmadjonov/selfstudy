from sqlalchemy import or_, select

from application.interfaces.dbcontextinterface import ISSDbContext
from application.operations.categories.queries.GetAll.get_all_categories_dto import CategoryLookupDto
from application.operations.categories.queries.GetAll.get_all_categories_query import GetAllCategoriesQuery
from application.operations.categories.queries.GetAll.get_all_categories_vm import GetAllCategoriesVm
from persistence.database.models.category_model import CategoryModel


class GetAllCategoriesHandler:
    """
    .NET'dagi `ProductCategoriesAllQueryHandler` ekvivalenti.
    """

    def __init__(self, context: ISSDbContext) -> None:
        self._context = context

    async def handle(self, request: GetAllCategoriesQuery) -> GetAllCategoriesVm:
        # Faqat o'chirilmaganlarni olish (.Where(x => !x.IsDeleted))
        stmt = select(CategoryModel).where(CategoryModel.is_deleted == False)

        # Qidiruv bo'lsa
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


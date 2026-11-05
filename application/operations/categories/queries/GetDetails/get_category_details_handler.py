from sqlalchemy import select

from application.exceptions import NotFoundException
from application.interfaces.dbcontextinterface import IBBDbContext
from application.operations.categories.queries.GetDetails.get_category_details_query import GetCategoryDetailsQuery
from application.operations.categories.queries.GetDetails.get_category_details_vm import CategoryDetailsVm
from persistence.database.models.category_model import CategoryModel


class GetCategoryDetailsHandler:
    """
    .NET'dagi `ProductCategoryDetailsQueryHandler` ekvivalenti.
    """

    def __init__(self, context: IBBDbContext) -> None:
        self._context = context

    async def handle(self, request: GetCategoryDetailsQuery) -> CategoryDetailsVm:
        # Faqat o'chirilmaganini topish (.FirstOrDefaultAsync(x => x.Id == id && !x.IsDeleted))
        stmt = select(CategoryModel).where(
            CategoryModel.id == request.id,
            CategoryModel.is_deleted == False,
        )
        result = await self._context.session.execute(stmt)
        entity = result.scalar_one_or_none()

        if entity is None:
            raise NotFoundException("Category", request.id)

        return CategoryDetailsVm.model_validate(entity)

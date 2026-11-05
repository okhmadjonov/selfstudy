from typing import List
from pydantic import BaseModel
from application.operations.categories.queries.GetList.get_categories_list_dto import CategoryListItemDto


class CategoriesListVm(BaseModel):
    """
    .NET'dagi `ProductCategoriesListVm : PaginatedList<ProductCategoryLookupDto>` ekvivalenti.
    """
    current_page: int
    total_pages: int
    page_size: int
    total_items: int
    items: List[CategoryListItemDto]


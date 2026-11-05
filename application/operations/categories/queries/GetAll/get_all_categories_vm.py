from typing import List
from pydantic import BaseModel
from application.operations.categories.queries.GetAll.get_all_categories_dto import CategoryLookupDto


class GetAllCategoriesVm(BaseModel):
    """
    .NET'dagi `ProductCategoriesAllVm` ekvivalenti:
    public IList<ProductCategoriesAllDto>? List { get; set; }
    """
    items: List[CategoryLookupDto]


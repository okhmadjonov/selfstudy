from dataclasses import dataclass
from typing import Optional


@dataclass
class GetCategoriesListQuery:
    """
    .NET'dagi `ProductCategoriesListQuery : IRequest<ProductCategoriesListVm>` ekvivalenti.
    """
    page_index: int = 1
    page_size: int = 10
    search: Optional[str] = ""
    order_column: str = "created_at"
    order_type: str = "asc"


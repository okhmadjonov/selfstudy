from dataclasses import dataclass
from typing import Optional


@dataclass
class GetAllCategoriesQuery:
    """
    .NET'dagi `ProductCategoriesAllQuery : IRequest<ProductCategoriesAllVm>` ekvivalenti.
    """
    search: Optional[str] = ""


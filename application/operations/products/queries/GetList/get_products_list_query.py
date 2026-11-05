from dataclasses import dataclass
from typing import Optional


@dataclass
class GetProductsListQuery:
    page_index: int = 1
    page_size: int = 10
    search: Optional[str] = ""
    category_id: Optional[int] = None
    order_column: str = "created_at"
    order_type: str = "desc"
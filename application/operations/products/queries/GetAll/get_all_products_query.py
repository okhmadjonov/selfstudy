from dataclasses import dataclass
from typing import Optional


@dataclass
class GetAllProductsQuery:
    search: Optional[str] = ""
    category_id: Optional[int] = None
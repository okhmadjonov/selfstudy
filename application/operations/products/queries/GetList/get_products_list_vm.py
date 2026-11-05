from typing import List
from pydantic import BaseModel
from .get_products_list_dto import ProductListItemDto


class ProductsListVm(BaseModel):
    current_page: int
    total_pages: int
    page_size: int
    total_items: int
    items: List[ProductListItemDto]
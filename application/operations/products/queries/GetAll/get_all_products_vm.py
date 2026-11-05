from typing import List
from pydantic import BaseModel
from .get_all_products_dto import ProductLookupDto


class GetAllProductsVm(BaseModel):
    items: List[ProductLookupDto]
from webapi.controllers import ProductsController
from fastapi import APIRouter
from webapi.controllers import CategoriesController
from webapi.controllers.v1.endpoints import health

api_router = APIRouter()

# Controller'larni ro'yxatdan o'tkazish (.NET: app.MapControllers())
api_router.include_router(health.router)
api_router.include_router(CategoriesController.router)

api_router.include_router(ProductsController.router)

from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from application.interfaces.dbcontextinterface import ISSDbContext
from application.operations.products.commands.CreateProduct import (
    CreateProductCommand,
    CreateProductDto,
    CreateProductHandler,
    CreateProductVm,
)
from application.operations.products.commands.DeleteProduct import (
    DeleteProductCommand,
    DeleteProductHandler,
)
from application.operations.products.commands.UpdateProduct import (
    UpdateProductCommand,
    UpdateProductDto,
    UpdateProductHandler,
    UpdateProductVm,
)
from application.operations.products.queries.GetAll import (
    GetAllProductsHandler,
    GetAllProductsQuery,
    GetAllProductsVm,
)
from application.operations.products.queries.GetDetails import (
    GetProductDetailsHandler,
    GetProductDetailsQuery,
    ProductDetailsVm,
)
from application.operations.products.queries.GetList import (
    GetProductsListHandler,
    GetProductsListQuery,
    ProductsListVm,
)
from persistence.database.appdbcontext import get_db_context

# .NET: [Route("api/[controller]")]
router = APIRouter(prefix="/products", tags=["Products"])


# 1. GET LIST (Pagination + Search + Category filter)
@router.get(
    "/",
    response_model=ProductsListVm,
    status_code=status.HTTP_200_OK,
    summary="Mahsulotlar ro'yxatini sahifalash bilan olish (GetList)",
)
async def get_list(
    pi: int = Query(1, ge=1, alias="pi", description="Sahifa raqami"),
    ps: int = Query(10, ge=1, le=100, alias="ps", description="Sahifa hajmi"),
    s: Optional[str] = Query("", alias="s", description="Qidiruv"),
    category_id: Optional[int] = Query(None, alias="category_id", description="Kategoriya bo'yicha filter"),
    ot: str = Query("desc", alias="ot", pattern="^(asc|desc)$", description="Saralash"),
    context: ISSDbContext = Depends(get_db_context),
) -> ProductsListVm:
    query = GetProductsListQuery(
        page_index=pi,
        page_size=ps,
        search=s,
        category_id=category_id,
        order_type=ot,
    )
    handler = GetProductsListHandler(context=context)
    return await handler.handle(query)


# 2. GET ALL
@router.get(
    "/all",
    response_model=GetAllProductsVm,
    status_code=status.HTTP_200_OK,
    summary="Barcha mahsulotlarni olish (GetAll)",
)
async def get_all(
    s: Optional[str] = Query("", alias="s"),
    category_id: Optional[int] = Query(None, alias="category_id"),
    context: ISSDbContext = Depends(get_db_context),
) -> GetAllProductsVm:
    query = GetAllProductsQuery(search=s, category_id=category_id)
    handler = GetAllProductsHandler(context=context)
    return await handler.handle(query)


# 3. GET DETAILS (Kategoriya nomi bilan birga chiqadi)
@router.get(
    "/{id}",
    response_model=ProductDetailsVm,
    status_code=status.HTTP_200_OK,
    summary="Mahsulot tafsilotlarini ID bo'yicha olish (GetDetails)",
)
async def get_details(
    id: int,
    context: ISSDbContext = Depends(get_db_context),
) -> ProductDetailsVm:
    query = GetProductDetailsQuery(id=id)
    handler = GetProductDetailsHandler(context=context)
    return await handler.handle(query)


# 4. CREATE
@router.post(
    "/",
    response_model=CreateProductVm,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi mahsulot yaratish (Create)",
)
async def create(
    dto: CreateProductDto,
    context: ISSDbContext = Depends(get_db_context),
) -> CreateProductVm:
    command = CreateProductCommand.from_dto(dto)
    handler = CreateProductHandler(context=context)
    return await handler.handle(command)


# 5. UPDATE
@router.put(
    "/{id}",
    response_model=UpdateProductVm,
    status_code=status.HTTP_200_OK,
    summary="Mahsulotni yangilash (Update)",
)
async def update(
    id: int,
    dto: UpdateProductDto,
    context: ISSDbContext = Depends(get_db_context),
) -> UpdateProductVm:
    command = UpdateProductCommand.from_dto(id=id, dto=dto)
    handler = UpdateProductHandler(context=context)
    return await handler.handle(command)


# 6. DELETE (Soft delete)
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Mahsulotni o'chirish (Delete)",
)
async def delete(
    id: int,
    context: ISSDbContext = Depends(get_db_context),
) -> None:
    command = DeleteProductCommand(id=id)
    handler = DeleteProductHandler(context=context)
    await handler.handle(command)

from typing import Optional
from fastapi import APIRouter, Depends, Query, status

from application.interfaces.dbcontextinterface import ISSDbContext
from application.operations.categories.commands.CreateCategory import (
    CreateCategoryCommand,
    CreateCategoryDto,
    CreateCategoryHandler,
    CreateCategoryVm,
)
from application.operations.categories.commands.DeleteCategory import (
    DeleteCategoryCommand,
    DeleteCategoryHandler,
)
from application.operations.categories.commands.UpdateCategory import (
    UpdateCategoryCommand,
    UpdateCategoryDto,
    UpdateCategoryHandler,
    UpdateCategoryVm,
)
from application.operations.categories.queries.GetAll import (
    GetAllCategoriesHandler,
    GetAllCategoriesQuery,
    GetAllCategoriesVm,
)
from application.operations.categories.queries.GetDetails import (
    CategoryDetailsVm,
    GetCategoryDetailsHandler,
    GetCategoryDetailsQuery,
)
from application.operations.categories.queries.GetList import (
    CategoriesListVm,
    GetCategoriesListHandler,
    GetCategoriesListQuery,
)
from persistence.database.appdbcontext import get_db_context

# .NET: [Route("api/[controller]")]
router = APIRouter(prefix="/categories", tags=["Categories"])


# 1. GET LIST (Sahifalash, saralash va qidirish bilan)
# .NET: [HttpGet] public async Task<ActionResult<ProductCategoriesListVm>> GetList(...)
@router.get(
    "/",
    response_model=CategoriesListVm,
    status_code=status.HTTP_200_OK,
    summary="Kategoriyalar ro'yxatini sahifalash bilan olish (GetList)",
)
async def get_list(
    pi: int = Query(1, ge=1, alias="pi", description="Sahifa raqami (PageIndex)"),
    ps: int = Query(10, ge=1, le=100, alias="ps", description="Sahifa hajmi (PageSize)"),
    s: Optional[str] = Query("", alias="s", description="Qidiruv matni (Search)"),
    ot: str = Query("asc", alias="ot", pattern="^(asc|desc)$", description="Saralash tartibi (OrderType)"),
    context: ISSDbContext = Depends(get_db_context),
) -> CategoriesListVm:
    query = GetCategoriesListQuery(
        page_index=pi,
        page_size=ps,
        search=s,
        order_type=ot,
    )
    handler = GetCategoriesListHandler(context=context)
    return await handler.handle(query)


# 2. GET ALL (Barcha kategoriyalarni olish)
# .NET: [HttpGet("all")] public async Task<ActionResult<ProductCategoriesAllVm>> GetAll(...)
@router.get(
    "/all",
    response_model=GetAllCategoriesVm,
    status_code=status.HTTP_200_OK,
    summary="Barcha faol kategoriyalarni olish (GetAll)",
)
async def get_all(
    s: Optional[str] = Query("", alias="s", description="Qidiruv matni"),
    context: ISSDbContext = Depends(get_db_context),
) -> GetAllCategoriesVm:
    query = GetAllCategoriesQuery(search=s)
    handler = GetAllCategoriesHandler(context=context)
    return await handler.handle(query)


# 3. GET DETAILS (Bitta kategoriyani ID bo'yicha olish)
# .NET: [HttpGet("{id}")] public async Task<ActionResult<ProductCategoryDetailsVm>> GetDetails(Guid id)
@router.get(
    "/{id}",
    response_model=CategoryDetailsVm,
    status_code=status.HTTP_200_OK,
    summary="Kategoriya tafsilotlarini ID bo'yicha olish (GetDetails)",
)
async def get_details(
    id: int,
    context: ISSDbContext = Depends(get_db_context),
) -> CategoryDetailsVm:
    query = GetCategoryDetailsQuery(id=id)
    handler = GetCategoryDetailsHandler(context=context)
    return await handler.handle(query)


# 4. CREATE (Yangi kategoriya qo'shish)
# .NET: [HttpPost] public async Task<ActionResult<CreateProductCategoryVm>> Create(...)
@router.post(
    "/",
    response_model=CreateCategoryVm,
    status_code=status.HTTP_201_CREATED,
    summary="Yangi kategoriya yaratish (Create)",
)
async def create(
    dto: CreateCategoryDto,
    context: ISSDbContext = Depends(get_db_context),
) -> CreateCategoryVm:
    command = CreateCategoryCommand.from_dto(dto)
    handler = CreateCategoryHandler(context=context)
    return await handler.handle(command)


# 5. UPDATE (Kategoriyani yangilash)
# .NET: [HttpPut("{id}")] public async Task<ActionResult<UpdateProductCategoryVm>> Update(...)
@router.put(
    "/{id}",
    response_model=UpdateCategoryVm,
    status_code=status.HTTP_200_OK,
    summary="Mavjud kategoriyani yangilash (Update)",
)
async def update(
    id: int,
    dto: UpdateCategoryDto,
    context: ISSDbContext = Depends(get_db_context),
) -> UpdateCategoryVm:
    command = UpdateCategoryCommand.from_dto(id=id, dto=dto)
    handler = UpdateCategoryHandler(context=context)
    return await handler.handle(command)


# 6. DELETE (Kategoriyani o'chirish)
# .NET: [HttpDelete("{id}")] public async Task<IActionResult> Delete(Guid id)
@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Kategoriyani o'chirish (Delete)",
)
async def delete(
    id: int,
    context: ISSDbContext = Depends(get_db_context),
) -> None:
    command = DeleteCategoryCommand(id=id)
    handler = DeleteCategoryHandler(context=context)
    await handler.handle(command)


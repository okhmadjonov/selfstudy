from application.interfaces.dbcontextinterface import IBBDbContext
from application.operations.categories.commands.CreateCategory.create_category_command import CreateCategoryCommand
from application.operations.categories.commands.CreateCategory.create_category_vm import CreateCategoryVm
from persistence.database.models.category_model import CategoryModel


class CreateCategoryHandler:
    """
    .NET'dagi `IRequestHandler<CreateProductCategoryCommand, CreateProductCategoryVm>` ekvivalenti.
    Biznes mantig'ini bajaruvchi klass.
    """

    def __init__(self, context: IBBDbContext) -> None:
        self._context = context

    async def handle(self, request: CreateCategoryCommand) -> CreateCategoryVm:
        # 1. Yangi Category entity obyektini yaratish
        category = CategoryModel(
            name=request.name,
            description=request.description,
            is_active=request.is_active,
        )

        # 2. Bazaga qo'shish (await _context.ProductCategories.AddAsync)
        self._context.session.add(category)

        # 3. O'zgarishlarni saqlash (await _context.SaveChangesAsync)
        await self._context.save_changes_async()

        # 4. Bazadan ID va hosil bo'lgan qiymatlarni yangilash
        await self._context.session.refresh(category)

        # 5. ViewModel qaytarish (AutoMapper: _mapper.Map<CreateCategoryVm>(category))
        return CreateCategoryVm.model_validate(category)


from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from application.interfaces.dbcontextinterface import IBBDbContext
from webapi.config import settings

# 1. Asinxron Engine (xuddi DbContextOptionsBuilder.UseNpgsql(...) kabi)
engine = create_async_engine(
    settings.database_url,
    echo=settings.DEBUG,
    future=True,
)

# 2. Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


# 3. Base ORM klassi (xuddi EF Core ModelBuilder / Base DbContext kabi)
class Base(AsyncAttrs, DeclarativeBase):
    pass


# 4. Haqiqiy BBDbContext klassi
# .NET: public class BBDbContext : DbContext, IBBDbContext
class BBDbContext(IBBDbContext):
    """
    .NET'dagi `public class BBDbContext : DbContext, IBBDbContext` to'liq ekvivalenti.
    """

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    @property
    def session(self) -> AsyncSession:
        return self._session

    async def save_changes_async(self) -> None:
        """EF Core: await _context.SaveChangesAsync()"""
        await self._session.commit()

    async def rollback_async(self) -> None:
        """EF Core: rollback"""
        await self._session.rollback()


# Ikkala nom bilan ham mos bo'lishi uchun alias
AppDbContext = BBDbContext


# 5. Dependency Injection (xuddi builder.Services.AddScoped<IBBDbContext, BBDbContext>() kabi)
async def get_db_context() -> AsyncGenerator[IBBDbContext, None]:
    async with AsyncSessionLocal() as session:
        context = BBDbContext(session=session)
        try:
            yield context
        except Exception:
            await context.rollback_async()
            raise
        finally:
            await session.close()

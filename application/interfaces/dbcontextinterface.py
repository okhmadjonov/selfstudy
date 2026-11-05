from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class IBBDbContext(ABC):
    """
    .NET'dagi `public interface IBBDbContext` ekvivalenti:
    
    public interface IBBDbContext
    {
        public DatabaseFacade Database { get; }
        Task<int> SaveChangesAsync(CancellationToken cancellationToken);
    }
    """

    @property
    @abstractmethod
    def session(self) -> AsyncSession:
        """
        EF Core'dagi DbContext / DatabaseFacade ekvivalenti.
        U orqali:
          - session.add(entity)           -> xuddi _context.Users.Add(user) kabi
          - session.delete(entity)        -> xuddi _context.Users.Remove(user) kabi
          - session.execute(select(...))  -> xuddi _context.Users.Where(...).ToListAsync() kabi
        """
        pass

    @abstractmethod
    async def save_changes_async(self) -> None:
        """EF Core: Task<int> SaveChangesAsync()"""
        pass

    @abstractmethod
    async def rollback_async(self) -> None:
        """Xatolik yuz berganda o'zgarishlarni bekor qilish"""
        pass


# Eski nom bilan ham mos bo'lishi uchun alias
IAppDbContext = IBBDbContext

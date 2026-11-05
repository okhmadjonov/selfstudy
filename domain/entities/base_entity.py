from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass(kw_only=True)
class BaseEntity:
    """
    .NET'dagi `public abstract class BaseEntity` ekvivalenti.
    Barcha entity'lar uchun umumiy takrorlanuvchi maydonlar (id, created_at, updated_at).
    """
    id: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None


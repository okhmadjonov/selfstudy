from typing import Any
from fastapi import HTTPException, status


class NotFoundException(HTTPException):
    """
    .NET'dagi `NotFoundException(nameof(Entity), id)` ekvivalenti.
    Topilmaganda avtomatik ravishda HTTP 404 Not Found xatosini qaytaradi.
    """

    def __init__(self, entity_name: str, key: Any) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"'{entity_name}' with key ({key}) was not found.",
        )


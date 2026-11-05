class ApplicationException(Exception):
    """Barcha maxsus biznes xatoliklar uchun asosiy klass (.NET: AppException)"""
    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.message = message


class NotFoundException(ApplicationException):
    """Element topilmaganda otiladigan xatolik (HTTP 404)"""
    def __init__(self, entity_name: str, key: any) -> None:
        super().__init__(f"'{entity_name}' with key ({key}) was not found.")
        self.entity_name = entity_name
        self.key = key


class ValidationException(ApplicationException):
    """Biznes validatsiya buzilganda otiladigan xatolik (HTTP 400)"""
    def __init__(self, message: str) -> None:
        super().__init__(message)